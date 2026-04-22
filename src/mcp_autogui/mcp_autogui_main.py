#coding: utf-8

import os
import sys
import threading
import io
import asyncio
from contextlib import redirect_stdout
import base64
import json
import subprocess
import pyautogui
import pyperclip
from mcp.server.fastmcp import Image
import PIL
import requests

INPUT_IMAGE_SIZE = 960

def mcp_autogui_main(mcp):
    omniparser_thread = None
    result_image = None
    detail = None
    is_finished = False

    current_mouse_x, current_mouse_y = pyautogui.position()

    if 'OMNI_PARSER_SERVER' not in os.environ:
        raise RuntimeError('OMNI_PARSER_SERVER environment variable is required.')

    @mcp.tool()
    async def omniparser_details_on_screen() -> list:
        """Get the screen and analyze its details.
        If a timeout occurs, you can continue by running it again.

    Return value:
        - Details such as the content of text.
        - Screen capture with ID number added.
        """
        nonlocal omniparser_thread, result_image, detail, is_finished

        detail_text = ''
        with redirect_stdout(sys.stderr):
            def omniparser_thread_func():
                nonlocal result_image, detail, is_finished, detail_text
                with redirect_stdout(sys.stderr):
                    screenshot_image = pyautogui.screenshot()

                    buffered = io.BytesIO()
                    screenshot_image.save(buffered, format='png')
                    send_img = base64.b64encode(buffered.getvalue()).decode('ascii')
                    json_data = json.dumps({'base64_image': send_img})
                    response = requests.post(
                        f"http://{os.environ['OMNI_PARSER_SERVER']}/parse/",
                        data=json_data,
                        headers={"Content-Type": "application/json"}
                    )
                    response_json = response.json()
                    dino_labled_img = response_json['som_image_base64']
                    detail = response_json['parsed_content_list']

                    image_bytes = base64.b64decode(dino_labled_img)
                    result_image_local = PIL.Image.open(io.BytesIO(image_bytes))

                    width, height = result_image_local.size
                    if width > height:
                        result_image_local = result_image_local.resize((INPUT_IMAGE_SIZE, INPUT_IMAGE_SIZE * height // width))
                    else:
                        result_image_local = result_image_local.resize((INPUT_IMAGE_SIZE * width // height, INPUT_IMAGE_SIZE))

                    result_image = io.BytesIO()
                    result_image_local.save(result_image, format='png')

                    detail_text = ''
                    for loop, content in enumerate(detail):
                        detail_text += f'ID: {loop}, {content["type"]}: {content["content"]}\n'

                    is_finished = True
            if omniparser_thread is None:
                result_image = None
                detail = None
                is_finished = False
                omniparser_thread = threading.Thread(target=omniparser_thread_func)
                omniparser_thread.start()

            while not is_finished:
                await asyncio.sleep(0.1)

            omniparser_thread = None

            # Save result image to /tmp only when debug mode is enabled
            if os.environ.get('OMNIPARSER_MCP_DEBUG') == '1':
                with open('/tmp/omniparser_mark.png', 'wb') as f:
                    f.write(result_image.getvalue())

            return [detail_text, Image(data=result_image.getvalue(), format="png")]

    @mcp.tool()
    async def omniparser_click(id: int, button: str = 'left', clicks: int = 1) -> bool:
        """Click on anything on the screen.

    Args:
        id: The element on the screen that it click. You can check it with "omniparser_details_on_screen".
        button: Button to click. 'left', 'middle', or 'right'.
        clicks: Number of clicks. 2 for double click.
    Return value:
        True is success. False is means "this is not found".
        """
        nonlocal current_mouse_x, current_mouse_y
        screen_width, screen_height = pyautogui.size()
        if len(detail) > id:
            compos = detail[id]['bbox']
            current_mouse_x = int((compos[0] + compos[2]) * screen_width) // 2
            current_mouse_y = int((compos[1] + compos[3]) * screen_height) // 2
            pyautogui.click(x=current_mouse_x, y=current_mouse_y, button=button, clicks=clicks)
            return True
        return False

    @mcp.tool()
    async def omniparser_drags(from_id: int, to_id: int, button: str = 'left', key: str = '') -> bool:
        """Drag and drop on the screen.

    Args:
        from_id: The element on the screen that it start to drag. You can check it with "omniparser_details_on_screen".
        to_id: The element on the screen that it end to drag. You can check it with "omniparser_details_on_screen".
        button: Button to click. 'left', 'middle', or 'right'.
        key: The name of the keyboard key if you hold down it while dragging. You can check key's name with "omniparser_get_keys_list".
    Return value:
        True is success. False is means "this is not found".
        """
        nonlocal current_mouse_x, current_mouse_y
        screen_width, screen_height = pyautogui.size()

        from_x = -1
        to_x = -1
        if len(detail) <= from_id or len(detail) <= to_id:
            return False
        compos = detail[from_id]['bbox']
        from_x = int((compos[0] + compos[2]) * screen_width) // 2
        from_y = int((compos[1] + compos[3]) * screen_height) // 2
        compos = detail[to_id]['bbox']
        to_x = int((compos[0] + compos[2]) * screen_width) // 2
        to_y = int((compos[1] + compos[3]) * screen_height) // 2

        if key is not None and key != '':
            pyautogui.keyDown(key)
        pyautogui.moveTo(from_x, from_y)
        pyautogui.dragTo(to_x, to_y, button=button)
        if key is not None and key != '':
            pyautogui.keyUp(key)
        current_mouse_x = to_x
        current_mouse_y = to_y
        return True

    @mcp.tool()
    async def omniparser_mouse_move(id: int) -> bool:
        """Moves the mouse cursor over the specified element.

    Args:
        id: The element on the screen that it move. You can check it with "omniparser_details_on_screen".
    Return value:
        True is success. False is means "this is not found".
        """
        nonlocal current_mouse_x, current_mouse_y
        screen_width, screen_height = pyautogui.size()
        if len(detail) <= id:
            return False
        compos = detail[id]['bbox']
        current_mouse_x = int((compos[0] + compos[2]) * screen_width) // 2
        current_mouse_y = int((compos[1] + compos[3]) * screen_height) // 2
        pyautogui.moveTo(current_mouse_x, current_mouse_y)
        return True

    @mcp.tool()
    async def omniparser_scroll(clicks: int) -> None:
        """The mouse scrolling wheel behavior.

    CRITICAL: Before scrolling, ensure the target window is focused.
        It is highly recommended to click the window title bar or the target area first.
    Args:
        clicks: Amount of scrolling. 1000 is scroll up 1000 "clicks" and -1000 is scroll down 1000 "clicks".
        """
        pyautogui.moveTo(current_mouse_x, current_mouse_y)
        pyautogui.scroll(clicks)

    @mcp.tool()
    async def omniparser_write(content: str, id: int = -1) -> None:
        """Type the characters in the string that is passed.

    IMPORTANT: A window must be active to receive text input.
        If 'id' is provided, this tool will click the element to focus it.
        If 'id' is -1, you MUST ensure the target window/input box is already focused
        (e.g., by clicking it in a previous step).

    Args:
        content: What to enter.
        id: Click on the target before typing. You can check it with "omniparser_details_on_screen".
        """
        if id >= 0:
            await omniparser_click(id)
        else:
            pyautogui.moveTo(current_mouse_x, current_mouse_y)
        if content.isascii():
            pyautogui.write(content)
        else:
            prev_clip = pyperclip.paste()
            pyperclip.copy(content)
            pyautogui.hotkey('ctrl', 'v')
            if prev_clip:
                pyperclip.copy(prev_clip)

    @mcp.tool()
    async def omniparser_get_keys_list() -> list[str]:
        """List of keyboard keys. Used in "omniparser_input_key" etc.

    Return value:
        List of keyboard keys.
        """
        return pyautogui.KEYBOARD_KEYS

    @mcp.tool()
    async def omniparser_input_key(key1: str, key2: str = '', key3: str = '') -> None:
        """Press of keyboard keys.

    CRITICAL: Shortcuts (like 'ctrl'+'c') only work if the target window is active.
        Ensure you have clicked the target window to focus it before calling this.

    Args:
        key1-3: Press of keyboard keys. You can check key's name with "omniparser_get_keys_list". If you specify multiple, keys will be pressed down in order, and then released in reverse order.
        """
        pyautogui.moveTo(current_mouse_x, current_mouse_y)
        if key2 is not None and key2 != '' and key3 is not None and key3 != '':
            pyautogui.hotkey(key1, key2, key3)
        elif key2 is not None and key2 != '':
            pyautogui.hotkey(key1, key2)
        else:
            pyautogui.hotkey(key1)

    @mcp.tool()
    async def omniparser_wait(time: float = 1.0) -> None:
        """Waits for the specified number of seconds.

    Args:
        time: Waiting time (seconds).
        """
        await asyncio.sleep(time)

    @mcp.tool()
    async def omniparser_exec_command(command: str, timeout: int = 30) -> dict:
        """Execute shell command on local machine.

    Args:
        command: Shell command to execute.
        timeout: Execution timeout in seconds.
    Return value:
        dict with stdout, stderr, return_code.
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                "stdout": "",
                "stderr": f"Command timed out after {timeout} seconds",
                "return_code": -1
            }
        except Exception as e:
            return {
                "stdout": "",
                "stderr": str(e),
                "return_code": -1
            }

    @mcp.tool()
    async def omniparser_get_screenshot_base64() -> str:
        """Get the last captured screenshot as base64 string.

    Return value:
        Base64 encoded PNG image string with ID labels.
        """
        nonlocal result_image
        if result_image is None:
            # 如果还没有截图，先执行一次
            await omniparser_details_on_screen()

        result_image.seek(0)
        return base64.b64encode(result_image.getvalue()).decode('ascii')
