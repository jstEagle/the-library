#!/bin/bash
# Watchdog for The Library generation. Run by cron every minute.
# Restarts generation (detached) if no live process is found.

ROOT="/Users/justus/Documents/Programming/the-library"
cd "$ROOT" || exit 1
LOG="$ROOT/watchdog.log"

ts() { date "+%F %T"; }

# Alive? (masked title OR classic cmdline)
if pgrep -f "thelibrary-generator" >/dev/null 2>&1 \
   || pgrep -f "scripts/generate.py --workers" >/dev/null 2>&1; then
    exit 0
fi

echo "$(ts) no live generator found; relaunching" >> "$LOG"
./.venv/bin/python scripts/generate.py --workers 1000 --daemon >> "$LOG" 2>&1
sleep 3

if pgrep -f "thelibrary-generator" >/dev/null 2>&1; then
    echo "$(ts) relaunch OK (pid $(cat generation.pid 2>/dev/null || echo '?'))" >> "$LOG"
else
    echo "$(ts) ERROR: relaunch failed" >> "$LOG"
fi
