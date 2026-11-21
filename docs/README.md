# Documentation map

The repository is the single source of truth for this project ([ADR-0003](decisions/0003-repo-is-source-of-truth.md)). A chat, a claude.ai Project, or another tool can hold a copy. The copy in this repository wins.

| Folder | Content | Who changes it |
|---|---|---|
| [roadmap.md](roadmap.md) | Plan and phases | Skipper ratifies |
| [requirements/](requirements/) | Requirements with stable IDs | Pull request, skipper approves |
| [decisions/](decisions/) | ADRs. Accepted ADRs do not change. | New ADR supersedes an old one |
| [specs/](specs/) | Agent Specifications, one per subsystem | Architect drafts, skipper approves |
| [process/](process/) | How we build: process, AI team, writing style | Skipper |
| [research/](research/) | Inputs: teardowns, guidance summaries. Not binding. | Any |
| [aboard/](aboard/) | Checklists and runbooks for work on the boat | Skipper |
| [plan/](plan/) | Current to-do lists | Skipper |

## Document status values

- DRAFT: work in progress. Not binding.
- RATIFIED: the skipper approved it. Changes need a pull request.
- SUPERSEDED: a newer document replaces it. The file stays for history.
