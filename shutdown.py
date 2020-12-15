# %%
import socket
from get_ip import *

HOST = [get_host_ip()]  # The server's hostname or IP address
print(HOST[0])

ports=range(10001, 10010)        # The port used by the server

for i in range(10):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST[0], ports[i]))
        s.sendall("shutdown".encode('utf-8'))


# %%
# %%

# %%
