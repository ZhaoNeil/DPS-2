LOGSIZE=10    #the size of finger table
CHORD_SIZE=2**LOGSIZE   # the maximum number of nodes in the chord ring
NSUCCESSORS=LOGSIZE
STABILIZE_INT=5  #the sleep time of the stabilize operation
STABILIZE_RET=3   #the maximum retry times of the stabilize operation
FIX_FINGERS_INT=5   #the sleep time of the fix_fingers operation
FIX_FINGERS_RET=3   #the maximum retry times of the fix_fingers operation
# FIND_SUCCESSOR_RET=1