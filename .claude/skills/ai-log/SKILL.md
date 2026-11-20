---
name: ai-log
description: Record how an AI tool contributed to convert_flux in AI_USAGE.md. Use when the user runs /ai-log, or before committing or opening a pull request. Pass args as "<model name> (<model ID>) | <Category> | <one-sentence summary>".
argument-hint: <model name> (<model ID>) | <Category> | <one-sentence summary>
context: fork
model: haiku
---

# AI contribution log

Add one entry to `AI_USAGE.md`, the public record of AI use in this package.

Input: $ARGUMENTS
- Model name and ID, for example `Claude Opus 5.5 (claude-opus-5-5)`. Log this model,
  not the model you are running as.
- Category: Code, Debugging, Refactoring, Review, or Resources.
- One-sentence summary of the work, in the past tense.
If any part is missing, stop and say what is missing.

1. Run this one command. It prints the branch, the Tools used table, and that branch's
   section:
   ```
   b=$(git branch --show-current); echo "$b"; sed -n '/^## Tools used/,/^## Categories/p' AI_USAGE.md; awk -v h="### \`$b\`" '$0==h{p=1;print;next} p&&/^### /{exit} p' AI_USAGE.md
   ```
2. Edit `AI_USAGE.md` with as few Edit calls as possible. Don't read anything else.
   - If a bullet in the branch section has the same category and model, extend it
     instead of adding a new one.
   - Otherwise add `- **<Category>** (<model name>): <summary>` to the section.
   - If the section is missing, add it above the first `### ` heading under
     `## Contributions`: a `` ### `<branch>` `` heading, then
     `*Started YYYY-MM. Pull request: TBD.*`.
   - If the model has no row in the Tools used table, add one. Otherwise, extend its
     `Used` range to the current month if needed.
   - Keep lines to about 90 characters. Name files or functions only for major changes.
3. Don't commit. Reply with one line saying what you added.
