#!/usr/bin/env python3
"""Guard-file check for pull requests. Standard library only.

Rule: a pull request that changes a guard file (tools/guard-files.txt) must
change only guard files, and must have the label type:guard.

Reason: an agent must not weaken a check in the same pull request as the code
that the check would fail. A separate pull request makes the change visible.

Usage:
  check_guard_pr.py --labels '<JSON list of label names>' < changed-files.txt

Exit code 0 when the rule holds, 1 when it does not.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

GUARD_LABEL = "type:guard"
ROOT = Path(__file__).resolve().parent.parent


def load_patterns(path: Path = ROOT / "tools" / "guard-files.txt") -> list[str]:
    patterns = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            patterns.append(line)
    return patterns


def is_guard(file: str, patterns: list[str]) -> bool:
    for pattern in patterns:
        if pattern.endswith("/**"):
            if file.startswith(pattern[:-2]):
                return True
        elif file == pattern:
            return True
    return False


def check(changed: list[str], labels: list[str], patterns: list[str]) -> list[str]:
    guard = [f for f in changed if is_guard(f, patterns)]
    if not guard:
        return []
    errors = []
    other = [f for f in changed if not is_guard(f, patterns)]
    if other:
        errors.append(
            "this pull request changes guard files and other files. Put the guard changes in their own pull request."
        )
        errors += [f"  guard file: {f}" for f in guard]
        errors += [f"  other file: {f}" for f in other]
    if GUARD_LABEL not in labels:
        errors.append(f"this pull request changes guard files. It needs the label {GUARD_LABEL}.")
    return errors


def main() -> int:
    labels: list[str] = []
    args = sys.argv[1:]
    if "--labels" in args:
        labels = json.loads(args[args.index("--labels") + 1])
    changed = [line.strip() for line in sys.stdin if line.strip()]
    errors = check(changed, labels, load_patterns())
    for line in errors:
        print(f"ERROR {line}")
    if errors:
        print("FAIL: guard-file rule")
        return 1
    print("PASS: guard-file rule")
    return 0


if __name__ == "__main__":
    sys.exit(main())
