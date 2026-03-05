# !/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
操作移动终端窗口
"""
import datetime
import os
import random
import time
import pyautogui

def test_move_window():
    """移动窗口"""
    # 打开终端窗口选择移动
    pyautogui.hotkey('ctrl', 'alt', 't')
    time.sleep(1)
    pyautogui.hotkey('alt', 'space')
    time.sleep(0.5)
    for i in range(3):
        pyautogui.hotkey('down')
    pyautogui.press('enter')
    # 移动窗口
    hd = os.popen('xrandr | grep current').read().split(',')[1]
    x = hd.split(' ')[2]
    y = hd.split(' ')[4]
    star_t = datetime.datetime.now()
    end_t = datetime.datetime.now()
    while (end_t - star_t).seconds <= 5:
        x1 = random.randint(0, int(x))
        y1 = random.randint(0, int(y))
        pyautogui.moveTo(x1, y1, duration=0.1)
        pyautogui.hotkey('esc')
        time.sleep(1)
        pyautogui.hotkey('alt', 'f4')
        end_t = datetime.datetime.now()
