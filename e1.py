import sys
from node import *
from conf import *
import os
import random

def lookup(cNode, keyId):
  if keyId in cNode.stepCounter.path_len:
    return True
  if cNode.find_successor(keyId):
    return True
  return False

if __name__=="__main__":
  local='127.0.0.1'
  port=int(sys.argv[1])
  print(port)
  rNodeAddr=sys.argv[2]
  if rNodeAddr=='None':
    rNodeAddr=None
  else:
    rNodeAddr=(rNodeAddr.split(':')[0], int(rNodeAddr.split(':')[1]))
  cNode=NodeServer(local, port, count_steps=True)
  cNode.join(rNodeAddr)
  cNode.start()
  print("Created at id=%d" % (cNode.id()))


  time.sleep(100)

  nStep=[]
  keyIdList=random.sample(range(CHORD_SIZE), NQUERY)

  for keyId in keyIdList:
    if lookup(keyId):
      nStep.append(cNode.stepCounter.path_len(keyId))
    else:
      nStep.append(False)

  folder='~/DPS-2/e1_'+str(LOGSIZE)
  filename=str(cNode.id())+'.txt'

  with open(os.path.join(folder, filename), 'w+') as f:
    for i in len(keyIdList):
      f.write(str(keyIdList[i])+'\t'+str(nStep[i]))
      f.write('\n')

  time.sleep(30)
  cNode.shutdown()

