import sys
from node import *
from conf import *
import os
import random

def create_cNode(port, rNodeAddr):
  cNode=NodeServer(ip, ports[i], count_steps=True)
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

  nStep={}

  for keyId in random.sample(range(CHORD_SIZE), NQUERY):
    cNode=random.choice(cNodeList)
    if lookup(cNode, keyId):
      nStep[keyId]=cNode.stepCounter.path_len[keyId]
    else:
      nStep[keyId]=False

  filename='/home/ddps2012/e1_'+str(LOGSIZE)+'.txt'

  with open(filename, 'w+') as f:
    for keyId, length in nStep.items():
      f.write(str(keyId)+'\t'+str(length))
      f.write('\n')

  time.sleep(30)
  for cNode on cNodeList:
    cNode.shutdown()

