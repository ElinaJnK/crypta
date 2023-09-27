""" 
Python telnet plugin update client v1.0. Copyright (C) LIP6

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; By running this program you implicitly agree
that it comes without even the implied warranty of MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE and you acknowledge that it may 
potentially COMPLETELY DESTROY YOUR COMPUTER (even if it is unlikely), 
INFECT IT WITH A VERY NASTY VIRUS or even RUN ARBITRARY CODE on it. 
See the GPL (GNU Public License) for more legal and technical details.
"""
import json
import uuid

from twisted.internet import protocol, defer

PLUGIN = b'U'
PLUGIN_DATA = bytes([0])
PLUGIN_CODE = bytes([1])

class Dispatcher(protocol.Protocol):
    """
    This class extends the LIP6 telnet client to support ``plugins''.
    Plugins written by h4x0rz can communicate with university web-services
    using a variant of json-RPC. This class encapsulates most of the RPC
    mechanism. It is for internal use.  Plugin developpers should use the
    Plugin class below.
    """
    def __init__(self, transport):
        self.transport = transport
        self.dispatch = {}

    def dataReceived(self, msg):
        try:
            answer = json.loads(msg)
        except:
            return   # malformed JSON
        if "jsonrpc" not in answer or answer["jsonrpc"] != "2.0":
            return   # drop bogus message
        request_id = answer["id"]
        if request_id not in self.dispatch:
            return   # invalid id
        deferred = self.dispatch[request_id]
        del self.dispatch[request_id]
        if "error" not in answer and "result" not in answer:            
            return
        if "error" in answer:
            deferred.errback(answer["error"])
        if "result" in answer:
            deferred.callback(answer["result"])

    def send(self, payload):
        self.transport.requestNegotiation(PLUGIN, payload.encode())

    def call(self, method, error_handler, **kwds):
        """
        Invoke a remote method. Returns a Deferred that fires with the result.
        """
        args = {"jsonrpc": "2.0", "method": method, "params": kwds}
        request_id = str(uuid.uuid4())
        args["id"] = request_id
        result = defer.Deferred()
        result.addErrback(error_handler)
        self.dispatch[request_id] = result
        self.send(json.dumps(args))
        return result

class Plugin:
    """
    Base class for ``plugins'' (actual plugins must inherit from this).
    Contains helper methods that perform Remote Procedure Call (RPC)
    to web-services of the university.    
    """
    def __init__(self, dispatcher):
        self.dispatcher = dispatcher

    @staticmethod
    def default_error_handler(failure):
        """
        Invoked if an RPC returns an error. Print the error.
        """
        d = failure.value
        print(f"RPC ERROR (code={d['code']}): {d['message']}")

    async def rpc(self, method, **kwds):
        """
        Initiate an RPC, wait for the response and return it.
        The extra named arguments (in **kwds) are sent to the remote method.
        This is a coroutine (async def). It must be awaited.
        """
        dispatcher = self.dispatcher
        deferred = dispatcher.call(method, error_handler=self.default_error_handler, **kwds)
        result = await deferred
        return result


    async def main(self):
        """
        Invoked when the user thinks about the plugin.
        This is a coroutine.
        """
        raise NotImplementedError("You must actually implement the plugin")


class ServiceDiscovery(Plugin):
    """
    Think: #! ServiceDiscovery
    """
    async def main(self):
        print()
        print("Available Remote Services")
        print("-------------------------")
        result = await self.rpc("service.list")
        for (name, description) in result:
            print(f"- {name}")
            print(description)
            print()