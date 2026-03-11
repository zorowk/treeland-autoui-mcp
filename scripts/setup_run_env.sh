#!/usr/bin/env bash

if [[ "${XDG_SESSION_TYPE:-}" == "tty" && -z "${WAYLAND_DISPLAY:-}" ]]; then
    echo "Variable not set, ready to set."
    export DISPLAY=:0
    export WAYLAND_DISPLAY="${XDG_RUNTIME_DIR}/treeland.socket"
    export XDG_SESSION_TYPE=wayland
    export QT_WAYLAND_SHELL_INTEGRATION="xdg-shell;wl-shell;ivi-shell;qt-shell;"
    export XDG_SESSION_DESKTOP=Deepin
    export GDMSESSION=Wayland
    export YDOTOOL_SOCKET="${XDG_RUNTIME_DIR}/.ydotool_socket"
fi

echo "Wayland environment variables have been set." >&2

UID="$(id -u)"
GID="$(id -g)"
touch_flag=()
if command -v libinput >/dev/null 2>&1; then
    echo "Checking touchscreen via libinput..." >&2
    if sudo libinput list-devices 2>/dev/null | grep -qi "Touchscreen"; then
        echo "Touchscreen detected; enabling -T for ydotoold." >&2
        touch_flag=(-T)
    else
        echo "No touchscreen detected via libinput." >&2
    fi
else
    echo "libinput not found; skipping touchscreen detection." >&2
fi
if ! pgrep -x ydotoold >/dev/null 2>&1; then
    echo "Starting ydotoold (UID=${UID}, GID=${GID})..." >&2
    sudo ydotoold "${touch_flag[@]}" -p "${XDG_RUNTIME_DIR}/.ydotool_socket" -o "${UID}:${GID}" >/dev/null 2>&1 &
else
    echo "ydotoold already running; skipping start." >&2
fi
