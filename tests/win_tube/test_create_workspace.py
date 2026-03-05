# !/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
多任务视图下增加删除工作区
"""

import time
import pyautogui

def test_create_workspace():
    pyautogui.hotkey('win', 's')
    for _ in range(5):
        pyautogui.moveTo(2080, 106, duration=0.1)
        pyautogui.click(button='left', duration=0.1)
    time.sleep(1)
    for _ in range(5):
        pyautogui.hotkey('alt', '-')
        time.sleep(1)
    pyautogui.hotkey('win', 's')