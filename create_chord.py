# %%
import sys
import random
from node import *
from hash import *
from conf import *
from client import *


def check_key_lookup():
  for keyId in random.sample(range(CHORD_SIZE), 50):
    while 1:
      node=random.choice(cNodeList)
      if node not in failed:
        break
    target=node.find_successor(keyId)
    for i in range(len(cNodeList)): 
      if keyInrange(keyId, cNodeIdList[i], cNodeIdList[(i+1)%len(cNodeIdList)]):
        if keyId==cNodeIdList[i]:
          j=i
        else:
          j=(i+1)%len(cNodeIdList)

        while cNodeIdList[j] in failedIds:
          j=(j+1)%len(cNodeIdList)
    
        actual=cNodeIdList[j]
        if target.id()==actual:
          print('keyId=%d, target=%d, True' %(keyId, target.id()))
        else:
          print('keyId=%d, target=%d, False' %(keyId, target.id()))
        break
    


# %%
local='127.0.0.1'
addrList=[]
portList=list(range(10001, 10010))

# %%
# create the chord nodes
addrList=[]
cNodeList=[]

for port in portList:
  cNode=NodeServer(local, port, count_timeout=True)
  if len(addrList)==0: 
    cNode.join()
  else:
    # use a random already created peer's address as a remote
    rNodeAddr=random.choice(addrList)
    cNode.join(rNodeAddr)

  cNode.start()
  addrList.append((local, port))
  cNodeList.append(cNode)
  print("Created at %s, id=%d" % (addrList[-1], get_hash(addrList[-1])))
  time.sleep(1)
# %%
time.sleep(20)
print('check begins')
import json
import numpy as np
cNodeIdList=sorted([get_hash(addr) for addr in addrList])

# for cNode in cNodeList:
#   cNode.stopFixing=True

nFailed=3
time.sleep(10)

print('cNodeIds:')
print(json.dumps(cNodeIdList))

failed=[]
failedIds=[]
# failed=random.sample(cNodeList, nFailed)
# for n in failed:
#   n.shutdown()
# failedIds=[n.id() for n in failed]
# print('failed node: %s' %(json.dumps(failedIds)))

check_key_lookup()

time.sleep(2)
for n in cNodeList:
  if n not in failed:
    n.shutdown()
    # print(n.id())
    # print(json.dumps(n.timeoutCounter.nTimeout))
    




# %%
