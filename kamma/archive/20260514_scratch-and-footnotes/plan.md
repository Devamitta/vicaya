# Plan — Research scratchpad + inline footnotes

## Architecture Decisions
- Scratch file at `/tmp/vicaya_<YYYYMMDD>_<slug>.md` — flat markdown,
  not JSON. Agents can read and grep markdown more reliably than parse JSON.
- Named footnote IDs over numeric — self-documenting and Obsidian-safe.
- Definitions at end of note (after final `---`) — standard markdown
  convention; doesn't disrupt reading flow.
- One new section in SKILL.md ("Research scratchpad"), one line per phase
  ("→ Scratch"), one instruction per phase-start ("read scratch"). Minimal
  surface area, maximum effect.

## Phase 1 — Add research scratchpad mechanism

- [x] Add `## Research scratchpad` section to SKILL.md, placed after
  `## Setup` and before `## The seven phases`
  → verify: section appears in file, contains slug/path instruction and
    "append after each phase" rule

- [x] Add `→ **Scratch** — append phase results` one-liner at the end of
  Phase 1, Phase 2, Phase 3, Phase 4a, and Phase 4b blocks
  → verify: each phase section ends with the append line

- [x] Add "Before drafting, read the scratch file" instruction at the start
  of Phase 5 (before "Draft the answer in your working notes")
  → verify: instruction appears at Phase 5 opening

- [x] Add "Delete the scratch file" instruction in Phase 7, after the
  `obsidian vault=Obsidian create` block
  → verify: instruction appears in Phase 7

## Phase 2 — Add inline footnote format

- [x] Add footnote ID conventions and inline usage rule to the
  "Citation forms" block in Phase 5
  → verify: three ID forms (canon, calibre, web) appear with examples

- [x] Add footnote definition format rules and worked example to the
  Phase 7 note template (after the existing `## Related Notes` block)
  → verify: `## Footnotes` section with example definitions appears in template

- [x] Add a "Footnote definitions" rule block to the Style notes section
  (after the Pāḷi/English presentation rules)
  → verify: rule block appears in Style notes, references the
    "short locator, not evidence repeat" constraint
