# /vicaya

Multi-source research skill for Pāḷi / Buddhist topics. Pulls from your local
Obsidian vault, the CST canon, your Calibre library, YouTube, and the open web;
cross-checks the synthesis with a second model; and writes one structured note
into your Obsidian vault.

## Usage

```
/vicaya <your question>
```

Examples:
```
/vicaya what does the Buddha mean by "the dart" in MN 105?
/vicaya is upādāna in the suttas always grasping or sometimes appropriation?
/vicaya compare the abhidhamma definition of cetanā with modern psychology
```

You can also pass seed references:

```
/vicaya how do the commentaries treat MN 1?
   See [[Mūlapariyāyasutta notes]] and SC's translation by Bodhi.
```

## Output

A single Markdown note in your Obsidian vault under `Vicaya/`:

```
Vicaya/YYYY-MM-DD - <slug>.md
```

Frontmatter is structured for Obsidian dataview queries. Citations are inline;
sources appear in dedicated sections (Canon / Library / Web / YouTube).

## How it works

Seven phases (see `SKILL.md`):

1. **Vault context** — `obsidian search:context` for related prior notes.
2. **Canon** — SQLite query over `tipitaka-translation-data.db` (CST + translations).
3. **Library** — `calibredb` search (metadata always; FTS once indexed).
4. **Web + YouTube** — `WebSearch` / `WebFetch`, plus YouTube search and
   transcript fetch over a curated channel allowlist.
5. **Synthesis** — Claude drafts findings with inline citations.
6. **Cross-check** — independent second-opinion pass.
7. **Write** — `obsidian create` saves the final note into `Vicaya/`.

## Dependencies

| Tool | Required | Status check |
|------|----------|--------------|
| `obsidian` CLI v1.12.4+ | yes | `obsidian version` |
| `calibredb` (Calibre 9+) | optional (library search) | `calibredb --version` |
| `sqlite3` | yes | `sqlite3 --version` |
| `yt-dlp` | yes (YouTube search) | `yt-dlp --version` |
| `gemini` CLI | optional (cross-check) | `gemini --version` |
| `uv` | yes (to run helpers) | `uv --version` |

## Configuration

All user-specific paths live in `.env` at the repo root. Copy `.env.example` to
`.env` and edit. See `SKILL.md` for the full schema.

## Known limitations

- **Calibre FTS** takes a long time to index a large library. Until ready,
  Calibre search is metadata-only. The skill degrades gracefully.
- **Citation human-refs** for canon are currently piṭaka/nikāya/paranum level
  (e.g. `MN 02 §23`). Full sutta-name resolution is a follow-up.
- **YouTube auto-captions** mishear Pāḷi terms. The skill paraphrases auto-
  caption material and links to the timestamp rather than quoting verbatim.

## Source layout

```
vicaya/
├── tools/research_sources.py    # source helpers (importable + CLI)
├── tests/                       # pytest suite
├── data/
│   ├── calibre_tags.csv         # tag vocabulary
│   ├── youtube_channels.md      # channel allowlist (trusted / probationary / excluded)
│   └── youtube_cache/           # cached transcripts (gitignored)
├── skill/vicaya/              # this skill
└── kamma/                       # design history
```
