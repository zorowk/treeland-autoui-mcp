from __future__ import annotations

import io
import subprocess

from PIL import Image


def take_screenshot() -> tuple[bytes, int, int]:
    proc = subprocess.run(
        ["grim", "-t", "png", "-"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    png_bytes = proc.stdout
    with Image.open(io.BytesIO(png_bytes)) as img:
        width, height = img.size
    return png_bytes, width, height
