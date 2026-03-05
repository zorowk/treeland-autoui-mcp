# !/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
wps test
"""

import os
import subprocess
import time

import pyautogui

from function.get_image import wait_for_img, get_image_path2, IMAGE_FOLDER_WPS
from function.screen_actions import match_and_click, move_mouse_to_center_of_screen

home = os.popen('echo /home/$(getent passwd `who` | head -n 1 | cut -d : -f 1)').read().strip()


def setup():
    subprocess.Popen('/bin/bash /opt/apps/cn.wps.wps-office-pro/files/bin/wps', shell=True,
                     stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE, encoding='utf-8')

    # 判断是否同意许可协议和隐私政策
    if wait_for_img(get_image_path2(IMAGE_FOLDER_WPS) + '/xukexieyi.png', max_wait_time=5) is not None:
        match_and_click(get_image_path2(IMAGE_FOLDER_WPS), 'yiyue.png')
        match_and_click(get_image_path2(IMAGE_FOLDER_WPS), 'OK.png')

    # wps未激活场景时处理关闭激活框
    if wait_for_img(get_image_path2(IMAGE_FOLDER_WPS) + '/jihuo_1.png', max_wait_time=5) is not None:
        match_and_click(get_image_path2(IMAGE_FOLDER_WPS), 'jihuoclose_1.png')


def test_wps_function():
    # input content
    # 新建表格
    match_and_click(get_image_path2(IMAGE_FOLDER_WPS), 'xinjian_3.png')
    assert wait_for_img(get_image_path2() + '/start.png') is not None
    # 关闭样式和格式
    if wait_for_img(get_image_path2() + '/wpp_8.png') is not None:
        match_and_click(get_image_path2(IMAGE_FOLDER_WPS), 'wpp_8.png')
    #  开始编辑内容
    pyautogui.typewrite('hellouniontech')
    assert wait_for_img(get_image_path2() + '/wps_5.png') is not None

    # copy paste
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    pyautogui.hotkey('right')
    pyautogui.hotkey('ctrl', 'v')
    assert wait_for_img(get_image_path2() + '/wps_6.png') is not None

    # screenshot
    pyautogui.hotkey('ctrl', 'alt', 'a')
    time.sleep(3)
    pyautogui.hotkey('enter')
    # match_and_click(get_image_path2(IMAGE_FOLDER_WPS), 'wps_7.png')
    # assert wait_for_img(get_image_path2() + '/wps_8.png') is not None
    # os.popen('killall -9 dde-file-manager')
    # time.sleep(0.5)
    #
    # # scroll
    # move_mouse_to_center_of_screen()
    # pyautogui.hotkey('ctrl', 'a')
    # pyautogui.hotkey('ctrl', 'c')
    # for _ in range(20):
    #     time.sleep(0.3)
    #     pyautogui.hotkey('ctrl', 'v')
    # pyautogui.typewrite('end')
    # pyautogui.scroll(300)
    # assert wait_for_img(get_image_path2() + '/wps_9.png', max_wait_time=3) is None
    # pyautogui.scroll(-300)
    # assert wait_for_img(get_image_path2() + '/wps_9.png') is not None


def teardown():
    os.popen('killall -9 wps')
    os.popen('rm -rf /home/' + home + '/.local/share/Kingsoft/office6/data/backup')
    os.popen('rm -rf ~/Desktop/截图*.png')
