import sys
import time
import random
from node import *
from conf import *
import os


def create_cNode(port, rNodeAddr):
  cNode=NodeServer(ip, ports[i], count_timeout=True)
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

  #stop stabilizing and fixing finger tables
  for cNode in cNodeList:
    cNode.stopFixing=True
  time.sleep(5)

  #each node fails with a certain probability
  failedId=[]
  for cNode in cNodeList:
    if random.uniform(0, 1)<FAIL_PROB:
      cNode.shutdown()
      failedId.append(cNode.id())

  #write failed node ids to the disk
  folder='/home/ddps2012/result'
  # folder='d:/dps/a2/DPS-2/result'
  failed_file='failed_'+str(FAIL_PROB)+'_'+str(cNodeList[0].id())+'.txt'
  if len(failedId)>0:
    with open(os.path.join(folder, failed_file), 'w+') as f:
      for id in failedId:
        f.write(str(id))
        f.write('\n')

  #if all nodes fail, exit the program
  if len(failedId)==len(cNodeList):
    sys.exit()
  
  #perform lookups
  nTimeout={}
  for keyId in random.sample(range(CHORD_SIZE), NQUERY):
    while 1:
      cNode=random.choice(cNodeList)
      if cNode.id() not in failedId:
        break
    targetId=lookup(cNode, keyId)
    if targetId:
      nTimeout[keyId]=(targetId, cNode.timeoutCounter.get_nTimeout(keyId))
    else:
      nTimeout[keyId]=(False, False)

  #write lookup results to the disk
  # folder='/home/ddps2012/result'
  folder='d:/dps/a2/DPS-2/result'
  timeout_file='e2_'+str(FAIL_PROB)+'_'+str(cNodeList[0].id())+'.txt'

  with open(os.path.join(folder, timeout_file), 'w+') as f:
    f.write('\t'.join(['keyId', 'targetId', 'timeout']))
    f.write('\n')
    for keyId, vs in nTimeout.items():
      f.write('\t'.join([str(keyId), str(vs[0]), str(vs[1])]))
      f.write('\n')

  #shutdown all running nodes
  time.sleep(30)
  for cNode in cNodeList:
    if cNode.id() not in failedId:
      cNode.shutdown()

  # %%
# %%
