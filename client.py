# %%
import socket
import json
from hash import *
import threading
from counter import *

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
  def __init__(self, server_address, stepCounter, timeoutCounter):
    self.addr=tuple(server_address)
    self.mutex=threading.Lock()
    self.stepCounter=stepCounter
    self.timeoutCounter=timeoutCounter

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
    return Client(response, self.stepCounter, self.timeoutCounter)

  @requires_connection
  def predecessor(self):
    self.send('get_predecessor')
    response=json.loads(self.recv())
    if response=="":
      return None
    return Client(response, self.stepCounter, self.timeoutCounter)

  @requires_connection
  def find_successor(self, keyId):
    self.send('find_successor %s' %keyId)
    response=json.loads(self.recv())
    if self.stepCounter!=None:
      nSteps=response[1]
      self.stepCounter.update_path_len(keyId, nSteps)
    if self.timeoutCounter!=None:
      nFailed=response[2] if len(response)==3 else response[1]
      self.timeoutCounter.update_nTimeout(keyId, nFailed)
    return Client(response[0], self.stepCounter, self.timeoutCounter)

  def update_path_length(self, keyId, nSteps):
    with open('path_len.json', 'r') as f:
      path_len=json.load(f)
    path_len[keyId]=nSteps+1
    with open('path_len.json', 'w') as f:
      json.dump(path_len, f)

  @requires_connection
  def closet_preceding_finger(self, keyId):
    self.send('closet_preceding_finger %s' %keyId)
    response=json.loads(self.recv())
    return Client(response, self.stepCounter, self.timeoutCounter)

  @requires_connection
  def notify(self, n_):
    self.send('notify %s %s' %(n_.addr[0], n_.addr[1]))

  @requires_connection
  def get_succList(self):
    self.send('get_succList')
    response=json.loads(self.recv())
    if response=="":
      return []
    return list(map(lambda addr: Client(addr, self.stepCounter, self.timeoutCounter), response))

# %%
