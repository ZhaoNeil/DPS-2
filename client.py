# %%
import socket
import json
from hash import *
import threading

def requires_connection(func):
  '''
  initialize and clean up connections with remote server
  '''
  def inner(self, *args, **kwargs):
    self.mutex.acquire()  #acquire lock
    self.open_connection()
    ret=func(self, *args, **kwargs)
    self.close_connection()
    self.mutex.release()  #release lock
    return ret
  return inner


class Client:
  def __init__(self, server_address):
    self.addr=tuple(server_address)
    self.mutex=threading.Lock()

  def open_connection(self):
    self.socket_=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket_.connect(self.addr)

  def close_connection(self):
    self.socket_.close()
    self.socket_=None
  
  def send(self, msg):
    self.socket_.sendall(msg.encode('utf-8'))

  def recv(self):
    return self.socket_.recv(256).decode('utf-8')

  def ping(self):
    try:
      s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.connect(self.addr)
      s.sendall(b"\r\n")
      s.close()
      return True
    except socket.error:
      return False

  def id(self):
    return get_hash(self.addr)

  @requires_connection
  def successor(self):
    self.send('get_successor')
    response=json.loads(self.recv())
    return Client(response)

  @requires_connection
  def predecessor(self):
    self.send('get_predecessor')
    response=json.loads(self.recv())
    if response=="":
      return None
    return Client(response)

  @requires_connection
  def find_successor(self, keyId):
    self.send('find_successor %s' %keyId)
    response=json.loads(self.recv())
    return Client(response)

  @requires_connection
  def closet_preceding_finger(self, keyId):
    self.send('closet_preceding_finger %s' %keyId)
    response=json.loads(self.recv())
    return Client(response)

  @requires_connection
  def notify(self, n_):
    self.send('notify %s %s' %(n_.addr[0], n_.addr[1]))

  @requires_connection
  def get_succList(self):
    self.send('get_succList')
    response=json.loads(self.recv())
    if response=="":
      return []
    return list(map(Client, response))

# %%
