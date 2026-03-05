# !/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
移动控制中心窗口
"""
import datetime
import os
import random
import subprocess
import time
import pyautogui



def test_move_window():
    """移动窗口"""
    subprocess.Popen('nohup bash -c "dde-control-center -s"', shell=True)
    # 打开控制中心窗口:nohup bash -c "dde-control-center -s"
    # 备注：如果测试跟移动窗口时窗口透明显示相关，就手动在控制中心开启该功能按钮
    # match_and_click(get_image_path2(IMAGE_FOLDER1), 'dde-control-center.png')
    time.sleep(1)
    pyautogui.hotkey('alt', 'space')
    time.sleep(1)
    for i in range(3):
        pyautogui.hotkey('down')
    pyautogui.press('enter')
    # 随机移动（窗口）
    #获取当前屏幕分辨率
    hd = os.popen('xrandr | grep current').read().split(',')[1]
    x = hd.split(' ')[2]
    y = hd.split(' ')[4]
    #记录两个时间戳
    star_t = datetime.datetime.now()
    end_t = datetime.datetime.now()
    #如果两个时间之差小于指定时长
    while (end_t - star_t).seconds <= 3:
        #获取随机数
        x1 = random.randint(0, int(x) - 20)
        y1 = random.randint(0, int(y) - 20)
        #移动鼠标到该位置
        pyautogui.moveTo(x1, y1, duration=0.1)
        end_t = datetime.datetime.now()

    pyautogui.hotkey('esc')
    time.sleep(1)
    pyautogui.hotkey('alt', 'f4')

