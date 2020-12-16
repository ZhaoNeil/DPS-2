var=$(preserve -llist | grep -P 'ddps2012')
id=`echo "$var"|awk -F ' ' '{print $1}'`
echo $id
preserve -c $id
