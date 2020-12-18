# %%
from conf import *
import hashlib
def get_hash(address):
  ip, port=address[0], address[1]
  result=hashlib.sha1(("%s:%s" %(ip, port)).encode('utf-8')).hexdigest()
  return int(result, 16)%SIZE
# %%
