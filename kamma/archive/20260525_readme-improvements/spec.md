## Overview
Two open GitHub issues: #1 (already fixed in code) and #3 (README improvements).

## GitHub issue reference
- Issue #1: subprocess.TimeoutExpired — already resolved in commit 1f593ea / PR #6
- Issue #3: README improvement for Calibre FTS setup and Obsidian CLI runtime requirement

## What it should do
1. Close issue #1 with a comment noting it was fixed in PR #6 / commit 1f593ea.
2. Add to README.md:
   - A `### Calibre full-text search` subsection with FT-button instructions,
     when-GUI-is-needed table, and platform PATH notes.
   - A `### Obsidian CLI` subsection with install instructions, the
     desktop-app-must-be-running requirement, and per-platform start commands.
   - A full "Runtime requirements" block (table + agent instructions) after
     step 0 of the Autonomous agent setup section.
3. Expand the Calibre FTS note in skill/vicaya/README.md.
4. Close issue #3 with a summary comment.

## Assumptions & uncertainties
- Issue #1's fix is confirmed in source: all three functions (fts_available,
  fts_search, metadata_search) already catch TimeoutExpired. Merged in PR #6.
- All suggested text in issue #3 is taken verbatim from the reporter
  (Devamitta Bhikkhu), a co-contributor — content is trusted.
- The `### Calibre FTS` section appears before the Autonomous agent setup,
  so "FT button steps above" in the agent section is valid.

## Constraints
- README changes only — no Python source changes.
- Minimal diff: no reformatting of surrounding text.

## How we'll know it's done
- Issue #1 closed with explanatory comment.
- Issue #3 closed after README changes land.
- Both README files render correctly in Markdown.

## What's not included
- No changes to SKILL.md.
- No code changes.
