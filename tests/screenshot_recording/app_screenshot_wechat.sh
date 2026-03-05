#! /usr/bin/bash

TIME=`date +%m%d%H%M%S`

mv ~/test_screenshot_wechat.log ~/test_screenshot_wechat-$TIME.log

for ((i=1; i<=$1; i++))
do
  TTIME=`date +%m%d%H%M%S`
  pytest test_screenshot_wechat.py
	sleep 10
	echo "*******$TTIME:第$i次测试********" >> ~/test_screenshot_wechat.log
done
