## Architecture Decisions
- Take issue #3's suggested text almost verbatim — the reporter wrote it for
  this README; no need to paraphrase.
- `### Calibre full-text search` and `### Obsidian CLI` go after the Setup
  numbered steps, before the first `---` separator — keeps the human-reader
  setup flow intact.
- "Runtime requirements" block goes after the step 0 code block in the
  Autonomous agent setup section, with the full table + agent instructions.
- The phrase "FT button steps above" in the agent section is valid because
  the Calibre FTS section appears earlier in the same document.

## Phase 1 — Close issue #1

- [ ] Post comment to issue #1 explaining the fix was in PR #6 / commit 1f593ea
  → verify: `gh issue view 1` shows a new comment
- [ ] Close issue #1
  → verify: `gh issue view 1` shows state: CLOSED

## Phase 2 — README.md improvements

- [ ] Add `### Calibre full-text search` subsection after Setup steps, before `---`:
      FT button steps, when-GUI-is-needed table, platform PATH notes
  → verify: `grep -n "FT button" README.md` returns a match

- [ ] Add `### Obsidian CLI` subsection immediately after:
      install path, desktop-app requirement, per-platform start commands, `obsidian version`
  → verify: `grep -n "obsidian version" README.md` returns a match in the new section

- [ ] Add full "Runtime requirements" block after step 0 in Autonomous agent setup:
      table + agent instructions ("walk them through the FT button steps above...")
  → verify: `grep -n "Runtime requirements" README.md` and `grep -n "walk them through" README.md`

## Phase 3 — skill/vicaya/README.md

- [ ] Expand "Calibre FTS takes a long time" bullet with FT button instructions
  → verify: `grep -n "FT button" skill/vicaya/README.md` returns a match

## Phase 4 — Close issue #3

- [ ] Post summary comment and close issue #3
  → verify: `gh issue view 3` shows state: CLOSED
