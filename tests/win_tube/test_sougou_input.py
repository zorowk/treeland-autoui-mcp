import subprocess
import time
import pyautogui

from function.get_image import get_image_path2
from function.screen_actions import match_and_click
"""
在浏览器地址栏使用搜狗输入法输入内容
"""

def test_sougou_input():
    # subprocess.Popen('bash -c browser', shell=True)
    # time.sleep(1)
    time.sleep(5)
    pyautogui.moveTo(1453, 91, duration=0.1)  # 浏览器地址栏位置坐标
    for _ in range(100):
        pyautogui.typewrite("w")

