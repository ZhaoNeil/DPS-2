# %%
from client import Client
from conf import *
from hash import *
import sys
from range import *
import random


import time
def repeat_and_sleep(sleep_time):
  def decorator(func):
    def inner(self, *args, **kwargs):
      while not self.stopFixing:
        time.sleep(sleep_time)
        if self.shutdown_:
          #print('finished')
          return
        ret=func(self, *args, **kwargs)
      return
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
        self.shutdown_=True
        sys.exit(-1)
    return inner
  return decorator


# %%
import json
import socket, threading

class NodeServer:
  def __init__(self, ip, port):
    self.addr=(ip, port)
    self.succList=[]
    self.shutdown_=False
    # self.next=0
    self.stopFixing=False

  def start(self):
    # accept connection from other threads
    threading.Thread(target=self.listen_thread, args=()).start()
    threading.Thread(target=self.stabilize, args=()).start()
    threading.Thread(target=self.fix_fingers, args=()).start()

  def listen_thread(self):
    '''
    listening socket for incoming connection and create a new thread for processing msgs.
    '''
    self.socket_=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket_.bind(self.addr)
    self.socket_.listen(10)
    while True:
      try:
        conn, addr=self.socket_.accept()
        # print("Connection from %s" %(str(addr)))
        threading.Thread(target=self.connection_thread, args=(conn, addr)).start()
      except socket.error:
        self.shutdown_=True
        break

  def connection_thread(self, conn, addr):
    '''
    Processing msgs from the remote clients
    '''
    request=conn.recv(1024).decode('utf-8')
    command=request.split(" ")[0]
    request=request[len(command)+1:]
  
    result=json.dumps("")
    if command=='get_successor':
      successor=self.successor()
      result=json.dumps(successor.addr)

    if command=='get_predecessor':
      if self.predecessor()!=None:
        predecessor=self.predecessor()
        result=json.dumps(predecessor.addr)

    if command=='find_successor':
      keyId=int(request)
      successor=self.find_successor(keyId)
      result=json.dumps(successor.addr)
    
    if command=='count_step':
      keyId=int(request)
      successor, steps=self.count_step(keyId)
      result=json.dumps((successor.addr, steps))

    if command=='count_timeout':
      keyId=int(request)
      successor, timeouts=self.count_timeout(keyId)
      result=json.dumps((successor.addr, timeouts))

    if command=='closet_preceding_finger':
      closet=self.closet_preceding_finger(int(request))
      result=json.dumps(closet.addr)

    if command=='notify':
      npred_addr=(request.split(" ")[0], int(request.split(" ")[1]))
      self.notify(Client(npred_addr))

    if command=='get_succList':
      succList=self.get_succList()
      result=json.dumps(list(map(lambda n: n.addr, succList)))

    conn.sendall(result.encode('utf-8'))
    conn.close()

    if command=='shutdown':
      self.socket_.close()
      self.shutdown_ = True
      

  def shutdown(self):
    self.shutdown_=True
    # self.socket_.shutdown(1)
    self.socket_.close()
    print('shutdown')

  def ping(self):
    return True

  def id(self, offset=0):
    return (get_hash(self.addr)+offset)%CHORD_SIZE

  def join(self, rNodeAddr=None):
    '''
    join a chord ring containing node n_
    '''
    self.finger=list(map(lambda x: None, range(LOGSIZE)))
    self.pred=None
    if rNodeAddr:  # join a chord ring containing node n_
      client=Client(rNodeAddr)
      self.finger[0]=client.find_successor(self.id())   #return the client connecting to succ
    else:   # create a new chord ring
      self.finger[0]=self
    self.update_successor_list()

  @retry_on_socket_error(FIND_SUCCESSOR_RET)
  def find_successor(self, keyId):
    '''
    ask node n to find keyid's successor
    1. the succ is us iff:
      - we have a predecessor
      - keyid is in (pred(n), n]
    2. the succ is succ(n) iff:
      - keyid is in (n, succ(n)]
    '''
    if self.predecessor() and keyInrange(keyId, self.predecessor().id(1), self.id(1)):
      return self
    elif keyInrange(keyId, self.id(1), self.successor().id(1)):
      return self.successor()
    else:
      n_=self.closet_preceding_finger(keyId)
      return n_.find_successor(keyId)

  def count_step(self, keyId):
    if self.predecessor() and keyInrange(keyId, self.predecessor().id(1), self.id(1)):
      return (self, 1)
    elif keyInrange(keyId, self.id(1), self.successor().id(1)):
      return (self.successor(), 1)
    else:
      n_=self.closet_preceding_finger(keyId)
      target, steps=n_.count_step(keyId)
      return (target, steps+1)

  def count_timeout(self, keyId):
    failed=set()
    #check if the target is myself
    if self.predecessor() and keyInrange(keyId, self.predecessor().id(1), self.id(1)):
      return (self, 0)

    #check if the target is my successor
    for n_ in [self.finger[0]]+self.succList:
      if keyInrange(keyId, self.id(1), n_.id(1)):
        if n_.ping():
          return (n_, len(failed))
        failed.add(n_)

    #look for the closet finger that precedes the keyId
    for n_ in reversed(self.succList+self.finger):
      if n_!=None and keyInrange(n_.id(), self.id(1), keyId):
        if n_.ping():
          target, nTimeout=n_.count_timeout(keyId)
          return (target, len(failed)+nTimeout)
        failed.add(n_)
    return (self, len(failed))
    
  def closet_preceding_finger(self, keyId):
    '''
    return the closet finger n_ preceding keyid iff:
    - n_ in (n, keyId)
    - n_ alive
    '''
    for n_ in reversed(self.succList+self.finger):
      if n_!=None and keyInrange(n_.id(), self.id(1), keyId) and n_.ping():
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
    '''
    succ=self.successor()
    # fix finger if succ failed
    if succ.id()!=self.finger[0].id():
      self.finger[0]=succ
    x=succ.predecessor()
    if x!=None and keyInrange(x.id(), self.id(1), self.finger[0].id(1)) and x.ping():
      self.finger[0]=x
    self.successor().notify(self)
    self.update_successor_list()
    # return True

  def notify(self, n_):
    '''
    n_ thinks it might be our predecessor, they are iff
    - we don't have a precedessor OR
    - n_ is in the range (pred(n), n]
    - our previous predecessor is dead
    '''
    if self.pred==None or \
      keyInrange(n_.id(), self.pred.id(1), self.id(1)) or \
      not self.predecessor().ping():
      self.pred=n_

  # @repeat_and_sleep(FIX_FINGERS_INT)
  # def fix_fingers(self):
  #   '''
  #   periodically refresh finger table entries
  #   '''
  #   if self.next>=LOGSIZE:
  #     self.next=0
  #   keyId=(self.id()+2**self.next)%(2**LOGSIZE)
  #   self.finger[self.next]=self.find_successor(keyId)
  #   self.next+=1
  #   # return True

  @repeat_and_sleep(FIX_FINGERS_INT)
  def fix_fingers(self):
    '''
    randomly select an entry in finger and update its value
    '''
    i=random.randrange(LOGSIZE-1)+1
    self.finger[i]=self.find_successor(self.id(1<<i))
    # return True
  

  def update_successor_list(self):
    '''
    update n' succList with succ and succ's successor list
    '''
    succ=self.successor()
    # if we are not alone in the ring
    if succ.id()!=self.id():
      succList=[succ]
      succList+=succ.get_succList()
      self.succList=succList

  def successor(self):
    '''
    return an existing successor, there might be redundance between finger[0]
    and succList[0], but it doesn't harm
    '''
    for n_ in [self.finger[0]]+self.succList:
      if n_.ping():
        self.finger[0]=n_
        return n_
    self.shutdown_=True
    sys.exit(-1)
  
  def predecessor(self):
    return self.pred
  
  def get_succList(self):
    return self.succList[:NSUCCESSORS-1]

  # def check_predecessor(self):
  #   if self.predecessor failed:
  #     self.precedessor=nil
  
