"""Tests for the guard-file rule, the Claude Code ask rules, and the Stop hook."""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))

import check_guard_pr  # noqa: E402

PATTERNS = check_guard_pr.load_patterns()


class GuardRuleTests(unittest.TestCase):
    def test_no_guard_files_passes(self):
        self.assertEqual(check_guard_pr.check(["docs/roadmap.md", "src/a.py"], [], PATTERNS), [])

    def test_guard_only_with_label_passes(self):
        changed = [".claude/settings.json", "tools/check_docs.py", "docs/process/ai-team.md"]
        self.assertEqual(check_guard_pr.check(changed, ["type:guard"], PATTERNS), [])

    def test_guard_without_label_fails(self):
        errors = check_guard_pr.check([".github/workflows/checks.yml"], [], PATTERNS)
        self.assertTrue(any("type:guard" in e for e in errors))

    def test_mixed_files_fail_even_with_label(self):
        errors = check_guard_pr.check(["tests/test_x.py", "src/alarm.py"], ["type:guard"], PATTERNS)
        self.assertTrue(any("own pull request" in e for e in errors))

    def test_folder_pattern_does_not_match_similar_name(self):
        self.assertFalse(check_guard_pr.is_guard("tests-extra/a.py", PATTERNS))
        self.assertTrue(check_guard_pr.is_guard("tests/a.py", PATTERNS))

    def test_seeded_defects_are_guarded(self):
        self.assertTrue(check_guard_pr.is_guard("eval/seeded-defects/sd_04.py", PATTERNS))


class AskRuleTests(unittest.TestCase):
    def test_every_guard_pattern_has_an_ask_rule(self):
        settings = json.loads((REPO / ".claude" / "settings.json").read_text(encoding="utf-8"))
        ask = set(settings["permissions"]["ask"])
        missing = [p for p in PATTERNS if f"Edit(./{p})" not in ask]
        self.assertEqual(missing, [], "tools/guard-files.txt and the ask rules in .claude/settings.json differ")

    def test_merge_is_denied(self):
        settings = json.loads((REPO / ".claude" / "settings.json").read_text(encoding="utf-8"))
        self.assertIn("Bash(gh pr merge:*)", settings["permissions"]["deny"])


HAVE_TOOLS = shutil.which("git") and shutil.which("jq") and shutil.which("make")


@unittest.skipUnless(HAVE_TOOLS, "needs git, jq and make")
class StopHookTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        shutil.copytree(REPO / ".claude" / "hooks", self.root / ".claude" / "hooks")
        hook = self.root / ".claude" / "hooks" / "stop-check.sh"
        hook.chmod(0o755)
        self.hook = hook
        self.env = {**os.environ, "CLAUDE_PROJECT_DIR": str(self.root)}
        for args in (["init", "-q"], ["config", "user.email", "t@example.com"], ["config", "user.name", "t"]):
            subprocess.run(["git", *args], cwd=self.root, check=True)
        (self.root / "Makefile").write_text("check:\n\t@test ! -f broken\n")
        subprocess.run(["git", "add", "-A"], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", "base"], cwd=self.root, check=True)

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def run_hook(self, active=False):
        payload = json.dumps({"stop_hook_active": active})
        return subprocess.run([str(self.hook)], input=payload, cwd=self.root, env=self.env,
                              capture_output=True, text=True)

    def test_clean_tree_allows_stop(self):
        self.assertEqual(self.run_hook().returncode, 0)

    def test_passing_check_allows_stop(self):
        (self.root / "note.txt").write_text("x")
        self.assertEqual(self.run_hook().returncode, 0)

    def test_failing_check_blocks_stop(self):
        (self.root / "broken").write_text("x")
        result = self.run_hook()
        self.assertEqual(result.returncode, 2)
        self.assertIn("make check fails", result.stderr)

    def test_second_stop_is_allowed(self):
        (self.root / "broken").write_text("x")
        self.assertEqual(self.run_hook(active=True).returncode, 0)


if __name__ == "__main__":
    unittest.main()
