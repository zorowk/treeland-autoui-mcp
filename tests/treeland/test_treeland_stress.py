# !/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
聚合了一些日常操作场景

"""
import random
import re
import subprocess

import pyautogui
import datetime
import time


def _get_current_screen_size():
    result = subprocess.run(['wlr-randr'], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Unable to run wlr-randr: {result.stderr}")
        return None, None

    current_scale = 1.0
    current_resolution = None

    for line in result.stdout.splitlines():
        line = line.strip()

        if line.startswith("Scale:"):
            try:
                current_scale = float(line.split(":", 1)[1].strip())
            except:
                current_scale = 1.0
            continue

        if "current" in line and re.match(r'^\s*\d+x\d+', line):
            res_match = re.match(r'^\s*(\d+)x(\d+)', line)
            if res_match:
                width = int(res_match.group(1))
                height = int(res_match.group(2))
                current_resolution = (width, height)
                break

    if not current_resolution:
        print("Unable to find current resolution from wlr-randr.")
        return None, None

    return (
        int(current_resolution[0] * current_scale),
        int(current_resolution[1] * current_scale),
    )


def test_move_window():
    """移动窗口"""
    # 打开窗口选择移动
    pyautogui.hotkey('ctrl', 'alt', 't')
    time.sleep(1)
    pyautogui.hotkey('alt', 'space')
    time.sleep(0.5)
    for i in range(3):
        pyautogui.hotkey('down')
    pyautogui.press('enter')
    # 移动窗口
    x, y = _get_current_screen_size()
    if x is None or y is None:
        return
    star_t = datetime.datetime.now()
    end_t = datetime.datetime.now()
    while (end_t - star_t).seconds <= 5:
        x1 = random.randint(0, int(x))
        y1 = random.randint(0, int(y)-40)
        pyautogui.moveTo(x1, y1, duration=0.1)
        end_t = datetime.datetime.now()
    pyautogui.hotkey('esc')
    time.sleep(1)
    pyautogui.hotkey('alt', 'f4')


def test_mouse_move():
    # 随机移动鼠标
    x, y = _get_current_screen_size()
    if x is None or y is None:
        return
    starttime = datetime.datetime.now()
    endtime = datetime.datetime.now()
    while (endtime - starttime).seconds <= 5:
        x1 = random.randint(0, int(x))
        y1 = random.randint(0, int(y)-40)
        pyautogui.moveTo(x1, y1, duration=0.1)
        pyautogui.click()
        endtime = datetime.datetime.now()


def test_tab_action():
    # 切换Alt+tab
    for i in range(3):
        pyautogui.keyDown('alt')
        pyautogui.press('tab', presses=8, interval=0.2)
        pyautogui.keyUp('alt')
        time.sleep(1)


def test_openbrowser():
    """打开浏览器输入内容"""
    subprocess.Popen('bash -c browser', shell=True)
    time.sleep(2)
    pyautogui.typewrite("https://pms.uniontech.com/bug-browse-111.html")
    time.sleep(2)
    pyautogui.hotkey("enter")
    time.sleep(2)
    pyautogui.hotkey('alt', 'f4')
    time.sleep(1)
#
#
# def test_ScreenResolution_switch():
#     """切换屏幕分辨率"""
#     # 暂时写死的方式
#     subprocess.Popen("xrandr --output Virtual-1 --mode 1024x768", shell=True)
#     time.sleep(5)
#     subprocess.Popen("xrandr --output Virtual-1 --mode 1920x1080", shell=True)
#     time.sleep(5)
#     subprocess.Popen("xrandr --output Virtual-1 --mode 1920x1040", shell=True)
#     time.sleep(5)
    # 本地调试数据
    # subprocess.Popen("xrandr --output HDMI-A-0 --mode 1440x900", shell=True)
    # time.sleep(5)
    # subprocess.Popen("xrandr --output HDMI-A-0 --mode 1024x768", shell=True)
    # time.sleep(5)
    # subprocess.Popen("xrandr --output HDMI-A-0 --mode 1920x1080", shell=True)
    # time.sleep(5)