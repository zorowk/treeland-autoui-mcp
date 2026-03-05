"""
images图片获取
"""
import os
import time

import pyautogui
from PIL import Image

from function.match_img import match_img

MAX_WAIT_TIME = 15
IMAGE_FOLDER = "images/"
IMAGE_FOLDER_WPS = "wps"
IMAGE_FOLDER_PINGAN = "pingan"
IMAGE_FOLDER_MAIL = "mail"
IMAGE_FOLDER_BROWSER = "browser"
IMAGE_FOLDER_KWIN = "kwin"
IMAGE_FOLDER_WIN_TUBE = "win_tube"
IMAGE_FOLDER_SCREENSHOT_RECORDING = "screenshot_recording"
IMAGE_FOLDER_SPLITVIEW = "splitview"

def get_image_path():
    """
    获取5.3.15-1目录
    """
    image_folder = os.path.dirname(os.path.abspath(__file__)) + '/../' + IMAGE_FOLDER + \
                   IMAGE_FOLDER_WPS + "/"
    return image_folder


def get_image_path2(*sub_folder_name):
    """
    获取images目录下的目录
    """
    image_path = os.path.dirname(os.path.abspath(__file__)) + '/../' + IMAGE_FOLDER
    if sub_folder_name:
        for sub_folder in sub_folder_name:
            image_path = image_path + sub_folder + "/"
    else:
        image_path = get_image_path()
    return image_path


def wait_for_img(template_image, confidencevalue=0.8, max_wait_time=MAX_WAIT_TIME):
    """
    循环对比图片
    :param template_image: 模板图片
    :param confidencevalue: 识别精度
    :param max_wait_time: 匹配时长
    :return: 匹配到的结果或noneadd
    """
    # global max_wait_time
    start = time.time()
    while True:
        time.sleep(1)
        end = time.time()
        if end - start <= max_wait_time:
            image = pyautogui.screenshot()
            match_result = match_img(image, template_image, confidencevalue)
            if match_result is not None:
                return match_result
        else:
            break


def get_any_path(folder_name):
    """
    获取browser目录下的目录
    """
    any_path = os.path.dirname(os.path.abspath(__file__)) + '/../' + folder_name + '/'
    return any_path


def find_and_click_img(img, x_axis=0, y_axis=0):
    """
    查找图片
    """
    match_result = wait_for_img(img)
    assert match_result is not None
    pyautogui.click(match_result['result'][0] + x_axis,
                    match_result['result'][1] + y_axis, duration=0.5)
    time.sleep(0.5)


def find_and_right_click_img(img, x_axis=0, y_axis=0):
    """
    查找图片并鼠标右键点击
    """
    match_result = wait_for_img(img)
    assert match_result is not None
    pyautogui.rightClick(match_result['result'][0] + x_axis,
                         match_result['result'][1] + y_axis, duration=0.5)
    time.sleep(0.5)


def find_and_middle_click_img(img, x_axis=0, y_axis=0):
    """
    查找图片并鼠标中键点击
    """
    match_result = wait_for_img(img)
    assert match_result is not None
    pyautogui.middleClick(match_result['result'][0] + x_axis,
                          match_result['result'][1] + y_axis, duration=0.5)
    time.sleep(0.5)


def moveto_img(img, x_axis=0, y_axis=0, confidencevalue=0.8):
    """
    移动到图片
    """
    match_result = wait_for_img(img, confidencevalue)
    assert match_result is not None
    pyautogui.moveTo(match_result['result'][0] + x_axis,
                     match_result['result'][1] + y_axis, duration=0.5)


def check_compare_result(img):
    """
    检查比对结果
    """
    match_result = wait_for_img(img)
    assert match_result is not None


def drag_img(img, x_axis=0, y_axis=0):
    """
    拖动图片
    """
    match_result = wait_for_img(img)
    assert match_result is not None
    pyautogui.moveTo(match_result['result'][0], match_result['result'][1], duration=1)
    pyautogui.dragTo(match_result['result'][0] + x_axis,
                     match_result['result'][1] + y_axis, duration=1)
    time.sleep(0.5)


# def extract_string_in_specific_area(locator_image_path,
#                                     locator_image_name, x_offset, y_offset, width, height):
#     """
#     识别指定区域的英文
#     @param locator_image_path: 锚点图片路径
#     @param locator_image_name: 锚点图片名
#     @param x_offset: 锚点x偏移位->偏移到识别区域左上角
#     @param y_offset: 锚点y偏移位>偏移到识别区域左上角
#     @param width:   区域宽度
#     @param height:  区域高度
#     @return: 识别到的英文字符
#     """
#     # 获取锚点坐标
#     match_result = wait_for_img(locator_image_path + locator_image_name)
#     assert match_result is not None
#     x_axis, y_axis = match_result['result'][0], match_result['result'][1]
#     # 计算出提取区域左上角坐标
#     x_axis = x_axis + x_offset
#     y_axis = y_axis + y_offset
#     # 截取图片
#     image = pyautogui.screenshot()
#     image.save('~/Pictures/screen.png')
#     img = Image.open("~/Pictures/screen.png")
#     cropped = img.crop((x_axis, y_axis, x_axis + width, y_axis + height))
#     cropped.save("~/Pictures/specific.png")
#     # 提取英文字符
#     text = pytesseract.image_to_string(Image.open('~/Pictures/specific.png'))
#     # os.popen('echo "' + text + '" > /home/uos/Pictures/test1.txt')
#     os.popen('rm ~/Pictures/screen.png')
#     os.popen('rm ~/Pictures/specific.png')
#     return text


def wait_for_img2(image, template_image, confidencevalue=0.8, max_wait_time=MAX_WAIT_TIME):
    """
    循环对比图片
    :param image: 大图片
    :param template_image: 小图片
    :param max_wait_time: 匹配时长
    :param confidencevalue: 识别精度
    :return: 匹配到的结果或noneadd
    """
    # global max_wait_time
    start = time.time()
    while True:
        time.sleep(1)
        end = time.time()
        if end - start <= max_wait_time:
            # image = pyautogui.screenshot()
            match_result = match_img(image, template_image, confidencevalue)
            if match_result is not None:
                return match_result
        else:
            break


def second_match(parent_image_name, image_name, oper='click'):
    """
    二级匹配并操作
    """
    # 一级匹配
    match_result = wait_for_img(parent_image_name)
    assert match_result is not None
    # 二级匹配
    image = Image.open(parent_image_name)
    match_result2 = wait_for_img2(image, image_name)
    assert match_result2 is not None

    if oper == 'click':
        pyautogui.click(match_result2['rectangle'][2] / 2 +
                        match_result['rectangle'][0] +
                        match_result2['rectangle'][0],
                        match_result2['rectangle'][3] / 2 +
                        match_result['rectangle'][1] +
                        match_result2['rectangle'][1],
                        duration=0.3)
    elif oper == 'move':
        pyautogui.moveTo(match_result2['rectangle'][2] / 2 +
                         match_result['rectangle'][0] +
                         match_result2['rectangle'][0],
                         match_result2['rectangle'][3] / 2 +
                         match_result['rectangle'][1] +
                         match_result2['rectangle'][1],
                         duration=0.3)
    elif oper == 'rightclick':
        pyautogui.rightClick(
            match_result2['rectangle'][2] / 2 + match_result['rectangle'][0]
            + match_result2['rectangle'][0],
            match_result2['rectangle'][3] / 2 + match_result['rectangle'][1]
            + match_result2['rectangle'][1],
            duration=0.3)
