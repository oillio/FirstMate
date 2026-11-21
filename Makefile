.PHONY: check docs test adr-index hooks

PYTHON ?= python3

check: docs test

docs:
	$(PYTHON) tools/check_docs.py

test:
	$(PYTHON) -m unittest discover -s tests -v

adr-index:
	$(PYTHON) tools/check_docs.py --write-adr-index

# Install the repository git hooks (Model: trailer). Run once per clone.
hooks:
	@command -v jq >/dev/null || { echo "ERROR: jq is missing. Run: brew install jq"; exit 1; }
	git config core.hooksPath tools/git-hooks
	chmod +x tools/git-hooks/* .claude/hooks/*.sh
