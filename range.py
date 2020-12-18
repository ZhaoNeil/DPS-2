from conf import *
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