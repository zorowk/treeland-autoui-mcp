from __future__ import annotations

import base64
import os
import sys
import time
from io import BytesIO
from pathlib import Path
from typing import Any

import requests
from PIL import Image

from mcp.server.fastmcp import FastMCP, Image as MCPImage

from ai_controller.remote_client import RemoteClient


DETAIL_LIST: list[dict[str, Any]] = []
SCREEN_WIDTH = 0
SCREEN_HEIGHT = 0
CURRENT_MOUSE_X = 0
CURRENT_MOUSE_Y = 0


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _b64_from_png(png_bytes: bytes) -> str:
    return base64.b64encode(png_bytes).decode("ascii")


def _load_omniparser():
    root = _repo_root() / "OmniParser"
    sys.path.insert(0, str(root))
    try:
        from util.omniparser import Omniparser  # type: ignore
    finally:
        sys.path.pop(0)
    return Omniparser


def _init_omniparser():
    Omniparser = _load_omniparser()
    som_model_path = os.environ.get("SOM_MODEL_PATH", "./weights/icon_detect/model.pt")
    caption_model_name = os.environ.get("CAPTION_MODEL_NAME", "florence2")
    caption_model_path = os.environ.get("CAPTION_MODEL_PATH", "./weights/icon_caption_florence")
    device = os.environ.get("OMNI_PARSER_DEVICE", "cuda")
    box_threshold = float(os.environ.get("BOX_TRESHOLD", "0.05"))
    return Omniparser(
        som_model_path=som_model_path,
        caption_model_name=caption_model_name,
        caption_model_path=caption_model_path,
        device=device,
        box_threshold=box_threshold,
    )


def _parse_with_server(server_url: str, png_bytes: bytes):
    image_key = os.environ.get("OMNI_PARSER_SERVER_IMAGE_KEY", "image")
    payload: dict[str, Any] = {image_key: _b64_from_png(png_bytes)}
    bbox_format = os.environ.get("OMNI_PARSER_SERVER_BBOX", "").strip()
    if bbox_format:
        payload["output_bbox_format"] = bbox_format
    timeout_s = float(os.environ.get("OMNI_PARSER_SERVER_TIMEOUT", "60"))
    resp = requests.post(server_url, json=payload, timeout=timeout_s)
    resp.raise_for_status()
    payload = resp.json()
    return payload["dino_labeled_img"], payload["detail"]


def _parse_local(omniparser, png_bytes: bytes):
    with Image.open(BytesIO(png_bytes)) as img:
        dino_labeled_img, detail = omniparser.parse(img)
    return dino_labeled_img, detail


def _bbox_center(bbox: list[float], width: int, height: int) -> tuple[int, int]:
    x1, y1, x2, y2 = bbox
    x = int((x1 + x2) * width / 2)
    y = int((y1 + y2) * height / 2)
    return x, y


def _detail_text(detail: list[dict[str, Any]]) -> str:
    lines = []
    for i, item in enumerate(detail):
        label = item.get("label", "")
        bbox = item.get("bbox", "")
        text = item.get("text", "")
        lines.append(f"#{i} {label} {bbox} {text}".strip())
    return "\n".join(lines)


