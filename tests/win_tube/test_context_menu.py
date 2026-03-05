# !/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
鼠标移动到文件管理器标题栏，连续右击，触发菜单栏
"""
import pyautogui
import time

def test_context_menu():
    try:
        pyautogui.hotkey('win', 'e')
        time.sleep(3)
        start_x = 900
        end_x = 1000
        for x in range(start_x, end_x + 1):  # 包含 end_x
            try:
                pyautogui.doubleClick(x, 200, duration=0.3, button="right")
            except Exception as e:
                print(f"在 x={x} 处点击时出错: {e}")
        time.sleep(1)
        pyautogui.hotkey('esc')
        pyautogui.hotkey('alt', 'f4')
    except Exception as e:
        print(f"整体执行过程中出错: {e}")