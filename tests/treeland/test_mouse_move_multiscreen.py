# !/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
mouse move
"""
import os
import re
import random
import datetime
import pyautogui


def test_mouse_move():
    # 执行 wlr-randr 获取输出信息
    try:
        output = os.popen('wlr-randr').read()
    except Exception as e:
        print(f"无法执行 wlr-randr: {e}")
        return

    screens = []
    current_output = None
    current_position = None
    current_scale = 1.0
    current_resolution = None

    for line in output.splitlines():
        line = line.strip()

        # 检测新的输出开始（以输出名开头，如 HDMI-A-1 或 eDP-1）
        if re.match(r'^[A-Za-z0-9\-]+ "', line):
            current_output = line.split('"')[0].strip()
            continue

        # 解析 Position
        if line.startswith("Position:"):
            try:
                pos_str = line.split(":", 1)[1].strip()
                x, y = map(int, pos_str.split(","))
                current_position = (x, y)
            except:
                current_position = (0, 0)
            continue

        # 解析 Scale
        if line.startswith("Scale:"):
            try:
                current_scale = float(line.split(":", 1)[1].strip())
            except:
                current_scale = 1.0
            continue

        # 检测当前模式行（包含 "current"）
        if "current" in line and re.match(r'^\s*\d+x\d+', line):
            try:
                # 提取 1920x1080 部分
                res_match = re.match(r'^\s*(\d+)x(\d+)', line)
                if res_match:
                    width = int(res_match.group(1))
                    height = int(res_match.group(2))
                    current_resolution = (width, height)
            except:
                pass

        # 当一个输出信息完整时（有位置 + 分辨率），添加到列表
        if current_position is not None and current_resolution is not None:
            w, h = current_resolution
            x, y = current_position

            # 逻辑屏幕尺寸（考虑缩放）
            # pyautogui 使用逻辑坐标（缩放后坐标系）
            logical_w = int(w * current_scale)
            logical_h = int(h * current_scale)

            screens.append([logical_w, logical_h, x, y])

            # 重置，准备下一个输出
            current_resolution = None
            # 注意：不重置 position 和 scale，因为下一个输出会覆盖

    if not screens:
        print("未检测到任何启用的屏幕")
        return

    print(f"检测到 {len(screens)} 个屏幕: {screens}")

    starttime = datetime.datetime.now()
    endtime = datetime.datetime.now()

    while (endtime - starttime).seconds <= 1:
        # 随机选一个屏幕
        n = random.randint(0, len(screens) - 1)
        w, h, x, y = screens[n]

        # 在逻辑坐标系中随机位置（pyautogui 用逻辑坐标）
        # 底部留 80 像素（逻辑像素）
        x1 = random.randint(x, x + w - 1)
        y1 = random.randint(y, y + h - 80 - 1)

        pyautogui.moveTo(x1, y1, duration=0.1)
        pyautogui.click()

        endtime = datetime.datetime.now()

# 测试运行
if __name__ == "__main__":
    test_mouse_move()
