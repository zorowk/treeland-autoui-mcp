# !/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
埋点场景：
1. wayland应用、x11应用来回进行窗口拖拽缩放窗口大小，几个应用直接来回执行这一操作即可
"""
import subprocess

import pyautogui
import time

def resize_window(x,y):
    # 修改窗口尺寸并关闭窗口
    # 选择更改大小按钮
    pyautogui.hotkey('alt', 'space')
    time.sleep(0.5)
    for i in range(4):
        pyautogui.hotkey('down')
    pyautogui.press('enter')
    # 修改窗口尺寸
    for i in range(5):
        pyautogui.moveRel(x, x, duration=0.5)
        pyautogui.moveRel(y, y, duration=0.5)
    pyautogui.mouseUp()
    # pyautogui.hotkey('alt', 'f4')

def move_window(x,y):
    # 选择移动按钮
    pyautogui.hotkey('alt', 'space')
    time.sleep(0.5)
    for i in range(3):
        pyautogui.hotkey('down')
    pyautogui.hotkey('enter')
    pyautogui.moveTo(x,y,duration=0.5)
    # pyautogui.mouseUp(button='left',x=300,y=300)
    pyautogui.click(button='left')
    time.sleep(1)

def test_move_window():
    """移动窗口"""
    # 打开X11窗口（终端窗口）
    pyautogui.hotkey('ctrl', 'alt', 't')
    time.sleep(1)
    # 选择移动窗口到左屏并修改尺寸
    move_window(500,400)
    resize_window(200,-200)
    time.sleep(1)
    subprocess.Popen('killall deepin-terminal', shell=True)
    time.sleep(1)
    #打开浏览器窗口
    subprocess.Popen('bash -c browser', shell=True)
    time.sleep(2)
    # 选择移动窗口到左屏并修改尺寸
    move_window(500,400)
    resize_window(-200,200)
    time.sleep(1)
    subprocess.Popen('killall browser', shell=True)


