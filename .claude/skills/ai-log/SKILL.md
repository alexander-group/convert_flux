---
name: ai-log
description: Record how Claude (or another AI/LLM) contributed to convert_flux in AI_USAGE.md. Use at the end of any task where Claude wrote, debugged, refactored, reviewed, or tested code, or found and explained outside resources (papers, docs, other packages). Also use when the user runs /ai-log, or when preparing a commit or pull request.
---

# AI contribution log

`AI_USAGE.md` at the repository root is the public record of how AI/LLM tools were used to
build `convert_flux`. It is committed and reviewed in pull requests. Its purpose is
transparency, so readers can tell
which parts of the package had AI help and what kind of help it was.

## When to update

Update the log once, at the end of a task, if the task did any of the following:

- **Code:** Wrote or changed source code, tests, docs, or config.
- **Debugging:** Found and fixed bugs or failing tests.
- **Refactoring:** Restructured code without changing behavior.
- **Review:** Reviewed code or a pull request.
- **Resources:** Found, summarized, or explained outside resources, for example papers,
  astropy or synphot docs, or other packages. Name the resource.

Skip it for trivial help that didn't shape the package, such as running the test suite on
request, answering general questions unrelated to the repo, or fixing typos in this log.

## How to write an entry

1. Run `git branch --show-current` to get the current branch name. Don't rely on the git
   status from the start of the session, because the branch may have changed since then.
   Read-only git commands are allowed.
2. Don't read all of `AI_USAGE.md`, because it grows with every branch. Read only the
   parts you need:
   - The first ~40 lines, which hold the "Tools used" table.
   - The current branch's section. Search for its heading (`### \`<branch-name>\``) and
     read from there to the next `### ` heading. If there's no heading, find the first
     `### ` heading under "Contributions" and add the new section above it.
3. Find the model name and version you are running as, from your environment information
   (for example, "Claude Opus 5.5", model ID `claude-opus-5-5`). If you can't tell, ask the
   user. Don't guess.
4. Find the section for that branch. If it doesn't exist, add one at the top of the
   "Contributions" section, newest first:

   ```markdown
   ### `<branch-name>`

   *Started YYYY-MM. Pull request: TBD.*
   ```

   Replace `TBD` with a link to the pull request once it exists.
5. Add or update bullets in that section. Each bullet starts with one bold category tag
   (`**Code**`, `**Debugging**`, `**Refactoring**`, `**Review**`, or `**Resources**`),
   then the model name and version in parentheses, then a colon and one short sentence:

   ```markdown
   - **Debugging** (Claude Opus 5.5): Debugged unit conversion failures in
     `MagFluxDensity`.
   ```

6. Before adding a bullet, check if one already covers the same work with the same model,
   and extend it instead. Many debugging sessions on the same feature should end up as one
   bullet, not one bullet per bug. If the same work was done with a different model, add a
   new bullet so each model's contribution stays clear.
7. Make sure the model has a row in the "Tools used" table (see below).

## Writing style

- Keep each bullet to one short sentence that describes the general task, for example
  "Updated imports and added `__init__.py` to resolve the new file structure." Don't list
  every step or detail.
- Name files, functions, or classes only for major changes, in backticks.
- Be factual. Say what the AI did and what the human decided or changed. Don't overstate
  either side. If the user rewrote or rejected AI output, it's fine to say so.
- Use the past tense ("Wrote", "Fixed", "Explained").
- Keep lines to about 90 characters so the diff is easy to review.

## Tools used table

`AI_USAGE.md` has a "Tools used" table near the top with one row per tool and model
version: the tool (for example, Claude Code), the model name, the exact model ID, and the
date range it was used (first and last month, `YYYY-MM`). If the current model isn't
listed, add a row. If it is, extend its date range when needed.

## Backfilling past contributions

To find earlier AI contributions, search the history for commits with AI co-author lines,
for example `git log --all --format='%h %ad %an | %s%n%b' --date=short`, and look for
`Co-Authored-By: Claude ...`. Take the model version from that line. Use
`git log --merges --ancestry-path <commit>..main` to find the pull request that merged a
commit. Mark entries inferred from history with "*(Backfilled from commit history.)*" so a
developer knows to check them. AI help that left no co-author line (for example,
debugging in a chat) can't be found this way, so ask the user to add it by hand.

## After updating

Tell the user in one line that you updated `AI_USAGE.md` and what you added. Don't commit
the change. The user commits it with the rest of the branch's work.
