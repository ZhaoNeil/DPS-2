# %%
import numpy as np
NNODE=64    #the number of nodes
NMACHINE=8  #number of machines
FAIL_PROB=0.2   #probility of node failure

M=20    #the size of finger table, or the number of bits for the identifier
SIZE=2**M   #the size of identifier space

NSUCCESSOR=2*int(np.log2(NNODE))  #the length of successor list

NQUERY=int(100/NMACHINE)+1  #number of queries for each machine
PORT_FROM=10021
PORT_TO=int(PORT_FROM+NNODE/NMACHINE)

STABILIZE_INT=1  #the sleep time of the stabilize operation
STABILIZE_RET=3   #the maximum retry times of the stabilize operation
FIX_FINGERS_INT=1   #the sleep time of the fix_fingers operation
FIX_FINGERS_RET=3   #the maximum retry times of the fix_fingers operation
FIND_SUCCESSOR_RET=3
COUNT_STEP_RET=4
COUNT_TIMEOUT_RET=4

# %%
