# Tech — Vicaya

## Tools & Platforms
- **Runtime:** Python 3.13+, managed with `uv`
- **Agent integration:** Claude Code skill (Markdown skill file at `skill/vicaya/SKILL.md`),
  symlinked to `~/.claude/skills/vicaya/`
- **Canon search:** SQLite (`tipitaka-translation-data.db`) via stdlib `sqlite3`
- **Vault I/O:** Obsidian CLI v1.12.7+ (subcommand-style; requires desktop app running)
- **Library search:** `calibredb` (Calibre 9+); metadata search always, FTS when indexed
- **YouTube:** `yt-dlp` for search, `youtube-transcript-api` for transcript fetch
- **Web:** `WebSearch` / `WebFetch` (Claude Code built-ins)
- **Cross-check:** `cross_check()` POSTs to OpenRouter (model list in `data/openrouter_models.json` — server-side fallback via the `models: [...]` field, cap 3). Current lead: `deepseek/deepseek-v4-flash` (paid, ~22s, ~$0.0001/call); free `gpt-oss-120b:free` as outage backup. On any failure returns a `# SELF_REVIEW:` sentinel so the calling agent runs the Phase 6 checklist on its own synthesis. Stdlib `urllib`; no SDK dep. Key from `OPENROUTER_API_KEY` env / `.env`, or `~/.local/share/opencode/auth.json` → `.openrouter.key`.
- **Sanskrit search:** `grep -rn -F --include="*.htm"` across a local GRETIL corpus (shallow clone of `wujastyk/GRETIL-mirror`). Unicode IAST `.htm` files; no new dependencies.
- **Tests:** pytest

## Constraints
- All paths are per-machine; configured via `.env` (not committed). See `.env.example`.
- Obsidian CLI requires the desktop app to be open; skill launches it automatically.
- Calibre FTS indexing is a background process that takes days on a large library.
- `yt-dlp` 2024.04.09 cannot fetch captions; `youtube-transcript-api` is used instead.
- No vector RAG. Local corpora are structured enough that SQL + tag search + vault search
  is more precise than embeddings.

## Resources
- Canon DB: `<dpd-db>/resources/tipitaka_translation_db/tipitaka-translation-data.db`
- DPD DB: `<dpd-db>/dpd.db` — used by `resolve_citation` to map CST codes → human refs via `sutta_info` table
- CST book translator: `<dpd-db>/tools/cst_book_translator.py` + `.tsv` — used by `lookup_book` to translate between cst_filename / SQLite table name / Pāḷi title / gui code / DPD code. Live-imported via file path.
- Vault: path in `$VICAYA_VAULT_PATH`, vault name `$VICAYA_VAULT_NAME`
- Calibre library: path in `$VICAYA_CALIBRE_LIBRARY`
- YouTube cache: `data/youtube_cache/` (gitignored, grows over time)
- Channel allowlist: `data/youtube_channels.md`

## Output shape
A single `.md` file per research session written into `<vault>/Vicaya/`.
Source helpers return plain Python lists-of-dicts; no external I/O inside helpers.
