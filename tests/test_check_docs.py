"""Tests for tools/check_docs.py. Each test makes a small repository in a temporary folder."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import check_docs  # noqa: E402

GOOD_ADR = "# ADR-0001: Something\n\nStatus: Accepted\n"


def make_repo(files: dict[str, str]) -> Path:
    root = Path(tempfile.mkdtemp())
    for name, text in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return root


class RequirementIdTests(unittest.TestCase):
    def test_clean_repo_passes(self):
        root = make_repo({
            "docs/requirements/r.md": "- CORE-DP-01. Text.\n- AC-CORE-1. Text. See CORE-DP-01.\n### DEC-001: Title\n",
            "docs/decisions/0001-x.md": GOOD_ADR,
        })
        self.assertEqual(check_docs.run(root).errors, [])

    def test_duplicate_id_fails(self):
        root = make_repo({"docs/requirements/r.md": "- CORE-DP-01. A.\n- CORE-DP-01. B.\n"})
        errors = check_docs.run(root).errors
        self.assertEqual(len(errors), 1)
        self.assertIn("defined again", errors[0])

    def test_unknown_reference_fails(self):
        root = make_repo({
            "docs/requirements/r.md": "- CORE-DP-01. A.\n",
            "docs/other.md": "See CORE-DP-99.\n",
        })
        errors = check_docs.run(root).errors
        self.assertEqual(len(errors), 1)
        self.assertIn("CORE-DP-99", errors[0])

    def test_unrelated_codes_are_ignored(self):
        root = make_repo({
            "docs/requirements/r.md": "- CORE-DP-01. Uses S-57 charts and RMI MI-108.\n",
        })
        self.assertEqual(check_docs.run(root).errors, [])


class AdrTests(unittest.TestCase):
    def test_bad_status_fails(self):
        root = make_repo({"docs/decisions/0001-x.md": "# ADR-0001: X\n\nStatus: Maybe\n"})
        self.assertIn("status is not valid", check_docs.run(root).errors[0])

    def test_title_number_mismatch_fails(self):
        root = make_repo({"docs/decisions/0002-x.md": GOOD_ADR})
        self.assertIn("does not match", check_docs.run(root).errors[0])

    def test_unknown_adr_reference_fails(self):
        root = make_repo({"docs/decisions/0001-x.md": GOOD_ADR, "README.md": "See ADR-0042.\n"})
        self.assertIn("unknown ADR-0042", check_docs.run(root).errors[0])

    def test_superseded_status_passes(self):
        root = make_repo({
            "docs/decisions/0001-x.md": "# ADR-0001: X\n\nStatus: Superseded by ADR-0002\n",
            "docs/decisions/0002-y.md": "# ADR-0002: Y\n\nStatus: Accepted\n",
        })
        self.assertEqual(check_docs.run(root).errors, [])


class AdrIndexTests(unittest.TestCase):
    README = "# ADRs\n\n" + check_docs.INDEX_BEGIN + "\n" + check_docs.INDEX_END + "\n"

    def test_missing_index_fails(self):
        root = make_repo({"docs/decisions/0001-x.md": GOOD_ADR, "docs/decisions/README.md": self.README})
        self.assertIn("out of date", check_docs.run(root).errors[0])

    def test_written_index_passes(self):
        root = make_repo({"docs/decisions/0001-x.md": GOOD_ADR, "docs/decisions/README.md": self.README})
        check_docs.write_adr_index(root)
        self.assertEqual(check_docs.run(root).errors, [])
        self.assertIn("| [0001](0001-x.md) | Something | Accepted |", (root / "docs/decisions/README.md").read_text())

    def test_status_change_makes_index_stale(self):
        root = make_repo({"docs/decisions/0001-x.md": GOOD_ADR, "docs/decisions/README.md": self.README})
        check_docs.write_adr_index(root)
        (root / "docs/decisions/0001-x.md").write_text("# ADR-0001: Something\n\nStatus: Rejected\n")
        self.assertIn("out of date", check_docs.run(root).errors[0])

    def test_issue_line_required_when_enabled(self):
        root = make_repo({"docs/decisions/0001-x.md": "# ADR-0001: X\n\nStatus: Proposed\n"})
        old = check_docs.REQUIRE_ADR_ISSUE
        check_docs.REQUIRE_ADR_ISSUE = True
        try:
            self.assertIn("Issue: #N", check_docs.run(root).errors[0])
            (root / "docs/decisions/0001-x.md").write_text("# ADR-0001: X\n\nStatus: Proposed\nIssue: #12\n")
            self.assertEqual(check_docs.run(root).errors, [])
        finally:
            check_docs.REQUIRE_ADR_ISSUE = old

    def test_template_is_exempt_from_issue_line(self):
        root = make_repo({"docs/decisions/0000-template.md": "# ADR-0000: Title\n\nStatus: Proposed\nIssue: #N\n"})
        old = check_docs.REQUIRE_ADR_ISSUE
        check_docs.REQUIRE_ADR_ISSUE = True
        try:
            self.assertEqual(check_docs.run(root).errors, [])
        finally:
            check_docs.REQUIRE_ADR_ISSUE = old


class CommandGuardTests(unittest.TestCase):
    def test_command_pgn_in_code_fails(self):
        root = make_repo({"src/pilot.py": "send(pgn=126208)\n"})
        self.assertIn("command PGN 126208", check_docs.run(root).errors[0])

    def test_alert_pgn_in_code_passes(self):
        root = make_repo({"src/alarm.py": "send(pgn=126983)\n"})
        self.assertEqual(check_docs.run(root).errors, [])

    def test_longer_number_is_not_a_match(self):
        root = make_repo({"src/data.py": "x = 11262081\n"})
        self.assertEqual(check_docs.run(root).errors, [])


if __name__ == "__main__":
    unittest.main()
