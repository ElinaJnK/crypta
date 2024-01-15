import hashlib
import os
from hashlib import sha256

def brent(f, x0) -> (int, int):
	"""Brent's cycle detection algorithm."""
	# main phase: search successive powers of two
	power = lam = 1
	tortoise = x0
	hare = f(x0)  # f(x0) is the element/node next to x0.
	while tortoise != hare:
		if power == lam:  # time to start a new power of two?
			tortoise = hare
			power *= 2
			lam = 0
		hare = f(hare)
		lam += 1

	# Find the position of the first repetition of length λ
	tortoise = hare = x0
	for i in range(lam):
	# range(lam) produces a list with the values 0, 1, ... , lam-1
		hare = f(hare)
	# The distance between the hare and tortoise is now λ.

	# Next, the hare and tortoise move at same speed until they agree
	mu = 0
	while tortoise != hare:
		tortoise = f(tortoise)
		hare = f(hare)
		mu += 1
 
	return lam, mu

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
	
	prefix = "Kyra"
	m1 = prefix + prev_tortoise
	m2 = prefix + prev_hare
	return m1.encode().hex(), m2.encode().hex()

def f(x):
	pref = "Kyra"
	x = pref + x
	return sha256(x.encode()).hexdigest()[:14]

x1, x2 = brent(f, "randomshietskraa")
print(x1, x2)

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