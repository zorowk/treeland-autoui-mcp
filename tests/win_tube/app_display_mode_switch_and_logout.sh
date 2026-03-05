#! /usr/bin/bash

TIME=`date +%m%d%H%M%S`

mv ~/test_display_mode_switch_and_logout.log ~/test_display_mode_switch_and_logout-$TIME.log
mv ~/top-displaymode.log ~/top-displaymode-$TIME.log

for ((i=1; i<=$1; i++))
do
  TTIME=`date +%m%d%H%M%S`
	pytest test_display_mode_switch_and_logout.py
	top -o+%MEM -b -n 1 | grep ^top -A 50 >> ~/top-displaymode.log
	echo "*******$TTIME:第$i次测试********" >> ~/test_display_mode_switch_and_logout.log
	sleep 1
done
