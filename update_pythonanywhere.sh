#!/bin/bash
set -e

PROJECT_DIR="${PROJECT_DIR:-$HOME/attendance_system_lyhoa}"
BRANCH="${BRANCH:-main}"
VENV_DIR="${VENV_DIR:-$PROJECT_DIR/venv}"
RELOAD_FILE="${RELOAD_FILE:-}"
INSTALL_DEPS="${INSTALL_DEPS:-1}"

echo "==> Chuyen vao thu muc project"
cd "$PROJECT_DIR"

echo "==> Kiem tra git repository"
git rev-parse --is-inside-work-tree >/dev/null 2>&1

echo "==> Pull code moi nhat tu branch $BRANCH"
git pull origin "$BRANCH"

if [ "$INSTALL_DEPS" = "1" ] && [ -d "$VENV_DIR" ] && [ -f "requirements.txt" ]; then
  echo "==> Cai dat/cap nhat dependencies"
  source "$VENV_DIR/bin/activate"
  pip install -r requirements.txt
fi

if [ -n "$RELOAD_FILE" ]; then
  echo "==> Reload web app"
  touch "$RELOAD_FILE"
else
  echo "==> Chua co RELOAD_FILE. Hay bam Reload trong tab Web hoac set RELOAD_FILE truoc khi chay script."
fi

echo "==> Hoan tat"
