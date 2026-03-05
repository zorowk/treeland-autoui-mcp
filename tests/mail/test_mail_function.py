# !/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
mail test
"""

import os
import subprocess
from time import sleep
import random
import pyautogui

from function.get_image import wait_for_img, get_image_path2, IMAGE_FOLDER_MAIL
from function.screen_actions import match_and_click, move_mouse_to_center_of_screen

home = os.popen('echo /home/$(getent passwd `who` | head -n 1 | cut -d : -f 1)').read().strip()


def setup():
    print("手动布置预制环境")
    # subprocess.Popen('/usr/lib/cmclient/cmclient', shell=True)


def teardown():
    print("压力测试，无须清除环境")


def mousemove():
    x = random.randint(0, 300)
    y = random.randint(-300, 0)
    y1 = random.randint(300, 1200)
    pyautogui.moveTo(650, 750, duration=0.25)
    pyautogui.scroll(x)
    pyautogui.moveTo(650, y1, duration=0.25)
    pyautogui.click()
    sleep(0.5)
    pyautogui.scroll(y)
    pyautogui.moveTo(650, y1, duration=0.25)
    pyautogui.click()


def printscreen():
    pyautogui.hotkey('ctrl', 'alt', 'a')
    sleep(3)
    pyautogui.hotkey('enter')


def test_mail_function():
    """
    :return:
    """
    # 检查是否有截图操作未完成
    if wait_for_img(get_image_path2(IMAGE_FOLDER_MAIL) + '/jt_1.png', max_wait_time=3) is not None:
        match_and_click(get_image_path2(IMAGE_FOLDER_MAIL), 'jt_1.png')
    # 打开浏览器并点击
    match_and_click(get_image_path2(IMAGE_FOLDER_MAIL), 'browser_3.png')
    assert wait_for_img(get_image_path2(IMAGE_FOLDER_MAIL) + '/browser_6.png') is not None
    pyautogui.press('space')
    # 依次点击控件
    # match_and_click(get_image_path2(IMAGE_FOLDER_MAIL), 'browser_5.png')
    # match_and_click(get_image_path2(IMAGE_FOLDER_MAIL), 'browser_2.png')
    # match_and_click(get_image_path2(IMAGE_FOLDER_MAIL), 'browser_1.png')
    # match_and_click(get_image_path2(IMAGE_FOLDER_MAIL), 'browser_7.png')
    sleep(0.5)
    printscreen()

    # 打开写信并输入
    match_and_click(get_image_path2(IMAGE_FOLDER_MAIL), 'mail_11.png')
    assert wait_for_img(get_image_path2(IMAGE_FOLDER_MAIL) + '/mail_1.png', max_wait_time=3) is not None
    # match_and_click(get_image_path2(IMAGE_FOLDER_MAIL), 'mail_1.png')
    # assert wait_for_img(get_image_path2(IMAGE_FOLDER_MAIL) + '/mail_8.png') is not None
    # pyautogui.typewrite('helloasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdmail')
    # printscreen()
    # assert wait_for_img(get_image_path2(IMAGE_FOLDER_MAIL) + '/mail_12.png') is not None
    # # 关闭写信
    # match_and_click(get_image_path2(IMAGE_FOLDER_MAIL), 'mail_6.png')
    # assert wait_for_img(get_image_path2(IMAGE_FOLDER_MAIL) + '/mail_7.png') is not None
    # match_and_click(get_image_path2(IMAGE_FOLDER_MAIL), 'mail_7.png')
    # 滚动查看邮件
    mousemove()
    printscreen()
    sleep(1)

    # 打开et并输入
    match_and_click(get_image_path2(IMAGE_FOLDER_MAIL), 'et_1.png')
    assert wait_for_img(get_image_path2(IMAGE_FOLDER_MAIL) + '/et_2.png', max_wait_time=3) is not None
    if wait_for_img(get_image_path2(IMAGE_FOLDER_MAIL) + '/et_3.png', max_wait_time=3) is not None:
        match_and_click(get_image_path2(IMAGE_FOLDER_MAIL), 'et_3.png')
    # 滚动查看邮件
    mousemove()

    printscreen()

    pyautogui.hotkey('ctrl', 'c')
    mousemove()
    pyautogui.hotkey('ctrl', 'v')
    printscreen()
    sleep(1)

    # # 打开回复并关闭
    # match_and_click(get_image_path2(IMAGE_FOLDER_MAIL), 'mail_3.png')
    # assert wait_for_img(get_image_path2(IMAGE_FOLDER_MAIL
    # ) + '/mail_9.png') is not None
    # # 关闭写信-回复
    # match_and_click(get_image_path2(IMAGE_FOLDER_MAIL), 'mail_6.png')
    # assert wait_for_img(get_image_path2(IMAGE_FOLDER_MAIL) + '/mail_7.png') is not None
    # match_and_click(get_image_path2(IMAGE_FOLDER_MAIL), 'mail_7.png')
    # #滚动查看邮件
    # mousemove()
    # printscreen()
    # sleep(1)
    #
    # # 打开转发并关闭
    # match_and_click(get_image_path2(IMAGE_FOLDER_MAIL), 'mail_4.png')
    # assert wait_for_img(get_image_path2(IMAGE_FOLDER_MAIL) + '/mail_7.png') is not None
    # # 关闭写信-转发
    # match_and_click(get_image_path2(IMAGE_FOLDER_MAIL), 'mail_10.png')
    # assert wait_for_img(get_image_path2(IMAGE_FOLDER_MAIL) + '/mail_7.png') is not None
    # match_and_click(get_image_path2(IMAGE_FOLDER_MAIL), 'mail_7.png')
    # #滚动查看邮件
    # mousemove()
    # sleep(1)
