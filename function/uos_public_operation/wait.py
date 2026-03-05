"""
等待元素
"""
# -*- coding:utf-8 -*-
import os
import time
from function.match_img import match_img
import pyautogui

pyautogui.FAILSAFE = False
MAX_WAIT_TIME = 30



def implicitly_wait(second):
    """
    设置默认等待时间
    :param second: 秒数
    :return:
    """
    global MAX_WAIT_TIME
    MAX_WAIT_TIME = second



def wait_for_child(app_object, name, role_name):
    """
    循环child查找节点
    :param app_object: 父节点对象
    :param name: 要等待节点名称
    :param role_name: 要等待节点角色名
    :return: 查找到的节点或none
    """
    global MAX_WAIT_TIME
    start = time.time()
    while True:
        time.sleep(1)
        end = time.time()
        max_wait = end - start
        print(max_wait)
        if max_wait <= MAX_WAIT_TIME:
            node = app_object.child(name, role_name)
            if node is not None:
                return node
            continue
        else:
            return None



def wait_for_children(app_object, children_list=None):
    """
    循环children查找节点
    :param app_object: 父节点对象
    :param children_list: children下标列表
    :return: 查找到的节点或none
    """
    global MAX_WAIT_TIME
    if children_list is None:
        children_list = []
    start = time.time()
    while True:
        time.sleep(1)
        end = time.time()
        max_wait = end - start
        count_child = len(children_list)
        children_node = app_object
        if max_wait <= MAX_WAIT_TIME:
            for i in range(0, count_child):
                if children_node is None:
                    continue
                children_node = children_node.children[children_list[i]]
            if children_node is not None:
                return children_node
            continue
        else:
            return None



def wait_for_img(template_image, confidencevalue=0.7):
    """
    循环对比图片
    :param template_image: 模板图片
    :param confidencevalue: 识别精度
    :return: 匹配到的结果或none
    """
    global MAX_WAIT_TIME
    start = time.time()
    while True:
        time.sleep(1)
        end = time.time()
        if end - start <= MAX_WAIT_TIME:
            image = pyautogui.screenshot()
            match_result = match_img(image, template_image, confidencevalue)
            if match_result is None:
                continue
            else:
                return match_result
        else:
            break


def img_click(template_image, confidencevalue=0.7, buttonclik='left', mun=0, num2=0):
    """
    图片点击事件
    template_image：模板图片
    confidencevalue: 识别精度
    buttonclik：点击方式
    mun:左移动或者右移动数值
    num2：上移或者下移动数值
    """
    match_result = wait_for_img(template_image, confidencevalue)
    assert match_result is not None
    pyautogui.click(match_result['result'][0] + mun, match_result['result'][1] + num2, button=buttonclik,
                    duration=0.5)


def setting_hot_rolling_boolean():
    """
    判断触控板选项中的自然滚动=是否开启
    result：true or false
    """
    command = 'dbus-send --session --dest=com.deepin.daemon.InputDevices --print-reply ' \
              '/com/deepin/daemon/InputDevice/TouchPad org.freedesktop.DBus.Properties.Get ' \
              'string:com.deepin.daemon.InputDevice.TouchPad string:NaturalScroll '
    result = os.popen(command).read().strip().split(' ')
    return result


def setting_hot_rolling(boolean):
    """
    打开设置触控板选项中的自然滚动
    boolean: true/false
    """
    command = 'dbus-send --session --dest=com.deepin.daemon.InputDevices --print-reply ' \
              '/com/deepin/daemon/InputDevice/TouchPad org.freedesktop.DBus.Properties.Set ' \
              'string:com.deepin.daemon.InputDevice.TouchPad string:NaturalScroll boolean:' + boolean
    os.system(command)


def setting_fontsize(size):
    """
    size:设置字体大小
    """
    command = 'dbus-send --session --dest=com.deepin.daemon.Appearance --print-reply  /com/deepin/daemon/Appearance ' \
              'com.deepin.daemon.Appearance.Set string:"FontSize" string:' + size
    os.system(command)


def getting_fontsize():
    """
    获取字体大小
    """
    command = 'dbus-send --session --dest=com.deepin.daemon.Appearance --print-reply  /com/deepin/daemon/Appearance ' \
              'org.freedesktop.DBus.Properties.Get  string:com.deepin.daemon.Appearance  string:FontSize '
    result = os.popen(command).read().strip().split(' ')
    return result[len(result) - 1]


def getting_voice_note():
    """
    h获取语音听写开关是否开启
    """
    command = 'qdbus com.iflytek.aiassistant /aiassistant/iat com.iflytek.aiassistant.iat.getIatEnable'
    result = os.popen(command).read().strip()
    return result


