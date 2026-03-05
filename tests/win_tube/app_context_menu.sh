#! /usr/bin/bash

TIME=`date +%m%d%H%M%S`

mv ~/test_Context_Menu.log ~/test_Context_Menu-$TIME.log

for ((i=1; i<=$1; i++))
do
  TTIME=`date +%m%d%H%M%S`
  pytest test_context_menu.py
	sleep 5
	echo "*******$TTIME:第$i次测试********" >> ~/test_Context_Menu.log
done
