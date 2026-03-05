# !/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
ppt test
"""
import os
import subprocess
import time

import pyautogui
import pyperclip
from function.get_image import wait_for_img, get_image_path2, IMAGE_FOLDER_WPS
from function.screen_actions import match_and_click, move_mouse_to_center_of_screen, match_and_move_to

pyperclip.copy('')
home = os.popen('echo /home/$(getent passwd `who` | head -n 1 | cut -d : -f 1)').read().strip()


def setup():
    subprocess.Popen('/bin/bash /opt/apps/cn.wps.wps-office-pro/files/bin/wpp', shell=True,
                     stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE, encoding='utf-8')

    # 判断是否同意许可协议和隐私政策
    if wait_for_img(get_image_path2(IMAGE_FOLDER_WPS) + '/xukexieyi.png', max_wait_time=5) is not None:
        match_and_click(get_image_path2(IMAGE_FOLDER_WPS), 'yiyue.png')
        match_and_click(get_image_path2(IMAGE_FOLDER_WPS), 'OK.png')

    # wps未激活场景时处理关闭激活框
    if wait_for_img(get_image_path2(IMAGE_FOLDER_WPS) + '/jihuo_1.png', max_wait_time=5) is not None:
        match_and_click(get_image_path2(IMAGE_FOLDER_WPS), 'jihuoclose_1.png')


def test_ppt_function():
    """
    :return:
    """
    # input content
    # 新建ppt页
    match_and_click(get_image_path2(IMAGE_FOLDER_WPS), 'xinjian_3.png')
    # 关闭样式和格式
    if wait_for_img(get_image_path2() + '/ppt_wpp_8.png') is not None:
        match_and_click(get_image_path2(IMAGE_FOLDER_WPS), 'ppt_wpp_8.png')
    # 进入到新建页面
    assert wait_for_img(get_image_path2() + '/wpp_1.png') is not None
    # 点击【单击此处】编辑内容
    match_and_click(get_image_path2(IMAGE_FOLDER_WPS), 'wpp_1.png')
    pyperclip.copy('12345678')
    time.sleep(2)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.typewrite('12345678')
    assert wait_for_img(get_image_path2() + '/wpp_2.png') is not None

    # copy paste
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    pyautogui.hotkey('right')
    pyautogui.hotkey('ctrl', 'v')
    assert wait_for_img(get_image_path2() + '/wpp_3.png') is not None

    # screenshot，手动设备保存到桌面
    pyautogui.hotkey('ctrl', 'alt', 'a')
    time.sleep(3)
    pyautogui.hotkey('enter')
    # 点击截图保存气泡框里的【查看】，识别不准确，不测试后续步骤
    # match_and_click(get_image_path2(IMAGE_FOLDER_WPS), 'wps_7.png')
    # assert wait_for_img(get_image_path2() + '/wpp_4.png') is not None
    # os.popen('killall -9 dde-file-manager')
    # time.sleep(0.5)

    # scroll
    # move_mouse_to_center_of_screen()
    # match_and_click(get_image_path2(IMAGE_FOLDER_WPS), 'wpp_5.png')
    # for _ in range(8):
    #     time.sleep(0.3)
    #     match_and_click(get_image_path2(IMAGE_FOLDER_WPS), 'wpp_6.png')
    # match_and_move_to(get_image_path2(IMAGE_FOLDER_WPS), 'wpp_7.png')
    # pyautogui.scroll(300)
    # assert wait_for_img(get_image_path2() + '/wpp_7.png', 0.9, 3) is None
    # pyautogui.scroll(-300)
    # assert wait_for_img(get_image_path2() + '/wpp_7.png', 0.9) is not None


def teardown():
    os.popen('killall -9 wpp')
    os.popen('rm -rf /home/' + home + '/.local/share/Kingsoft/office6/data/backup')
    os.popen('rm -rf ~/Desktop/截图*.png')
