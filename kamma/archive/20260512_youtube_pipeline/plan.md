# Plan — YouTube source pipeline

## Architecture Decisions

- **Two tools, two jobs.** `yt-dlp` for search (`ytsearchN:`), `youtube-transcript-api`
  for transcript fetch. `yt-dlp 2024.04.09` fails on caption fetch with current
  YouTube; `youtube-transcript-api` works first try. Search probe still works in
  the older `yt-dlp` so we keep it for that.
- **Cache transcripts unconditionally.** Every fetch writes to
  `data/youtube_cache/<video_id>.json`. Subsequent calls read from cache. This is
  how the corpus gets richer over time — without an explicit ingest pipeline.
- **Channel allowlist as plain Markdown.** `data/youtube_channels.md` is the
  source of truth, human-readable, easy to prune by hand. Helper parses it on
  load. No DB, no JSON config.
- **Default tier is probationary, never excluded.** Per user instruction: do
  not exclude up-front. Exclusion requires concrete noise evidence noted in a
  run reflection. New channels surfaced by a search are added at probationary
  automatically the first time they appear.
- **Citations distinguish caption type.** `(human captions)` vs `(auto-captions;
  paraphrase)` annotates every YouTube citation. Pāḷi quoted verbatim only from
  human-uploaded captions; auto-captions → paraphrase + timestamp link.
- **No project-internal package.** Keep `tools/research_sources.py` flat; the
  CLI subcommand pattern is the integration point. Two new dataclasses
  (`YouTubeHit`, `YouTubeTranscript`) added next to the existing four.
- **Existing helpers untouched.** Scope strictly to YouTube + SKILL.md
  sections that change. No drive-by refactors.

## Phase 1 — Helpers + CLI

- [x] 1.1 Add `youtube-transcript-api` as a project dependency
  → verify: `grep "youtube-transcript-api" pyproject.toml` shows the entry
- [x] 1.2 Add `YouTubeHit` and `YouTubeTranscript` dataclasses to
      `tools/research_sources.py`
  → verify: `uv run python -c "from tools.research_sources import YouTubeHit, YouTubeTranscript; print('ok')"`
      prints `ok`
- [x] 1.3 Implement `search_youtube(query, channels=None, limit=20)` using
      `yt-dlp --flat-playlist --print "..."  "ytsearch<N>:<query>"`; parse the
      pipe-delimited stdout into `YouTubeHit` records
  → verify: `uv run python -c "from tools.research_sources import search_youtube; r=search_youtube('apannaka sutta MN 60', limit=5); print(len(r), r[0].channel, r[0].title[:60])"`
      prints 5 and a real channel + title
- [x] 1.4 Implement `fetch_youtube_transcript(video_id, cache_dir=...)` using
      `youtube-transcript-api`; cache to `data/youtube_cache/<video_id>.json`;
      on cache-hit, read from disk and skip the network call
  → verify: fetch transcript for `R0vhivplJuM` once → file appears under
      `data/youtube_cache/`; second call returns same data without a network
      delay (test by deleting `tools/research_sources.py` import cache and
      timing both calls — second should be <0.5s)
- [x] 1.5 Add CLI subcommands `search-youtube` and `fetch-transcript` to the
      argparse block at the bottom of `tools/research_sources.py`. Match the
      existing JSON-to-stdout pattern.
  → verify: `uv run tools/research_sources.py search-youtube "apannaka sutta MN 60" --limit 3 | jq '.[0].channel'`
      prints a non-empty channel string
- [x] 1.6 Phase verification: full smoke test
  → verify: `uv run tools/research_sources.py search-youtube "apannaka sutta MN 60" --limit 5`
      AND `uv run tools/research_sources.py fetch-transcript R0vhivplJuM | jq '.segments | length'`
      both succeed and the second returns a number > 100

## Phase 2 — Channel allowlist

- [x] 2.1 Create `data/youtube_channels.md` with three sections (`## trusted`,
      `## probationary`, `## excluded`), a documented format header, and an
      initial seed from the three probe runs:
      probationary list to include — `Buddhist Insights @ Empty Cloud`,
      `Clear Mountain Monastery Project`, `Candana Bhikkhu`,
      `Bhikkhu Dhammānanda`, `Dharma robe`, `Wisdom Park`,
      `Theravada Buddhism Learning`, `Culture Exchange Blog`, `Buddha Tube`.
      Trusted and excluded sections start empty (per user instruction).
  → verify: `wc -l data/youtube_channels.md` ≥ 25; file parses with `grep -c "^- "` ≥ 9
- [x] 2.2 Implement `load_channel_allowlist(path=DEFAULT_CHANNELS_FILE)` →
      returns a dict `{"trusted": [...], "probationary": [...], "excluded": [...]}`.
      Each channel entry can be `display name` alone OR `display name | UCxxxx...`.
  → verify: `uv run python -c "from tools.research_sources import load_channel_allowlist; a=load_channel_allowlist(); print(sorted(a.keys()), len(a['probationary']))"`
      prints all three keys and `len(probationary) >= 9`
