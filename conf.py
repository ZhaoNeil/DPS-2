LOGSIZE=8    #the size of finger table
NMACHINES=16  #number of machines
FAIL_PROB=0.2   #probility of node failure

CHORD_SIZE=(2**LOGSIZE)*50   # the size the chord ring
NSUCCESSORS=2*LOGSIZE

NQUERY=int(100/NMACHINES)+1  #number of queries for each machine
PORT_FROM=10021
PORT_TO=int(PORT_FROM+(2**LOGSIZE)/NMACHINES)

STABILIZE_INT=1  #the sleep time of the stabilize operation
STABILIZE_RET=3   #the maximum retry times of the stabilize operation
FIX_FINGERS_INT=1   #the sleep time of the fix_fingers operation
FIX_FINGERS_RET=3   #the maximum retry times of the fix_fingers operation
FIND_SUCCESSOR_RET=3
COUNT_STEP_RET=4
COUNT_TIMEOUT_RET=4
