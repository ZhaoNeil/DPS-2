import random
from get_ip import *
# %%
def create_addr(nodeList,nNodes):
    # addrList=[]
    portList=random.sample(range(10001, 10010), nNodes)
    for n in nodeList:
        # addrList+=list(map(lambda port: (n, port), portList))
        addrList = list(map(lambda port: (n, port), portList))
        return addrList

host_ip = get_host_ip()
nodeList=[host_ip]
nNodes=3
addrList = create_addr(nodeList,nNodes)

for addr in addrList:
    f = open("./addrList.txt",'a')
    f.write(str(addr))
    f.write('\n')
    f.close()