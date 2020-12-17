LOGSIZE=6    #the size of finger table
NMACHINES=16  #number of machines
FAIL_PROB=0.2   #probility of node failure

CHORD_SIZE=(2**LOGSIZE)*100   # the size the chord ring
NSUCCESSORS=2*LOGSIZE

# NQUERY=int(5000/NMACHINES)+1  #number of queries for each machine
NQUERY=20
PORT_FROM=10010
# PORT_TO=int(PORT_FROM+(2**LOGSIZE)/NMACHINES)
PORT_TO=10030

STABILIZE_INT=1  #the sleep time of the stabilize operation
STABILIZE_RET=3   #the maximum retry times of the stabilize operation
FIX_FINGERS_INT=0.5   #the sleep time of the fix_fingers operation
FIX_FINGERS_RET=3   #the maximum retry times of the fix_fingers operation
FIND_SUCCESSOR_RET=3