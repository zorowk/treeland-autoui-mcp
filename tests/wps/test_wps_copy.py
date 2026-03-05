import os
import subprocess
import time

import pyautogui


def openExcel():
    # 打开wps表格
    subprocess.Popen('/bin/bash /opt/apps/cn.wps.wps-office-pro/files/bin/et', shell=True,
                     stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE, encoding='utf-8')
    time.sleep(1)


def openWord():
    # 打开wps文字
    subprocess.Popen('/bin/bash /opt/apps/cn.wps.wps-office-pro/files/bin/wps', shell=True,
                     stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE, encoding='utf-8')
    time.sleep(1)


def openPPT():
    # 打开wps演示
    subprocess.Popen('/bin/bash /opt/apps/cn.wps.wps-office-pro/files/bin/wpp', shell=True,
                     stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE, encoding='utf-8')


# wps之间复制文字
def Word():
    openWord()
    pyautogui.click(960, 540)
    time.sleep(1.5)
    pyautogui.press('right')
    pyautogui.press('enter')
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(4)
    pyautogui.hotkey('ctrl', 'n')
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(4)
    os.system('pkill wps')


# excel之间复制文字
def Excel():
    openExcel()
    pyautogui.click(960, 540)
    time.sleep(1.5)
    pyautogui.press('right')
    pyautogui.press('enter')
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(4)
    pyautogui.hotkey('ctrl', 'n')
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(4)
    os.system('pkill et')


# ppt之间复制文字
def PPT():
    openPPT()
    pyautogui.click(960, 540)
    time.sleep(1.5)
    pyautogui.hotkey('right')
    pyautogui.hotkey('enter')
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(4)
    pyautogui.hotkey('ctrl', 'n')
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(4)
    os.system('pkill wpp')


# excel复制到word
def excel_word():
    openExcel()
    pyautogui.click(960, 540)
    time.sleep(1.5)
    pyautogui.press('right')
    pyautogui.press('enter')
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(4)
    openWord()
    time.sleep(1.5)
    pyautogui.hotkey('ctrl', 'n')
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(4)
    os.system('pkill et')
    os.system('pkill wps')


# excel复制到ppt
def excel_ppt():
    openExcel()
    pyautogui.click(960, 540)
    time.sleep(1.5)
    pyautogui.press('right')
    pyautogui.press('enter')
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(4)
    openPPT()
    time.sleep(1.5)
    pyautogui.hotkey('ctrl', 'n')
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(4)
    os.system('pkill et')
    os.system('pkill wpp')


# excel复制到word
def word_ppt():
    openWord()
    pyautogui.click(960, 540)
    time.sleep(1.5)
    pyautogui.press('right')
    pyautogui.press('enter')
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(4)
    openPPT()
    time.sleep(1.5)
    pyautogui.hotkey('ctrl', 'n')
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(4)
    os.system('pkill et')
    os.system('pkill wpp')


excel_word()
excel_ppt()
word_ppt()
Word()
Excel()
PPT()
