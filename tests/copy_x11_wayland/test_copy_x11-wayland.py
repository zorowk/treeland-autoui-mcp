# !/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
x11 wayland copy
"""
import subprocess
import time
import pyautogui
import os


current_directory = os.path.dirname(__file__)
def test_copy_textTOdoc():
    # 打开wps文档
    subprocess.run(['xdg-open', f'{current_directory}/test1.txt'])
    time.sleep(0.2)
    pyautogui.doubleClick()
    pyautogui.hotkey('ctrl','c')
    time.sleep(0.5)
    subprocess.run(['xdg-open', f'{current_directory}/测试文档.docx'])
    time.sleep(0.2)
    pyautogui.doubleClick()
    time.sleep(2)
    pyautogui.moveTo(960,540)
    pyautogui.click()
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(2)


def test_copy_pptTOtext():
    subprocess.run(['xdg-open', f'{current_directory}/测试表格.xlsx'])
    time.sleep(0.5)
    pyautogui.click()
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl','c')
    time.sleep(0.2)
    subprocess.run(['xdg-open', f'{current_directory}/test2.txt'])
    time.sleep(0.2)
    pyautogui.moveTo(980, 520)
    pyautogui.click()
    pyautogui.hotkey('ctrl', 'v')
    #time.sleep(1)
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('delete')
    time.sleep(2)
#
def test_browserTotermial():
    """打开浏览器输入内容"""
    subprocess.Popen('bash -c browser', shell=True)
    time.sleep(1)
    pyautogui.typewrite("https://www.baidu.com")
    time.sleep(1)
    pyautogui.hotkey("enter")
    time.sleep(3)
    pyautogui.click(button='left')
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl','c')
    time.sleep(2)
    subprocess.run(['xdg-open', f'{current_directory}/test3.txt'])
    time.sleep(1)
    # pyautogui.rightClick()
    # pyautogui.move(10,10)
    # time.sleep(1)
    # pyautogui.click()
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('delete')
    time.sleep(2)
#
# if __name__ == '__main__':
#     test_copy_pptTOtext();
#     time.sleep(2)
#     test_copy_pptTOtext();
#     time.sleep(2)
#     test_browserTotermial()