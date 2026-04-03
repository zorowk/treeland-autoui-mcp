from __future__ import annotations

import subprocess
import time


def run(command: str, timeout_s: int = 10) -> tuple[str, str, int, int]:
    start = time.monotonic()
    try:
        completed = subprocess.run(
            ["bash", "-lc", command],
            text=True,
            capture_output=True,
            timeout=timeout_s,
        )
        duration_ms = int((time.monotonic() - start) * 1000)
        return completed.stdout, completed.stderr, completed.returncode, duration_ms
    except subprocess.TimeoutExpired as e:
        duration_ms = int((time.monotonic() - start) * 1000)
        stdout = e.stdout or ""
        stderr = e.stderr or ""
        return stdout, f"{stderr}\n[timeout after {timeout_s}s]".strip(), 124, duration_ms