def setting_voice_note(num):
    """
    设置语音听写开关打开
     num: 0  或  1
     0 ：关闭
     1：开启
    """
    command = 'qdbus com.iflytek.aiassistant /aiassistant/iat com.iflytek.aiassistant.iat.setIatEnable  ' + num
    os.popen(command)


def setting_text_trans(num):
    """
    文本翻译设置开关打开
    num: 0  或  1
    0 ：关闭
    1：开启
    """
    command = 'qdbus  com.iflytek.aiassistant /aiassistant/trans com.iflytek.aiassistant.trans.setTransEnable ' + num
    os.system(command)


def get_test_trans():
    """
    获取文本开关状态
    """
    command = 'qdbus  com.iflytek.aiassistant     /aiassistant/trans    com.iflytek.aiassistant.trans.getTransEnable'
    result = os.popen(command).read().strip()
    return result


def get_voice_note():
    """
    语音朗读开关状态获取
    """
    command = 'qdbus  com.iflytek.aiassistant      /aiassistant/tts       com.iflytek.aiassistant.tts.getTTSEnable'
    result = os.popen(command).read().strip()
    return result


def set_voice_note(num):
    """
     语音朗读开关
     num: 0  或  1
     0 ：关闭
     1：开启
     """
    command = 'qdbus  com.iflytek.aiassistant     /aiassistant/tts    com.iflytek.aiassistant.tts.setTTSEnable   ' + num
    os.popen(command)


def set_adivo_notes(num):
    """
        修改音量大小的接口
        num；为double类型传参为0.35该类型

    """
    pid = os.popen(
        'dbus-send --session --dest=com.deepin.daemon.Audio  --print-reply  /com/deepin/daemon/Audio  '
        'org.freedesktop.DBus.Properties.Get string:"com.deepin.daemon.Audio"  string:"DefaultSink"')
    string2 = pid.read().strip().replace(' ', '')
    name = string2.split("\"")

    command = 'dbus-send --session --dest=com.deepin.daemon.Audio  --print-reply  ' + str(
        name[1]) + '  com.deepin.daemon.Audio.Sink.SetVolume double:' + num + ' boolean:true'
    os.popen(command)


def set_font(font):
    """
    修改字体中的标准字体
    font:为需要修改的字体名称

    """
    command = 'dbus-send --session --print-reply --dest=com.deepin.daemon.Appearance /com/deepin/daemon/Appearance ' \
              'com.deepin.daemon.Appearance.Set string:StandardFont string:' + font
    os.system(command)


def set_shortcuts(name, action, keystroke):
    """
    设置快捷键
    name:K快捷键的名称
    action：快捷键的命令
    keystroke：设置的快捷键如 “<Control>Q”

    """
    command = "dbus-send --session --print-reply --dest=com.deepin.daemon.Keybinding  /com/deepin/daemon/Keybinding " \
              "com.deepin.daemon.Keybinding.AddCustomShortcut  string:" + name + "   string:" + action + "   string:"\
              + keystroke
    os.system(command)


def del_shortcuts(action):
    """
    删除自定义的快捷键
    action:这表示设置快捷键的命令
    """
    command = 'dbus-send --session --print-reply --dest=com.deepin.daemon.Keybinding  /com/deepin/daemon/Keybinding ' \
              'com.deepin.daemon.Keybinding.DeleteCustomShortcut   string:' + action
    os.system(command)


