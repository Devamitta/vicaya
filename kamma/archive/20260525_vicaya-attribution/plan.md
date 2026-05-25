## Architecture Decisions
- `tool` field uses a bare URL string; Obsidian renders URL-type properties as
  clickable links without markdown syntax in YAML.
- `tool` is ordered before `agent` — framework attribution precedes model identity.
- Rule F6 sits immediately after Rule F5 so both self-identification rules are
  co-located.
- Four edit locations in SKILL.md only; no other files.

## Phase 1 — Update SKILL.md

- [x] 1.1 Add `tool` field (before `agent`) to frontmatter template
  → verify: `tool:` appears before `agent:` in template block ✓

- [x] 1.2 Update footer line in note template
  → verify: footer contains `[Vicaya]` link and `HH:MM` ✓

- [x] 1.3 Update footer example in Rule F5 description
  → verify: Rule F5 inline example matches new footer format ✓

- [x] 1.4 Add Rule F6 after Rule F5
  → verify: Rule F6 block exists with correct URL ✓

- [x] 1.5 Update correct frontmatter example block
  → verify: example contains `tool:` before `agent:` ✓

## Phase 1 verification
All five edit locations confirmed via `git diff` and `grep`. Consistent across
template, reference example, and rule documentation.
