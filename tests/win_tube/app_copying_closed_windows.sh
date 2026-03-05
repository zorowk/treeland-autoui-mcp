#! /usr/bin/bash

TIME=`date +%m%d%H%M%S`

mv ~/kwin_test.log ~/kwin_test-$TIME.log

for ((i=1; i<=$1; i++))
do
  TTIME=`date +%m%d%H%M%S`
  python3 -m pytest test_copying_closed_windows.py
	sleep 5
	echo "*******$TTIME:第$i次测试********" >> ~/kwin_test.log
done
