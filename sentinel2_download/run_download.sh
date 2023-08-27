#!/bin/bash
#Author: Amirhossein Nikfal <https://github.com/anikfal>

#Set the variables below:
export USERNAME=""
export PASSWORD=""
date1=2023-08-10T01:00:00.000Z
date2=2023-08-14T23:00:00.000Z
#--------------------------------------------------------

if [ -z $USERNAME ]; then
	echo No Username. Set one and try again.
	exit
fi
if [ -z $PASSWORD ]; then
	echo No Password. Set one and try again.
	exit
fi

echo There are also more detailed information in dhusget.sh you can modify.
echo ""
AllLines=`cat latlon_list.csv | wc -l`
for var in `seq 2 $AllLines`
do
	long1=`sed -n "$var p" latlon_list.csv | cut -d "," -f 2`
	long2=$long1"1"
	lat1=`sed -n "$var p" latlon_list.csv | cut -d "," -f 3`
	lat2=$lat1"1"
	./dhusget.sh -c $long1,$lat1:$long2,$lat2 -S $date1 -E $date2
	cat product_list >> product_list_copy
done

mv product_list_copy product_list  ##product_list_copy must be moved or removed, otherwise, new product_list will be appended to it
./dhusget.sh -r product_list
