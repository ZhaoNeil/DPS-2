from node import *
from client import *
from conf import *

ip='127.0.0.1'
ports=range(10001, 10010)
n0=NodeServer(ip, ports[0])
n0.join(None)
n0.connection_thread()