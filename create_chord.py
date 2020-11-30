# %%
import sys
import random
from node import Node

# %%
nodeList=['127.0.0.1']
portList=random.randint(range(10000, 60000), nNodes)
for n in nodeList:
  addressList+=map(lambda port: (n, port), portList)

# create the chord nodes
cNodeList=[]

for i in range(0, len(address_list)):
  if len(cNodeList)==0:
    cNode=Node(addressList[i])
  else:
    # use a random already created peer's address as a remote
    remote=cNodeList[random.choice(len(cNodeList))]
    cNode=Local(address_list[i], remote)
  
  
  cNode.start()
  print("Created at %s" % addressList[i])
  cNodeList.append(cNode)
  time.sleep(0.5)