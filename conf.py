# %%
import math
NNODE=1020    #the number of nodes
NMACHINE=51  #number of machines
FAIL_PROB=0.5   #probility of node failure

M=20    #the size of finger table, or the number of bits for the identifier
SIZE=2**M   #the size of identifier space

#NSUCCESSOR=2*int(math.log2(NNODE))  #the length of successor list
NSUCCESSOR=20

NQUERY=int(10000/NMACHINE)+1  #number of queries for each machine
PORT_FROM=10100
PORT_TO=int(PORT_FROM+NNODE/NMACHINE)

STABILIZE_INT=0.3  #the sleep time of the stabilize operation
STABILIZE_RET=3   #the maximum retry times of the stabilize operation
FIX_FINGERS_INT=0.3   #the sleep time of the fix_fingers operation
FIX_FINGERS_RET=3   #the maximum retry times of the fix_fingers operation
FIND_SUCCESSOR_RET=3
COUNT_STEP_RET=4
COUNT_TIMEOUT_RET=4

# %%
