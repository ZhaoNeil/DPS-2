var1=$(preserve -llist | grep ddps2012)
nodes=$(echo $var1 | grep -P 'node\d+' -o)

for node in $nodes
do
{
    ssh $node
    cd ./DPS-2
    while read line
    do
    {
    python e1.py $line 
    }&
    done < addrList.txt
    rm addrList.txt
}&
done
wait
