import hashlib
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

"""
Exercise specifications in books/ludothèque/description_jeux.txt
"""
def sha256(data):
    return hashlib.sha256(data).digest()

def aes_encrypt(key, data):
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    return encryptor.update(data) + encryptor.finalize()

# Generate K[i], X[i], Y[i]
seed = os.urandom(16)  # random seed
A = [seed]
K = []
X = []
Y = []

A.append(A[0])
for i in range(1, 1024):
    new_bytes = sha256(A[i])
    A.append(new_bytes[:16])
    A.append(new_bytes[16:])

for i in range(0, 1024):
    K.append(A[i + 1024])
    X.append(aes_encrypt(K[i], b'\x00' * 16))
    Y.append(aes_encrypt(K[i], b'\xff' * 16))

# Commitment <--- SHA256(X[0] || Y[0] || X[1] || Y[1] || ...)
interleaved = b''.join(x + y for x, y in zip(X, Y))
commitment = sha256(interleaved)
print("Commitment : ", commitment.hex())

# Ask for user input
i = int(input("Input i: "))

# Get X[i], Y[i] and the path
def reveal_path(i, A):
    path = []
    j = i + 1024
    for k in range(10):
        path.append(A[j ^ 1])
        j //= 2
    return X[i], Y[i], path

x_i, y_i, path = reveal_path(i, A)
print("X[i]: ", x_i.hex(), " Y[i]: ", y_i.hex())
print("Both of them appended : ", x_i.hex()+y_i.hex())

print("This is the path")
for i in path:
	print(i.hex())

# Signature obtained : Signature: 303502182C066777DB84B085A72831547B7B07200529D76F64B2BFF4021900E27FE0C0CEC4C8FEB31FCBBB44A1D486E713327730D1F0B5

