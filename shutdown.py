# %%
import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
ports=range(10001, 10010)        # The port used by the server

for i in range(10):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, ports[i]))
        s.sendall("shutdown".encode('utf-8'))


# %%
# %%

# %%
