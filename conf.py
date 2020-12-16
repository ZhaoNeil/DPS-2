LOGSIZE=6    #the size of finger table
CHORD_SIZE=(2**LOGSIZE)*100   # the size the chord ring
NSUCCESSORS=2*LOGSIZE
STABILIZE_INT=1  #the sleep time of the stabilize operation
STABILIZE_RET=3   #the maximum retry times of the stabilize operation
FIX_FINGERS_INT=1   #the sleep time of the fix_fingers operation
FIX_FINGERS_RET=3   #the maximum retry times of the fix_fingers operation
FIND_SUCCESSOR_RET=3
NQUERY=333   #number of queries for each chord node
FAIL_PROB=0.2   #probility of node failure
