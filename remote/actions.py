from __future__ import annotations

import time

import pyautogui
import pyperclip


def click(x: int, y: int, button: str = "left", clicks: int = 1) -> None:
    pyautogui.click(x=x, y=y, clicks=clicks, button=button)


def drag(from_x: int, from_y: int, to_x: int, to_y: int, button: str = "left", key: str = "") -> None:
    pyautogui.moveTo(from_x, from_y)
    if key:
        pyautogui.keyDown(key)
    pyautogui.dragTo(to_x, to_y, button=button)
    if key:
        pyautogui.keyUp(key)


def move(x: int, y: int) -> None:
    pyautogui.moveTo(x, y)


def type_text(text: str, use_clipboard: bool = True) -> None:
    if use_clipboard:
        pyperclip.copy(text)
        pyautogui.hotkey("ctrl", "v")
    else:
        pyautogui.write(text, interval=0.0)
    time.sleep(0.1)


def hotkey(keys: list[str]) -> None:
    if not keys:
        return
    pyautogui.hotkey(*keys)

def keyboard_keys() -> list[str]:
    return list(pyautogui.KEYBOARD_KEYS)


def scroll(clicks: int, direction: str = "down") -> None:
    direction = direction.lower()
    if direction in ("up", "down"):
        pyautogui.scroll(clicks if direction == "up" else -clicks)
        return
    if direction in ("left", "right"):
        pyautogui.hscroll(clicks if direction == "right" else -clicks)
        return
    raise ValueError(f"unknown scroll direction: {direction}")
