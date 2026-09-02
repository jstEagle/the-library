#!/bin/bash
# Installs a per-user, 30-minute cron job for scripts/maintenance.sh.
# Cron is deliberately used here: this project lives under Documents, where a
# background launchd agent can be denied macOS privacy access. The existing
# user cron service has already been verified to read this project directory.
set -euo pipefail

ROOT="/Users/justus/Documents/Programming/the-library"
LABEL="com.justeagle.the-library-maintenance"
MARKER="# the-library-maintenance"

launchctl bootout "gui/$(id -u)/${LABEL}" 2>/dev/null || true
rm -f "/Users/justus/Library/LaunchAgents/${LABEL}.plist"

current=$(crontab -l 2>/dev/null || true)
(printf '%s\n' "$current" | grep -vF "$MARKER" || true) > /tmp/the-library-crontab.$$
printf '7,37 * * * * /bin/bash %s/scripts/maintenance.sh %s\n' "$ROOT" "$MARKER" >> /tmp/the-library-crontab.$$
crontab /tmp/the-library-crontab.$$
rm -f /tmp/the-library-crontab.$$
