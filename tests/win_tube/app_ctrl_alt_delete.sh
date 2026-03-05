#! /usr/bin/bash

TIME=`date +%m%d%H%M%S`

#如果采用开机自启动的方式执行该脚本
#第一步：将脚本文件放在家目录下
#第二步：将 ~/.config/autostart/test.start.desktop路径下的test.start.desktop文件下的Exec参数改为：bash /home/uos/pythonProject/script/app_ctrl_alt_delete.sh
#第三步：将本脚本添加切换路径命令,如下：
# cd /home/uos/pythonProject/script/

for ((i=1; i<=1; i++))
do
	TTIME=`date +%m%d%H%M%S`
	pytest test_ctrl_alt_delete.py &
	sleep 15
	echo "1" | sudo -S reboot
	echo "*******$TTIME:第$i次测试********" >> ~/test_ctrl_alt_delete.log
	sleep 3
done


