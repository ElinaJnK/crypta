from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import secrets
import hashlib
from pyasn1.type import univ
from pyasn1.codec.der.encoder import encode as der_encode
from pyasn1.codec.der.decoder import decode as der_decode


print("SDSA : ")
# my public key for testing purposes
public_key_dsa = b"""
-----BEGIN PUBLIC KEY-----
MIIDQzCCAjYGByqGSM44BAEwggIpAoIBAQDFzSdQJ6NHIY0NQr95xqRDy4ZzD+6W
fneHVDPDuVG59IgW5L1OEhcxisP6AI7WnDyhZzn7ohcWWrtsy15Tm0tTKCSe5VBK
dK6Zn99aXmqvzMRbE7EuZ0MCLXu9Qv1I9/IR5A8F0hmhcNY0fdEmXcL90erqPXqZ
1RAm4FcINMZBUw2XI5EijN3R2YIvq+gMyr9xIgmmYSClhf9oSFsywiNr8dQQskBF
jHYL8ooyXxqmzW5URMkPrqXYdjI48UqLGlgkwAnArBsKsXRE31kq2sKpdH/f0XJP
wIED1RNKA7sP08Rw4iirnKE+zGajHtlNDa0N3YNaX+/bmD6aJx927921Ah0A/GhL
CEy2SCPLwwcfBod3VmMdinSQlAROQyvENQKCAQEAkAeHmX+rnyqq4ZJ7FP4T12/z
ZBH+ITOijAqu2mXt6KalZO9fKMEx7oJhIqPeYJB1AHli3sz4yNW2TG52BN0yE135
W2n/jCONWr3ALJL9MZ6Q9ZNIEWTaNyvvurBGJVE6fiOGJwYLrrr4CRf46kCcSWq9
uonnWK9vM6o7eWAqlFRAjWTXXOeeOG++bIKtatIRofRdpd94FsHA+aWkj+px5W4C
yY3616CdHq46EV7brAcwJzF+6blGyBN/OqBc8EKVzeYP91kqxgpBUfvXsBXgtXbH
VYgAfy6Pf02uUGvutM1We8OYBx2Iu854LgrD2uqrB4H6mNRdBJnMuiGrCP8lcQOC
AQUAAoIBAEAeGriQGwFxGjkbLEVwFSxGDZI1Yij+T9poEaeRcPk3esSghoNgrYJi
mj+e3C47F/9/lOjdwI8/dDuEAXPDYg1ha0SAv8O1Uj0H6pEZxSi9hwBBwsGU3rHw
3/Bxu5bJjDrbUb+QubRZHcW9o/JrgHVwFmA43+t/qu/oOmaZr5A1V8zsU4NFVrNa
OTLypsNOxb9zb2xh0ugOV8Xn4ITZaDdgVxaci79ZwxMiPQrfQ2rRxB8Ql6q7YjMc
+Wop6oSx9N/3y2B9GDLP7nMHCt1Vg76ziG0a3ry7jvJz8mydDmzDgDmzdskc7pLt
bZFh0RS7mu9X8lHHBdYib6fd5WjyxWQ=
-----END PUBLIC KEY-----
"""

# my signatures using the same k and message : "hello"
sig_1 = "3046022100F5A7FB683AE7A988C6DF7876343BD8235F9CDB957A1778C22555635398EA2013022100E45F9D967B87A2AB3A9DA01BDB38EBB762FBE72AF93A58E2C2D1B110164D5554"
sig_2 = "3046022100A2547F045D85BF2D8605965F9DC1E2B9B623D4ADF2E526568F79D944EEF6B082022100B56D6FA5EE2A084FC21C0FF83F877E8B7286BBFBBBC7F854AE579B810F545EFC"

challenge = input("Input the challenge : ")
challenge = "dinar dater crumb gluts leper"
public_key = serialization.load_pem_public_key(
    public_key_dsa,
    backend=default_backend()
)

if public_key.key_size is None or public_key.public_numbers().parameter_numbers is None:
    print("Not a DSA public key")
    exit(1)

p = public_key.public_numbers().parameter_numbers.p
q = public_key.public_numbers().parameter_numbers.q
g = public_key.public_numbers().parameter_numbers.g

print("YOUR PUBLIC KEY VARIABLES : ")
print(f"p: {p}")
print(f"q: {q}")
print(f"g: {g}")
sig_1 = "3041022100ffd21651f9309489b983c3bb74310fc117e124f561a3131f3a04df4ed469def2021c075b59f12d12064851077d8616f63194cb13c2c8ad50dac4d7f513eb"
sig_2 = "3041022100f19ffe622b906c91662fe2b345e952009ca2dc5b90d0ff3da49584c29d67fd2a021c726e7a28a37c55c86662a4b62b9c3d33b324a7112a79484b0ccb6d92"
# first decode the signature : get c1 and s1
signature_der = bytes.fromhex(sig_1)
# decode from DER to ASN.1 structure
signature_asn1, remainder = der_decode(signature_der, asn1Spec=univ.Sequence())
# extract c and s from the ASN.1 structure
c1 = int(signature_asn1.getComponentByPosition(0))
s1 = int(signature_asn1.getComponentByPosition(1))

# then get c2 and s2
signature_der = bytes.fromhex(sig_2)
# decode from DER to ASN.1 structure
signature_asn1, remainder = der_decode(signature_der, asn1Spec=univ.Sequence())
# extract c and s from the ASN.1 structure
c2 = int(signature_asn1.getComponentByPosition(0))
s2 = int(signature_asn1.getComponentByPosition(1))
print(f"c1 : {c1}")
# we have s = k + c * x mod q use it with s1, s2, c1, c2 to find x and k
x = ((s1 - s2) * pow(c1 - c2, -1, q)) % q
# then put x in and find k
k = (s1 - c1 * x) % q
print(f"k : {k} x : {x}")
# now that you have all this, nice, you can replicate the signature process
# k = secrets.randbelow(q - 1) + 1
# print("the k i'll be using : ", k)
# k = 9912189282716782230780523803914208129084737439407853807761256887957
# x = 3
# use r = g**k mod p.
r = pow(g, k, p)
# c = sha256(M || r) (r is on 2048 bits)
message = challenge + hex(r)
hash_object = hashlib.sha256(message.encode())
c = int(hash_object.hexdigest(), 16)
# s = k + c * x mod q.
s = (k + c * x) % q
# create ASN.1
signature_asn1 = univ.Sequence()
signature_asn1.setComponentByPosition(0, univ.Integer(c))
signature_asn1.setComponentByPosition(1, univ.Integer(s))
# der
signature_der = der_encode(signature_asn1)
# hex
signature_hex = signature_der.hex()
print(f"Final signature : {signature_hex}")

