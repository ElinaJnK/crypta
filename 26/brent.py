import hashlib

name = input("Name : ")
name_hex = ''.join([hex(ord(c))[2:] for c in name])
print("name in hex : ", name_hex)

def sha256_hexdigest(input_str: str) -> str:
	m = hashlib.sha256()
	m.update(input_str.encode('utf-8'))
	# return the hash in hex (only keep the first 56 bits 56/4 (one hex is 4 bits))
	return m.hexdigest()[:14]

# here prefix = x0
def brent_collision(prefix: str):
	power = lam = 1
	tortoise = tortoise_1 = prefix + "0001"  # x0
	hare = hare_1 = sha256_hexdigest(prefix + "0002")  # f(x0)
	while tortoise != hare:
		if power == lam:  # time to start a new power of two?
			tortoise = hare
			power *= 2
			lam = 0
		hare_1 = hare
		hare = sha256_hexdigest(hare)
		lam += 1

	# Find the position μ of first repetition of length λ
	tortoise = hare = prefix + "0001"  # x0
	tortoise_1 = hare_1 = tortoise
	for _ in range(lam):
		hare_1 = hare
		hare = sha256_hexdigest(hare)

	mu = 0
	while tortoise != hare:
		tortoise_1 = tortoise
		hare_1 = hare
		tortoise = sha256_hexdigest(tortoise)
		hare = sha256_hexdigest(hare)
		mu += 1

	print(f"Two keys with similar 56-bit SHA-256 hash prefixes: {tortoise_1}, {hare_1}")
	return lam, mu

brent_collision(name_hex)
#print("sha256 (1) : ", sha256_hexdigest("da90efdd"), "(2) ", sha256_hexdigest("015e2c85"))

# taken from https://en.wikipedia.org/wiki/Cycle_detection
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