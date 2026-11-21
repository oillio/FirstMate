#!/bin/sh
# Claude Code Stop hook.
# When Claude tries to stop with changed files in the working tree, run
# "make check". If it fails, exit 2: Claude Code then continues the task and
# reads the reason. This stops a false "done".
#
# Loop limit: if this hook already blocked a stop in this turn
# (stop_hook_active is true), let Claude stop. Claude must then report the
# failure. Hooks are best-effort. CI stays the real gate.

input=$(cat)
active=$(printf '%s' "$input" | jq -r '.stop_hook_active // false' 2>/dev/null)
[ "$active" = "true" ] && exit 0

cd "${CLAUDE_PROJECT_DIR:-.}" 2>/dev/null || exit 0
[ -n "$(git status --porcelain 2>/dev/null)" ] || exit 0

if output=$(make check 2>&1); then
  exit 0
fi

{
  echo "make check fails. The task is not done. Fix the failure, or report it to the skipper."
  printf '%s\n' "$output" | tail -n 20
} >&2
exit 2
