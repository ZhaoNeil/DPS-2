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
  target=cNode.find_successor(keyId)
  if target:
    return target.id()
  return False

if __name__=="__main__":
  ip=sys.argv[1]
  ports=range(10020, 10040)

  #choose the random address from existing nodes
  remoteAddr=sys.argv[2]
  if remoteAddr=='None':
    remoteAddr=None
  else:
    remoteAddr=(remoteAddr.split(':')[0], int(remoteAddr.split(':')[1]))

  #create chord nodes
  cNodeList=[]
  for i in range(len(ports)):
    if i==0:
      rNodeAddr=remoteAddr
    else:
      rNodeAddr=random.choice(cNodeList).addr
    cNodeList.append(create_cNode(ports[i], rNodeAddr))

  time.sleep(30)

  #perfrom lookups
  nStep={}

  for keyId in random.sample(range(CHORD_SIZE), NQUERY):
    cNode=random.choice(cNodeList)
    targetId=lookup(cNode, keyId)
    if targetId:
      nStep[keyId]=(targetId, cNode.stepCounter.path_len[keyId])
    else:
      nStep[keyId]=(False, False)

  #write the lookup results to the disk
  folder='/home/ddps2012/result'
  # folder='d:/dps/a2/DPS-2/result'
  filename='e1_'+str(LOGSIZE)+'_'+str(cNodeList[0].id())+'.txt'

  with open(os.path.join(folder, filename), 'w+') as f:
    f.write('\t'.join(['keyId', 'targetId', 'steps']))
    f.write('\n')
    for keyId, vs in nStep.items():
      f.write('\t'.join([str(keyId), str(vs[0]), str(vs[1])]))
      f.write('\n')

  #shutdown all running nodes
  time.sleep(30)
  for cNode in cNodeList:
    cNode.shutdown()

