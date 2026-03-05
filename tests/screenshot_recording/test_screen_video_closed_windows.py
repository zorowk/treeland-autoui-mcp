# !/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
录屏回放过程中关闭窗口,复现bug：188393
"""
import os
import time
import pyautogui
from function.get_image import get_image_path2, IMAGE_FOLDER_SCREENSHOT_RECORDING
from function.screen_actions import match_and_move_to, match_and_click


def test_screen_video_windows():
    # 1. 录制视频，(设置录屏保存路径默认为桌面)
    pyautogui.moveTo(0, 0)
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'alt', 'r')
    time.sleep(1)
    pyautogui.dragTo(1800, 900)
    time.sleep(1)
    pyautogui.moveTo(1770, 950)
    time.sleep(0.5)
    pyautogui.click()
    time.sleep(15)
    # 2. 停止录制视频，点击录制按钮（关机按钮前面的坐标位置）
    pyautogui.click(x=1645, y=1055)
    time.sleep(3)
    # 3. 播放视频
    match_and_click(get_image_path2(IMAGE_FOLDER_SCREENSHOT_RECORDING), 'review.png')
    match_and_click()
    time.sleep(3)
    # 4. 视频播放过程中关闭影院，在dock栏点击关闭所有
    match_and_move_to(get_image_path2(IMAGE_FOLDER_SCREENSHOT_RECORDING), 'video.png')
    time.sleep(0.5)
    pyautogui.click(button='right')
    time.sleep(0.5)
    match_and_click(get_image_path2(IMAGE_FOLDER_SCREENSHOT_RECORDING), 'closed.png')
    # 删除录制的视频
    time.sleep(1)
    cmd = 'rm -r ~/Desktop/*.mp4'
    os.system(cmd)
    time.sleep(0.5)
