import random

"""
First you want to get the Flipper (so you can use the lock), it is in tower 25 3rd room 307
We want  y**e == x * J**c mod N
with
y != 0 mod N
We need to generate y randomely and calculate x to send so
x =  y^e * J^(-c) mod N"""

"""conseil serrure:
>>> conseil serrure
Pour exécuter le protocole normalement, il faudrait que vous possédiez le nombre
``secret'' J**d mod N, qui donne le droit d'entrer... or clairement ce n'est pas
le cas.

>>> conseil serrure
Heureusement, la serrure contient une implantation buguée du protocole.  On peut
la tromper et la convaincre d'ouvrir même sans posséder le ``secret''.

>>> conseil serrure
Essayez de lancer plusieurs sessions et observez le ``défi'' aléatoire envoyé par
la serrure.

>>> conseil serrure
Si par malheur le ``défi'' n'était pas aléatoire mais, au contraire, prévisible,
alors ne pourrait-il pas y avoir un moyen simple de fabriquer une paire (x, y) qui
satisfait l'égalitée testée par le vérifieur ?

>>> conseil serrure
(Moi, je dis ça, hein, je dis rien...)

>>> conseil serrure
En principe, on ne devrait pas pouvoir faire ça, et le protocole est censé être
sûr s'il est implanté correctement.  Mais là, vu que le ``défi'' est prévisible,
on peut mettre en oeuvre cette entourloupe."""

# public key of the system
e = 0x10001
N = 0xba4530d0c5d4094f4557699683a69dcac790935e0d8ed82451920f73b7c05c0873e8a9650020f1a1783e7256237a10e37f27762808e651ac5348a2a7f4d5c073d0350ba88525f96eec5e8974012a0241c0564af6f1e58a1f52c93c7446742deb1815ffcc3d21fb5141d1d765662b14d5089a3a647749ad7be7175f4eed215327

# given challenge c that doesn't change
c = 0x7c18698faa11155acf710fe50bff86474cdd391b13b258b6b838a7d52008ff42d705f5643f80973270f6ee9b7e02054b2a685159cfb46ced49b001fa036c426cf3ad2d96b8f6c963dfb84e1566a7df607038c5a7c9cd7c81e847aa5ef71657fc1e3f999d538b2a01054d6c2e6c098585a55deaa05c08267e3570994d9a2e0770

J = 0x323063393039393836623033393865343334356239386261326631653938663962333631396566373739393366386436613436343562616137393031363534382d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d20202020202020202020202020202020202020202020202020202020202020456c696e612e4a616e6b6f76736b616a61

# generate y randomely (we want to avoid y = 0)
y = random.randint(0, N)
print("Here is your y: ", hex(y))
x = (pow(y, e, N) * pow(J, -c, N)) % N
print("Here is your x: ", hex(x))

if pow(y, e, N) == (x * pow(J, c, N)) % N:
	print("Yes")
else:
	print("Problem somewhere")
