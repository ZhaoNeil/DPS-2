# %%
from glob import glob
import os
from hash import *
import sys
from range import *
from conf import *

# check the result of experiment 1
def read_result(nnode):
  result=[]
  files=glob(os.path.join(folder, 'e1_'+str(nnode)+'*'))
  for file in files:
    with open(file, 'r') as f:
      next(f)
      for line in f:
        fromId, keyId, targetId, steps=line.strip().split('\t')
        result.append([int(fromId), int(keyId), int(targetId), int(steps)])
  return result

def get_node_ids(nnode):
  nodeIds=set()
  ports=range(PORT_FROM, PORT_TO)
  file=os.path.join(folder, 'ips_e1_'+str(nnode)+'.txt')
  with open(file, 'r') as f:
    for line in f:
      ip=line.strip()
      for port in ports:
        nodeIds.add(get_hash((ip, port)))
  return list(nodeIds)

def get_true_id(keyId, nodeIds):
  for i in range(len(nodeIds)):
    if keyInrange(keyId, nodeIds[i], nodeIds[(i+1)%len(nodeIds)]):
      if keyId==nodeIds[i]:
          j=i
      else:
        j=(i+1)%len(nodeIds)
      return nodeIds[j]

# %%
if __name__ == "__main__":
  folder='/home/ddps2012/DPS-2/result'
  #folder='d:/dps/a2/result'
  nnode=int(sys.argv[1])
 # result=read_result(nnode)
  nodeIds=sorted(get_node_ids(nnode))
  print(len(nodeIds))
