from conf import *
def keyInrange(key, a, b):
  '''
  is key in [a, b)?
  '''
  a=a%CHORD_SIZE
  b=b%CHORD_SIZE
  key=key%CHORD_SIZE
  if a<b:
    return a<=key and key<b
  else:
    return a<=key or key<b