"""
启动程序，退出程序函数
"""
import os
import time


class AppOperation:
    """
    启动程序，退出程序函数
    """
    def __init__(self, app_name):
        self.app_name = app_name

    # 退出指定程序

    def exit_program(self):
        """
        退出程序
        :return: None
        """
        os.system('killall ' + self.app_name)
        os.system(
            "dbus-send --session --print-reply --dest=com.deepin.deepinid /com/deepin/deepinid "
            "com.deepin.deepinid.Logout")
        time.sleep(0.1)


    def start_program(self):
        """
        驱动程序
        :return: None
        """
        time.sleep(0.1)
        pid = os.popen('pidof  ' + self.app_name)
        if pid.read().strip() != "":
            self.exit_program()

        os.popen(self.app_name)
        time.sleep(0.2)


    def set_light_theme(self):
        """
        设置系统主题为浅色
        :return: None
        """
        os.system('gsettings set com.deepin.dtk:/dtk/deepin/' + self.app_name + '/  palette-type "LightType"')
        time.sleep(0.1)
