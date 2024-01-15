# Big thanks to Jessica

"""
TME #3 : somme de carrés
========================

Difficulté : ***


But     : écrire un entier p premier (congru à 1 mod 4) comme p == a**2 + b**2.

p = d72db4b95b42edf1680c45e01facc551b08bb29601de69b0832d979f7d8c4b63316694baded52879ef5e2add8e024f57a16b1a526792eab60a25bd097ff181e0bda8601e74fd37c2e9568337f16418c683daea312f12bfc179f5d7952d4e8c317d8c9412aa72986db5eb3d2480a505c73dc70b5f210f0c8ee48c153be8a237a5"""

from sage.modules.free_module_integer import IntegerLattice

p = 0xebcacf6c9a79b4e65e2603e4c01d2b74bdc196bcdd50a69ce0f3bd823b7cb6a427d517ea368107ae0bb2c182339d77ac31cb6fb983f782deee494652c612082b6c5d6b952467bcf2fee0e538316536aefd9fb2fb51746efb10e976b6526cd702252c3c09a6738b916cc204d75a85d797af63f3f78e48e60860b4776343b73a21

p=int(p)

k = GF(p)

beta2=k(-1)
beta=beta2.nth_root(2)


print('beta=',beta)

# to do in another terminal
# create a matrix
A= Matrix([
           [p,0],
           [beta,1]
            ])           
print(A)

# create the LLL base
A=IntegerLattice(A)
base=A.LLL()
B=IntegerLattice(base)

# calculate the shortest vector
sol_base=B.shortest_vector()
s=[]
for i in sol_base:
    s.append(i)
    if abs(i) > sqrt(p):
        print(i, "n'est pas conforme.")

# a = s[0] and b = s[1]
if p==s[0]**2+s[1]**2 :
    print("a :")
    print(s[0])
    print("b :")
    print(s[1])