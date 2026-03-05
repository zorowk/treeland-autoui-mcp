#! /usr/bin/bash

TIME=`date +%m%d%H%M%S`

mv ~/copy.log ~/copy-$TIME.log
mv ~/top.log ~/top-$TIME.log

for ((i=1; i<=$1; i++))
do
	TTIME=`date +%m%d%H%M%S`
	pytest test_copy_x11-wayland.py
	top -o+%MEM -b -n 1 | grep ^top -A 50 >> ~/top.log
	echo "*******$TTIME:第$i次测试********" >> ~/copy.log

	sleep 3
#	process=("browser" "et" "terminal"  "wps" "wpp" "deepin-editor")
  process=("browser" "terminal" "deepin-editor")
  for pcs in "${process[@]}"
  do
	pkill "$pcs" &
	killall /opt/apps/cn.wps.wps-office-pro/files/kingsoft/wps-office/office6/wps
	killall /opt/apps/cn.wps.wps-office-pro/files/kingsoft/wps-office/office6/et
	sleep 1
done
done

ps -ef | grep test_copy_x11-wayland | grep -v grep | awk '{print $2}' | xargs kill -9
