import sys
from node import *
from conf import *
import os
import random

def create_cNode(port, rNodeAddr):
  cNode=NodeServer(ip, ports[i])
  cNode.join(rNodeAddr)
  cNode.start()
  #time.sleep(0.1)
  return cNode

def lookup(cNode, keyId):
  target, steps=cNode.count_step(keyId)
  if target:
    return target.id(), steps
  return False

if __name__=="__main__":
  ip=sys.argv[1]
  ports=range(PORT_FROM, PORT_TO)

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

  print('Creating nodes done')
  time.sleep(60)

  #perfrom lookups
  print("Lookup begins")
  nStep={}

  for keyId in random.sample(range(SIZE), NQUERY):
    cNode=random.choice(cNodeList)
    targetId, steps=lookup(cNode, keyId)
    if targetId:
      nStep[(cNode.id(), keyId)]=(targetId, steps)
    else:
      nStep[(cNode.id(), keyId)]=(False, False)
  print("Lookup done")

  #write the lookup results to the disk
  # folder='/home/ddps2012/result'
  folder='d:/dps/a2/result'
  filename='e1_'+str(NNODE)+'_'+str(cNodeList[0].id())+'.txt'

  with open(os.path.join(folder, filename), 'w+') as f:
    f.write('\t'.join(['fromId','keyId', 'targetId', 'steps']))
    f.write('\n')
    for ks, vs in nStep.items():
      f.write('\t'.join([str(ks[0]), str(ks[1]), str(vs[0]), str(vs[1])]))
      f.write('\n')

  #shutdown all running nodes
  time.sleep(60)

  for cNode in cNodeList:
    cNode.shutdown()
  print('end')
