var1=$(preserve -llist | grep ddps2012)
nodes=$(echo $var1 | grep -P 'node\d+' -o)
nodes=($nodes)
ips=()

for i in ${!nodes[@]}
do
  {
    var2=$(host ${nodes[$i]} | grep -P '\d+.\d+.\d+.\d+' -o)
    ips+=($var2)
  } done

for i in ${!ips[@]}
do
{
    sleep $(($i*3))
    if [ $i -eq 0 ]
    then
	rNodeAddr='None'
    else
	rNodeAddr=${ips[0]}':10020'
    fi
    ssh ${ips[$i]} python3 -u ~/DPS-2/e1.py ${ips[$i]} $rNodeAddr
}&
done
wait
