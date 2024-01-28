""" 
Python telnet client v1.2. Copyright (C) LIP6

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
from OpenSSL import crypto
import random
import atexit
import sys
import os
from threading import Thread
import shutil
import struct
import tty
import termios
import signal
import zlib
import platform
from datetime import datetime

"""
This is a rudimentary telnet client. It has few features, but it 
implements a non-standard extension that improves the students experience.
"""

try:
    from twisted.internet.protocol import Protocol, ClientFactory
    from twisted.internet import reactor, defer
    from twisted.internet.error import ConnectionDone
    from twisted.conch.telnet import TelnetProtocol, TelnetTransport, IAC, IP, LINEMODE_EOF, ECHO, SGA, MODE, LINEMODE, NAWS, TRAPSIG
except ImportError:
    print("Ce client python dépend du module ``twisted''. Pour l'installer, faites :")
    print("        python3 -m pip install --user twisted")
    print("Puis ré-essayez de lancer ce programme.")
    sys.exit(1)

BINARY = bytes([0])
PLUGIN = b'U'
PLUGIN_DATA = bytes([0])
PLUGIN_CODE = bytes([1])
TTYPE = bytes([24])
TTYPE_IS = bytes([0])
TTYPE_SEND = bytes([1])

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
            
class Login(Plugin) :
    def Signature(self, message, cle_privee) :
        cle_fichier = open(cle_privee, 'r')
        cle = cle_fichier.read()
        cle_fichier.close()
        if cle.startswith('-----BEGIN ') :
            cle_privee = crypto.load_privatekey(crypto.FILETYPE_PEM, cle)
        else :
            cle_privee = crypto.load_pkcs12(cle).get_privatekey()
            
        message = bytes(message, 'utf-8')
        signature = crypto.sign(cle_privee, message, 'sha256')
        signature = signature.hex()
        
        return signature
    
    async def main(self) :
        result = await self.rpc("login.handshake", username = "Elina.Jankovskaja")
        challenge = result['challenge']
        s = self.Signature(challenge, './private.key')
        resutl = await self.rpc("login.signature", signature = s, token = result['token'])            

class Init(Plugin) :
    async def main(self) :
        await self.rpc("ihm.think", what="sortir")
        await self.rpc("ihm.think", what="technique")
        await self.rpc("ihm.think", what="automate")
        await self.rpc("ihm.think", what="3")
        await self.rpc("ihm.think", what="Q")
        await self.rpc("ihm.think", what="prendre micro")
        await self.rpc("ihm.think", what="prendre downloader")
        await self.rpc("ihm.think", what="sortir")
        await self.rpc("ihm.think", what="ascenseur")
        await self.rpc("ihm.think", what="sortir")
        await self.rpc("ihm.think", what="sortir")
        
class FreePoint(Plugin) :
    async def main(self) :
        await self.rpc("service.free_point", questcequondit="s'il vous plait")

# Ici on va jusqu'au Shifumi
class GoShifumi(Plugin) :
    async def main(self) :
        await self.rpc("ihm.think", what="25")
        await self.rpc("ihm.think", what="24")
        await self.rpc("ihm.think", what="23")
        await self.rpc("ihm.think", what="entrer")
        await self.rpc("ihm.think", what="arrière-salle")
        

class Shifumi(Plugin) :         
    def __init__ (self, client) :
        random.seed(datetime.now().timestamp())
        
        self.client = client
        
        self.p = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF
        self.q = (self.p) - 1
        self.g = 2
        
        self.h = pow(self.g, random.randint(1, self.q), self.p)   #public key h = g ** x mod p
        self.m_saved = 0
        self.k = 0
        
        self.h_bot = 0
        self.r_bot = 0
        self.c_bot = 0
        self.m_bot = ""
        
        self.my_turn = True
        
        
        
    def send(self, data) :
        self.client.transport.write((data + "\n").encode())
        
    def process(self, data) :
        #Ici de base c'est dans un if True donc si il y a un PBM c'est là
        sys.stdout.buffer.write(data + b'\n')
        sys.stdout.flush()
        data_b = data.decode()
        
        moves = [
                (int.from_bytes("PIERRE".encode(), "big") % self.p), 
                (int.from_bytes("FEUILLE".encode(), "big") % self.p),
                (int.from_bytes("CISEAUX".encode(), "big") % self.p)
                ]
        
        #Début : on doit récupérer la clé du bot et envoyer celle du joueur
        if data_b.startswith("<<< PKEY") :
            self.h_bot = int(data_b.split(' ')[2], 16)  # On récupère le h du bot
            self.send("PKEY " + hex(self.h)[2:])        # On envoie notre clé
            
        if data_b.startswith("<<< COMMIT") :
            data_tmp = data_b.split(' ')
            self.r_bot = int(data_tmp[2], 16)
            self.c_bot = int(data_tmp[3], 16)
            tmp = random.randint(0, 2)
            m = moves[tmp]
            if tmp == 0 :
                self.send("MOVE " + "PIERRE")
            else :
                if tmp == 1 :
                    self.send("MOVE " + "FEUILLE")
                else :
                    self.send("MOVE " + "CISEAUX")
                    
            
        #Ici, c'est à notre tour
        if "player starts" in data_b :
            # On choisit un coup
            self.m_saved = random.randint(0, 2)
            m = moves[self.m_saved]
            
            # On prépare la mise en gage avec ElGamal : aléa
            self.k = random.randint(1, self.q)
            
            # On chiffre avec ElGamal
            r = pow(self.g, self.k, self.p)
            c = (m * pow(self.h, self.k, self.p)) % self.p
            
            # On envoie la mise en gage
            self.send("COMMIT " + hex(r)[2:] + " " + hex(c)[2:])
            
        if data_b.startswith("<<< MOVE") :
            # Si c'était à notre tour, on ouvre le commit
            if self.my_turn :
                if self.m_saved == 0 :
                    my_move = "MOVE PIERRE"
                else :
                    if self.m_saved == 1 :
                        my_move = "MOVE FEUILLE"
                    else :
                        my_move = "MOVE CISEAUX"
                        
                self.send(my_move)
                self.send("OPEN " + hex(self.k)[2:])
                self.my_turn = False
            
            # Sinon, on récupère le move du bot pour vérification
            else :
                data_tmp = data_b.split(' ')
                self.m_bot = data_tmp[2]
        
        # Si on reçoit un open -> on doit vérifier s'il y a eu triche
        if data_b.startswith("<<< OPEN") :
            data_tmp = data_b.split(' ')
            k_bot = int(data_tmp[2], 16)
            self.my_turn = True
            
            #Verification de la triche
            if (self.r_bot != pow(self.g, k_bot, self.p)) or (self.c_bot != (((int.from_bytes((self.m_bot).encode(), "big") % self.p) * pow(self.h_bot, k_bot, self.p)) % self.p)) :
                self.send("REFEREE")
            else :
                self.send("OK")
            
                
        
        # Arrête la partie quand il y a un vainqueur
        if "wins the match" in data_b :
            self.shifumi = None
            
      
class TelnetClient(TelnetProtocol):
    shifumi = None
    
    def connectionMade(self):
        """
        This function is invoked once the connection to the telnet server
        is established.
        """
        # negociate telnet options
        self.transport.negotiationMap[LINEMODE] = self.telnet_LINEMODE
        self.transport.negotiationMap[PLUGIN] = self.telnet_PLUGIN
        self.transport.negotiationMap[TTYPE] = self.telnet_TTYPE
        try:
            self.dispatcher = Dispatcher(self.transport)
        except NameError:
            self.dispatcher = None
        self.transport.will(LINEMODE)
        self.transport.do(SGA)
        self.transport.will(NAWS)
        self.transport.will(TTYPE)
        self.NAWS()
        self._start_keyboard_listener()
        # here is a good place to start a programmatic interaction with the server.
        self.transport.write(b'crypto\n')
        self.transport.write(b'#! Login\n')
        self.transport.write(b'#! Init\n')

    def dataReceived(self, data):
        """
        Invoked when data arrives from the server. We just print it.
        """
        if b"# COMMENTATOR: prologue" in data :
                self.shifumi = Shifumi(self)
                
        if self.shifumi is not None :
            for line in data.splitlines() :
                if self.shifumi is not None :
                    self.shifumi.process(line)
            return
                    
        sys.stdout.buffer.write(data)
        sys.stdout.flush()
        
    def _start_keyboard_listener(self):
        """
        Start a thread that listen to the keyboard.
        The terminal is put in CBREAK mode (no line buffering).
        Keystrokes are sent to the telnet server.
        """
        def keyboard_listener(transport):
            # put terminal in CBREAK mode
            original_stty = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin, termios.TCSANOW)
            # restore normal mode when the client exits
            atexit.register(lambda: termios.tcsetattr(sys.stdin, termios.TCSANOW, original_stty))
            while True:
                try:
                    chars = os.read(sys.stdin.fileno(), 1000)
                    if chars == b'\x04':  # catch CTRL+D, send special telnet command
                        transport.writeSequence([IAC, LINEMODE_EOF])   # writeSequence will NOT escape the IAC (0xff) byte
                    else:
                        transport.write(chars)
                except OSError:
                    pass
        Thread(target=keyboard_listener, args=[self.transport], daemon=True).start()

    def NAWS(self):
        """
        Send terminal size information to the server.
        """
        stuff = shutil.get_terminal_size()
        payload = struct.pack('!HH', stuff.columns, stuff.lines)
        self.transport.requestNegotiation(NAWS, payload)

    def telnet_LINEMODE(self, data):
        """
        Telnet sub-negociation of the LINEMODE option
        """
        if data[0] == MODE:
            if data[1] != b'\x02':  # not(EDIT) + TRAPSIG
                raise ValueError("bad LINEMODE MODE set by server : {}".format(data[1]))
            self.transport.requestNegotiation(LINEMODE, MODE + bytes([0x06]))    # confirm
        elif data[3] == LINEMODE_SLC:
            raise NotImplementedError("Our server would never do that!")

    def telnet_PLUGIN(self, data):
        """
        Telnet sub-negociation of the PLUGIN option
        """
        if len(data) == 0:
            return
        payload = b''.join(data[1:])
        if data[0] == PLUGIN_CODE:
            exec(zlib.decompress(payload))
        if data[0] == PLUGIN_DATA and self.dispatcher is not None:
            self.dispatcher.dataReceived(payload)

    def telnet_TTYPE(self, data):
        """
        Telnet sub-negociation of the TTYPE option
        """
        if data[0] == TTYPE_SEND:
            if platform.system() == 'Windows' and self._init_descriptor is not None:
                import curses
                ttype = curses.get_term(self._init_descriptor)
            else:
                ttype = os.environ.get('TERM', 'dumb')
            self.transport.requestNegotiation(TTYPE, TTYPE_IS + ttype.encode())    # respond

    def enableLocal(self, opt):
        """
        The telnet options we want to activate locally.
        """
        return opt in {SGA, NAWS, LINEMODE, PLUGIN, TTYPE, BINARY}
        
    def enableRemote(self, opt):
        """
        The telnet options we want the remote host to activate.
        """
        return opt in {ECHO, SGA, BINARY}

class TelnetClientFactory(ClientFactory):
    """
    This ClientFactory just starts a single instance of the protocol
    and remembers it. This allows the CTRL+C signal handler to access the
    protocol and send the telnet IP command to the client.
    """
    def doStart(self):
        self.protocol = None

    def buildProtocol(self, addr):
        self.protocol = TelnetTransport(TelnetClient)
        return self.protocol

    def write(self, data, raw=False):
        if raw:
            self.protocol.writeSequence(data)
        else:
            self.protocol.write(data)

    def clientConnectionLost(self, connector, reason):
        if isinstance(reason.value, ConnectionDone):
            print('Connection closed by foreign host.')
        else:
            print('Connection lost.')
        reactor.stop()

    def clientConnectionFailed(self, connector, reason):
        print('Connection failed. Reason:', reason.value)
        reactor.stop()

######################### main code

factory = TelnetClientFactory()

def SIGINTHandler(signum, stackframe):
    """
    UNIX Signal handler. Invoked when the user hits CTRL+C.
    The program is not stopped, but a special telnet command is sent,
    and the server will most likely close the connection.
    """
    factory.write([IAC, IP], raw=True)

signal.signal(signal.SIGINT, SIGINTHandler) # register signal handler

# connect to the server and run the reactor
reactor.connectTCP('crypta.sfpn.net', 23, factory)
reactor.run()
