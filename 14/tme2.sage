"""
TME #2 : représentation alternative
===================================

Difficulté : **


But     : écrire un entier x sous la forme x == a / b (modulo p)
          avec |a| <= sqrt(p) et |b| <= sqrt(p).

p = d4ff1612c161bf0d63a987b8ea649afda40b1c3986d4c1d8b9fb096826fa17f63550dc8ebdacc9a4864622ed98551a90bcfeb00ca1b25b86911a15f2bd75b3ff7e2a0996be83b49c286199179ab47e6348c278c41f791c01f7398bddae0be482b8cc8c5c2235d45504baaf45ff19a99329125a1e5d7ff20b6b154e3e8d6a2fc9

x = 1059d7313cebcbcb7cc0970412cf4bb87b87ebaee8ae2bf0e047cd27be9656cb4454168eaf5518ba758d3388f0e5d8ca536cd7c100d891b5199183ad2effee08364235082c6781ba878282f1ddc92ad6a328f30160a180a909a1e8cdccae4c611ebb02fbc382c67b2b48f398ccf3e6230aa0712408d315969d56122c355facd"""

from fpylll import IntegerMatrix, LLL, SVP
# init the parameters
p = 0xed9584bdfe6b6256d42a9e3b19761a05efebabfbc88bec5657307b06e784f2b2c769ffeb35fe3369672b2d4cc8f6d9146a5515c921d3a69d3c91c4c8d247ee6066e0ad103e33806e576b0d921b43cf8c75f46864aa1262004c1db3864b9f2c0e9d28c282d307c747b687be02fee403cc9f917d2920920a0bc70aa80292ee7d81

x = 0xa1b3bcbde30487ba10448179824d395eca447a3bc1e5d6e6549341fbcf48b2113d176cb590f24e90ed63216bb23536d85cf2e07d3e721f75e1a313b2886467d87d0aab0f330c5737812444cbf9954f2d543b89ebba10f6e6164f80114b6e053a1198ced8e264e19d123602818fba7944f84e8da28119d13f4168f88120216c28

n = 2

# create a matrix
B_list = [[0 for _ in range(n)] for _ in range(n)]
B_list[0][0] = 1
B_list[0][1] = x
B_list[1][0] = 0
B_list[1][1] = p

B = IntegerMatrix.from_matrix(B_list)
lll_B = LLL.reduction(B)

# Solve for the shortest vector using the SVP class
svp_solution = SVP.shortest_vector(lll_B)
print("Solution in format : (b, a)")
print(svp_solution)