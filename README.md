# treeland-autotests

treeland auto test base python

## Quick start

### 1) Prepare environment

```bash
chmod +x scripts/setup_env.sh
./scripts/setup_env.sh
```

This will:
- create python virtual environment at `.venv`
- clone:
  - `https://github.com/zorowk/pyautogui.git`
  - `https://github.com/zorowk/pyperclip.git`
  to a system temp directory under `/tmp`
- install both cloned repos into the venv
- install `dogtail` into the venv
- check whether `pyatspi` is available and print system package hint if missing

### 2) Run automation tests

```bash
source .venv/bin/activate
python tests/desktop_demo.py
```

## Directory

- `scripts/setup_env.sh`: one-click environment bootstrap tests
- `script/desktop_demo.py`: sample tests that imports `pyautogui`, `pyperclip`, `dogtail`

## Notes

- `dogtail` relies on Linux accessibility stack. If import/runtime fails, install system packages for your distro (e.g. `python3-gi`, `python3-pyatspi`, AT-SPI related packages).
