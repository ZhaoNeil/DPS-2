from conf import *
def get_hash(address):
  ip, port=address[0], address[1]
  return hash(("%s:%s" %(ip, port)).encode())%CHORD_SIZE