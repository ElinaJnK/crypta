# README - CRYPTA2

This is resolution algorithms as well as methods to solve the CTF event that was organized during my
second year in my Masters degree.

The solutions are organized in folders except the solutions that require no code.
Those are down below.
If you are from the futur years I strongly advise you to try and solve the exercises on your own. It's hard but worth it :)

The folder books/ contains all the information I could get throughout the game (it was easier to read that way :))

First, we get an exercise in the technical room:

1. Generate an openssl ECDSA public-key using the sect163r1 curve:
- Generate the private key using openssl (it will be in private_key.pem):
```bash
openssl ecparam -name sect163r1 -genkey -noout -out private_key.pem
```
- Extract the public key:
```bash
openssl ec -in private_key.pem -pubout -out public_key.pem
```

For SM2 because apparently I can't read: 
```bash
openssl ecparam -name SM2 -genkey -noout -out sm2_private_key.pem
```
```bash
openssl ecparam -name SM2 -genkey -noout -out sm2_private_key.pem
```

2. 
Produire une signature:
```bash
openssl dgst -sha256 -sign secret_key.pem
# or
openssl dgst -sha256 -hex -sign c2pnb272w1_private_key.pem
```
Vérifier une signature:
```bash
openssl dgst -sha256 -verify public_key.pem -signature signature.bin
```
Pour sm2 (Chinese standard):
```bash
openssl dgst -sm3 -sign sm2_private_key.pem -out data_signature.bin
```