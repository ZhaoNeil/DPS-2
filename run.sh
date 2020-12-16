var1=$(preserve -llist | grep ddps2012)
nodes=$(echo $var1 | grep -P 'node\d+' -o)
nodes=($nodes)

ports=({10001..10020})
addrList=()


for i in ${!nodes[@]}
do
{
    for j in ${!ports[@]}
	{
		time.sleep(i+j*2)
		
		if [ $i -eq 0 ] && [ $j -eq 0 ]
		then
			rNodeAddr='None'
		else
			ix=$[$RANDOM % ${#addrList[@]}]
			rNodeAddr=${addrList[$ix]}
		fi
		addrList+=(${nodes[$i]}':'${ports[$j]})
		ssh ${nodes[$i]} python3 -u python e1.py ${ports[$j]} $rNodeAddr
    }&
    done
}&
done
wait
