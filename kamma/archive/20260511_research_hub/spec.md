# Spec — Research Hub

## Overview
A unified research workspace inside Claude Code (terminal) for Pāḷi / Buddhist research.
Ask a question, drop references, walk away. The system pulls from the user's local sources
in priority order, cross-checks with a second model, and writes a single structured note
into the Obsidian vault.

## What it should do

A `/vicaya <topic>` skill that orchestrates these phases:

1. **Vault context** — `obsidian search:context` over the existing Obsidian vault to surface
   related prior notes. New research must cross-link these, never duplicate them.
2. **Canon search** — direct SQL on `tipitaka-translation-data.db` (CST + translations).
   Returns paragraphs with Pali + English (and Chinese where present) plus citation data.
3. **Library search** — `calibredb` over the the Calibre library: tag-scoped metadata
   search always; FTS once the index is built. Returns book + author + location + snippet.
4. **Web search** — `WebSearch` + `WebFetch` for modern scholarship, SuttaCentral, etc.
5. **Synthesis** — Claude drafts findings with citations from steps 1–4.
6. **Cross-check** — pipe synthesis to `gemini` CLI; capture any disagreements.
7. **Write** — render the final note (frontmatter + sectioned markdown + wiki-links) and
   create it in `<vault>/Research/YYYY-MM-DD - <slug>.md` via `obsidian create`.

## Assumptions & uncertainties

- **Obsidian vault**: `$VAULT` (vault name `Obsidian`).
- **Output folder**: `Research/` inside the vault. Created on disk; Obsidian sees it.
- **Calibre library**: `$CALIBRE_LIBRARY`.
- **Calibre FTS**: not yet indexed. Skill must degrade gracefully to metadata-only search.
- **Canon DB**: `<dpd-db>/resources/tipitaka_translation_db/tipitaka-translation-data.db`.
  Schema: one table per CST book (e.g. `s0101m_mul` = MN Mūla, `vin01m_mul` = Pārājika Mūla),
  columns `id, rend, paranum, pali_text, myanmar_pali_text, chinese_translation,
  english_translation` (+ mark/timestamp columns). Translation columns may be empty.
- **Citation helpers**: `tools/cst_source_sutta_example.py` (piṭaka-aware extractors) and
  `extract_sutta_from_file` from `tools/cst_sc_text_sets.py` resolve human-readable sutta
  references. Both live in the `dpd-db` repo and must be importable from vicaya.
- **Gemini CLI**: `gemini` v0.40.1 on PATH.
- **Obsidian CLI**: v1.12.7. Subcommand-style (`obsidian search`, not `--search`). No daemon.
- **Default canon scope**: per question (user's preference) — the skill infers from the
  phrasing ("in the suttas" → `s*`, "in the suttas and commentaries" → `s*` + `*_att`).
- **Default Calibre scope**: whole library is non-fiction Buddhism / religion / psychology,
  so default scope = whole library; only narrow when the question is clearly narrower.

## Constraints

- All output is markdown — no proprietary formats.
- The vault is the single permanent home for output.
- Every claim has a citation (canon ref, vault wiki-link, calibre book+location, or URL).
- Canon citations carry both **machine ref** (`s0101m_mul:23`) and **human ref**
  (`MN 1 Mūlapariyāyasutta §3`).
- No automatic git commits, no automatic pushes.
- The skill is globally available (`~/.claude/skills/vicaya/`), not locked to dpd-db.
- Source helpers live in `vicaya/tools/` — new project, version-controlled separately.

## How we'll know it's done

- `/vicaya "<a real Pāḷi question>"` produces, in 10–30 min, a note in the vault with:
  - Valid YAML frontmatter (parses cleanly in Obsidian).
  - ≥1 canon citation with human + machine refs.
  - ≥1 library citation (book + author).
  - ≥1 web citation with retrieval date.
  - Wiki-links to relevant existing vault notes when they exist.
  - A non-empty Gemini Cross-Check section when models disagree.
- A second run on a related topic links back to the first via `[[wiki-link]]`.
- All four source helpers have passing pytest tests.

## What's not included (deferred)

- Open Notebook / Khoj / SurfSense RAG layer — superseded by direct canon SQL + Calibre.
- Audio summaries.
- Voice input, GUI, mobile.
- Cron / background scheduling — sync long-running session for now.
- A vault plugin to deep-link `obsidian://canon?book=...&para=...` from Research notes —
  nice-to-have, not v1.
- Migration to a dedicated research vault (user said maybe later; markdown is portable).
