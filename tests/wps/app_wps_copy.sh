#! /usr/bin/bash

TIME=`date +%m%d%H%M%S`

mv ~/wpsCopy.log ~/wpsCopy-$TIME.log

for ((i=1; i<=$1; i++))
do
	pytest test_wps_copy.py
	echo "*******第$i次测试********" >> ~/wpsCopy.log
done
