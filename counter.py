class StepCounter:
  def __init__(self):
    self.path_len={}

  def update_path_len(self, keyId, nSteps):
    if keyId not in self.path_len:
      self.path_len[keyId]=nSteps
    else:
      self.path_len[keyId]+=nSteps


class TimeoutCounter:
  def __init__(self):
    self.timeouts={}
    self.nTimeout={}

  def update_timeouts(self, keyId, n_):
    if keyId not in self.timeouts:
      self.timeouts[keyId]=[n_.addr]
      self.nTimeout[keyId]=1
    else:
      if n_.addr not in self.timeouts[keyId]:
        self.timeouts[keyId].append(n_.addr)
        self.nTimeouts[keyId]+=1

  def update_nTimeout(self, keyId, nFailed):
    if keyId not in self.nTimeout:
      self.nTimeout[keyId]=nFailed
    else:
      self.nTimeout[keyId]+=nFailed
