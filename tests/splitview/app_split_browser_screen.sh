#! /usr/bin/bash

TIME=`date +%m%d%H%M%S`

mv ~/test_split_browser_screen.log ~/test_split_browser_screen-$TIME.log

for ((i=1; i<=$1; i++))
do
	TTIME=`date +%m%d%H%M%S`
	pytest test_split_browser_screen.py
	echo "*******$TTIME:第$i次测试********" >> ~/test_split_browser_screen.log
	sleep 3
done