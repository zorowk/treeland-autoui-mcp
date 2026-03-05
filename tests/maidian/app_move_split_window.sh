#! /usr/bin/bash

TIME=`date +%m%d%H%M%S`


mv ~/move_split_window.log ~/move_split_window-$TIME.log
mv ~/move_split_window_top.log ~/move_split_window_top-$TIME.log



for ((i=1; i<=$1; i++))
do
	TTIME=`date +%m%d%H%M%S`
	pytest test_split_screen.py
	sleep 3
	pytest test_resize_window.py
	sleep 1

	top -o+%MEM -b -n 1 | grep ^top -A 50 >> ~/move_split_window_top.log

	echo "*******$TTIME:第$i次测试********" >> ~/move_split_window.log

	sleep 3
done


ps -ef | grep test_resize_window | grep -v grep | awk '{print $2}' | xargs kill -9
ps -ef | grep test_split_screen | grep -v grep | awk '{print $2}' | xargs kill -9
