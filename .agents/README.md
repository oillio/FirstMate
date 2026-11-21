# Agent roles and prompts

Plain Markdown files. Any agent can load them. They do not depend on one vendor.

- `roles/`: one file per role. Load the role file at the start of a task.
- `prompts/`: reusable task prompts.

To start a task with any agent, write:

> Read `AGENTS.md` and `.agents/roles/<role>.md`. Your task: <task>. Requirement IDs: <IDs>.
