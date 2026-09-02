#!/bin/bash
# Bounded, non-disruptive maintenance for the long-running generator.
# Intended for launchd. It never signals the generator or stages credentials,
# logs, virtual environments, or other temporary state.

set -u

ROOT="/Users/justus/Documents/Programming/the-library"
LOG="$ROOT/maintenance.log"
GENERATION_LOG="$ROOT/generation.log"
RECENT_LOG="$ROOT/generation.log.recent"
LOCK="$ROOT/.maintenance.lock"
KEEP_BYTES=$((2 * 1024 * 1024))
ROTATE_AT=$((32 * 1024 * 1024))
MIN_AGE_MINUTES=5

ts() { date '+%F %T'; }
note() { echo "$(ts) $*" >> "$LOG"; }

mkdir "$LOCK" 2>/dev/null || exit 0
trap 'rmdir "$LOCK"' EXIT
cd "$ROOT" || exit 1

# Keep a small, replaceable diagnostic tail. Truncating the open file is safe:
# the generator keeps its file descriptor and continues writing uninterrupted.
if [ -f "$GENERATION_LOG" ]; then
  log_size=$(stat -f '%z' "$GENERATION_LOG" 2>/dev/null || echo 0)
  if [ "$log_size" -ge "$ROTATE_AT" ]; then
    tmp="$RECENT_LOG.tmp.$$"
    tail -c "$KEEP_BYTES" "$GENERATION_LOG" > "$tmp" 2>/dev/null || true
    mv -f "$tmp" "$RECENT_LOG"
    : > "$GENERATION_LOG"
    note "rotated generation log from ${log_size} bytes; retained last ${KEEP_BYTES} bytes"
  fi
fi

# Do not surprise a user by rebasing/merging a tree which is behind or has a
# remote divergence. A later run resumes automatically once the branch is
# fast-forward-safe again.
git fetch origin --quiet || { note 'git fetch failed; leaving work untouched'; exit 0; }
if ! git merge-base --is-ancestor origin/main HEAD; then
  note 'origin/main is ahead or diverged; skipped commit/push to avoid conflict'
  exit 0
fi

# Only stage durable project content. Generated chapters need to be quiet for
# a few minutes first, avoiding an in-progress write during a batch commit.
git add -- config.json scripts/generate.py scripts/watchdog.sh scripts/maintenance.sh scripts/install-maintenance-launchd.sh .gitignore README.md 2>/dev/null || true
# xargs batches avoid one git process per chapter when a large historical
# generation batch is ready to publish.
find books -type f -name '*.md' -mmin +"$MIN_AGE_MINUTES" -print0 \
  | xargs -0 -n 200 git add --

if git diff --cached --quiet; then
  exit 0
fi

chapter_count=$(git diff --cached --name-only | awk '/^books\/.*\.md$/ { count += 1 } END { print count + 0 }')
git commit -m "chore: sync generated library batch (${chapter_count} chapters)" || {
  note 'git commit failed; index retained for inspection'
  exit 0
}

if git push origin main; then
  note "pushed generated batch (${chapter_count} chapters)"
else
  note 'git push failed; local commit retained for a later retry'
fi
