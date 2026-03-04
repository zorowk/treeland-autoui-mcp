#!/usr/bin/env python3
"""
Minimal desktop automation sample that uses:
- pyautogui
- pyperclip
- dogtail
"""

import time

import pyautogui
import pyperclip
from dogtail import tree


def main() -> None:
  print("Starting desktop automation demo...")

  # Example: prepare clipboard text and trigger paste shortcut.
  pyperclip.copy("treeland autotest demo text")
  time.sleep(0.5)
  pyautogui.hotkey("ctrl", "v")

  # Example: query running applications in accessibility tree.
  root = tree.root
  apps = root.applications()
  print(f"Detected applications via dogtail: {len(apps)}")
  for app in apps[:10]:
    print(f"- {app.name}")

  print("Demo finished.")


if __name__ == "__main__":
  main()
