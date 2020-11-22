# %%

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

def crange(start, stop):
  result=[]
  index=start
  while index!=stop:
    result.append(index)
    index=(index+1)%modulo
  result.append(index)
  return result

class dotdict(dict):
  def __getattr__(self, name):
    return self[name]

# %%
m=3
modulo=2**m
import hashlib
keyList=[]

import socket, threading
class Node:
  def __init__(self, tmp):
    # self.ip=ip
    # self.port=port
    # self.address=(ip, port)
    self.id=get_hash(tmp)
    self.finger={}
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

  # def connection_thread(self, connection, address):
  #   dDataList=pickle.loads(connection.recv(buffer))
  #   # 5 Types of connections
  #   # type 0: peer connect, type 1: client, type 2: ping, type 3: lookupID, type 4: updateSucc/Pred
  #   connectionType=rDataList[0]
  #   if connectionType==0:
  #     print("Connection with:", address[0], ":", address[1])
  #     print("Join network request received")
  #     self.joinNode(connection, address, rDataList)
  #     self.printMenu()
  #   elif connectionType==1:
  #     print("Connection with:", address[0], ":", address[1])
  #     print("Upload/Download request received")
  #     self.transferFile(connection, address, rDataList)
  #     self.printMenu()
  #   elif connectionType==2:
  #     #print("Ping received")
  #     connection.sendall(pickle.dumps(self.pred))
  #   elif connectionType==3:
  #     #print("Lookip request received")
  #     self.lookupID(connection, address, rDataList)
  #   elif connectionType==4:
  #     #print("Predecessor/Successor update request received")
  #     if rDataList[1]==1:
  #       self.updateSucc(rDataList)
  #     else:
  #       self.updatePred(rDataList)
  #   elif connectionType==5:
  #     #print("Update Finger Table request received")
  #     self.updateTable()
  #     connection.sendall(pickle.dumps(self.succ))
  #   else:
  #     print("Problem with connection type")
  #   #connection.close()


  def find_successor(self, keyId):
    '''
    ask node n to find id's successor
    '''
    if self.pred and keyId in crange(self.pred.id+1, self.id):
      return self
    elif keyId in crange(self.id+1, self.succ.id):
      return self.succ
    else:
      n_=self.closet_preceding_node(keyId)
      return n_.succ

  def closet_preceding_node(self, keyId):
    '''
    return closet node preceding id
    '''
    for i in range(m, 0, -1):
      if self.finger[i].id in crange(self.id+1, keyId-1):
        return finger[i]
    return self

  def stabilize(self):
    '''
    Periodically verify n's immediate successor,
    and tell the successor about n
    '''
    x=self.succ.pred
    if x and x.id in crange(self.id+1, self.succ.id):
      self.succ=x
    self.succ.notify(self)
    # self.update_successor_list(self.succ.succList)

  def notify(self, n_):
    '''
    n_ thinks it might be our predecessor, they are iff
    - we don't have a precedessor OR
    - n_ is in the range (pred(n), n]
    '''
    if self.pred==None or n_.id in crange(self.pred.id+1, self.id):
      self.pred=n_

  def fix_fingers(self):
    '''
    periodically refresh finger table entries
    '''
    self.next+=1
    if self.next>m:
      self.next=1
    keyId=(self.id+2**(self.next-1))%(2**m)
    self.finger[self.next]=self.find_successor(keyId)
  
  def join(self, n_):
    '''
    join a chord ring containing node n_
    '''
    self.pred=None
    if n_:  # join a chord ring containing node n_
      self.succ=n_.find_successor(self.id)
    else:   # create a new chord ring
      self.succ=self
    # self.update_successor_list(self.succ.succList)

  # def check_predecessor(self):
  #   if self.predecessor failed:
  #     self.precedessor=nil
  


# %%
n0=Node('0')
n0.join(None)
n0.fix_fingers()
# %%
n1=Node('1')
n1.join(n0)

n1.stabilize()
n0.stabilize()
# %%
