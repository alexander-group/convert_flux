# AI usage in `convert_flux`

This file records how AI and large language model (LLM) tools were used to develop
`convert_flux`. It covers written code and also debugging, refactoring, review, and
finding or explaining outside resources.

All AI output was reviewed by the human developers, who made the final decisions and are
responsible for the code in this package. The entries are grouped by branch and pull
request, newest first. They describe tasks in general terms, not every individual change.
Each entry names the model version that did the work.

Entries are written by the AI tool at the end of a task (see
`.claude/skills/ai-log/SKILL.md`) and checked by a developer in pull request review.

## Tools used

| Tool | Model | Model ID | Used |
|---|---|---|---|
| Claude Code | Claude Opus 5.5 | `claude-opus-5-5` | 2026-10 to 2026-11 |

## Categories

- **Code:** Wrote or changed source code, tests, docs, or config.
- **Debugging:** Found and fixed bugs or failing tests.
- **Refactoring:** Restructured code without changing behavior.
- **Review:** Reviewed code or a pull request.
- **Resources:** Found, summarized, or explained outside resources.

## Contributions

### `33-tracking-ai-usage`

*Started 2026-11. Pull request: TBD.*

- **Code** (Claude Opus 5.5): Created the `ai-log` skill and this log, and backfilled
  earlier entries from the commit history. Added `CLAUDE.md` file based on developer's guildelines.

### `28-write-the-convert_flux-function`

*Started 2026-11. Pull request: TBD.*

- **Resources** (Claude Opus 5.5): Explained how synphot converts fluxes and how it
  compares with this package's design.
- **Code** (Claude Opus 5.5): Modified the `convert_flux()` docstring.
- **Refactoring** (Claude Opus 5.5): Updated imports and added `__init__.py` to resolve
  the new file structure.

### `25-add-and-improve-github-automation`

*2026-10. Pull request:
[#29](https://github.com/alexander-group/convert_flux/pull/29).
(Backfilled from commit history.)*

- **Debugging** (Claude Opus 5.5): Fixed the Codecov upload failing on macOS in CI.
- **Debugging** (Claude Opus 5.5): Fixed `python-semantic-release` not bumping the
  version.
