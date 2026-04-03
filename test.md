# Treeland AI Tests - Deployment and Interface Test Guide

This document describes how to deploy on:
- **Machine B** (target test machine)
- **Machine A** (AI control machine)

And provides test methods for each interface.

## 1) Machine B (Target Test Machine)

### 1.1 Environment setup

Use your existing environment script:

```bash
source client_env.sh
```

Install Python deps:

```bash
python -m pip install -r requirements_client.txt
```

Ensure Wayland screenshot tool is available:

```bash
grim --version
```

### 1.2 Start gRPC server

```bash
export TREELAND_RPC_TOKEN="your-strong-token"
export TREELAND_RPC_HOST="0.0.0.0"
export TREELAND_RPC_PORT="50051"
python -m remote.server
```

## 2) Machine A (AI Control Machine)

### 2.1 Environment setup

```bash
python -m pip install -r requirements_ai.txt
```

### 2.2 Start MCP tools

```bash
export TREELAND_RPC_ADDR="B_IP:50051"
export TREELAND_RPC_TOKEN="your-strong-token"
export OMNI_PARSER_SERVER="http://OMNIPARSER_IP:8000"
python -m ai_controller.mcp_remote_autogui
```

## 3) Interface Tests

All tests are executed from **Machine A** unless otherwise noted.

### 3.1 gRPC connectivity test (screenshot)

```bash
export TREELAND_RPC_ADDR="B_IP:50051"
export TREELAND_RPC_TOKEN="your-strong-token"
python -m remote.client screenshot ./screen.png
```

Expected:
- `screen.png` is saved
- output prints resolution

### 3.2 MCP: screenshot + parse

In your MCP/agent environment, call:

```python
treeland_screenshot()
omniparser_parse_last(output_level="both")
```

Expected:
- Returns labeled UI elements text
- Returns labeled image

### 3.3 MCP: mouse click / double-click

```python
treeland_click(0, clicks=1)
treeland_click(0, clicks=2)
```

Expected:
- Single or double click on element index `0`

### 3.4 MCP: mouse move + drag

```python
treeland_mouse_move(0)
treeland_drags(0, 1)
```

Expected:
- Cursor moves to element `0`
- Drag from element `0` to `1`

### 3.5 MCP: keyboard hotkeys

```python
treeland_input_key("ctrl", "l")
treeland_input_key("ctrl", "shift", "t")
```

Expected:
- Browser focus URL bar / reopen last tab (depends on active app)

### 3.6 MCP: text input

```python
treeland_write("hello world")
```

Expected:
- Text typed at current focus

### 3.7 MCP: scroll

```python
treeland_scroll(5, direction="down")
```

Expected:
- Page scrolls down

### 3.8 MCP: remote command execution (Machine B)

```python
treeland_exec("uname -a", timeout_s=5, output_level="all")
treeland_exec("sleep 2; echo ok", timeout_s=1, output_level="all")
```

Expected:
- First returns stdout/stderr/exit_code/duration_ms
- Second returns timeout with exit_code `124`

## 4) Troubleshooting

- If screenshots fail: ensure `grim` works on Machine B
- If auth fails: check `TREELAND_RPC_TOKEN` matches on A/B
- If actions fail: confirm `ydotoold` is running and Wayland env vars are set
