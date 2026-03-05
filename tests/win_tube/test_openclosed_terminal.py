# !/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
快捷键打开多个终端窗口，dock栏全部关闭多个终端窗口
"""
import time
import pyautogui
from function.get_image import get_image_path2, IMAGE_FOLDER_WIN_TUBE
from function.screen_actions import match_and_move_to,match_and_click


def test_mouse_move():
    LOOP_TIMES = 20  # 循环次数
    for i in range(LOOP_TIMES):
        pyautogui.hotkey('ctrl', 'alt', 't')
    match_and_move_to(get_image_path2(IMAGE_FOLDER_WIN_TUBE), 'terminal.png')
    time.sleep(0.5)
    pyautogui.mouseDown(button='right')
    time.sleep(0.5)
    match_and_click(get_image_path2(IMAGE_FOLDER_WIN_TUBE), 'closed.png')
