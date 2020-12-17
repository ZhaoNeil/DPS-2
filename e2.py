import sys
import time
import random
from node import *
from conf import *
import os


def create_cNode(port, rNodeAddr):
  cNode=NodeServer(ip, ports[i], count_steps=True)
  cNode.join(rNodeAddr)
  cNode.start()
  print("Created at id=%d" % (cNode.id()))
  return cNode

def lookup(cNode, keyId):
  if cNode.find_successor(keyId):
    return True
  return False

if __name__=="__main__":
  ip=sys.argv[1]
  ports=range(10020, 10040)
  remoteAddr=sys.argv[2]
  if remoteAddr=='None':
    remoteAddr=None
  else:
    remoteAddr=(remoteAddr.split(':')[0], int(remoteAddr.split(':')[1]))

  cNodeList=[]
  for i in range(len(ports)):
    if i==0:
      rNodeAddr=remoteAddr
    else:
      rNodeAddr=random.choice(cNodeList).addr
    cNodeList.append(create_cNode(ports[i], rNodeAddr))

  time.sleep(30)

  for cNode on cNodeList:
    cNode.stopFixing=True
  time.sleep(5)

  if random.uniform(0, 1)<FAIL_PROB:
    cNode.shutdown()
    sys.exit()
  
  nTimeout={}

  keyIdList=random.sample(range(CHORD_SIZE), NQUERY)
  for keyId in random.sample(range(CHORD_SIZE), NQUERY):
    if lookup(cNode, keyId):
      nTimeout[keyId]=cNode.timeoutCounter.nTimeout[keyId]
    else:
      nTimeout[keyId]=False

  filename='/home/ddps2012/e1_'+str(FAIL_PROB)+'_'+ip+'.txt'

  with open(path_file, 'w+') as f:
    for keyId, count in nTimeout.items():
      f.write(str(keyId)+'\t'+str(count))
      f.write('\n')

  time.sleep(30)
  for cNode in cNodeList:
    cNode.shutdown()

  # %%
# %%
