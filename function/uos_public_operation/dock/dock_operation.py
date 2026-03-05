# """
# dock栏相关的所有操作
# """
# # -*- coding:utf-8 -*-
#
# import os
# import time
# import dbus
# from dogtail.tree import root
# import pyautogui
# from lib.uos_public_operation.config import CONFIG
#
# pyautogui.FAILSAFE = False
#
#
# class DockOperation:
#     """
#     任务栏相关操作
#     """
#
#     def __init__(self):
#         os.popen('nohup dde-dock > /dev/null 2>&1 &')
#         time.sleep(CONFIG.wait_time_tree)
#         self.dock_dogtail = root.application(appName="dde-dock", description="/usr/bin/dde-dock")
#
#     def is_docked(self, desktop_file_path):
#         """
#         判断应用是否驻留任务栏
#         :param desktop_file_path: 系统应用快捷方式文件路径 如：/usr/share/applications/deepin-calculator.desktop
#         :return: True 驻留任务栏or False 未驻留任务栏
#         """
#         command = 'dbus-send --session --print-reply --dest=com.deepin.dde.daemon.Dock /com/deepin/dde/daemon/Dock ' \
#                   'com.deepin.dde.daemon.Dock.IsDocked string:"' + desktop_file_path + '"'
#         content = os.popen(command).read().strip().split(' ')
#         if content:
#             return content[-1]
#         return None
#
#     def is_on_dock(self, desktop_file_path):
#         """
#         判断应用图标是否出现在任务栏，例如应用未驻留任务栏，但是启动后就会显示在任务栏。
#         :param desktop_file_path: 系统应用快捷方式文件路径 如：/usr/share/applications/deepin-calculator.desktop
#         :return: True 在任务栏出现or False 未出现在任务栏
#         """
#         command = 'dbus-send --session --print-reply --dest=com.deepin.dde.daemon.Dock /com/deepin/dde/daemon/Dock ' \
#                   'com.deepin.dde.daemon.Dock.IsOnDock string:"' + desktop_file_path + '"'
#         content = os.popen(command).read().strip().split(' ')
#         if content:
#             return content[-1]
#         return None
#
#     def request_dock(self, desktop_file_path, index):
#         """
#         驻留图标至任务栏指定坐标
#         :param desktop_file_path: 系统应用快捷方式文件路径 如：/usr/share/applications/deepin-calculator.desktop
#         :param index: 任务栏图标位置，0代表在多任务视图按钮之后
#         :return:True 驻留任务栏or False 未驻留任务栏
#         """
#         command = 'dbus-send --session --print-reply --dest=com.deepin.dde.daemon.Dock /com/deepin/dde/daemon/Dock ' \
#                   'com.deepin.dde.daemon.Dock.RequestDock string:"' + desktop_file_path + '" int32:' + str(index)
#         content = os.popen(command).read().strip().split(' ')
#         if content:
#             return content[-1]
#         return None
#
#     def request_undock(self, desktop_file_path):
#         """
#          移除应用驻留任务栏
#         :param desktop_file_path: 系统应用快捷方式文件路径 如：/usr/share/applications/deepin-calculator.desktop
#         :return: True 移除驻留任务栏成功or False 移除驻留任务栏失败
#         """
#         command = 'dbus-send --session --print-reply --dest=com.deepin.dde.daemon.Dock /com/deepin/dde/daemon/Dock ' \
#                   'com.deepin.dde.daemon.Dock.RequestUndock string:"' + desktop_file_path + '"'
#         content = os.popen(command).read().strip().split(' ')
#         if content:
#             return content[-1]
#         return None
#
#     def get_window_id(self, window_name):
#         """
#         获取窗口的ID
#         :param window_name: 窗口的名称
#         :return: 窗口ID list int类型
#         """
#         window_id = os.popen('xdotool search ' + window_name).read().rstrip('\n').split('\n')
#         window_id = [int(x) for x in window_id]
#         if len(window_id) > 1:
#             window_id.sort(reverse=False)
#         return window_id
#
#     def close_window(self, window_id):
#         """
#         关闭窗口
#         :param window_id: 窗口ID 可调用GetWindowID获取
#         :return: None
#         """
#         session_bus = dbus.SessionBus()
#         dock_poxy = session_bus.get_object('com.deepin.dde.daemon.Dock', '/com/deepin/dde/daemon/Dock')
#         daemon_dock = dbus.Interface(dock_poxy, dbus_interface='com.deepin.dde.daemon.Dock')
#         close_window_method = daemon_dock.get_dbus_method("CloseWindow")
#         assert close_window_method is not None
#         return close_window_method(window_id)
#
#     def activate_window(self, window_id):
#         """
#         激活当前窗口，相当于点击dock预览窗口，打开被点击的预览窗口
#         :param window_id:窗口ID 可调用GetWindowID获取
#         :return:None
#         """
#         session_bus = dbus.SessionBus()
#         dock_poxy = session_bus.get_object('com.deepin.dde.daemon.Dock', '/com/deepin/dde/daemon/Dock')
#         daemon_dock = dbus.Interface(dock_poxy, dbus_interface='com.deepin.dde.daemon.Dock')
#         activate_window_method = daemon_dock.get_dbus_method("ActivateWindow")
#         assert activate_window_method is not None
#         return activate_window_method(window_id)
#
#     def make_window_above(self, window_id):
#         """
#         使给定id的窗口处于桌面最上层位置，首先会调用ActivateWindow激活窗口再设置处于桌面最上层显示
#         :param window_id:窗口ID 可调用GetWindowID获取
#         :return:None
#         """
#         session_bus = dbus.SessionBus()
#         dock_poxy = session_bus.get_object('com.deepin.dde.daemon.Dock', '/com/deepin/dde/daemon/Dock')
#         daemon_dock = dbus.Interface(dock_poxy, dbus_interface='com.deepin.dde.daemon.Dock')
#         make_window_above_method = daemon_dock.get_dbus_method("MakeWindowAbove")
#         assert make_window_above_method is not None
#         return make_window_above_method(window_id)
#
#     def maximize_window(self, window_id):
#         """
#         最大化给定id的窗口实例，首先会调用ActivateWindow激活窗口再使之最大化
#         :param window_id: 窗口ID 可调用GetWindowID获取
#         :return: None
#         """
#         session_bus = dbus.SessionBus()
#         dock_poxy = session_bus.get_object('com.deepin.dde.daemon.Dock', '/com/deepin/dde/daemon/Dock')
#         daemon_dock = dbus.Interface(dock_poxy, dbus_interface='com.deepin.dde.daemon.Dock')
#         maximize_window_method = daemon_dock.get_dbus_method("MaximizeWindow")
#         assert maximize_window_method is not None
#         return maximize_window_method(window_id)
#
#     def minimize_window(self, window_id):
#         """
#         最小化给定id的窗口实例
#         :param window_id: 窗口ID 可调用GetWindowID获取
#         :return:None
#         """
#         session_bus = dbus.SessionBus()
#         dock_poxy = session_bus.get_object('com.deepin.dde.daemon.Dock', '/com/deepin/dde/daemon/Dock')
#         daemon_dock = dbus.Interface(dock_poxy, dbus_interface='com.deepin.dde.daemon.Dock')
#         minimize_window_method = daemon_dock.get_dbus_method("MinimizeWindow")
#         assert minimize_window_method is not None
#         return minimize_window_method(window_id)
#
#     def ui_click_dock_icon(self, icon_name, button='left'):
#         """
#         点击任务栏图标
#         :param icon_name: accessName 如：Btn_计算器
#         :param button: string left 左键点击，right右键点击 ，middle 滚轮点击
#         :return: True 点击成功，False 点击失败
#         """
#         self.dock_dogtail.clearCache()
#         icon_button = self.dock_dogtail.child(icon_name, roleName='push button')
#         if icon_button is None:
#             raise Exception("未找到图标!")
#         if icon_button.name != 'Btn_launcheritem' and (icon_button.position[0] == 0 or icon_button.position[1] == 0):
#             raise Exception("获取图标坐标出错！")
#         pyautogui.click(icon_button.position[0] + 18, icon_button.position[1] + 18, button=button)
#         time.sleep(CONFIG.wait_time_one)
#         return True
#
#     def ui_dock_right_menu(self, icon_name, started=False):
#         """
#         移除任务栏图标，或驻留任务栏
#         :param icon_name: accessName 如：Btn_计算器
#         :param started:程序是否已启动，True 已启动
#         :return: None
#         """
#         self.ui_click_dock_icon(icon_name, button='right')
#         if not started:
#             time.sleep(CONFIG.wait_time_tree)
#             pyautogui.press('up')
#             time.sleep(CONFIG.wait_time_one)
#             pyautogui.press('enter')
#         else:
#             for _ in range(0, 3):
#                 time.sleep(CONFIG.wait_time_tree)
#                 pyautogui.press('up')
#             time.sleep(CONFIG.wait_time_one)
#             pyautogui.press('enter')
#             time.sleep(CONFIG.wait_time_one)
#
#     def ui_dock_right_menu_custom(self, icon_name, index=1):
#         """
#         点击任务栏图标右键菜单某项
#         :param icon_name: accessName 如：Btn_计算器
#         :param index: 点击菜单项 从下往上第几个 从1开始。
#         :return:
#         """
#         self.ui_click_dock_icon(icon_name, button='right')
#         for _ in range(0, index):
#             time.sleep(CONFIG.wait_time_tree)
#             pyautogui.press('up')
#             time.sleep(CONFIG.wait_time_one)
#             pyautogui.press('enter')
#             time.sleep(CONFIG.wait_time_one)
#
#     def resume_dock_size(self):
#         """
#         恢复dock栏尺寸为（0,1040,1920,40)
#         :return:
#         """
#         command = 'dbus-send --session --print-reply --dest=com.deepin.dde.daemon.Dock /com/deepin/dde/daemon/Dock ' \
#                   'org.freedesktop.DBus.Properties.Set string:"com.deepin.dde.daemon.Dock" ' \
#                   'string:"WindowSizeEfficient" variant:uint32:40 '
#         os.system(command)
