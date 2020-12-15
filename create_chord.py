# %%
import sys
import random
from node import *
from hash import *
# %%
addrList = []
f = open('./addrAll.txt')
for line in f:
  addrList.append(line)
# %%
# create the chord nodes
cNodeList=[]

for i in range(0, len(addrList)):
  ip, port=addrList[i][0], addrList[i][1]
  cNode=NodeServer(ip, port)
  if len(cNodeList)==0: 
    cNode.join()
  else:
    # use a random already created peer's address as a remote
    rNodeAddr=cNodeList[random.choice(range(len(cNodeList)))]
    cNode.join(rNodeAddr)

  cNode.start()
  print("Created at %s, id=%d" % (addrList[i], get_hash(addrList[i])))
  cNodeList.append(addrList[i])
  time.sleep(0.5)
# %%
