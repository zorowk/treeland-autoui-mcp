#! /usr/bin/bash

TIME=`date +%m%d%H%M%S`

mv ~/test_win.log ~/test_win-$TIME.log

for ((i=1; i<=$1; i++))
do
  TTIME=`date +%m%d%H%M%S`
	pytest test_sougou_input.py
	pytest test_win.py
	sleep 1
	echo "*******$TTIME:第$i次测试********" >> ~/test_win.log
done