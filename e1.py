import sys
from node import *
from conf import *


def create_cNode(port, rNodeAddr):
  cNode=NodeServer(local, port)
  cNode.join(rNodeAddr)
  cNode.start()

def lookup(cNode, keyId):
  if keyId in cNode.stepCounter.path_len:
    return True
  if cNode.find_successor(keyId):
    return True
  return False

if __name__=="__main__":
  # local='127.0.0.1'
  # port=int(sys.argv[1])
  addr = sys.argv[1]
  rNodeAddr=sys.argv[2]
  cNode=create_cNode(addr[0], addr[1], count_steps=True)

  nStep=[]
  keyIdList=random.sample(range(CHORD_SIZE), NQUERY)

  for keyId in keyIdList:
    if lookup(keyId):
      nStep.append(cNode.stepCounter.path_len(keyId))
    else:
      nStep.append(False)


  path_file='steps_'+str(port)+'.txt'

  with open(path_file, 'w+') as f:
    for i in len(keyIdList):
      f.write(str(keyIdList[i])+'\t'+str(nStep[i]))
      f.write('\n')

