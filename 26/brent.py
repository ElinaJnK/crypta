import hashlib
from hashlib import sha256
import random
import os

name = input("Name : ")

def brent(f, x0) -> (str, str):
	"""Brent's cycle detection algorithm."""
	# main phase: search successive powers of two
	power = lam = 1
	tortoise = x0
	hare = f(x0)
	
	# The "tortoise and hare" step.  We start at the same place
	while tortoise != hare:
		if power == lam:   # time to start a new power of two?
			tortoise = hare
			power *= 2
			lam = 0
		hare = f(hare)
		lam += 1

	# Find the position of the first repetition of length λ
	tortoise = hare = x0
	for _ in range(lam):
		hare = f(hare)

	# Next, hare and tortoise move at the same speed until they agree
	while tortoise != hare:
		prev_tortoise = tortoise
		prev_hare = hare
		tortoise = f(tortoise)
		hare = f(hare)
	
	prefix = name
	m1 = prefix + prev_tortoise
	m2 = prefix + prev_hare
	return m1.encode().hex(), m2.encode().hex()

def f(x):
	pref = name
	x = pref + x
	return sha256(x.encode()).hexdigest()[:14]

x1, x2 = brent(f, "randomstring")
print(x1, x2)

# Test if the Hash is the same on the first 56 bits
def get_first_56_bits(data):
	hash_obj = sha256()
	hash_obj.update(data)
	digest = hash_obj.digest()
	first_7_bytes = digest[:7]  # Extract the first 7 bytes (56 bits)
	return first_7_bytes

# Convert the hex strings to bytes
b1 = bytes.fromhex(x1)
b2 = bytes.fromhex(x2)

# Get the first 56 bits of the SHA-256 hash for each byte string
v1 = get_first_56_bits(b1)
v2 = get_first_56_bits(b2)

# Compare
if v1 == v2:
	print("The first 56 bits of the SHA-256 hashes are identical.")
else:
	print("The first 56 bits of the SHA-256 hashes are different.")