# !/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
:Author:yuanrui@uniontech.com
:Date  :2024/5/21 上午10:12
触发浏览器分屏
"""

import time
import pyautogui
from function.get_image import get_image_path2, IMAGE_FOLDER_SPLITVIEW
from function.screen_actions import match_and_click


def test_split_browser_screen():
    """触发浏览器分屏"""
    # subprocess.Popen('bash -c browser', shell=True)
    match_and_click(get_image_path2(IMAGE_FOLDER_SPLITVIEW), 'browser.png')
    #拖拽触发
    time.sleep(3)
    pyautogui.hotkey('win', 'up')
    match_and_click(get_image_path2(IMAGE_FOLDER_SPLITVIEW),'browsers_icon.png')
    time.sleep(1)
    pyautogui.mouseDown()
    pyautogui.dragTo(2880,0,duration=0.5)
    time.sleep(0.5)
    pyautogui.mouseUp()
    time.sleep(0.5)
    #窗口分屏菜单触发
    pyautogui.moveTo(2103, 25, duration=0.1)
    pyautogui.click(button='left', duration=0.1)
    time.sleep(2)
    pyautogui.moveTo(2082, 100, duration=0.1)
    pyautogui.click(button='left', duration=0.1)
    time.sleep(1)
    time.sleep(0.5)
    pyautogui.click(button='left', duration=0.1)
    #关闭
    pyautogui.hotkey('alt', 'f4')
    time.sleep(0.5)