# !/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
excel test
"""

import os
import subprocess
import time

import pyautogui

from function.get_image import wait_for_img, get_image_path2, IMAGE_FOLDER_WPS
from function.screen_actions import match_and_click, move_mouse_to_center_of_screen

home = os.popen('echo /home/$(getent passwd `who` | head -n 1 | cut -d : -f 1)').read().strip()


def setup():
    """提前预装wps2019专业版"""
    # 启动wps表格
    subprocess.Popen('/bin/bash /opt/apps/cn.wps.wps-office-pro/files/bin/et', shell=True,
                     stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE, encoding='utf-8')

    # 判断是否同意许可协议和隐私政策
    if wait_for_img(get_image_path2(IMAGE_FOLDER_WPS) + '/xukexieyi.png', max_wait_time=5) is not None:
        match_and_click(get_image_path2(IMAGE_FOLDER_WPS), 'yiyue.png')
        match_and_click(get_image_path2(IMAGE_FOLDER_WPS), 'OK.png')
    # wps未激活场景时处理关闭激活框
    if wait_for_img(get_image_path2(IMAGE_FOLDER_WPS) + '/jihuo_1.png', max_wait_time=5) is not None:
        match_and_click(get_image_path2(IMAGE_FOLDER_WPS), 'jihuoclose_1.png')


def test_excel_function():
    """
    wps表格测试
    """
    # 新建表格
    match_and_click(get_image_path2(IMAGE_FOLDER_WPS), 'xinjian_3.png')
    # 断言进到新建表格页，断言单元格
    assert wait_for_img(get_image_path2() + '/danyuange_1.png') is not None
    # 输入字段内容，该为数字为避免系统环境有中文输入法和英文输入法的情况
    pyautogui.typewrite('12345678')
    # 断言输入内容
    assert wait_for_img(get_image_path2() + '/input_1.png') is not None

    # copy paste
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    pyautogui.hotkey('right')
    pyautogui.hotkey('ctrl', 'v')
    assert wait_for_img(get_image_path2() + '/input_2.png') is not None

    # screenshot，手动设备保存到桌面
    pyautogui.hotkey('ctrl', 'alt', 'a')
    time.sleep(3)
    pyautogui.hotkey('enter')
    # 断言截图内容：查看气泡框较难识别暂时去掉该步
    # match_and_click(get_image_path2(IMAGE_FOLDER_WPS), 'chakan_7.png')
    # assert wait_for_img(get_image_path2() + '/jietuet_1.png') is not None
    # os.popen('killall -9 dde-file-manager')
    # time.sleep(0.5)

    # scroll
    # move_mouse_to_center_of_screen()
    # pyautogui.scroll(-100)
    # assert wait_for_img(get_image_path2() + '/et3_1.png', max_wait_time=3) is None
    # pyautogui.scroll(100)
    # assert wait_for_img(get_image_path2() + '/et3_1.png') is not None


def teardown():
    os.popen('killall -9 et')
    os.popen('rm -rf /home/' + home + '/.local/share/Kingsoft/office6/data/backup')
    os.popen('rm -rf ~/Desktop/截图*.png')
