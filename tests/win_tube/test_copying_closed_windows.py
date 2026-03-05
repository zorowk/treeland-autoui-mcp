# !/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
拷贝大文件过程中关闭窗口，为复现bug：https://pms.uniontech.com/bug-view-195239.html
"""
import os
import time
import pyautogui
from function.get_image import get_image_path2, IMAGE_FOLDER_MAIL
from function.screen_actions import match_and_move_to, match_and_click


def test_copying_closed_windows():
    # 1. 打开10个文件管理器
    for i in range(10):
        pyautogui.hotkey('win', 'e')
    time.sleep(3)
    # 2. 选择桌面上待拷贝的文件
    match_and_click(get_image_path2(IMAGE_FOLDER_MAIL), 'desk_manager.png')
    time.sleep(0.5)
    # 前置：将大文件放在名字叫big_file文件夹中/home/cuicui/Desktop/big_file.png
    match_and_click(get_image_path2(IMAGE_FOLDER_MAIL), 'big_file.png')
    # 3. 操作复制
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.5)
    # 4. 粘贴到文档中
    match_and_click(get_image_path2(IMAGE_FOLDER_MAIL), 'wendang.png')
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(2)
    # dock栏关闭文管窗口
    match_and_move_to(get_image_path2(IMAGE_FOLDER_MAIL), 'filemanager.png')
    time.sleep(0.5)
    pyautogui.click(button='right')
    time.sleep(0.5)
    match_and_click(get_image_path2(IMAGE_FOLDER_MAIL), 'closed.png')
    time.sleep(1)
    cmd = 'rm -r ~/Documents/big_file*'
    os.system(cmd)
    time.sleep(0.5)


# def test_screen_video_windows():
#
#     pyautogui.moveTo(0, 0)
#     time.sleep(0.5)
#     pyautogui.hotkey('ctrl', 'alt', 'r')
#     time.sleep(1)
#     pyautogui.dragTo(1920, 1080)
#     time.sleep(1)
#     pyautogui.move(-40, 40)
#     time.sleep(0.5)
#     pyautogui.click()
#     time.sleep(15)
#     # 2. 停止录制视频，点击录制按钮（关节按钮前面的坐标位置）
#     pyautogui.click(x=1980, y=1410)
#     time.sleep(1)
#     # 3. 点击查看
#     match_and_click(get_image_path2(IMAGE_FOLDER_MAIL), 'review.png')
#     time.sleep(3)
#     # 4. 视频播放过程中关闭影院，在dock栏点击关闭所有
#     match_and_move_to(get_image_path2(IMAGE_FOLDER_MAIL), 'video.png')
#     time.sleep(0.5)
#     pyautogui.click(button='right')
#     time.sleep(0.5)
#     match_and_click(get_image_path2(IMAGE_FOLDER_MAIL), 'closed.png')
