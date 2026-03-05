#! /usr/bin/bash

TIME=`date +%m%d%H%M%S`

mv ~/test_openclosed_windows.log ~/test_openclosed_windows-$TIME.log

for ((i=1; i<=$1; i++))
do
	TTIME=`date +%m%d%H%M%S`
	pytest test_openclosed_windows.py
	echo "*******$TTIME:第$i次测试********" >> ~/test_openclosed_windows.log
	sleep 3
done
