# !/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
mouse move
"""
import os
import random
from time import sleep
import pyautogui


def printscreen():
    x = random.randint(900, 1800)
    y = random.randint(600, 1200)
    pyautogui.hotkey('ctrl', 'alt', 'a')
    sleep(1)
    pyautogui.click()
    pyautogui.dragTo(x, y, duration=1)
    pyautogui.hotkey('enter')


def mailscroll():
    pyautogui.click(380, 1400, duration=1)
    pyautogui.click(650, 700, duration=0.5)
    x = random.randint(0, 300)
    y = random.randint(-300, 0)
    y1 = random.randint(300, 1200)
    # pyautogui.scroll(x)
    pyautogui.moveTo(650, y1, duration=0.5)
    pyautogui.click()
    sleep(0.5)
    # pyautogui.scroll(y)
    pyautogui.moveTo(650, y1, duration=0.5)
    pyautogui.click()
    pyautogui.moveTo(1500, 650, duration=0.5)
    pyautogui.click()
    pyautogui.dragTo(1500, 0, duration=1)
    sleep(0.5)
    pyautogui.hotkey('ctrl', 'c')
    sleep(0.5)


def sendmsg():
    pyautogui.click(440, 1400, duration=1)
    x1 = random.randint(1400, 2000)
    y1 = random.randint(1210, 1250)
    x2 = random.randint(500, 800)
    y2 = random.randint(200, 1200)
    pyautogui.moveTo(x1, y1, duration=0.5)
    pyautogui.click()
    pyautogui.hotkey('ctrl', 'v')
    sleep(0.5)
    pyautogui.hotkey('enter')
    pyautogui.typewrite('asfsadfsadfsadfasfda')
    pyautogui.hotkey('space')
    sleep(0.5)
    pyautogui.hotkey('enter')
    sleep(0.5)
    pyautogui.click(500, 1400, duration=1)
    pyautogui.moveTo(x2, y2, duration=0.5)
    # pyautogui.click()
    sleep(0.5)
    pyautogui.dragTo(x1, y1, duration=1)
    sleep(0.5)


def browsertest():
    # pyautogui.click(550, 1400, duration=1)
    # x1 = random.randint(70, 120)
    # y1 = random.randint(350, 370)
    # pyautogui.moveTo(x1, y1, duration=0.1)
    # pyautogui.click()
    # x2 = random.randint(70, 170)
    # y2 = random.randint(420, 430)
    # pyautogui.moveTo(x2, y2, duration=0.1)
    # pyautogui.click()
    pyautogui.press('space', presses=3, interval=0.5)
    sleep(0.5)


def test_pingan():
    mailscroll()
    sendmsg()
    browsertest()