- [x] 2.3 Wire the allowlist into `search_youtube`: if a channel matches a name
      or ID in `excluded`, drop it from results. `probationary` and `trusted`
      both pass through (with a `tier` field on `YouTubeHit` so the agent can
      see at a glance). Default behavior: load the allowlist if no `channels`
      arg passed.
  → verify: add `Test Channel` under excluded, run a search, confirm any
      result from that channel is absent; remove `Test Channel` after.
- [x] 2.4 Phase verification:
  → verify: `uv run tools/research_sources.py search-youtube "paticcasamuppada dependent origination" --limit 10 | jq '[.[] | .tier] | unique'`
      shows at least one `"probationary"` entry and zero results from any
      excluded channel.

## Phase 3 — SKILL.md integration

- [x] 3.1 Split SKILL.md Phase 4 into `### Phase 4a — Web search` (existing
      content) and `### Phase 4b — YouTube search`.
  → verify: `grep -c "Phase 4" skill/vicaya/SKILL.md` ≥ 2; both subsections
      present
- [x] 3.2 Phase 4b body: query construction rule (English + Pāḷi sutta name +
      numeric reference); CLI invocation examples for `search-youtube` and
      `fetch-transcript`; pointer to the channel allowlist file.
  → verify: section contains the strings `search-youtube`, `fetch-transcript`,
      and `data/youtube_channels.md`
- [x] 3.3 Add a Hard Rule (rule #7 or appended): "Auto-captions mishear Pāḷi.
      Never quote Pāḷi verbatim from auto-captions; paraphrase and link to the
      timestamp. Human-uploaded captions may be quoted with normal care."
  → verify: SKILL.md "Hard rules" section contains the phrase "Auto-captions
      mishear Pāḷi"
- [x] 3.4 Add `YouTubeHit` and `YouTubeTranscript` to the "Helper return
      shapes" section.
  → verify: `grep -A1 "YouTubeHit" skill/vicaya/SKILL.md` shows the field
      list including `tier`
- [x] 3.5 Update the note template (Phase 7) with a `## YouTube Evidence`
      section showing the citation form
      `[Channel — Title](https://youtu.be/<id>?t=<sec>) — fetched YYYY-MM-DD
      (auto-captions; paraphrase | human captions)`.
  → verify: `grep -c "YouTube Evidence" skill/vicaya/SKILL.md` ≥ 1
- [x] 3.6 Update the run-reflection template (self-improvement loop) to add a
      `## Channel tuning` section: which channels surfaced new evidence
      (→ promote to trusted), which surfaced noise (→ demote to excluded).
      Empty bullets allowed.
  → verify: `grep -c "Channel tuning" skill/vicaya/SKILL.md` ≥ 1
- [x] 3.7 Phase verification:
  → verify: SKILL.md still references no `python -c` heredocs for YouTube;
      `grep -n "python -c" skill/vicaya/SKILL.md` returns 0 lines

## Phase 4 — Tests

- [x] 4.1 Add a test asserting `load_channel_allowlist` returns three tier
      lists and the seeded probationary entries appear.
  → verify: `uv run pytest tests/ -k "channel_allowlist" -q` passes
- [x] 4.2 Add a test for `search_youtube` parsing that mocks
      `subprocess.run` with a fixed stdout fixture and asserts the records
      parse into `YouTubeHit` correctly (3+ rows, expected fields).
  → verify: `uv run pytest tests/ -k "search_youtube" -q` passes
- [x] 4.3 Add a test for the cache behaviour of `fetch_youtube_transcript`:
      pre-seed a cache file, call the function, assert it returned the cached
      data WITHOUT calling out to the network (mock the API class).
  → verify: `uv run pytest tests/ -k "transcript_cache" -q` passes
- [x] 4.4 Phase verification:
  → verify: `uv run pytest -q` shows all tests pass (existing 14 + 3 new = 17)

## Phase 5 — End-to-end probe and corpus seed

- [x] 5.1 Run a real `search-youtube` on `paticcasamuppada dependent
      origination` (limit 10). Inspect channels; promote 1–3 channels with
      obviously good content (e.g. anything from Empty Cloud / Clear Mountain
      / Bhikkhu Bodhi reposted) from probationary to trusted in
      `data/youtube_channels.md`.
  → verify: `data/youtube_channels.md` `## trusted` section now has ≥1 entry
- [x] 5.2 Run `fetch-transcript` on at least one Bhante Suddhāso or Clear
      Mountain video from the search.
  → verify: `ls data/youtube_cache/*.json` shows ≥1 cached transcript;
      `jq '.segments | length' data/youtube_cache/*.json | head -1` > 100
- [x] 5.3 Write a short note to `kamma/threads/20260512_youtube_pipeline/probe_notes.md`
      summarising: queries used, hit counts, channels promoted, gotchas.
      This becomes the first piece of corpus-tuning evidence and demonstrates
      the workflow the reflection template will produce on every future run.
  → verify: file exists and is ≥ 15 lines
- [x] 5.4 Phase verification:
  → verify: at least 1 trusted channel, at least 1 cached transcript, probe
      notes file present.
