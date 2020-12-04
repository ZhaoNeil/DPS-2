# %%
from node import *
from client import *
from conf import *

ip='127.0.0.1'
ports=range(10001, 10010)

n1=NodeServer(ip, ports[1])
n1.join((ip, ports[0]))

# %%
n2=NodeServer(ip,ports[2])
n2.join((ip,ports[0]))
# %%
n3=NodeServer(ip,ports[3])
n3.join((ip,ports[0]))
# %%
n1.stabilize()
n2.stabilize()
n3.stabilize()
# %%
n1.fix_fingers()
n2.fix_fingers()
n3.fix_fingers()
# %%
n1.update_successor_list()
n2.update_successor_list()
n3.update_successor_list()
# %%
