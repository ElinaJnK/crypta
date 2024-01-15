"""
Pierre Feuille Ciseau :
Quand on commence, on s'échange nos public key avec le bot 
Il t'envoi son PKEY : 
<<< PKEY h_bot
et tu lui envoie ton PKEY : 
>>> PKEY h
Comment tu calcul ton h ?
h = g^x mod p 
Le x tu le tire aléatoirement entre 1 et q
q = p - 1
p tu le trouves sur le site https://www.ietf.org/rfc/rfc3526.txt  (c'est le gros pavé qui commence par FFF tu copie et tu le formate bien (enlever les espaces)

Maintenant le jeu commence, si c'est à ton tour, toi qui commence tu dois : 
Choisir un coup, exemple "PIERRE"
Tu récupère l'entier de "PIERRE", (faut faire les conversions pour récupéré un int à la fin)
ce qui te donne en écrire simplifier : 
m = int("PIERRE") 
Donc m c'est ton coup 
Après tu doit calculer 2 chiffrés pour la "garantie" que tu joue bien "PIERRE" qui est c1 et c2
c1 = g^y mod p
c2 = (m * h^y) mod p
Maintenant que tu a tout ça, tu peux enfin lui envoyé ta garantie 
>>> COMMIT c1 c2
Comme je l'ai écrit, il faut qu'il y ait un espace entre c1 et c2 (très important)
La le bot va te répondre avec le coup qu'il a choisi imaginons "CISEAUX" qui sera m_bot
<<< MOVE CISEAUX
La tu lui révèle ce que tu a envoyé + le y qui va lui permettre de calculer c1 et c2 pour voir si tu a vraiment triché ou non
>>> MOVE PIERRE
>>> OPEN y
Et la lui (ou toi si c'est lui qui a envoyé le COMMIT), va falloir calculer le c1 et c2 pour savoir si tu (ou lui) a triché, pour le calculer tu fait : 
g^y mod p == c1 ?
m * h^y mod p == c2 ? 
(je t'aides, pour pas que ça te prennes la tête xD, si c'est toi qui doit calculer son commit à lui ça sera :
g^y mod p == c1_bot
m_bot * h_bot mod p == c2_bot)
La si la vérification passe, alors il faut envoyer 
OK
Si la vérification passe pas = triche alors faut envoyer 
REFEREE"""