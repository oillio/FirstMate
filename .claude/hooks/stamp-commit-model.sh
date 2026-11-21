#!/bin/sh
# Claude Code PreToolUse hook for Bash.
# Before a "git commit" runs, write the session model to a file in the git
# directory. The git hook tools/git-hooks/prepare-commit-msg reads the file and
# adds a "Model:" trailer to the commit message. This hook never blocks.
#
# The stamp file has two lines: the current model, then every model used
# since the last commit (comma-separated). After the stamp, the session file
# keeps only the current model, so the next commit starts from it.
#
# Model source, in order:
#   1. The models that record-model.sh saved for this session.
#   2. The model of the last assistant message in the transcript.
#   3. "unknown". A visible "unknown" is better than no trailer.

input=$(cat)
command=$(printf '%s' "$input" | jq -r '.tool_input.command // empty' 2>/dev/null)
case "$command" in
  *"git commit"*|*"git -c "*" commit"*) ;;
  *) exit 0 ;;
esac

session=$(printf '%s' "$input" | jq -r '.session_id // empty' 2>/dev/null)
transcript=$(printf '%s' "$input" | jq -r '.transcript_path // empty' 2>/dev/null)

cd "${CLAUDE_PROJECT_DIR:-.}" 2>/dev/null || exit 0
common=$(git rev-parse --git-common-dir 2>/dev/null) || exit 0
gitdir=$(git rev-parse --git-dir 2>/dev/null) || exit 0

model=""
used=""
sessfile="$common/firstmate/sessions/$session"
if [ -n "$session" ] && [ -s "$sessfile" ]; then
  model=$(tail -n 1 "$sessfile")
  used=$(awk 'NF && !seen[$0]++' "$sessfile" | paste -sd, - | sed 's/,/, /g')
  printf '%s\n' "$model" > "$sessfile"
fi
if [ -z "$model" ] && [ -f "$transcript" ]; then
  model=$(jq -r 'select(.type == "assistant") | .message.model // empty' "$transcript" 2>/dev/null | tail -n 1)
fi
[ -n "$model" ] || model="unknown"

[ -n "$used" ] || used="$model"
printf '%s\n%s\n' "$model" "$used" > "$gitdir/firstmate-commit-model"
exit 0
