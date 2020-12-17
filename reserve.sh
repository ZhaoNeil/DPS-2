var1=$(grep -E 'NMACHINES=' /home/ddps2012/DPS-2/conf.py)
N=$(echo $var1 | grep -P '\d+' -o)

preserve -# $N -t 00:15:00
sleep 2
preserve -llist
