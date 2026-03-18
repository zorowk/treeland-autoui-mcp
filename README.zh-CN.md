# treeland-autotests

treeland 自动化测试基础（Python）

## 快速开始

### 1) 准备 Python 环境

```bash
chmod +x scripts/setup_build_env.sh
./scripts/setup_build_env.sh
```

该脚本将：
- 在 `.venv` 创建 Python 虚拟环境
- 克隆：
  - `https://github.com/zorowk/pyautogui.git`
  - `https://github.com/zorowk/pyperclip.git`
  到 `/tmp` 下的系统临时目录
- 将克隆的两个仓库安装到虚拟环境中
- 在虚拟环境中安装 `dogtail`
- 检查 `pyatspi` 是否可用，若缺失则打印系统包提示

### 2) 运行自动化测试

```bash
# inputAccelProfile 必须设置为 1（重要！！！）
dde-dconfig set -a org.deepin.dde.treeland -r org.deepin.dde.treeland.user -s /uos -k inputAccelProfile -v 1
source scripts/setup_run_env.sh
source .venv/bin/activate.sh
# 示例
python pytest tests/treeland/test_tab_action.py
```

## 目录

- `scripts/setup_build_env.sh`：一键引导测试环境
- `source scripts/setup_run_env.sh` 一键部署测试运行环境
- `tests`：uos 相关的测试场景

## 故障排查

**问：** 为什么 `pyautogui` 移动坐标时会崩溃？
**答：** 因为 libinput 的鼠标加速没有设置为 `flat`。默认是自适应模式（值为 `2`）。自动化测试需要将 `inputAccelProfile` 设置为 `flat`（值为 `1`）。同时确保 Treeland 合入了 [这个修复](https://github.com/linuxdeepin/treeland/pull/778/changes/9d04804fe24b9b1cf947f8ab250207cfe0bec9ca)。

## 相关库修改

- [wl-find-cursor](https://github.com/zorowk/wl-find-cursor)：[修复安装报错](https://github.com/zorowk/wl-find-cursor/commit/512b9bf9cb7af94059c54d14b3e319ed6c794f9d)
- [pyautogui](https://github.com/zorowk/pyautogui)：[修复 alt/altleft/altright 键 code 映射错误](https://github.com/zorowk/pyautogui/commit/bb4319499eeac2c2df68cb750ba614cb6ea5543c)，[新增对 win/winleft/winright 键映射的支持](https://github.com/KavyanshKhaitan2/pyautogui/commit/28f3a41df4456eaf23daae6542d27a13d7d325a7)

## 待修改
  [autotool](https://github.com/zorowk/treeland-autotests/tree/main/function/uos_public_operation/autotool) 需要替换为更通用的ydotool 已经支持触摸屏
