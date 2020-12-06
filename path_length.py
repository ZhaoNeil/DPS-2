from conf import *
from node import *
from client import *
from hash import *
import random
import numpy as np

nodeList = ['127.0.0.1']
addrList = []
portList = [x for x in range(10001,10001+CHORD_SIZE)]
for n in nodeList:
    addrList += map(lambda port: (n,port), portList)
print(addrList)
cNodeList = []

for i in range(0,len(addrList)):
    ip, port = addrList[i][0],addrList[i][1]
    cNode = NodeServer(ip,port)
    if len(cNodeList) == 0:
        cNode.join()
    else:
        rNodeAddr=random.choice(addrList)
        cNode.join(rNodeAddr)

    cNode.start()
    print("Create at %s, id=%d" %(addrList[i],get_hash(addrList[i])))
    cNodeList.append(cNode)
    time.sleep(0.5)

keyList = [x for x in range(KEY_SIZE)]
keyIdList = map(get_hash, keyList)

def path_length(cNodeList,keyIdList):
    n_list = []
    for node in cNodeList:
        keyIdList_ = random.sample(keyIdList,int(len(keyIdList)/len(cNodeList)))
        for keyid in keyIdList_:
            n = node.find_successor(keyid)
            n_list.append(n)
    return np.mean(n_list)
