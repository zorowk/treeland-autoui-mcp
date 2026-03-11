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
    if sudo libinput list-devices 2>/dev/null | grep -qi "Touchscreen"; then
        touch_flag=(-T)
    fi
fi
sudo ydotoold "${touch_flag[@]}" -p "${XDG_RUNTIME_DIR}/.ydotool_socket" -o "${UID}:${GID}" >/dev/null 2>&1 &
