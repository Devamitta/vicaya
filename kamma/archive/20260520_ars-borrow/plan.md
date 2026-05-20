# Plan

## Architecture Decisions
- **No new skills, no new agents.** Vicaya's design constraint is a single
  portable SKILL.md; lifts become checklist sections, frontmatter rules, or
  hard rules — not agents.
- **Recommend, don't apply.** All items are presented for discussion. The
  user picks before any vicaya file is touched.
- **Order suggestions by expected impact**, not by source location in ARS.
  Top items should fix observable gaps in current vicaya runs; bottom items
  are nice-to-have polish.

## Phase 1 — Produce suggestions.md
- [ ] Draft `suggestions.md` with numbered items.
  → verify: file exists; each item has title + source + rationale +
  vicaya landing point + effort + verdict; verdicts span adopt/adapt/skip
  (not all "adopt").
- [ ] Present the list inline in chat for discussion.
  → verify: user has the list and can point to item numbers.

No vicaya edits in this thread. Future threads will apply selected items
one by one after discussion.
