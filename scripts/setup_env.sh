#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${PROJECT_ROOT}/.venv"
TMP_BASE="$(mktemp -d /tmp/treeland-autotests-deps.XXXXXX)"

REPO_1_URL="https://github.com/zorowk/pyautogui.git"
REPO_2_URL="https://github.com/zorowk/pyperclip.git"
REPO_1_DIR="${TMP_BASE}/pyautogui"
REPO_2_DIR="${TMP_BASE}/pyperclip"

cleanup() {
  if [[ "${KEEP_TMP:-0}" != "1" && -d "${TMP_BASE}" ]]; then
    rm -rf "${TMP_BASE}"
  fi
}
trap cleanup EXIT

echo "[1/5] Create python virtual environment: ${VENV_DIR}"
python3 -m venv "${VENV_DIR}"

echo "[2/5] Activate venv and upgrade pip tooling"
# shellcheck disable=SC1091
source "${VENV_DIR}/bin/activate"
python -m pip install --upgrade pip setuptools wheel

echo "[3/5] Clone required repositories into system temp dir: ${TMP_BASE}"
git clone --depth 1 "${REPO_1_URL}" "${REPO_1_DIR}"
git clone --depth 1 "${REPO_2_URL}" "${REPO_2_DIR}"

echo "[4/5] Install pyautogui and pyperclip from cloned repositories"
python -m pip install "${REPO_1_DIR}" "${REPO_2_DIR}"

echo "[5/5] Install dogtail"
python -m pip install dogtail

if python - <<'PY'
import pyatspi
print(pyatspi.__name__)
PY
then
  echo "pyatspi import check: OK"
else
  cat <<'EOF'
Warning: pyatspi is not available in the current environment.
dogtail may require system-level AT-SPI packages from your distro.
Example (Debian/Ubuntu):
  sudo apt-get install -y python3-pyatspi python3-gi gir1.2-atspi-2.0
EOF
fi

cat <<EOF

Setup completed.
Virtual environment: ${VENV_DIR}
Temporary source path used: ${TMP_BASE}

Run:
  source .venv/bin/activate
  python tests/desktop_demo.py

Set KEEP_TMP=1 before running this tests if you want to keep cloned sources in /tmp.
EOF
