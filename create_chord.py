# %%
import sys
import random
from node import *
from hash import *

# %%
nodeList=['127.0.0.1']
portList=random.randint(range(10001, 10010), nNodes)
for n in nodeList:
  addrList+=map(lambda port: (n, port), portList)

# create the chord nodes
cNodeList=[]

for i in range(0, len(addrList)):
  ip, port=addrList[i][0], addrList[i][1]
  cNode=NodeServer(ip, port)
  if len(cNodeList)==0: 
    cNode.join()
  else:
    # use a random already created peer's address as a remote
    rNodeAddr=cNodeList[random.choice(len(cNodeList))]
    cNode.join(rNodeAddr)

  cNode.start()
  print("Created at %s, id=%d" % (addrList[i], get_hash(addrList[i]))
  cNodeList.append(addrList[i])
  time.sleep(0.5)