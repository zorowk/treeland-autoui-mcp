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
# inputAccelProfile 必须设置为 1
dde-dconfig set -a org.deepin.dde.treeland -r org.deepin.dde.treeland.user -s /uos -k inputAccelProfile -v 1
source scripts/setup_run_env.sh
source .venv/bin/activate.sh
python pytest tests/treeland/test_tab_action.py
```

## 目录

- `scripts/setup_build_env.sh`：一键引导测试环境
- `script/desktop_demo.py`：示例测试，导入 `pyautogui`、`pyperclip`、`dogtail`

## 备注

- `dogtail` 依赖 Linux 辅助功能栈。如果导入或运行失败，请为你的发行版安装系统包（例如 `python3-gi`、`python3-pyatspi`、AT-SPI 相关包）。
