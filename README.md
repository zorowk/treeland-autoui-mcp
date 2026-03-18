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
# inputAccelProfile must set to 1 (Import !!!)
dde-dconfig set -a org.deepin.dde.treeland -r org.deepin.dde.treeland.user -s /uos -k inputAccelProfile -v 1
source scripts/setup_run_env.sh
source .venv/bin/activate.sh
# example
python pytest tests/treeland/test_tab_action.py
```

## Directory

- `scripts/setup_build_env.sh`: one-click environment bootstrap tests
- `source scripts/setup_run_env.sh` one-click deployment of test runtime environment
- `tests`: test-related scenarios written in uos

## Troubleshooting

**Q:** Why does `pyautogui` crash when moving the cursor?
**A:** This happens when libinput mouse acceleration is not set to `flat`. The default is adaptive (value `2`). For automated tests, set `inputAccelProfile` to `flat` (value `1`). Also ensure Treeland includes [this fix](https://github.com/linuxdeepin/treeland/pull/778/changes/9d04804fe24b9b1cf947f8ab250207cfe0bec9ca).

## Related Library Changes

- [wl-find-cursor](https://github.com/zorowk/wl-find-cursor): [Fix installation error](https://github.com/zorowk/wl-find-cursor/commit/512b9bf9cb7af94059c54d14b3e319ed6c794f9d)
- [pyautogui](https://github.com/zorowk/pyautogui): [Fix keycode mapping errors for alt/altleft/altright](https://github.com/zorowk/pyautogui/commit/bb4319499eeac2c2df68cb750ba614cb6ea5543c), [Add support for win/winleft/winright key mapping](https://github.com/KavyanshKhaitan2/pyautogui/commit/28f3a41df4456eaf23daae6542d27a13d7d325a7)
