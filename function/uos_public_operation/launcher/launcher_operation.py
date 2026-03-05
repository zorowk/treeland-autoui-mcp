"""
启动器相关操作
"""
# -*- coding:utf-8 -*-
import os
import time
import dbus
from dogtail.tree import root
import pyperclip
import pyautogui
from function.uos_public_operation.config import CONFIG

pyautogui.FAILSAFE = False


class LauncherOpration:
    """
    启动器相关操作
    """

    def __init__(self):
        os.popen('nohup dde-lancher > /dev/null 2>&1 &')
        time.sleep(CONFIG.wait_time_one)
        self.launcher_dogtail = root.application(appName="dde-launcher", description="/usr/bin/dde-launcher")

    def launcher_show(self):
        """
        显示启动器
        :return:None
        """
        session_bus = dbus.SessionBus()
        launcher_poxy = session_bus.get_object('com.deepin.dde.Launcher', '/com/deepin/dde/Launcher')
        launcher = dbus.Interface(launcher_poxy, dbus_interface='com.deepin.dde.Launcher')
        show_method = launcher.get_dbus_method("Show")
        assert show_method is not None
        show_method()

    def launcher_hide(self):
        """
        隐藏启动器
        :return:None
        """
        session_bus = dbus.SessionBus()
        launcher_poxy = session_bus.get_object('com.deepin.dde.Launcher', '/com/deepin/dde/Launcher')
        launcher = dbus.Interface(launcher_poxy, dbus_interface='com.deepin.dde.Launcher')
        hide_method = launcher.get_dbus_method("Hide")
        assert hide_method is not None
        hide_method()

    def launcher_is_visible(self):
        """
        判断启动器是否弹出
        :return:True 弹出or False未弹出
        """
        session_bus = dbus.SessionBus()
        launcher_poxy = session_bus.get_object('com.deepin.dde.Launcher', '/com/deepin/dde/Launcher')
        launcher = dbus.Interface(launcher_poxy, dbus_interface='com.deepin.dde.Launcher')
        is_visible_method = launcher.get_dbus_method("IsVisible")
        assert is_visible_method is not None
        return is_visible_method()

    def launcher_exit(self):
        """
        退出启动器
        :return:None
        """
        session_bus = dbus.SessionBus()
        launcher_poxy = session_bus.get_object('com.deepin.dde.Launcher', '/com/deepin/dde/Launcher')
        launcher = dbus.Interface(launcher_poxy, dbus_interface='com.deepin.dde.Launcher')
        exit_method = launcher.get_dbus_method("Exit")
        assert exit_method is not None
        return exit_method()

    def launcher_uninstall_app(self, app_name):
        """
        卸载应用
        :param app_name: 应用名称例如 deepin-calculator
        :return:None
        """
        session_bus = dbus.SessionBus()
        launcher_poxy = session_bus.get_object('com.deepin.dde.Launcher', '/com/deepin/dde/Launcher')
        launcher = dbus.Interface(launcher_poxy, dbus_interface='com.deepin.dde.Launcher')
        uninstall_app_method = launcher.get_dbus_method("UninstallApp")
        assert uninstall_app_method is not None
        return uninstall_app_method(app_name)

    def is_item_on_desktop(self, app_name):
        """
        判断应用快捷方式是否在桌面
        :param app_name: 应用名称例如 deepin-calculator
        :return: True 在桌面or False不在桌面
        """
        session_bus = dbus.SessionBus()
        launcher_daemon_poxy = session_bus.get_object('com.deepin.dde.daemon.Launcher',
                                                      '/com/deepin/dde/daemon/Launcher')
        launcher = dbus.Interface(launcher_daemon_poxy, dbus_interface='com.deepin.dde.daemon.Launcher')
        is_item_on_desktop_method = launcher.get_dbus_method("IsItemOnDesktop")
        assert is_item_on_desktop_method is not None
        return is_item_on_desktop_method(app_name)

    def request_send_to_desktop(self, app_name):
        """
        发送应用快捷方式到桌面
        :param app_name: 应用名称例如 deepin-calculator
        :return: True 发送桌面成功or False发送失败 如果快捷方式已存在---异常
        """
        if self.is_item_on_desktop(app_name) == 0:
            session_bus = dbus.SessionBus()
            launcher_daemon_poxy = session_bus.get_object('com.deepin.dde.daemon.Launcher',
                                                          '/com/deepin/dde/daemon/Launcher')
            launcher = dbus.Interface(launcher_daemon_poxy, dbus_interface='com.deepin.dde.daemon.Launcher')
            request_send_to_desktop_method = launcher.get_dbus_method("RequestSendToDesktop")
            assert request_send_to_desktop_method is not None
            return request_send_to_desktop_method(app_name)
        return None

    def request_remove_from_desktop(self, app_name):
        """
        移除桌面快捷方式
        :param app_name: 应用名称例如 deepin-calculator
        :return: True 移除桌面成功or False移除失败 如果快捷方式不存在---异常
        """
        session_bus = dbus.SessionBus()
        launcher_daemon_poxy = session_bus.get_object('com.deepin.dde.daemon.Launcher',
                                                      '/com/deepin/dde/daemon/Launcher')
        launcher = dbus.Interface(launcher_daemon_poxy, dbus_interface='com.deepin.dde.daemon.Launcher')
        request_remove_from_desktop_method = launcher.get_dbus_method("RequestRemoveFromDesktop")
        assert request_remove_from_desktop_method is not None
        return request_remove_from_desktop_method(app_name)

    def ui_search_key_word(self, key_word):
        """
        启动器搜索框搜索关键字，前提条件，启动器必须弹出
        :param key_word: 搜索的关键字
        :return:True 搜索成功or搜索失败
        """
        self.launcher_dogtail = root.application(appName="dde-launcher", description="/usr/bin/dde-launcher")
        # 获取搜索框
        search_edit = self.launcher_dogtail.child('Form_windowedsearcheredit', roleName='form')
        if search_edit is None:
            raise Exception("未找到搜索框!")
        if search_edit.position[0] == 0 or search_edit.position[1] == 0:
            raise Exception("获取搜索框坐标出错！")
        # 复制关键字至剪贴板
        pyperclip.copy(key_word)
        pyautogui.click(search_edit.position[0] + 50, search_edit.position[1] + 10, duration=0.5)
        time.sleep(CONFIG.wait_time_one)
        # 粘贴关键字
        pyautogui.hotkey('ctrlleft', 'v')
        time.sleep(CONFIG.wait_time_two)
        return True

    def ui_right_menu_click(self, app_name, button='left'):
        """
        动器打开应用右键菜单
        :param app_name:应用名，如：计算器
        :param button: 鼠标按钮类型
        :return:None
        """
        self.ui_search_key_word(app_name)
        # 获取匹配到的条目句柄
        menu_item = self.launcher_dogtail.child(app_name, roleName='list item')
        if menu_item is None:
            raise Exception("未找到菜单项!")
        if menu_item.position[0] == 0 or menu_item.position[1] == 0:
            raise Exception("获取菜单项坐标出错！")
        #
        pyautogui.click(menu_item.position[0] + 18, menu_item.position[1] + 18, button=button)
        time.sleep(CONFIG.wait_time_one)

    def ui_right_menu_open(self, app_name):
        """
        启动器打开应用右键菜单打开应用
        :param app_name:应用名，如：计算器
        :return:None
        """
        self.ui_right_menu_click(app_name, button='right')
        time.sleep(CONFIG.wait_time_tree)
        pyautogui.press('down')
        time.sleep(CONFIG.wait_time_one)
        pyautogui.press('enter')
        time.sleep(CONFIG.wait_time_one)
        pyautogui.press('esc')

    def ui_right_menu_desktop(self, app_name):
        """
        启动器打开应用右键菜单发送至桌面，或从桌面删除
        :param app_name:应用名，如：计算器
        :return:None
        """
        self.ui_right_menu_click(app_name, button='right')
        time.sleep(CONFIG.wait_time_tree)
        # 选择桌面选项
        for _ in range(0, 2):
            pyautogui.press('down')
            time.sleep(CONFIG.wait_time_one)
        pyautogui.press('enter')
        time.sleep(CONFIG.wait_time_one)
        pyautogui.press('esc')

    def ui_right_menu_dock(self, app_name):
        """
        启动器打开应用右键菜单发送至任务栏，或从任务栏删除
        :param app_name:应用名，如：计算器
        :return:None
        """
        self.ui_right_menu_click(app_name, button='right')
        time.sleep(CONFIG.wait_time_tree)
        # 选择任务栏选项
        for _ in range(0, 3):
            pyautogui.press('down')
            time.sleep(CONFIG.wait_time_one)
        pyautogui.press('enter')
        time.sleep(CONFIG.wait_time_one)
        pyautogui.press('esc')

    def ui_right_menu_uninstall(self, app_name):
        """
        启动器打开应用右键菜单卸载应用。
        :param app_name:应用名，如：计算器
        :return:None
        """
        self.ui_right_menu_click(app_name, button='right')
        time.sleep(CONFIG.wait_time_tree)
        # 选择卸载选项
        # for i in range(0,5):
        pyautogui.press('up')
        time.sleep(CONFIG.wait_time_one)
        # 确定卸载menu
        pyautogui.press('enter')
        time.sleep(CONFIG.wait_time_two)
        self.launcher_dogtail.clearCache()
        time.sleep(CONFIG.wait_time_two)
        # 获取确认卸载按钮
        confirm = self.launcher_dogtail.child('确定', roleName='push button')
        # 兼容不同sniff版本
        if confirm is None:
            confirm = self.launcher_dogtail.child('Form_确定', roleName='form')
        if confirm is None:
            raise Exception("确定按钮找不到！")
        if confirm.position[0] == 0 or confirm.position[1] == 0:
            raise Exception("确定按钮坐标获取失败！")
        time.sleep(CONFIG.wait_time_one)
        pyautogui.click(confirm.position[0] + 50, confirm.position[1] + 18, button='left')
        time.sleep(CONFIG.wait_time_one)
