  #! /usr/bin/bash
  TIME=`date +%m%d%H%M%S` #记录执行时间戳

  mv ~/test_move_window.log ~/test_move_window-$TIME.log #测试日志记录
  for ((i=1; i<=$1; i++)) #循环，$1表示接收一个参数，此处表示循环次数
  do
#    pytest test_split_screen.py
    TTIME=`date +%m%d%H%M%S`
    pytest test_move_contorl_center_window.py #pytest后跟需要执行的测试文件
    sleep 5
    echo "*******$TTIME:第$i次测试********" >> ~/test_move_window.log #记录日志
  done
