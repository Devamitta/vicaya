# Spec — SKILL.md improvements (trio + structural fixes)

## Overview
Four improvements to skill/vicaya/SKILL.md, plus fixing two structural
corruptions introduced by recent in-run edits, and relocating run reflection
files from a defunct thread path to a permanent home.

## What it should do

1. **Fix structural corruption** — Hard rules 9 & 10 are currently stranded
   inside Phase 4b instead of the Hard Rules section. A dangling `## Inputs`
   header and orphaned code fragment break Phase 4b's prose flow.

2. **Relocate run reflections** — The reflection write path is hardcoded to
   `kamma/threads/20260511_research_hub/runs/` (an archived, defunct thread).
   Reflections should live at `kamma/runs/` permanently. Move the 4 existing
   files there and update the path in SKILL.md.

3. **Perspective mapping** — Before Phase 2 (canon search), the agent should
   explicitly name the competing schools of thought the question touches.
   This frames the entire search so evidence is gathered for all positions,
   not just the most prominent one.

4. **Recursive citation discovery** — During Phase 5 (synthesis), if a
   "load-bearing" source emerges that hasn't been searched yet, the agent
   should loop back to Phase 2/3 before finalising. Currently this is possible
   but not instructed.

5. **Paragraph numbering guidance** — CST book file paragraph numbers are
   continuous across all suttas in that file (e.g. para 261 in s0202m_mul is
   MN78, not MN60). Agents have gotten this wrong. SKILL.md should make
   this explicit in Phase 2.

## Assumptions & uncertainties
- All changes are to SKILL.md only — no code changes
- The 4 run reflection files in the defunct path are worth keeping
- `kamma/runs/` is the right permanent home (flat, not nested inside threads)

## Constraints
- Hard rules must stay numbered 1–N in sequence
- Phase numbering (1–7) must not change
- Run reflection template content is preserved exactly; only the path changes

## How we'll know it's done
- SKILL.md has no rules stranded outside the Hard Rules section
- `kamma/runs/` contains all 4 existing reflection files
- SKILL.md reflection path points to `kamma/runs/`
- Phase 4b reads cleanly with the YouTube command in the right place
- `uv run pytest tests/ -q` still passes
