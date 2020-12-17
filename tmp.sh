var1=$(preserve -llist | grep ddps2012)
nodes=$(echo $var1 | grep -P 'node\d+' -o)
nodes=($nodes)
ips=()

for i in ${!nodes[@]}
do
  {
    var2=host $(nodes[i])
    var3=$(echo $var2 | grep -P '\d+.\d+.\d+.\d+' -o)
    ips+=($var3)
  } done
