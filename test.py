# %%
from node import *
from client import *
from conf import *

# %%
ip='127.0.0.1'
ports=range(12001, 12010)
n0=NodeServer(ip, ports[0])
# n0.join()
# n0.start()
# %%
n1=NodeServer(ip, ports[1])
n1.join((ip, ports[0]))
n1.start()
# %%