class AutoTool:
    """
    该类主要封装触摸板与触摸屏相关操作
    """

    def __init__(self):
        # 获取cpu架构
        self.arch = os.popen('uname -m').read().strip()
        # 获取模拟工具命令位置
        self.autotool = os.path.abspath(self.get_command_path())


    def get_command_path(self):
        """
        该函数主要通过运行平台cpu架构返回对应多点触控设备模拟命令位置
        :return: 多点触控设备模拟工具命令位置
        """
        try:
            os.environ['LD_LIBRARY_PATH']
        except KeyError:
            os.environ['LD_LIBRARY_PATH'] = ''
        bin_path = ""
        if "x86_64" in self.arch:
            if os.path.dirname(os.path.abspath(__file__)) + "/autotool/autotool_amd/" not in os.environ['LD_LIBRARY_PATH']:
                os.environ['LD_LIBRARY_PATH'] = os.path.dirname(
                    os.path.abspath(__file__)) + "/autotool/autotool_amd/:" + os.environ['LD_LIBRARY_PATH']
            bin_path = os.path.dirname(os.path.abspath(__file__)) + "/autotool/autotool_amd/autotool"
        elif "aarch64" in self.arch:
            if os.path.dirname(os.path.abspath(__file__)) + "/autotool/autotool_arm/" not in os.environ['LD_LIBRARY_PATH']:
                os.environ['LD_LIBRARY_PATH'] = os.path.dirname(
                    os.path.abspath(__file__)) + "/autotool/autotool_arm/:" + os.environ['LD_LIBRARY_PATH']
            bin_path = os.path.dirname(os.path.abspath(__file__)) + "/autotool/autotool_arm/autotool"
        elif "mips64" in self.arch:
            if os.path.dirname(os.path.abspath(__file__)) + "/autotool/autotool_mips/" not in os.environ['LD_LIBRARY_PATH']:
                os.environ['LD_LIBRARY_PATH'] = os.path.dirname(
                    os.path.abspath(__file__)) + "/autotool/autotool_mips/:" + os.environ['LD_LIBRARY_PATH']
            bin_path = os.path.dirname(os.path.abspath(__file__)) + "/autotool/autotool_mips/autotool"
        elif "loongarch64" in self.arch:
            if os.path.dirname(os.path.abspath(__file__)) + "/autotool/autotool_loongarch/" not in os.environ['LD_LIBRARY_PATH']:
                os.environ['LD_LIBRARY_PATH'] = os.path.dirname(
                    os.path.abspath(__file__)) + "/autotool/autotool_loongarch/:" + os.environ['LD_LIBRARY_PATH']
            bin_path = os.path.dirname(os.path.abspath(__file__)) + "/autotool/autotool_loongarch/autotool"
        elif "sw_64" in self.arch:
            if os.path.dirname(os.path.abspath(__file__)) + "/autotool/autotool_sw/" not in os.environ['LD_LIBRARY_PATH']:
                os.environ['LD_LIBRARY_PATH'] = os.path.dirname(
                    os.path.abspath(__file__)) + "/autotool/autotool_sw/:" + os.environ['LD_LIBRARY_PATH']
            bin_path = os.path.dirname(os.path.abspath(__file__)) + "/autotool/autotool_sw/autotool"
        return bin_path


    def combine_coordinate_string(self, pos_x=0, pos_y=0, movex=0, movey=0):
        """
        将坐标以逗号分割组成字符串
        :param pos_x: x坐标
        :param pos_y: y坐标
        :param movex: 移动后x坐标
        :param movey: 移动后y坐标
        :return:
        """
        return str(pos_x) + "," + str(pos_y) + "," + str(movex) + "," + str(movey)


    def pad_single_finger_click(self):
        """
        触摸板单指点击
        :return: null
        """
        command = "sudo " + self.autotool + " -p -c single_finger_click"
        os.system(command)
        time.sleep(0.5)


    def pad_two_finger_click(self):
        """
        触摸板二指点击
        :return: null
        """
        command = "sudo " + self.autotool + " -p -c two_finger_click"
        os.system(command)
        time.sleep(0.5)


    def pad_two_finger_up(self):
        """
        触摸板二指上滑
        :return: null
        """
        command = "sudo " + self.autotool + " -p -c two_finger_up"
        os.system(command)
        time.sleep(0.5)


    def pad_two_finger_down(self):
        """
        触摸板二指下滑
        :return: null
        """
        command = "sudo " + self.autotool + " -p -c two_finger_down"
        os.system(command)
        time.sleep(0.5)


    def pad_two_finger_left(self):
        """
        触摸板二指左滑
        :return: null
        """
        command = "sudo " + self.autotool + " -p -c two_finger_left"
        os.system(command)
        time.sleep(0.5)


    def pad_two_finger_right(self):
        """
        触摸板二指右滑
        :return: null
        """
        command = "sudo " + self.autotool + " -p -c two_finger_right"
        os.system(command)
        time.sleep(0.5)


    def pad_two_finger_big(self):
        """
        触摸板二指放大
        :return: null
        """
        command = "sudo " + self.autotool + " -p -c two_finger_big"
        os.system(command)
        time.sleep(0.5)


    def pad_two_finger_small(self):
        """
        触摸板二指缩小
        :return: null
        """
        command = "sudo " + self.autotool + " -p -c two_finger_small"
        os.system(command)
        time.sleep(0.5)


    def pad_three_finger_down(self):
        """
        触摸板三指下滑
        :return: null
        """
        command = "sudo " + self.autotool + " -p -c three_finger_down"
        os.system(command)
        time.sleep(0.5)


    def pad_three_finger_up(self):
        """
        触摸板三指上滑
        :return: null
        """
        command = "sudo " + self.autotool + " -p -c three_finger_up"
        os.system(command)
        time.sleep(0.5)


    def pad_three_finger_left(self):
        """
        触摸板三指左滑
        :return: null
        """
        command = "sudo " + self.autotool + " -p -c three_finger_left"
        os.system(command)
        time.sleep(0.5)


    def pad_three_finger_right(self):
        """
        触摸板三指右滑
        :return: null
        """
        command = "sudo " + self.autotool + " -p -c three_finger_right"
        os.system(command)
        time.sleep(0.5)


    def screen_single_finger_click(self, pos_x, pos_y):
        """
        触摸屏单指点击
        :param pos_x: x坐标
        :param pos_y: y坐标
        :return: null
        """
        command = "sudo " + self.autotool + " -s -c single_finger_click -w " + self.combine_coordinate_string(pos_x, pos_y)
        os.system(command)
        time.sleep(0.5)


    def screen_single_finger_long_press(self, pos_x, pos_y):
        """
        触摸屏单指长按
        :param pos_x: x坐标
        :param pos_y: y坐标
        :return: null
        """
        command = "sudo " + self.autotool + " -s -c single_finger_long_press -w " + self.combine_coordinate_string(pos_x, pos_y)
        os.system(command)
        time.sleep(0.5)


    def screen_single_finger_down_long(self, pos_x, pos_y):
        """
        触摸屏单指长按1分钟
        :param pos_x: x坐标
        :param pos_y: y坐标
        :return: null
        """
        command = "sudo " + self.autotool + " -s -c single_finger_down_long -w " + self.combine_coordinate_string(
            pos_x, pos_y)
        os.system(command)
        time.sleep(0.5)


    def screen_single_finger_drag(self, pos_x, pos_y, movex, movey):
        """
        触摸屏拖拽
        :param pos_x: x坐标
        :param pos_y: y坐标
        :param movex: 拖拽x坐标
        :param movey: 拖拽y坐标
        :return:
        """
        command = "sudo " + self.autotool + " -s -c single_finger_drag -w " + self.combine_coordinate_string(pos_x, pos_y,
                                                                                                             movex,
                                                                                                             movey)
        os.system(command)
        time.sleep(0.5)


    def screen_single_finger_double_click(self, pos_x, pos_y):
        """
        触摸屏单指双击
        :param pos_x: x坐标
        :param pos_y: y坐标
        :return: null
        """
        command = "sudo " + self.autotool + " -s -c single_finger_double_click -w " + self.combine_coordinate_string(pos_x,
                                                                                                                     pos_y)
        os.system(command)
        time.sleep(0.5)


    def screen_single_finger_up(self, pos_x, pos_y):
        """
        触摸屏单指上滑
        :param pos_x: x坐标
        :param pos_y: y坐标
        :return: null
        """
        command = "sudo " + self.autotool + " -s -c single_finger_up -w " + self.combine_coordinate_string(pos_x,
                                                                                                           pos_y)
        os.system(command)
        time.sleep(0.5)


    def screen_single_finger_down(self, pos_x, pos_y):
        """
        触摸屏单指下滑
        :param pos_x: x坐标
        :param pos_y: y坐标
        :return: null
        """
        command = "sudo " + self.autotool + " -s -c single_finger_down -w " + self.combine_coordinate_string(pos_x,
                                                                                                             pos_y)
        os.system(command)
        time.sleep(0.5)


    def screen_single_finger_left(self, pos_x, pos_y):
        """
        触摸屏单指左滑
        :param pos_x: x坐标
        :param pos_y: y坐标
        :return: null
        """
        command = "sudo " + self.autotool + " -s -c single_finger_left -w " + self.combine_coordinate_string(pos_x,
                                                                                                             pos_y)
        print("-*30" + command)
        os.system(command)
        time.sleep(0.5)


    def screen_single_finger_right(self, pos_x, pos_y):
        """
        触摸屏单指右滑
        :param pos_x: x坐标
        :param pos_y: y坐标
        :return: null
        """
        command = "sudo " + self.autotool + " -s -c single_finger_right -w " + self.combine_coordinate_string(pos_x,
                                                                                                              pos_y)
        os.system(command)
        time.sleep(0.5)


    def screen_two_finger_big(self, pos_x, pos_y):
        """
        触摸屏双指放大
        :param pos_x: x坐标
        :param pos_y: y坐标
        :return: null
        """
        command = "sudo " + self.autotool + " -s -c two_finger_big -w " + self.combine_coordinate_string(pos_x,
                                                                                                         pos_y)
        os.system(command)
        time.sleep(0.5)


    def screen_two_finger_small(self, pos_x, pos_y):
        """
        触摸屏双指缩小
        :param pos_x: x坐标
        :param pos_y: y坐标
        :return: null
        """
        command = "sudo " + self.autotool + " -s -c two_finger_small -w " + self.combine_coordinate_string(pos_x,
                                                                                                           pos_y)
        os.system(command)
        time.sleep(0.5)


    def screen_two_finger_rotate(self, pos_x, pos_y):
        """
        触摸屏二指顺时针旋转
        :param pos_x: x坐标
        :param pos_y: y坐标
        :return: null
        """
        command = "sudo " + self.autotool + " -s -c two_finger_rotate -w " + self.combine_coordinate_string(pos_x,
                                                                                                            pos_y)
        os.system(command)
        time.sleep(0.5)


    def screen_two_finger_rotate1(self, pos_x, pos_y):
        """
        触摸屏二指逆时针旋转
        :param pos_x: x坐标
        :param pos_y: y坐标
        :return: null
        """
        command = "sudo " + self.autotool + " -s -c two_finger_rotate1 -w " + self.combine_coordinate_string(pos_x,
                                                                                                             pos_y)
        os.system(command)
        time.sleep(0.5)


    def screen_three_finger_rotate(self, pos_x, pos_y):
        """
        触摸屏三指顺时针旋转
        :param pos_x: x坐标
        :param pos_y: y坐标
        :return: null
        """
        command = "sudo " + self.autotool + " -s -c three_finger_rotate -w " + self.combine_coordinate_string(pos_x,
                                                                                                              pos_y)
        os.system(command)
        time.sleep(0.5)


    def screen_three_finger_rotate1(self, pos_x, pos_y):
        """
        触摸屏三指逆时针旋转
        :param pos_x: x坐标
        :param pos_y: y坐标
        :return: null
        """
        command = "sudo " + self.autotool + " -s -c three_finger_rotate1 -w " + self.combine_coordinate_string(pos_x,
                                                                                                               pos_y)
        os.system(command)
        time.sleep(0.5)


    def screen_four_finger_rotate(self, pos_x, pos_y):
        """
        触摸屏四指顺时针旋转
        :param pos_x: x坐标
        :param pos_y: y坐标
        :return: null
        """
        command = "sudo " + self.autotool + " -s -c four_finger_rotate -w " + self.combine_coordinate_string(pos_x,
                                                                                                             pos_y)
        os.system(command)
        time.sleep(0.5)


    def screen_four_finger_rotate1(self, pos_x, pos_y):
        """
        触摸屏四指逆时针旋转
        :param pos_x: x坐标
        :param pos_y: y坐标
        :return: null
        """
        command = "sudo " + self.autotool + " -s -c four_finger_rotate1 -w " + self.combine_coordinate_string(pos_x,
                                                                                                              pos_y)
        os.system(command)
        time.sleep(0.5)


    def screen_five_finger_rotate(self, pos_x, pos_y):
        """
        触摸屏五指顺时针旋转
        :param pos_x: x坐标
        :param pos_y: y坐标
        :return: null
        """
        command = "sudo " + self.autotool + " -s -c five_finger_rotate -w " + self.combine_coordinate_string(pos_x,
                                                                                                             pos_y)
        os.system(command)
        time.sleep(0.5)


    def screen_five_finger_rotate1(self, pos_x, pos_y):
        """
        触摸屏五指逆时针旋转
        :param pos_x: x坐标
        :param pos_y: y坐标
        :return: null
        """
        command = "sudo " + self.autotool + " -s -c five_finger_rotate1 -w " + self.combine_coordinate_string(pos_x,
                                                                                                              pos_y)
        os.system(command)
        time.sleep(0.5)


    def screen_two_finger_up(self, pos_x, pos_y):
        """
        触摸屏二指上滑
        :param pos_x: x坐标
        :param pos_y: y坐标
        :return: null
        """
        command = "sudo " + self.autotool + " -s -c two_finger_up -w " + self.combine_coordinate_string(pos_x,
                                                                                                        pos_y)
        os.system(command)
        time.sleep(0.5)


    def screen_two_finger_down(self, pos_x, pos_y):
        """
        触摸屏二指下滑
        :param pos_x: x坐标
        :param pos_y: y坐标
        :return: null
        """
        command = "sudo " + self.autotool + " -s -c two_finger_down -w " + self.combine_coordinate_string(pos_x,
                                                                                                          pos_y)
        os.system(command)
        time.sleep(0.5)
