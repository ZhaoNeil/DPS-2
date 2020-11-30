# %%
from address import Address
from utils import *

def get_hash(key):
  '''
  Convert key string to a 10-bit integer by using SHA-1 hashing
  '''
  # result=hashlib.sha1(key.encode())
  # return int(result.hexdigest(), 16)
  for i in range(len(keyList)):
    if key==keyList[i]:
      return i
  keyList.append(key)
  return len(keyList)-1

def keyInrange(key, a, b):
  '''
  is key in [a, b)?
  '''
  a=a%SIZE
  b=b%SIZE
  key=key%SIZE
  if a<b:
    return a<=key and key<b
  else:
    return a<=key or key<b

import time
def repeat_and_sleep(sleep_time):
  def decorator(func):
    def inner(self, *args, **kwargs):
      while 1:
        time.sleep(sleep_time)
        ret=func(self, *args, **kwargs)
    return inner
  return decorator

def retry_on_socket_error(retry_limit):
  def decorator(func):
    def inner(self, *args, **kwargs):
      retry_count=0
      while retry_count<retry_limit:
        try:
          ret=func(self, *args, **kwargs)
          return ret
        except socket.error:
          time.sleep(2**retry_count)
          retry_count+=1
      if retry_count==retry_limit:
        print("Retry count limit reached, aborting.. (%s)" % func.__name__)
        self.shutdown=True
        sys.exit(-1)
    return inner
  return decorator

def get_hash(address):
  ip, port=address[0], address[1]
  return hash(("%s:%s" %(ip, port)).encode())%CHORD_SIZE


# %%
import json
keyList=[]

