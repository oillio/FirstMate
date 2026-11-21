#!/bin/sh
# Claude Code hook for SessionStart and PostModelSwitch.
# Records the model of this session, so stamp-commit-model.sh can read it.
# SessionStart gives "model" (not always). PostModelSwitch gives "to_model",
# also after an automatic fallback. This hook never blocks.

input=$(cat)
session=$(printf '%s' "$input" | jq -r '.session_id // empty' 2>/dev/null)
model=$(printf '%s' "$input" | jq -r '.to_model // .model // empty' 2>/dev/null)
[ -n "$session" ] && [ -n "$model" ] || exit 0

cd "${CLAUDE_PROJECT_DIR:-.}" 2>/dev/null || exit 0
dir="$(git rev-parse --git-common-dir 2>/dev/null)/firstmate/sessions" || exit 0
mkdir -p "$dir" 2>/dev/null && printf '%s\n' "$model" > "$dir/$session"
exit 0
