# %%
from glob import glob
import os
from hash import *
import sys
from range import *
from conf import *

# check the result of experiment 1
def read_result(logsize):
  result=[]
  files=glob(os.path.join(folder, 'e1_'+str(logsize)+'*'))
  for file in files:
    with open(file, 'r') as f:
      next(f)
      for line in f:
        fromId, keyId, targetId, steps=line.strip().split('\t')
        result.append([int(fromId), int(keyId), int(targetId), int(steps)])
  return result

def get_node_ids(logsize):
  nodeIds=[]
  ports=range(PORT_FROM, PORT_TO)
  file=os.path.join(folder, 'ips_e1_'+str(logsize)+'.txt')
  with open(file, 'r') as f:
    for line in f:
      ip=line.strip()
      for port in ports:
        nodeIds.append(get_hash((ip, port)))
  return nodeIds

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
  # folder='/home/ddps2012/result'
  folder='d:/dps/a2/result'
  logsize=int(sys.argv[1])
  result=read_result(logsize)
  nodeIds=sorted(get_node_ids(logsize))
  mistakes=[]
  for r in result:
    keyId, targetId=r[1], r[2]
    trueId=get_true_id(keyId, nodeIds)
    if trueId!=targetId:
      mistakes.append([keyId, trueId, targetId])
      print(False)

  if len(mistakes)>0:
    file=os.path.join(folder, 'mis_e1+'+str(logsize)+'.txt')
    with open(file, 'w+') as f:
      f.write('\t'.join(['keyId', 'trueId', 'targetId']))
      f.write('\n')
      for m in mistakes:
        f.write('\t'.join([str(v) for v in m]))
        f.write('\n')
# %%
