"""Tests for the Model: commit trailer (Claude Code hooks + git prepare-commit-msg hook).

Each test makes a temporary git repository with the hooks installed. Needs git and jq.
"""

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
HAVE_TOOLS = shutil.which("git") and shutil.which("jq")


@unittest.skipUnless(HAVE_TOOLS, "needs git and jq")
class ModelTrailerTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        shutil.copytree(REPO / "tools" / "git-hooks", self.root / "tools" / "git-hooks")
        shutil.copytree(REPO / ".claude" / "hooks", self.root / ".claude" / "hooks")
        for path in list((self.root / "tools" / "git-hooks").iterdir()) + list((self.root / ".claude" / "hooks").iterdir()):
            path.chmod(0o755)
        self.env = {**os.environ, "CLAUDE_PROJECT_DIR": str(self.root)}
        self.env.pop("FIRSTMATE_MODEL", None)
        for args in (["init", "-q"], ["config", "user.email", "t@example.com"], ["config", "user.name", "t"],
                     ["config", "core.hooksPath", "tools/git-hooks"]):
            self.git(*args)

    def git(self, *args, env=None):
        return subprocess.run(["git", *args], cwd=self.root, env=env or self.env, check=True,
                              capture_output=True, text=True).stdout

    def hook(self, name, payload):
        subprocess.run([str(self.root / ".claude" / "hooks" / name)], input=json.dumps(payload),
                       cwd=self.root, env=self.env, check=True, text=True)

    def commit(self, message, env=None):
        (self.root / "f.txt").write_text(message)
        self.git("add", "f.txt", env=env)
        self.git("commit", "-q", "-m", message, env=env)
        return self.git("log", "-1", "--format=%B")

    def stamp(self, session, transcript=None):
        payload = {"session_id": session, "tool_input": {"command": "git commit -m x"}}
        if transcript:
            payload["transcript_path"] = transcript
        self.hook("stamp-commit-model.sh", payload)

    def test_session_model_after_fallback(self):
        self.hook("record-model.sh", {"session_id": "s1", "model": "claude-opus-5-5"})
        self.hook("record-model.sh", {"session_id": "s1", "to_model": "claude-opus-4-8", "source": "auto"})
        self.stamp("s1")
        self.assertIn("Model: claude-opus-4-8", self.commit("one"))

    def test_transcript_fallback(self):
        transcript = self.root / "t.jsonl"
        transcript.write_text(json.dumps({"type": "assistant", "message": {"model": "claude-sonnet-5-5"}}) + "\n")
        self.stamp("s2", str(transcript))
        self.assertIn("Model: claude-sonnet-5-5", self.commit("two"))

    def test_unknown_when_no_source(self):
        self.stamp("s3")
        self.assertIn("Model: unknown", self.commit("three"))

    def test_human_commit_has_no_trailer(self):
        self.assertNotIn("Model:", self.commit("four"))

    def test_env_variable_for_other_agents(self):
        env = {**self.env, "FIRSTMATE_MODEL": "gpt-5-codex"}
        self.assertIn("Model: gpt-5-codex", self.commit("five", env=env))

    def test_stamp_is_used_once(self):
        self.hook("record-model.sh", {"session_id": "s1", "model": "claude-opus-5-5"})
        self.stamp("s1")
        self.commit("six")
        self.assertNotIn("Model:", self.commit("seven"))

    def test_models_used_after_switch(self):
        self.hook("record-model.sh", {"session_id": "s4", "model": "claude-opus-5-5"})
        self.hook("record-model.sh", {"session_id": "s4", "to_model": "claude-opus-5", "source": "auto"})
        self.stamp("s4")
        message = self.commit("eight")
        self.assertIn("Model: claude-opus-5", message)
        self.assertIn("Session-Models: claude-opus-5-5, claude-opus-5", message)

    def test_models_used_resets_after_commit(self):
        self.hook("record-model.sh", {"session_id": "s5", "model": "claude-opus-5-5"})
        self.hook("record-model.sh", {"session_id": "s5", "to_model": "claude-opus-5", "source": "auto"})
        self.stamp("s5")
        self.commit("nine")
        self.stamp("s5")
        message = self.commit("ten")
        self.assertIn("Model: claude-opus-5", message)
        self.assertNotIn("Session-Models:", message)

    def test_one_model_has_no_models_used(self):
        self.hook("record-model.sh", {"session_id": "s6", "model": "claude-opus-5-5"})
        self.hook("record-model.sh", {"session_id": "s6", "to_model": "claude-opus-5-5", "source": "resume"})
        self.stamp("s6")
        self.assertNotIn("Session-Models:", self.commit("eleven"))

    def test_other_bash_commands_are_ignored(self):
        self.hook("stamp-commit-model.sh", {"session_id": "s1", "tool_input": {"command": "ls -la"}})
        self.assertFalse((self.root / ".git" / "firstmate-commit-model").exists())


if __name__ == "__main__":
    unittest.main()
