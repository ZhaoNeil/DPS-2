import sys
import time
import random
from node import *
from conf import *
import os


def create_cNode(port, rNodeAddr):
  cNode=NodeServer(local, port)
  cNode.join(rNodeAddr)
  cNode.start()
  print("Created at id=%d" % (cNode.id()))

def lookup(cNode, keyId):
  if cNode.find_successor(keyId):
    return True
  return False

if __name__=="__main__":
  local='127.0.0.1'
  port=int(sys.argv[1])
  rNodeAddr=sys.argv[2]
  if rNodeAddr=='None':
    rNodeAddr=None
  else:
    rNodeAddr=(rNodeAddr.split(':')[0], int(rNodeAddr.split(':')[1]))
  cNode=create_cNode(local, port, count_timeout=True)

  time.sleep(60)

  cNode.stopFixing=True
  time.sleep(5)

  if random.uniform(0, 1)<FAIL_PROB:
    cNode.shutdown()
    sys.exit()
  
  nTimeout=[]
  keyIdList=random.sample(range(CHORD_SIZE), NQUERY)
  for keyId in keyIdList:
    if lookup(keyId):
      nTimeout.append(cNode.timeoutCounter.nTimeout[keyId])
    else:
      nTimeout.append(False)


  folder='~/DPS-2/e2_'+str(FAIL_PROB)
  file=str(cNode.id())'.txt'

  with open(path_file, 'w+') as f:
    for i in len(keyIdList):
      f.write(str(keyIdList[i])+'\t'+str(nTimeout[i]))
      f.write('\n')

  time.sleep(30)
  cNode.shutdown()