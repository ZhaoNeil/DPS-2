import sys
from node import *
from conf import *
import os
import random

def create_cNode(port, rNodeAddr):
  cNode=NodeServer(local, ports[i], count_steps=True)
  cNode.join(rNodeAddr)
  cNode.start()
  print("Created at id=%d" % (cNode.id()))
  return cNode

def lookup(cNode, keyId):
  if keyId in cNode.stepCounter.path_len:
    return True
  if cNode.find_successor(keyId):
    return True
  return False

if __name__=="__main__":
  local='127.0.0.1'
  ports=range(10001, 10021)
  remoteAddr=sys.argv[1]
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
    cNodeList.append(ports[i], rNodeAddr)

  time.sleep(30)

  nStep={}

  for keyId in random.sample(range(CHORD_SIZE), NQUERY):
    cNode=random.choice(cNodeList)
    if lookup(cNode, keyId):
      nStep[keyId]=cNode.stepCounter.path_len(keyId)
    else:
      nStep[keyId]=False

  folder='~/DPS-2/e1_'+str(LOGSIZE)
  filename='~/DPS-2/e1_'+str(LOGSIZE)+'.txt'

  with open(os.path.join(folder, filename), 'w+') as f:
    for keyId, length in nStep.items():
      f.write(str(keyId)+'\t'+str(length))
      f.write('\n')

  time.sleep(30)
  cNode.shutdown()

