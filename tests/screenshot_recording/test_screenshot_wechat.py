# !/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
1. 系统截图
2. 微信截图
"""
import time
import pyautogui
from function.get_image import get_image_path2, IMAGE_FOLDER_SCREENSHOT_RECORDING
from function.screen_actions import match_and_click


def test_screenshot_wechat():
    # 1. 操作系统截图(设置截图路径默认为剪切板)
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'alt', 'a')
    time.sleep(1)
    # 鼠标移动
    pyautogui.moveTo(300, 300)
    time.sleep(1)
    pyautogui.dragTo(1200, 900)
    time.sleep(1)
    pyautogui.hotkey('enter')
    time.sleep(1)
    # 2. 操作微信截图
    # for i in range(5):
    #     match_and_click(get_image_path2(IMAGE_FOLDER_SCREENSHOT_RECORDING), 'wechat_screen.png')
    #     # 鼠标移动
    #     pyautogui.moveTo(300, 300)
    #     time.sleep(1)
    #     pyautogui.dragTo(1200, 900)
    #     time.sleep(1)
    #     pyautogui.hotkey('esc')
    #     time.sleep(1)
    #     pyautogui.moveTo(300, 300)

