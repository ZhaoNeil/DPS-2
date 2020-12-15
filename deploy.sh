var1=$(preserve -llist | grep ddps2012)
nodes=$(echo $var1 | grep -P 'node\d+' -o)

for node in $nodes
do
	ssh $node 'python create_addr.py'
    touch addrAll.txt
    cat addrList.txt > addrAll.txt
done

for node in $nodes
do
    ssh $node 'python create_chord.py'
    break
done
