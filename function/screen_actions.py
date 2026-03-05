# !/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
触摸屏操作
"""
# ****************************************************
# File Name: screen_actions.py
# Author:  UT003267
# Created : 2021/6/21 上午11:14
# Description:
#
# Function List:
#
# ****************************************************
import time

import pyautogui
import pyperclip
from PIL import Image

from function.uos_public_operation.wait import AutoTool
from function.get_image import get_image_path, wait_for_img, wait_for_img2

image_path = get_image_path()

def move_mouse_to_center_of_screen():
    """
    把鼠标移动到屏幕中央
    """
    # 获取当前屏幕分辨率
    screen_width, screen_height = pyautogui.size()

    # 移动鼠标到屏幕中央
    pyautogui.moveTo(screen_width / 2, screen_height / 2)


def match_and_click(image_path_abs=image_path, image_name='',
                    click_action='left', confidencevalue=0.5, x_axis=0, y_axis=0):
    """
    匹配图片并点击
    @param click_action: 左击/右击
    @param image_path_abs:  图片所在绝对路径
    @param image_name:  图片名字
    @param confidencevalue:  精度
    @param x_axis:  x偏移量
    @param y_axis:  y偏移量
    """
    # 匹配图片坐标
    match_result = wait_for_img(image_path_abs + image_name, confidencevalue)
    assert match_result is not None
    # 根据偏移，刷新坐标
    x_refresh = match_result['result'][0] + x_axis
    y_refresh = match_result['result'][1] + y_axis
    # 移动到
    pyautogui.moveTo(x_refresh, y_refresh, duration=0.5)
    time.sleep(0.5)
    # 点击
    if click_action == 'left':
        pyautogui.click(x_refresh, y_refresh, duration=0.5)
    elif click_action == 'right':
        pyautogui.rightClick(x_refresh, y_refresh, duration=0.5)
    elif click_action == 'double':
        pyautogui.doubleClick(x_refresh, y_refresh, duration=0.5)
    time.sleep(0.5)


def match_and_click2(image1='', image2='',
                     click_action='left', confidencevalue=0.5, x_axis=0, y_axis=0):
    """
    二级匹配图片并点击
    @param click_action: 左击/右击
    @param image1:  大图
    @param image2: 小图
    @param confidencevalue:  精度
    @param x_axis:  x偏移量
    @param y_axis:  y偏移量
    """
    # 二级匹配图片坐标
    match_result = wait_for_img(image1, confidencevalue=confidencevalue)
    assert match_result is not None
    match_result2 = wait_for_img2(Image.open(image1), image2, confidencevalue=confidencevalue)
    assert match_result2 is not None
    # 根据偏移，刷新坐标
    x_refresh = match_result2['rectangle'][2] / 2 + match_result['rectangle'][0] + \
                match_result2['rectangle'][0] + x_axis
    y_refresh = match_result2['rectangle'][3] / 2 + match_result['rectangle'][1] + \
                match_result2['rectangle'][1] + y_axis
    # 移动到
    pyautogui.moveTo(x_refresh, y_refresh, duration=0.5)
    time.sleep(0.5)
    # 点击
    if click_action == 'left':
        pyautogui.click(x_refresh, y_refresh, duration=0.5)
    elif click_action == 'right':
        pyautogui.rightClick(x_refresh, y_refresh, duration=0.5)
    elif click_action == 'double':
        pyautogui.doubleClick(x_refresh, y_refresh, duration=0.5)
    time.sleep(0.5)


def match_and_input(image_path_abs=image_path, image_name='', text='', confidencevalue=0.7):
    """
    匹配图片并点击,且输入
    @param image_path_abs: 图片所在绝对路径
    @param image_name: 图片名字
    @param text: 待输入的文本内容
    @param confidencevalue: 精度
    """
    # 匹配图片并点击
    match_and_click(image_path_abs=image_path_abs,
                    image_name=image_name, confidencevalue=confidencevalue)
    time.sleep(0.5)

    # 输入
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'a')
    if text != '':
        pyautogui.hotkey('ctrl', 'v')
    elif text == '':
        pyautogui.hotkey('backspace')
    time.sleep(0.5)


def match_and_move_to(image_path_abs=image_path, image_name='', confidencevalue=0.7):
    """
    匹配图片并移动鼠标到图片中央
    @param image_path_abs:  图片所在绝对路径
    @param image_name:  图片名字
    @param confidencevalue: 匹配精度
    """
    # 匹配图片坐标
    match_result = wait_for_img(image_path_abs + image_name, confidencevalue)
    assert match_result is not None
    # 移动到
    pyautogui.moveTo(match_result['result'][0], match_result['result'][1], duration=0.5)
    time.sleep(0.5)


def match_and_move_to_with_pixel_offset(image_path_abs=image_path,
                                        image_name='', x_axis=0, y_axis=0, confidencevalue=0.7):
    """
    匹配图片并移动鼠标到图片中央的偏移位
    @param image_path_abs:  图片所在绝对路径
    @param image_name:  图片名字
    @param confidencevalue: 匹配精度
    @param x_axis: x轴偏移值
    @param y_axis: y轴偏移值
    """
    # 匹配图片坐标
    match_result = wait_for_img(image_path_abs + image_name, confidencevalue)
    assert match_result is not None
    # 根据偏移，刷新坐标
    x_refresh = match_result['result'][0] + x_axis
    y_refresh = match_result['result'][1] + y_axis
    # 移动到
    pyautogui.moveTo(x_refresh, y_refresh, duration=0.5)
    time.sleep(0.5)


def input_paster_and_enter(text='hello'):
    """
    输入文本内容，回车
    """
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.hotkey('enter')
    time.sleep(0.5)


def click_center_of_screen_and_send_hotkey(*args):
    """
    点击屏幕中央，并按快捷键
    @param args: 快捷键们
    """
    # 点击图片中央
    screen_width, screen_height = pyautogui.size()
    pyautogui.click(screen_width / 2, screen_height / 2)

    # 按快捷键
    pyautogui.hotkey(args[0], args[1])


def match_and_move_to_then_scroll(image_path_abs=image_path, image_name='', scroll=''):
    """
    匹配图片并移动到，（鼠标滚动）
    @param scroll: 移动数值
    @param image_path_abs:  图片所在绝对路径
    @param image_name:  图片名字
    """
    # 匹配图片坐标
    match_result = wait_for_img(image_path_abs + image_name)
    assert match_result is not None

    # 移动到坐标
    pyautogui.moveTo(match_result['result'][0], match_result['result'][1], duration=0.5)

    # 滚轮滚一滚
    if scroll:
        pyautogui.scroll(scroll)


def move_mouse_to_center_of_screen_and_click(click_action='left'):
    """
    鼠标移动到屏幕中央，并点击
    @param click_action: left/right
    """
    # 鼠标移动到屏幕中央
    move_mouse_to_center_of_screen()

    # 点击
    pyautogui.click(button=click_action)


def one_key_repeat_several_times(key='left', times=2):
    """
    重复同一单一按键多次
    @param key: 按键
    @param times: 次数
    """
    # 循环次数
    for _ in range(times):
        # 输入单个按键
        pyautogui.hotkey(key)


def send_combined_keys(key1='ctrl', key2='a', key3='i', key_num=2):
    """
    输入组合键
    @param key3: 键3
    @param key_num: 发送快捷键的键数
    @param key1: 键1
    @param key2: 键2
    """
    if key_num == 2:
        pyautogui.hotkey(key1, key2)
    elif key_num == 3:
        pyautogui.hotkey(key1, key2, key3)


def move_mouse_to_top_center(duration_move=0.0):
    """
    把鼠标移动到屏幕顶部中央
    @param duration_move: 移动鼠标所需的时间
    """
    # 获取当前屏幕分辨率
    screen_width, screen_height = pyautogui.size()

    # 移动鼠标到屏幕顶部中央
    pyautogui.moveTo(screen_width / 2, screen_height / 100, duration=duration_move)


def compatible_match_and_click(image_path_abs=image_path,
                               image_name1='', image_name2='', click_action='left'):
    """
    兼容的匹配图片并点击
    @param image_name1:
    @param image_name2:
    @param click_action: 左击/右击
    @param image_path_abs:  图片所在绝对路径
    """

    match_result = wait_for_img(image_path_abs + image_name1)
    if match_result is not None:
        if click_action == 'left':
            pyautogui.click(match_result['result'][0], match_result['result'][1], duration=0.5)
        elif click_action == 'right':
            pyautogui.rightClick(match_result['result'][0], match_result['result'][1], duration=0.5)
    else:
        match_result = wait_for_img(image_path_abs + image_name2)
        assert match_result is not None
        if click_action == 'left':
            pyautogui.click(match_result['result'][0], match_result['result'][1], duration=0.5)
        elif click_action == 'right':
            pyautogui.rightClick(match_result['result'][0], match_result['result'][1], duration=0.5)

    time.sleep(0.5)


def repeat_one_function_times(fun, num: int, *arg, **kwargs):
    """
    重复执行一个函数多次
    @param fun: 函数名
    @param num: 次数
    @param arg: 传递给函数的参数, x模式
    @param kwargs: 传递给函数的参数, x=1模式
    """
    for _ in range(num):
        fun(*arg, **kwargs)


def multiple_match_image(*args, con, max_wait_time=15, path=image_path):
    """
    匹配多种可能图片
    @param con: 图片匹配度
    @param max_wait_time: 最大匹配数
    @param path: 图片路径
    @param args: 图片名们
    @return: True/False
    """
    for image_name in args:
        match_result = wait_for_img(path + image_name, con, max_wait_time)
        if match_result is not None:
            return True
    return False


def multiple_match_all_images_path_specified(*args, con, path=image_path):
    """
    匹配所有图片
    @param path: 图片路径
    @param con: 图片匹配度
    @param args: 图片名们
    @return: True/False
    """
    for image_name in args:
        match_result = wait_for_img(path + image_name, confidencevalue=con)
        if match_result is None:
            return False
    return True


def input_one_by_one_paster_and_enter(text='hello', interval_used=0.0):
    """
    一个字符一个字符的输入，而后回车
    @param interval_used: 输入间隔时间
    @param text: 待输入的内容
    """
    pyautogui.typewrite(text, interval=interval_used)
    time.sleep(1)
    pyautogui.hotkey('enter')
    time.sleep(0.5)


def match_and_input_with_pixel_offset(image_path_abs=image_path,
                                      image_name='', text='', x_axis=0, y_axis=0):
    """
    匹配图片并点击偏移坐标后，输入内容
    @param image_path_abs: 图片所在绝对路径
    @param image_name: 图片名字
    @param text: 待输入的文本
    @param x_axis: x轴偏移值
    @param y_axis: y轴偏移值
    """
    # 匹配图片并点击
    match_and_click(image_path_abs, image_name, x_axis=x_axis, y_axis=y_axis)

    # 输入
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'a')
    if text != '':
        pyautogui.hotkey('ctrl', 'v')
    elif text == '':
        pyautogui.hotkey('backspace')
    time.sleep(0.5)


def scroll_match(image_path_abs=image_path, image_name='',
                 scroll=-1, click_action='left', confidencevalue=0.8,
                 x_axis=0, y_axis=0, count=30):
    """
    滚动页面查询图片
    :param image_path_abs: 图片路径
    :param image_name: 图片名
    :param scroll: 每次滚动距离
    :param click_action: 点击操作
    :param confidencevalue: 精度
    :param x_axis: x偏移量
    :param y_axis: y偏移量
    :param count: 最多滚动次数
    """
    num = 0
    while wait_for_img(image_path_abs + image_name, confidencevalue, 3) is None and num < count:
        num += 1
        pyautogui.scroll(scroll)
    match_result = wait_for_img(image_path_abs + image_name, confidencevalue)
    assert match_result is not None
    # 根据偏移，刷新坐标
    x_refresh = match_result['result'][0] + x_axis
    y_refresh = match_result['result'][1] + y_axis
    if click_action == 'left':
        pyautogui.click(x_refresh, y_refresh, duration=0.5)
    elif click_action == 'right':
        pyautogui.rightClick(x_refresh, y_refresh, duration=0.5)
    elif click_action == 'double':
        pyautogui.doubleClick(x_refresh, y_refresh, duration=0.5)
    return match_result


class TouchScreen:
    """
    触摸屏类
    """

    def __init__(self):
        """
        初始化触摸屏类
        """
        self.tool = AutoTool()

    def screen_single_finger_click(self, image_path_abs=image_path, image_name=''):
        """
        通过触摸屏点击图片中央
        @param image_path_abs: 图片所在目录
        @param image_name: 图片名
        """
        # 定位到图片，然后获取图片中心坐标
        match_result = wait_for_img(image_path_abs + image_name)
        assert match_result is not None

        # 触摸屏单指点击图片中心
        x_axis = match_result['result'][0]
        y_axis = match_result['result'][1]
        self.tool.screen_single_finger_click(x_axis, y_axis)

    def tap_and_input(self, image_path_abs=image_path, image_name='', text=''):
        """
        单指触屏点击后，输入内容
        @param image_path_abs:  图片所在目录
        @param image_name:  图片名
        @param text: 输入的文本内容
        """
        # 单指点击图片
        self.screen_single_finger_click(image_path_abs=image_path_abs, image_name=image_name)

        # 输入内容
        pyperclip.copy(text)
        pyautogui.hotkey('ctrl', 'a')
        if text != '':
            pyautogui.hotkey('ctrl', 'v')
        elif text == '':
            pyautogui.hotkey('backspace')
        time.sleep(0.5)

    def screen_single_finger_long_press(self, image_path_abs=image_path, image_name=''):
        """
        通过触摸屏长按图片中央
        @param image_path_abs: 图片所在目录
        @param image_name: 图片名
        """
        # 定位到图片，然后获取图片中心坐标
        match_result = wait_for_img(image_path_abs + image_name)
        assert match_result is not None

        # 触摸屏单指点击图片中心
        x_axis = match_result['result'][0]
        y_axis = match_result['result'][1]
        self.tool.screen_single_finger_long_press(x_axis, y_axis)

    def screen_single_finger_click_with_pixel_offset(
            self, image_path_abs=image_path, image_name='', x_axis=0, y_axis=0):
        """
        通过触摸屏点击<图片中央偏移后的坐标>
        @param image_path_abs: 图片所在目录
        @param image_name: 图片名
        @param x_axis: x轴偏移值
        @param y_axis: y轴偏移值
        """
        # 定位到图片，然后获取图片中心坐标
        match_result = wait_for_img(image_path_abs + image_name)
        assert match_result is not None

        # 触摸屏单指点击图片中心
        x_axis = match_result['result'][0] + x_axis
        y_axis = match_result['result'][1] + y_axis
        self.tool.screen_single_finger_click(x_axis, y_axis)

    def screen_two_finger_big(self, image_path_abs=image_path, image_name=''):
        """
        通过触摸屏双指放大当前网页
        @param image_path_abs: 图片所在目录
        @param image_name: 图片名
        """
        # 定位到图片，然后获取图片中心坐标
        match_result = wait_for_img(image_path_abs + image_name)
        assert match_result is not None

        # 触摸屏单指点击图片中心
        x_axis = match_result['result'][0]
        y_axis = match_result['result'][1]
        self.tool.screen_two_finger_big(x_axis, y_axis)

    def screen_two_finger_small(self, image_path_abs=image_path, image_name=''):
        """
        方法存在问题，暂时不要使用
        通过触摸屏双指缩小当前网页
        @param image_path_abs: 图片所在目录
        @param image_name: 图片名
        """
        # 定位到图片，然后获取图片中心坐标
        match_result = wait_for_img(image_path_abs + image_name)
        assert match_result is not None

        # 触摸屏单指点击图片中心
        x_axis = match_result['result'][0]
        y_axis = match_result['result'][1]
        self.tool.screen_two_finger_small(x_axis, y_axis)

    def screen_single_finger_long_press_with_pixel_offset(
            self, image_path_abs=image_path, image_name='', x_axis=0, y_axis=0):
        """
        通过触摸屏长按<图片中央偏移后的坐标>
        @param image_path_abs: 图片所在目录
        @param image_name: 图片名
        @param x_axis: x轴偏移值
        @param y_axis: y轴偏移值
        """
        # 定位到图片，然后获取图片中心坐标
        match_result = wait_for_img(image_path_abs + image_name)
        assert match_result is not None

        # 触摸屏单指点击图片中心
        x_axis = match_result['result'][0] + x_axis
        y_axis = match_result['result'][1] + y_axis
        self.tool.screen_single_finger_long_press(x_axis, y_axis)

    def screen_single_finger_drag_with_pixel_offset(
            self, image_path_abs=image_path, image_name='', x_axis=0, y_axis=0, x_path=0, y_path=0):
        """
        通过触摸屏拖动<图片中央偏移后的坐标>到目的坐标
        @param image_path_abs: 图片所在目录
        @param image_name: 图片名
        @param x_axis: x轴偏移值
        @param y_axis: y轴偏移值
        @param x_path: 移动到的x坐标
        @param y_path: 移动到的y坐标
        """
        # 定位到图片，然后获取图片中心坐标
        match_result = wait_for_img(image_path_abs + image_name)
        assert match_result is not None

        # 触摸屏单指点击图片中心
        x_axis = match_result['result'][0] + x_axis
        y_axis = match_result['result'][1] + y_axis
        self.tool.screen_single_finger_drag(x_axis, y_axis, x_path, y_path)