import socket, threading
class NodeServer:
  def __init__(self, ip, port):
    self.addr=(ip, port)
    self.next=0
    
    # try:
    #   self.server_socket=socket.socket(socket.AF_INET, socket,SOCK_STREAM)
    #   self.server_socket.bind((IP, PORT))
    #   self.server_socket.listen()
    # except socket.error:
    #   print("Socket not opened")

  # def listen_thread(self):
  #   '''
  #   store the ip and port in address and save the connection and threading
  #   '''
  #   while True:
  #     try:
  #       connection, address=self.server_socket.accept()
  #       connection.settimeout(120)
  #       threading.Thread(target=self.connection_thread, args=(connection, address))
  #     except socket.error:
  #       pass #print("Error: Connection not accepted. Try again.")

  # def start(self):
  #   # accept connection from other threads
  #   threading.Thread(target=self.listen_thread, args=()).start()
  #   threading.Thread(target=self.ping_successor, args=()).start()
  #   # In case of connecting to other clients
  #   while True:
  #     print("Listenning to other clients")
  #     self.asAClientThread()

  def ping(self):
    return True

  def id(self):
    return get_hash(self.addr)

  def join(self, n_):
    '''
    join a chord ring containing node n_
    '''
    self.finger=list(map(lambda x: None, range(LOGSIZE)))
    self.pred=None
    if n_:  # join a chord ring containing node n_
      client=Client(n_.addr)
      self.finger[0]=client.find_successor(self.id())   #return the client connecting to succ
    else:   # create a new chord ring
      self.finger[0]=self
    self.update_successor_list()

  def find_successor(self, keyId):
    '''
    ask node n to find keyid's successor
    1. the succ is us iff:
      - we have a predecessor
      - keyid is in (pred(n), n]
    2. the succ is succ(n) iff:
      - keyid is in (n, succ(n)]
    '''
    if self.predecessor() and keyInrange(keyId, self.predecessor().id()+1, self.id()+1):
      return self
    elif keyInrange(keyId, self.id()+1, self.successor().id()+1):
      return self.successor()
    else:
      n_=self.closet_preceding_finger(keyId)
      return n_.find_successor()

  def closet_preceding_finger(self, keyId):
    '''
    return the closet finger n_ preceding keyid iff:
    - n_ in (n, keyId)
    - n_ alive
    '''
    for n_ in reversed(self.succList+self.finger):
      if n_!=None and keyInrange(n_.id(), self.id()+1, keyId) and n_.ping():
        return n_
    return self

  @repeat_and_sleep(STABILIZE_INT)
  @retry_on_socket_error(STABILIZE_RET)
  def stabilize(self):
    '''
    Periodically verify n's immediate successor,and tell the successor about n.
    x might be our new successor iff:
    - x=pred(succ(n))
    - x alive
    - x is in range (n, succ(n))
    # - [n+1, succ(n)] is non-empty
    '''
    succ=self.successor()
    # fix finger if succ failed
    if succ.id()!=self.finger[0].id():
      self.finger[0]=succ
    x=succ.precedessor()
    if x and keyInrange(x.id(), self.id()+1, self.finger[0].id()+1) and x.ping():
      self.finger[0]=x
    self.successor().notify(self)
    self.update_successor_list()

  def notify(self, n_):
    '''
    n_ thinks it might be our predecessor, they are iff
    - we don't have a precedessor OR
    - n_ is in the range (pred(n), n]
    '''
    if self.pred==None or keyInrange(n_.id(), self.pred.id()+1, self.id()+1):
      self.pred=n_

  @repeat_and_sleep(FIX_FINGERS_INT)
  def fix_fingers(self):
    '''
    periodically refresh finger table entries
    '''
    if self.next>=LOGSIZE:
      self.next=0
    keyId=(self.id()+2**self.next)%(2**m)
    self.finger[self.next]=self.find_successor(keyId)
    self.next+=1
  

  def update_successor_list(self):
    '''
    update n' succList with succ and succ's successor list
    '''
    succ=self.successor()
    if succ.id!=self.id():
      succ_list=succ.get_succList()
      self.succList=[succ]+succ_list

  def successor(self):
    '''
    return an existing successor, there might be redundance between finger[0]
    and succList[0], but it doesn't harm
    '''
    for n_ in [self.finger[0]]+self.succList:
      if n_.ping():
        self.finger[0]=n_
        return n_
  
  def predecessor(self):
    return self.pred
  

  def get_succList(self):
    return self.succList[:NSUCCESSORS-1]

  # def check_predecessor(self):
  #   if self.predecessor failed:
  #     self.precedessor=nil
  
  def connection_thread(self):
    # listen to incomming connections
    self.socket_=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket_.bind(self.addr)
    self.socket_.listen()

    while 1:
      try:
        conn, addr=self.socket_.accept()
      except socket.error:
        self.shutdown_=True
        break

      # request=read_from_socket(conn)
      request=conn.recv(256).decode('utf-8')
      command=request.split()[0]
      request=request[len(command):]

      if command=='get_successor':
        successor=self.successor()
        result=json.dumps(successor.addr)
      if command=='get_predecessor':
        if self.pred!=None:
          predecessor=self.pred
          result=json.dumps(predecessor.addr)
      if command=='find_successor':
        successor=self.find_successor(int(request))
        result=json.dumps(successor.addr)
      if command=='closet_preceding_finger':
        closet=self.closet_preceding_finger(int(request))
        result=json.dumps(closet.addr)
      if command=='notify':
        ip, port=request.split()
        npred_addr=(ip, int(port))
        self.notify(Client(npred_addr))
      if command=='get_succList':
        succList=self.get_succList()
        result=json.dumps(list(map(lambda n: n.addr, succList)))

      conn.sendall(result.encode('utf-8'))
      conn.close()

      # if command=='shutdown':
      #   self.socket_.close()
      #   self.shutdown_=True
      #   break

  # def register_command(self, cmd, callback):
  #   self.command_.append((cmd, callback))

  # def unregister_command(self, cmd):
  #   self.command_=filter(lambda t: True if t[0]!=cmd else False, self.command_)


