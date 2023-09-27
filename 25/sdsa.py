from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import secrets
import hashlib
from pyasn1.type import univ
from pyasn1.codec.der.encoder import encode as der_encode
from pyasn1.codec.der.decoder import decode as der_decode


print("SDSA : ")

public_key_dsa = b"""-----BEGIN PUBLIC KEY-----
MIIDSDCCAjoGByqGSM44BAEwggItAoIBAQD+TrmX70MlK5VQTB/3ByHaipCp6N5C
QKT5+WOXcPIgXU0+f3rdj6TvflvYZOaaQj53oVQDOg4FEbc8y7mfYz7LoAGFbXnv
ylxjbRjLAvCnw4NfqaFPuOLjV+k948OkjcnqGkeNG6+XSxDZgNjXYs+55+PD7nsX
ARLdwL/k7hKfY8bt2bLw77GX+A6LBIOCzxPqdV1vSwO5tFiLBjXyjo26A00RuKI1
xX4Be+nSdt8U+2dCs55Tzvq1Zm10CKCMCiJ4BFObgHP6G7JVuXHwsxbyhHWaF0a4
01e1ITsJeI1lDoYGkrFlNSQCUdxeo1Gkz2N+3JQm0cPlgRDmJXHiSDjNAiEA7/BY
XCmA8Ng8RKfqXZh/Ds0BeDYPI3Bhgs0wpIbOqYsCggEBAJcQdO866MgpH9yOI09s
yAKqTA5K3Qv5hyGJVq1QasYYabHvdI4zCmCrro2evIrU5FMAiBLMeSnlA0QCGhD7
EkU92GN/gfJ7bYSkTxEN/KCT1nlcBJpWyRDZBcbBJmKGZjPo0QIDQ+Y9JjJsGclk
9ZtjGVrXLDq3g/QQU304KXxiFs7GyC+0sunCLDMfjXY8vsOwAC0MgNenGdsIT2io
iRRTFXnVne47EMVt9y8MswMl1Sv9aKyGjYhN47a9z2uZC4y4RVVU1s/vymLG424G
W6Y7z5mDO33HdO/Rr+yCYjbX+2Vn1MHpNfO5gfFzu6ya7lbKM936JdgCKXTMFpIK
Z6sDggEGAAKCAQEA+42gCBOZ+5mPRcEfcqzSNxOm1/V0rjlcQxVfh4m7VblgEwws
Tmlyb0YLGU0GECYNSo0q495sWsEWu4ar//5wNf53rjETLhLgIE9nV64xaOYXbnJT
Y7vl4fYkqR47fZzNIDIDgKn3eKdJ7aCKwlRBujwqn1MtZNLp2ynp9GyCN3jvpF80
K4apbrVtz3VaKp9HHAjhPx2hmmTNgfoKneRyYN/Wdvv3C6GlbmCQ4VtmTRuA4D5U
RrDPTaWPBPCVSMNNEetFEol/GdTJ6943hjlhK8jcnWfQy9Z12qnS+7OeP6ngJ1wz
bz7ytpRqzEGbLywF+KmkwPx/SEMPf2sP6RWaAA==
-----END PUBLIC KEY-----"""

# 2 signatures using the same k
sig_1 = "3046022100F5A7FB683AE7A988C6DF7876343BD8235F9CDB957A1778C22555635398EA2013022100E45F9D967B87A2AB3A9DA01BDB38EBB762FBE72AF93A58E2C2D1B110164D5554"
sig_2 = "3046022100A2547F045D85BF2D8605965F9DC1E2B9B623D4ADF2E526568F79D944EEF6B082022100B56D6FA5EE2A084FC21C0FF83F877E8B7286BBFBBBC7F854AE579B810F545EFC"

challenge = input("Input the challenge : ")
public_key = serialization.load_pem_public_key(
    public_key_dsa,
    backend=default_backend()
)

if public_key.key_size is None or public_key.public_numbers().parameter_numbers is None:
    print("Not a DSA public key :(")
    exit(1)

p = public_key.public_numbers().parameter_numbers.p
q = public_key.public_numbers().parameter_numbers.q
g = public_key.public_numbers().parameter_numbers.g

print("YOUR PUBLIC KEY VARIABLES : ")
print(f"p: {p}")
print(f"q: {q}")
print(f"g: {g}")

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

# now that you have all this, nice, you can replicate the signature process
# use r = g**k mod p.
r = pow(g, k, p)

# r to byte rep
r_bytes = r.to_bytes((r.bit_length() + 7) // 8, 'big')
message = challenge.encode() + r_bytes

# compute the hash of message
final_hash = hashlib.sha256(message).digest()
n = q.bit_length()
# big -> most significant byte is at the beginning
z = int.from_bytes(final_hash, 'big')
# IF YOU ENCOUNTER ISSUES USE THIS
# mask so that it's masked beyond n (but not really necessary)
# z = z & ((1 << n) - 1) # (chatgpt gave me this one lol)
c = z % q
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

# verify the signature : r <-- g**s * h**(-c) modulo p
h = pow(g, x, p)
r = (pow(g, s, p) * pow(h, -c, p)) % p
signature_der = bytes.fromhex(signature_hex)
signature_asn1, remainder = der_decode(signature_der, asn1Spec=univ.Sequence())
c_verif = int(signature_asn1.getComponentByPosition(0))
s_verif = int(signature_asn1.getComponentByPosition(1))

# message = challenge + hex(r)
# hash_object = hashlib.sha256(message.encode())
# c_final = int(hash_object.hexdigest(), 16)
r_bytes = r.to_bytes((r.bit_length() + 7) // 8, 'big')
message = challenge.encode() + r_bytes
# compute the hash of message
final_hash = hashlib.sha256(message).digest()
n = q.bit_length()
z = int.from_bytes(final_hash, 'big')
# z = z & ((1 << n) - 1)
c_final = z % q
if (c_verif == c_final):
	print("YES")
else:
	print("NO")
