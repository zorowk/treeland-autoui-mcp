# !/usr/bin/env python3
# -*- coding:utf-8 -*-
#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
:Author:yuanrui@uniontech.com
:Date  :2024/6/15 上午11:14
"""

"""
move window
"""
import subprocess
import time
import pyautogui
from function.screen_actions import match_and_click, match_and_move_to
from function.get_image import get_image_path2
from function.get_image import IMAGE_FOLDER_BROWSER

def test_openbrowser_tab():
    """打开浏览器选项卡"""
    NUM_NEW_TABS = 2
    for _ in range(3):
        try:
            subprocess.Popen('bash -c browser', shell=True)
            time.sleep(0.5)
            pyautogui.hotkey('win', 'up')
            for _ in range(NUM_NEW_TABS):
                pyautogui.hotkey('ctrl', 't')
        except Exception as e:
            print(f"Error opening browser or creating new tabs: {e}")
    time.sleep(2)
    match_and_move_to(get_image_path2(IMAGE_FOLDER_BROWSER), 'browser.png')
    time.sleep(0.5)
    pyautogui.click(button='right')
    time.sleep(0.5)
    match_and_click(get_image_path2(IMAGE_FOLDER_BROWSER), 'closed.png')
