#! /usr/bin/bash

TIME=`date +%m%d%H%M%S`

#打开系统自研应用
apps=( "deepin-movie" "deepin-music" "dman" "browser" "wps")

for app in "${apps[@]}"
do
	nohup bash -c "$app" &
	sleep 1
done

mv ~/apptab.log ~/apptab-$TIME.log
mv ~/top.log ~/top-$TIME.log

#循环alt_tab
mv ~/test_alt_tab_action.log ~/test_alt_tab_action-$TIME.log
for ((i=1; i<=$1; i++))
do
  TTIME=`date +%m%d%H%M%S`
  pytest test_alt_tab_action.py
  top -o+%MEM -b -n 1 | grep ^top -A 50 >> ~/top.log
	sleep 5
	echo "*******$TTIME:第$i次测试********" >> ~/test_alt_tab_action.log
done

for pcs in "${apps[@]}"
do
	pkill "$pcs" &
	sleep 1
done
