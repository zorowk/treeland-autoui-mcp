# treeland-autotests

treeland auto test base python

[中文文档](README.zh-CN.md)

## Quick start

### 1) Prepare python environment

```bash
chmod +x scripts/setup_build_env.sh
./scripts/setup_build_env.sh
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
# inputAccelProfile must set to 1
dde-dconfig set -a org.deepin.dde.treeland -r org.deepin.dde.treeland.user -s /uos -k inputAccelProfile -v 1
source scripts/setup_run_env.sh
source .venv/bin/activate.sh
python pytest tests/treeland/test_tab_action.py
```

## Directory

- `scripts/setup_build_env.sh`: one-click environment bootstrap tests
- `script/desktop_demo.py`: sample tests that imports `pyautogui`, `pyperclip`, `dogtail`

## Notes

- `dogtail` relies on Linux accessibility stack. If import/runtime fails, install system packages for your distro (e.g. `python3-gi`, `python3-pyatspi`, AT-SPI related packages).
