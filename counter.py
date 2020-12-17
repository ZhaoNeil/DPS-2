class StepCounter:
  def __init__(self):
    self.path_len={}

  def init_path_len(self, keyId):
    self.path_len[keyId]=1

  def update_path_len(self, keyId, nSteps):
    if keyId not in self.path_len:
      self.path_len[keyId]=nSteps
    else:
      self.path_len[keyId]+=nSteps


class TimeoutCounter:
  def __init__(self):
    self.failedAddr={}
    self.nTimeout={}

  def update_failedAddr(self, keyId, n_):
    if keyId not in self.failedAddr:
      self.failedAddr[keyId]=[n_.addr]
      self.update_nTimeout(keyId, 1)
    else:
      if n_.addr not in self.failedAddr[keyId]:
        self.failedAddr[keyId].append(n_.addr)
        self.update_nTimeout(keyId, 1)

  def update_nTimeout(self, keyId, nFailed):
    if nFailed>0:
      if keyId not in self.nTimeout:
        self.nTimeout[keyId]=nFailed
      else:
        self.nTimeout[keyId]+=nFailed

  def get_nTimeout(self, keyId):
    if keyId in self.nTimeout:
      return self.nTimeout[keyId]
    return 0
