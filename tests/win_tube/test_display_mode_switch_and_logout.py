# !/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
1. 切换屏幕模式然后注销系统
"""
import os
import time
import pyautogui
from function.get_image import get_image_path2, IMAGE_FOLDER_WIN_TUBE
from function.screen_actions import match_and_click


def test_displaymode_switch_logout():
    # 切换屏幕模式
    for i in range(4):
        pyautogui.keyDown('win')
        pyautogui.press('p', presses=2, interval=0.2)
        pyautogui.keyUp('win')
        time.sleep(6)
    # # 点击电源管理界面的注销按钮，注销系统
    # pyautogui.hotkey('ctrl', 'alt', 'delete')
    # match_and_click(get_image_path2(IMAGE_FOLDER_WIN_TUBE), 'logout.png')
    # time.sleep(2)
    # # 通过重启lightdm的方式来模拟重启：sudo systemctl restart lightdm
    # os.system("echo '1'|sudo -S systemctl restart lightdm")
    # time.sleep(2)
