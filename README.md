# Vicaya

A research tool for Pāḷi and Buddhist topics.

You ask a question. The tool searches your Obsidian vault, the Pāḷi canon
(suttas, Vinaya, Abhidhamma, commentaries, sub-commentaries), your Calibre
library, YouTube talks, and the open web. It drafts an answer with full
citations, has a second model review the draft, and saves a single Markdown
note into your vault under `Research/`. Notes link back to existing notes
on related topics, so the vault accumulates as a connected body of work.

The skill is invoked as `/vicaya <your question>` inside Claude Code (or any
agent that reads a Markdown skill file).

## Sources

Each source is optional — if the tool or path isn't configured it is silently skipped.

| Source | What it searches |
|---|---|
| **Obsidian vault** | Your existing research notes |
| **Pāḷi canon** | Local SQLite DB — CST text, translations, commentaries |
| **Calibre library** | Your book collection; metadata always, full-text when indexed |
| **YouTube** | Dhamma talks and sutta studies via a curated channel allowlist |
| **Web** | General search and page fetch |
| **Gemini cross-check** | Second model reviews the draft before the note is written |

## Setup

1. `cp .env.example .env` and edit the paths to match your vault, library,
   and canon database.
2. Install whichever of these you want to use: `obsidian` CLI, `calibredb`
   (Calibre 9+), `yt-dlp`, `sqlite3`, `gemini` CLI.
3. `uv sync` to install Python dependencies.
4. Symlink the skill folder into your agent's skills directory:

   ```bash
   ln -s "$(pwd)/skill/vicaya" ~/.claude/skills/vicaya
   ```

5. Run `/vicaya <a question>` in Claude Code.

Full setup notes are in [`skill/vicaya/SKILL.md`](skill/vicaya/SKILL.md).

---

## Autonomous agent setup

> These instructions are written for AI agents (Claude Code, GitHub Copilot,
> etc.) that need to set up this project without human intervention. Read this
> section in full before running any commands. Every step includes a
> verification check — do not proceed past a failed check without telling the
> user.

### 0 — Prerequisites check

Run the following and note what is missing:

```bash
which uv          # Python package manager — required
which obsidian    # Obsidian CLI — optional (vault search)
which calibredb   # Calibre — optional (library search)
which yt-dlp      # yt-dlp — optional (YouTube search)
which gemini      # Gemini CLI — optional (cross-check model)
python3 --version # system Python — only needed if uv is absent
```

`uv` is the only hard requirement. Install it if missing:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install optional CLI tools only if the user wants those sources. Skip any
tool the user does not need — the skill degrades gracefully.

```bash
# yt-dlp (YouTube search + transcript)
pip install -U yt-dlp          # or: uv tool install yt-dlp

# Calibre CLI — install Calibre from https://calibre-ebook.com/download
# then calibredb is available in PATH automatically.

# Gemini CLI — requires Google AI Studio API key
npm install -g @google/gemini-cli   # or follow https://github.com/google-gemini/gemini-cli
```

The `obsidian` CLI is bundled with the Obsidian desktop app on some platforms.
Check `which obsidian`; if missing, the vault search source is disabled.

### 1 — Python environment

```bash
uv sync
```

Verify:

```bash
uv run python -c "import youtube_transcript_api; print('ok')"
```

### 2 — Discover local paths

The `.env` file maps four paths to the user's local data. Discover them
automatically before writing:

```bash
# Obsidian vault — find the vault directory (contains .obsidian/)
find ~ -maxdepth 4 -name ".obsidian" -type d 2>/dev/null | head -5

# Calibre library — contains metadata.db
find ~ -maxdepth 5 -name "metadata.db" 2>/dev/null | grep -i calibre | head -5

# Canon DB — tipitaka-translation-data.db (from dpd-db project)
find ~ -maxdepth 8 -name "tipitaka-translation-data.db" 2>/dev/null | head -3

# DPD DB — dpd.db (from dpd-db project)
find ~ -maxdepth 8 -name "dpd.db" 2>/dev/null | head -3
```

If any path is not found, leave that variable blank in `.env` — the
corresponding source will be silently skipped.

### 3 — Write .env

Copy the template and fill in the discovered paths:

```bash
cp .env.example .env
```

Edit `.env` with the values found in step 2. Use `~` for the home directory.
Example layout (adjust to actual paths):

```
VICAYA_VAULT_NAME=Obsidian
VICAYA_VAULT_PATH=~/Obsidian
VICAYA_CALIBRE_LIBRARY=~/Calibre Library
VICAYA_CANON_DB=~/path/to/dpd-db/resources/tipitaka_translation_db/tipitaka-translation-data.db
VICAYA_DPD_DB=~/path/to/dpd-db/dpd.db
```

Verify the file was written and does not contain placeholder text:

```bash
cat .env
```

`.env` is gitignored and will never be committed.

### 4 — Run the test suite

```bash
uv run pytest tests/ -q
```

Expected: all tests pass or are skipped (skipped = optional tool not
installed, which is fine). Zero failures.

If DPD-backed citation tests are skipped because `VICAYA_DPD_DB` is blank
but you did find a `dpd.db` in step 2, go back and fill in that path.

### 5 — Symlink the skill

For Claude Code:

```bash
mkdir -p ~/.claude/skills
ln -sf "$(pwd)/skill/vicaya" ~/.claude/skills/vicaya
```

Verify the symlink resolves:

```bash
ls ~/.claude/skills/vicaya/SKILL.md
```

For other agents that read skill files from a different directory, symlink
`skill/vicaya/` into the appropriate location.

### 6 — Final verification

```bash
# Resolve a known citation (requires VICAYA_DPD_DB to be set)
uv run tools/research_sources.py resolve-citation s0202m_mul 97
# Expected: { "human": "MN60 Apaṇṇakasuttaṃ para 97", ... }

# Search canon (requires VICAYA_CANON_DB to be set)
uv run tools/research_sources.py search-canon "dukkha" --limit 3
# Expected: list of CanonHit objects
```

Setup is complete when both return results without errors. The skill is
ready to use: `/vicaya <your question>` in Claude Code.

## Layout

```
vicaya/
├── tools/research_sources.py   # source helpers + CLI subcommands
├── tests/                       # pytest suite
├── data/
│   ├── calibre_tags.csv         # tag vocabulary
│   ├── youtube_channels.md      # YouTube channel allowlist
│   └── youtube_cache/           # cached transcripts (gitignored)
├── skill/vicaya/                # the skill prompt
└── kamma/                       # design history
```
