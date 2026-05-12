# Plan — SKILL.md improvements

## Architecture Decisions
- `kamma/runs/` as a flat permanent directory alongside `threads/` and `archive/`
- Perspective mapping added as a named step inside Phase 1, not a new phase
  (keeps the seven-phase count stable)
- Recursive citation discovery added as a boxed instruction inside Phase 5

## Phase 1 — Fix structural corruption in SKILL.md

- [x] 1.1 Move hard rules 9 & 10 from Phase 4b into the Hard Rules section
  → verify: rules 1–10 appear in sequence under Hard Rules; Phase 4b has no numbered list items

- [x] 1.2 Restore Phase 4b prose — remove dangling `## Inputs` header,
  close the orphaned code fence, ensure the `search-youtube` command
  appears correctly inside Phase 4b
  → verify: Phase 4b reads as continuous prose ending with the fetch-transcript command

## Phase 2 — Fix run reflection path

- [x] 2.1 Create `kamma/runs/` and move 4 existing reflection files there
  → verify: `ls kamma/runs/` shows 4 .md files

- [x] 2.2 Delete `kamma/threads/20260511_research_hub/` (now empty)
  → verify: directory no longer exists

- [x] 2.3 Update SKILL.md reflection write path to `kamma/runs/<UTC-timestamp>.md`
  → verify: grep for `20260511_research_hub` in SKILL.md returns 0 lines

## Phase 3 — Perspective mapping

- [x] 3.1 Add perspective-mapping step at end of Phase 1
  → verify: Phase 1 ends with the perspective-mapping instruction

## Phase 4 — Recursive citation discovery

- [x] 4.1 Add recursive-search instruction in Phase 5
  → verify: Phase 5 contains the instruction

## Phase 5 — Paragraph numbering guidance

- [x] 5.1 Add paragraph-numbering warning in Phase 2
  → verify: Phase 2 contains the warning

## Phase 6 — Final verification

- [x] 6.1 `uv run pytest tests/ -q` → 0 failures
