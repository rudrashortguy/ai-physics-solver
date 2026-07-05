#!/usr/bin/env bash
set -e

kill_port() { lsof -ti:$1 2>/dev/null | xargs kill -9 2>/dev/null || true; }
kill_port 8000

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

# ponytail: source venv if it exists; if not, user must pip install
[ -f "$PROJECT_DIR/backend/.venv/bin/activate" ] && source "$PROJECT_DIR/backend/.venv/bin/activate"

cd "$PROJECT_DIR/backend"
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!

cd "$PROJECT_DIR/frontend"
npm run dev &
FRONTEND_PID=$!

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT
wait
