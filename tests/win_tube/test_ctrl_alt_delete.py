# !/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
进入电源管理界面并退出
"""
import time
import pyautogui


def test_move_window():
    """ctrl_alt_delete"""
    for i in range(10):
        pyautogui.hotkey('ctrl', 'alt', 'delete')
        time.sleep(0.5)
        pyautogui.hotkey('esc')
        time.sleep(0.5)