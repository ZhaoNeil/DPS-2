# %%
from node import *
from client import *
from conf import *

ip='127.0.0.1'
ports=range(10001, 10010)

n1=NodeServer(ip, ports[1])
n1.join((ip, ports[0]))


