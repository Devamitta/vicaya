# Plan — Research Hub

## Architecture decisions

1. **Hub = Claude Code** with a custom `/vicaya` skill at `~/.claude/skills/vicaya/`.
2. **Vault I/O = official Obsidian CLI v1.12.7** (subcommands, `vault=Obsidian` targeting).
   YAML-safe via `obsidian property:set`. Folder creation via `mkdir` on disk + `reload`.
3. **Canon search = direct SQL** on `tipitaka-translation-data.db` (one table per CST book).
   Federated search via UNION over relevant tables. Citation = `<book_code>:<paranum>`.
4. **Library search = `calibredb`** — `list --search` for metadata always; `fts_search` once
   the index is built. Skill must check FTS availability and degrade gracefully.
5. **Web = `WebSearch` / `WebFetch`** (already in Claude Code).
6. **Cross-check = `gemini` CLI** subprocess. Timeout 120 s. No crash on failure.
7. **Citations are dual-layer** for canon: machine ref (`s0101m_mul:23`) + human ref
   (`MN 1 Mūlapariyāyasutta §3`). Resolver dispatches by book-code prefix to the right
   piṭaka helper in `dpd-db/tools/cst_source_sutta_example.py`.
8. **Source helpers live in `vicaya/tools/research_sources.py`** — reusable, testable,
   not buried inside a skill prompt.
9. **No vector RAG, no Open Notebook.** User already has structured local corpora —
   precise SQL + Calibre + vault search beats fuzzy embeddings for this use case.
10. **Output path = `<vault>/Research/YYYY-MM-DD - <slug>.md`**. One note per question.

## Phase 1 — Setup & sanity ✅ (mostly done)

- [x] Confirm `obsidian version` ≥ 1.12.4 → got 1.12.7.
- [x] Confirm `calibredb --version`, `gemini --version`, `sqlite3` all present.
- [x] Confirm canon db query: `s0101m_mul WHERE pali_text LIKE '%dukkha%'` returns rows
      with both `pali_text` and `english_translation`.
- [x] Create `Research/` folder on disk in vault, reload Obsidian, verify it sees it.
- [ ] Run `calibredb fts_index enable --wait-until-complete` (user's task, in background).
      → verify: `calibredb fts_search "test"` returns rows.
- [ ] Capture full Calibre tag vocabulary into `vicaya/data/calibre_tags.csv` so the
      skill prompt knows what to scope to.
      → verify: file exists, contains ≥1000 tag rows.

## Phase 2 — Source helpers (`vicaya/tools/research_sources.py`)

Every helper returns plain Python data (lists of dicts). No printing. Pure functions where
possible. Subprocess wrappers raise on tool-missing, return `[]` on no-results.

- [ ] **`search_vault(query, vault="Obsidian", folder=None, limit=20)`** — wraps
      `obsidian vault=<v> search:context query=<q> format=json [path=<folder>]`.
      Returns `[{path, snippet, line}]`.
      → verify: `search_vault("dukkha")` returns ≥1 result if vault has notes mentioning it.
- [ ] **`search_canon(query, books=None, lang="pali", limit=20)`** — federated SQL search.
      `books=None` defaults to suttas (`s*`). `lang` ∈ {`pali`, `english`, `chinese`, `any`}.
      Returns `[{book_code, paranum, pali, english, chinese}]`.
      → verify: `search_canon("dukkha", books=["s0101m_mul"])` returns the MN1 hits.
- [ ] **`resolve_citation(book_code, paranum)`** — dispatches by prefix:
      `vin*` → vinaya, `s0[1-4]*` → dn/mn/sn/an (need finer mapping), `abh*` → abhidhamma,
      `e*` → khuddaka / extras. Returns `{machine, human, sutta_name, paranum}`.
      Falls back to `{machine, human: machine}` when the dispatcher can't resolve.
      → verify: returns human-readable ref for at least the major sutta cases.
- [ ] **`search_calibre(query, tags=None, library=<path>, limit=20)`** — two-mode:
      if FTS available, `calibredb fts_search` with `--restrict-to search:tags:<t>`;
      else `calibredb list --search '<query>' --for-machine`. Returns
      `[{book_id, title, authors, tags, location, snippet}]`.
      → verify: tag-scoped search returns books matching that tag.
- [ ] **`gemini_cross_check(prompt, model=None, timeout=120)`** — subprocess `gemini -p <p>`.
      Returns the text response or empty string on timeout/failure.
      → verify: trivial prompt returns non-empty text.
- [ ] **`tests/test_research_sources.py`** — pytest covering all five helpers.
      → verify: `uv run pytest vicaya/tests/` passes.

## Phase 3 — The `/vicaya` skill

- [ ] Scaffold `~/.claude/skills/vicaya/SKILL.md` orchestrating the seven-phase flow.
      The skill prompt:
      - Calls `search_vault` first, summarises top 3–5 hits as "prior context".
      - Infers canon scope from question phrasing ("suttas" → `s*`, etc).
      - Calls `search_canon`, then `resolve_citation` per hit, accumulates evidence.
      - Calls `search_calibre` with inferred tags.
      - Calls `WebSearch` for ≥3 distinct sources.
      - Drafts synthesis with inline citations.
      - Calls `gemini_cross_check` with the synthesis; captures disagreements.
      - Renders the final markdown note from a template.
      - Creates it via `obsidian vault=Obsidian create path="Research/..." content=...`
        followed by `obsidian property:set` calls for frontmatter values.
      → verify: `/vicaya` is listed and invokable.
- [ ] **Note template** with frontmatter (`date`, `topic`, `canon_refs`, `library_refs`,
      `web_refs`, `tags: [research, pali]`) and sections:
      `## Question` / `## Findings` / `## Canon Evidence` / `## Library Evidence` /
      `## Web Evidence` / `## Gemini Cross-Check` / `## Open Threads` / `## Sources`.
      → verify: dry run produces a note that opens cleanly in Obsidian, frontmatter parses.
- [ ] **Citation formats**:
      - Canon: `**MN 1 Mūlapariyāyasutta §3** (s0101m_mul:23) — "<pali>" / "<english>"`
      - Calibre: `[[<Title>]] — <Author>, loc.<N>: "<excerpt>"`
      - Web: `[<title>](<url>) — retrieved YYYY-MM-DD`
      - Vault: `[[<Note Title>]]`
      → verify: every claim in the output has a citation in one of these forms.
- [ ] **`~/.claude/skills/vicaya/README.md`** — usage, args, output location, extension.
      → verify: a fresh agent reading only the README can run the skill correctly.

## Phase 4 — Dogfood & tune

- [ ] Run `/vicaya` on a real Pāḷi question. Read result in Obsidian.
      → verify: you'd actually keep this note.
- [ ] Tune SKILL.md (citation style, scope inference, frontmatter) based on that run.
      → verify: second real run reads better than the first.

## Open follow-ups (post-thread)

- Vault plugin or shell handler for `obsidian://canon?book=...&para=...` deep links.
- `--rag` flag if/when a curated PDF corpus needs to live outside Calibre.
- Cron / scheduled background runs once the sync flow proves out.
