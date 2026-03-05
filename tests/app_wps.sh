#! /usr/bin/bash

TIME=`date +%m%d%H%M%S`

#preapps=("/usr/lib/cmclient/cmclient" "/usr/lib/unity-happypa/unity-happypa" "/opt/apps/cn.com.topsec.topdesk/files/TDABDGL2" "/opt/apps/cn.com.topsec.edragent/files/Edragent.sh" "/usr/bin/browser")

#for preapp in "${preapps[@]}"
#do
#	nohup bash -c "$preapp" &
#	sleep 1
#done

mv ~/looptest.log ~/looptest-$TIME.log

for ((i=1; i<=$1; i++))
do
  TTIME=`date +%m%d%H%M%S`
	pytest wps
	echo "*******$TTIME:第$i次测试********" >> ~/looptest.log
done
