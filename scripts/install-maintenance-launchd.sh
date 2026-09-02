#!/bin/bash
# Installs a per-user, 30-minute launchd job for scripts/maintenance.sh.
set -euo pipefail

ROOT="/Users/justus/Documents/Programming/the-library"
LABEL="com.justeagle.the-library-maintenance"
PLIST="/Users/justus/Library/LaunchAgents/${LABEL}.plist"

mkdir -p "/Users/justus/Library/LaunchAgents"
cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>${LABEL}</string>
  <key>ProgramArguments</key><array><string>${ROOT}/scripts/maintenance.sh</string></array>
  <key>StartInterval</key><integer>1800</integer>
  <key>RunAtLoad</key><true/>
  <key>ProcessType</key><string>Background</string>
</dict></plist>
EOF

launchctl bootout "gui/$(id -u)/${LABEL}" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$PLIST"
launchctl kickstart -k "gui/$(id -u)/${LABEL}"
