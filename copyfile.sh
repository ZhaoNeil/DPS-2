var1=$(preserve -llist | grep ddps2012)
nodes=$(echo $var1 | grep -P 'node\d+' -o)

for node in $nodes
do
    scp -r ../DPS-2 $node:/home/ddps2012
done