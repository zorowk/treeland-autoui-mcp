#! /usr/bin/bash

TIME=`date +%m%d%H%M%S`

mv ~/test_open_browser_tab.log ~/test_open_browser_tab-$TIME.log
mv ~/apptab.log ~/apptab-$TIME.log
mv ~/top.log ~/top-$TIME.log

for ((i=1; i<=$1; i++))
do
  TTIME=`date +%m%d%H%M%S`
  pytest test_open_browser_tab.py
  top -o+%MEM -b -n 1 | grep ^top -A 50 >> ~/top.log
	sleep 10
	echo "*******$TTIME:第$i次测试********" >> ~/test_open_browser_tab.log
done