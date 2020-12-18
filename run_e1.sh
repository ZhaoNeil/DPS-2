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

var3=$(grep -E 'NNODE=' /home/ddps2012/DPS-2/conf.py)
NNODE=$(echo $var3 | grep -P '\d+' -o)

file='ips_e1_'$NNODE'.txt'

printf "%s\n" "${ips[@]}" > /home/ddps2012/result/$file

for i in ${!ips[@]}
do
{
    sleep $(($i*1))
    if [ $i -eq 0 ]
    then
	rNodeAddr='None'
    else
	rNodeAddr=${ips[0]}':10021'
    fi
    ssh ${ips[$i]} python3 -u ~/DPS-2/e1.py ${ips[$i]} $rNodeAddr
}&
done
wait
