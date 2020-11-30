import socket

class Client:
  def __init__(self, server_address):
    self.addr=server_address

  def open_connection(self):
    self.socket_=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket_.connect(self.addr)

  def close_connection(self):
    self.socket_.close()
    self.socket_=None
  
  def send(self, msg):
    self.socket_.sendall(msg).encode('utf-8')

  def recv(self):
    return self.socket_.recv().decode('utf-8')

  def ping(self):
    try:
      s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.connect(self.addr)
      s.sendall("\r\n")
      s.close()
      return True
    except socket.error:
      return False

  def id(self):
    return get_hash(self.addr)

  def successor(self):
    self.send('get_successor')
    response=json.loads(self.recv())
    return Client(response)

  def predecessor(self):
    self.send('get_predecessor')
    response=self.recv()
    if response=="":
      return None
    response=json.loads(response)
    return Client(response)

  def find_successor(self, keyId):
    self.send('find_successor %s' %keyId)
    response=json.loads(self.recv())
    return Client(response)

  def closet_preceding_finger(self, keyId):
    self.send('closet_preceding_finger %s' %keyId)
    response=json.loads(self.recv())
    return Client(response)

  def notify(self, n_):
    self.send('notify %s %s' %(n_.addr[0], n_addr[1]))

  def get_succList(self):
    self.send('get_succList')
    response=self.recv()

    if response=="":
      return []
    response=json.loads(response)
    return list(map(lambda addr: Client(addr), response))
