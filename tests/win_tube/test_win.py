import time
import pyautogui
from function.get_image import get_image_path2
from function.screen_actions import match_and_click
"""
操作点击左下角启动器
"""

def test_win():
    for _ in range(30):
        time.sleep(0.1)
        # pyautogui.moveTo(21, 1055, duration=0.1)#测试机
        pyautogui.moveTo(31,1408,duration= 0.1)#本机
        pyautogui.click(button='left', duration=0.1)

