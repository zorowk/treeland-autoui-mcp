# !/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
埋点场景：
1. 双屏扩展模式下，在扩展屏/最右边屏幕上触发分屏预览
"""
import subprocess
import pyautogui
import time

def move_window(x,y):
    # 选择移动按钮
    pyautogui.hotkey('alt', 'space')
    time.sleep(0.5)
    for i in range(3):
        pyautogui.hotkey('down')
    pyautogui.hotkey('enter')
    pyautogui.moveTo(x,y,duration=0.5)
    time.sleep(1)

def test_openbrowserer():
    # """打开文管触发分屏"""
    pyautogui.hotkey('win', 'e')
    time.sleep(1)
    screen_width, screen_height = pyautogui.size()
    # print("屏幕尺寸为：宽度 {} 像素，高度 {} 像素".format(screen_width, screen_height))
    move_window(screen_width,screen_height/2)
    time.sleep(1)
    pyautogui.leftClick()
    time.sleep(0.5)
    pyautogui.leftClick()
    time.sleep(1)
    subprocess.Popen('pkill dde-file-manage', shell=True)



