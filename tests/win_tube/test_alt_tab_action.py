# !/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
测试Alt+Tab快捷键
"""

import pyautogui
import time
import logging


def test_alt_tab_action():
    # while True:
    # pyautogui.hotkey('alt', 'tab')

    LOOP_TIMES = 10  #循环次数
    for i in range(LOOP_TIMES):
        retry_count = 3  # 设置重试次数
        try:
            pyautogui.keyDown('alt')
            for _ in range(retry_count):
                try:
                    pyautogui.press('tab', presses=4, interval=0.2)
                    break  # 如果成功则跳出重试循环
                except Exception as e:
                    logging.error(f"Error during tab press in retry {_ + 1}: {e}")
                    time.sleep(0.5)  # 等待一小段时间再重试
            pyautogui.keyUp('alt')
        except Exception as e:
            logging.error(f"Error in key operations: {e}")

