var1=$(preserve -llist | grep ddps2012)
nodes=$(echo $var1 | grep -P 'node\d+' -o)
nodes=($nodes)

for i in ${!nodes[@]}
do
{
	sleep $i
	if [ $i -eq 0 ]
		then
			rNodeAddr='None'
		else
			rNodeAddr=(${nodes[$i]}':10001')
		fi
		ssh ${nodes[$i]} python3 -u ~/DPS-2/e1.py ${ports[$j]} $rNodeAddr
    }& done
}&
done
wait
