#! /usr/bin/bash

TIME=`date +%m%d%H%M%S`

# 检查是否提供了参数，如果没有就提示并退出
if [ $# -ne 1 ]; then
    echo "用法: $0 <循环次数>"
    echo "示例: $0 3    （表示循环执行 3 次监控）"
    echo "错误：必须提供一个正整数作为循环次数！"
    exit 1
fi

#打开系统自研应用如邮箱等
apps=("firefox" "dde-file-manager" "deepin-terminal")

for app in "${apps[@]}"
do
    echo "即将执行的命令: $app"
	bash -c "$app" &
	sleep 1
done

echo "------------------------------------------------"
for ((i=1; i<=$1; i++))
do
	TTIME=`date +%m%d%H%M%S`
	top -b -d 5 -n 60 | grep "treeland" > ~/top-cpu.txt
	sleep 5
done

#关闭应用窗口
process=("deepin-editor" "firefox" "dde-file-manager" )
for pcs in "${process[@]}"
do
	pkill -f "$pcs" &
	sleep 1
done
