#!/usr/bin/env bash
# Launch the "Data to Decisions" interactive workshop platform.
# Runs from this script's directory so relative asset paths resolve.
set -euo pipefail

cd "$(dirname "$(readlink -f "$0")")"

PORT="${PORT:-8501}"

# Install dependencies only if Streamlit isn't importable yet.
if ! python3 -c "import streamlit" >/dev/null 2>&1; then
  echo "[run.sh] Installing dependencies..."
  python3 -m pip install -r requirements.txt
fi

echo "[run.sh] Starting the workshop platform on http://localhost:${PORT}"
echo "[run.sh] Use the sidebar to move through slides and demos. Ctrl+C to stop."
exec python3 -m streamlit run Home.py \
  --server.port "${PORT}" \
  --server.headless false \
  --browser.gatherUsageStats false
