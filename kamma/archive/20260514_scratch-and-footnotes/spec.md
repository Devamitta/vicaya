# Spec — Research scratchpad + inline footnotes

## Overview
Two independent improvements to `skill/vicaya/SKILL.md`:
1. **Research scratchpad** — write findings to disk after each phase so
   auto-compaction (which triggers at ~85% context) cannot erase evidence
   gathered so far. Any agent re-entering the run can read the file and
   continue from where the last phase left off.
2. **Inline footnotes** — add `[^named-ref]` superscripts in the Findings
   prose so the reader can hover over a claim and see enough to locate and
   quote the source without scrolling to the Evidence sections.
   Evidence sections are unchanged; footnote definitions are short
   (1–2 lines) — not a repeat of the full Pāḷi/English blocks.

## What it should do

### Scratchpad
- At the start of each run, create `/tmp/vicaya_<YYYYMMDD>_<slug>.md`.
- After each of Phases 1–4b, append a structured summary to that file:
  phase name, queries run, key hits (human refs and snippets), perspective
  map, any tool errors.
- At the start of Phase 5 (synthesis), explicitly read the scratch file to
  recover all findings before drafting. This is the compaction rescue step.
- After Phase 7 (vault note written), delete the scratch file.

### Inline footnotes
- In Phase 5 (synthesis), when writing the Findings prose, place a
  `[^named-ref]` superscript immediately after any claim that rests on a
  specific source.
- Footnote ID conventions:
  - Canon: `[^<book>-<para>]` e.g. `[^s0201-70]`
  - Library: `[^calibre-<id>]` e.g. `[^calibre-223]`
  - Web/YouTube: `[^web-<n>]` e.g. `[^web-1]`
- Footnote definition format (short — enough to open/quote the source):
  - Canon: `[^s0201-70]: MN9 Sammādiṭṭhisuttaṃ para 70 — db: s0201m_mul, para 70`
  - Library: `[^calibre-223]: [[On Meditation]] — Ajahn Chah (Calibre #223)`
  - Web: `[^web-1]: [Ānāpānasati Sutta](url) — retrieved 2026-05-14`
- Footnote definitions go at the bottom of the note, after the final
  horizontal rule.
- Evidence sections remain unchanged.

## Assumptions & uncertainties
- Obsidian renders standard markdown footnotes (`[^id]` / `[^id]: ...`)
  and shows hover previews in reading mode — verified behaviour.
- `/tmp/` is reliable for the session duration; the scratch file is
  ephemeral and can be re-created if lost.
- The compaction summary Claude Code generates should preserve the scratch
  file path; the re-entering agent just needs to know the path.

## Constraints
- SKILL.md only — no code changes.
- Phase numbering (1–7) and Hard Rule numbering unchanged.
- Evidence sections unchanged (keep-both decision confirmed).
- Footnote definitions must NOT repeat the full Pāḷi/English blockquote —
  that's in the Evidence section. Definitions are locators, not evidence.

## How we'll know it's done
- SKILL.md contains a "Research scratchpad" setup section before Phase 1.
- Each Phase 1–4b heading block ends with a "→ Scratch" append instruction.
- Phase 5 opens with an instruction to read the scratch file.
- Phase 7 ends with an instruction to delete the scratch file.
- Phase 5 Citation forms list includes the three footnote ID conventions.
- Phase 7 note template includes a `## Footnotes` section example.
- Style notes include footnote definition format rules.
- A worked example shows `[^s0201-70]` inline and the matching definition.

## What's not included
- No code changes (e.g. new helper subcommand).
- No changes to the Evidence section template.
- No resume/continue mechanism — the scratch file is a safety net for
  synthesis, not a full checkpoint-restart system.
