# %%
from glob import glob
import os
from hash import *
import sys
from range import *
from conf import *

# check the result of experiment 1
def read_result(prob):
  result=[]
  files=glob(os.path.join(folder, 'e2_'+str(prob)+'*'))
  for file in files:
    with open(file, 'r') as f:
      next(f)
      for line in f:
        fromId, keyId, targetId, steps=line.strip().split('\t')
        result.append([int(fromId), int(keyId), int(targetId), int(steps)])
  return result

def get_node_ids(prob):
  nodeIds=[]
  ports=range(PORT_FROM, PORT_TO)
  file=os.path.join(folder, 'ips_e2_'+str(prob)+'.txt')
  with open(file, 'r') as f:
    for line in f:
      ip=line.strip()
      for port in ports:
        nodeIds.append(get_hash((ip,port)))
  return nodeIds

def get_failed_ids(prob):
  failedId=[]
  files=glob(os.path.join(folder, 'failed_'+str(prob)+'*'))
  for file in files:
    with open(file, 'r') as f:
      for line in f:
        failedId.append(int(line.strip()))
  return failedId

def get_true_id(keyId, nodeIds, failedId):
  for i in range(len(nodeIds)): 
    if keyInrange(keyId, nodeIds[i], nodeIds[(i+1)%len(nodeIds)]):
      if keyId==nodeIds[i]:
          j=i
      else:
        j=(i+1)%len(nodeIds)
      while nodeIds[j] in failedId:
        j=(j+1)%len(nodeIds)
      return nodeIds[j]

# %%
if __name__ == "__main__":
  folder='/home/ddps2012/DPS-2/result'
  #folder='d:/dps/a2/result'
  prob=float(sys.argv[1])
  # prob=0.2
  result=read_result(prob)
  nodeIds=sorted(get_node_ids(prob))
  failedId=get_failed_ids(prob)
  print(failedId)
  mistakes=[]
  for r in result:
    keyId, targetId=r[1], r[2]
    trueId=get_true_id(keyId, nodeIds, failedId)
    if trueId!=targetId:
      mistakes.append([keyId, trueId, targetId])
      print(False)

  if len(mistakes)>0:
    file=os.path.join(folder, 'mis_e2_'+str(prob)+'.txt')
    with open(file, 'w+') as f:
      f.write('\t'.join(['keyId', 'trueId', 'targetId']))
      f.write('\n')
      for m in mistakes:
        f.write('\t'.join([str(v) for v in m]))
        f.write('\n')

# %%