def register_tools(mcp: FastMCP) -> None:
    omniparser = None
    omniparser_server = os.environ.get("OMNI_PARSER_SERVER", "").strip()
    if not omniparser_server:
        omniparser = _init_omniparser()

    remote = RemoteClient()

    @mcp.tool()
    def omniparser_details_on_screen():
        """Capture remote screen, parse UI elements, return detail list and annotated image."""
        global DETAIL_LIST, SCREEN_WIDTH, SCREEN_HEIGHT
        png_bytes, width, height = remote.get_screenshot()
        SCREEN_WIDTH = width
        SCREEN_HEIGHT = height

        if omniparser_server:
            dino_labeled_img, detail = _parse_with_server(omniparser_server, png_bytes)
        else:
            if omniparser is None:
                raise RuntimeError("OmniParser not initialized")
            dino_labeled_img, detail = _parse_local(omniparser, png_bytes)

        DETAIL_LIST = detail
        detail_text = _detail_text(detail)
        return [
            detail_text,
            MCPImage(data=base64.b64decode(dino_labeled_img), format="png"),
        ]

    @mcp.tool()
    def omniparser_click(idx: int, button: str = "left", clicks: int = 1):
        """Click UI element by index from details_on_screen."""
        global CURRENT_MOUSE_X, CURRENT_MOUSE_Y
        if idx < 0 or idx >= len(DETAIL_LIST):
            return "invalid index"
        bbox = DETAIL_LIST[idx]["bbox"]
        x, y = _bbox_center(bbox, SCREEN_WIDTH, SCREEN_HEIGHT)
        remote.click(x, y, button=button, clicks=clicks)
        CURRENT_MOUSE_X, CURRENT_MOUSE_Y = x, y
        return f"clicked #{idx} at ({x},{y})"

    @mcp.tool()
    def omniparser_mouse_move(idx: int):
        """Move mouse to UI element by index."""
        global CURRENT_MOUSE_X, CURRENT_MOUSE_Y
        if idx < 0 or idx >= len(DETAIL_LIST):
            return "invalid index"
        bbox = DETAIL_LIST[idx]["bbox"]
        x, y = _bbox_center(bbox, SCREEN_WIDTH, SCREEN_HEIGHT)
        remote.move(x, y)
        CURRENT_MOUSE_X, CURRENT_MOUSE_Y = x, y
        return f"moved to #{idx} at ({x},{y})"

    @mcp.tool()
    def omniparser_drags(start_idx: int, end_idx: int, button: str = "left", key: str = ""):
        """Drag from one UI element to another."""
        if start_idx < 0 or start_idx >= len(DETAIL_LIST):
            return "invalid start index"
        if end_idx < 0 or end_idx >= len(DETAIL_LIST):
            return "invalid end index"
        start_bbox = DETAIL_LIST[start_idx]["bbox"]
        end_bbox = DETAIL_LIST[end_idx]["bbox"]
        from_x, from_y = _bbox_center(start_bbox, SCREEN_WIDTH, SCREEN_HEIGHT)
        to_x, to_y = _bbox_center(end_bbox, SCREEN_WIDTH, SCREEN_HEIGHT)
        remote.drag(from_x, from_y, to_x, to_y, button=button, key=key)
        return f"dragged #{start_idx} -> #{end_idx}"

    @mcp.tool()
    def omniparser_write(content: str, idx: int = -1, use_clipboard: bool = True):
        """Type text, optionally clicking a UI element first."""
        if idx >= 0:
            result = omniparser_click(idx)
            if isinstance(result, str) and result.startswith("invalid"):
                return result
        remote.type_text(content, use_clipboard=use_clipboard)
        return "typed"

    @mcp.tool()
    def omniparser_input_key(key1: str, key2: str = "", key3: str = ""):
        """Press keyboard keys (up to 3)."""
        keys = [k for k in (key1, key2, key3) if k]
        remote.hotkey(keys)
        return "hotkey sent"

    @mcp.tool()
    def omniparser_scroll(clicks: int, direction: str = "down"):
        """Scroll on remote machine."""
        remote.scroll(abs(clicks), direction=direction)
        return "scrolled"

    @mcp.tool()
    def omniparser_get_keys_list():
        """Get available keyboard keys from remote pyautogui."""
        return remote.get_keys()

    @mcp.tool()
    def omniparser_wait(seconds: float = 1.0):
        """Wait for UI to settle."""
        time.sleep(seconds)
        return f"waited {seconds}s"

    @mcp.tool()
    def omniparser_watch(duration_s: float = 2.0, fps: int = 16, include_images: bool = False, max_frames: int = 32):
        """Periodically refresh screen, parse UI elements, and return summaries for AI error checks."""
        if fps <= 0:
            return "invalid fps"
        if duration_s <= 0:
            return "invalid duration"
        if max_frames <= 0:
            return "invalid max_frames"

        interval = 1.0 / fps
        total_frames = max(1, int(duration_s * fps))
        if total_frames > max_frames:
            total_frames = max_frames
            interval = duration_s / total_frames

        summaries: list[str] = []
        images: list[MCPImage] = []
        for i in range(total_frames):
            start = time.monotonic()
            png_bytes, width, height = remote.get_screenshot()

            if omniparser_server:
                dino_labeled_img, detail = _parse_with_server(omniparser_server, png_bytes)
            else:
                if omniparser is None:
                    return "OmniParser not initialized"
                dino_labeled_img, detail = _parse_local(omniparser, png_bytes)

            summary = _detail_text(detail)
            summaries.append(f"[frame {i + 1}/{total_frames}] {width}x{height}\n{summary}")

            if include_images:
                images.append(MCPImage(data=base64.b64decode(dino_labeled_img), format="png"))

            elapsed = time.monotonic() - start
            sleep_s = interval - elapsed
            if sleep_s > 0:
                time.sleep(sleep_s)

        result: list[Any] = ["\n\n".join(summaries)]
        if include_images:
            result.extend(images)
        else:
            # return last frame image by default for inspection
            last_img = dino_labeled_img if "dino_labeled_img" in locals() else None
            if last_img:
                result.append(MCPImage(data=base64.b64decode(last_img), format="png"))
        return result


def main() -> None:
    mcp = FastMCP("treeland-remote-autogui")
    register_tools(mcp)
    mcp.run()


if __name__ == "__main__":
    main()
