# Spec — YouTube source pipeline for /vicaya

## Overview

Add YouTube — and specifically YouTube transcripts — as a first-class source for
the `/vicaya` skill, alongside the Obsidian vault, the CST canon SQLite, the
Calibre library, and web search. Build a pipeline that gets *richer over time*:
every run caches the transcripts it fetched, and maintains a channel allowlist
that is promoted / demoted by evidence rather than vibes.

## Why now

A probe across the three existing notes in `~/MyFiles/Obsidian/Research/`
(paṭiccasamuppāda, arahant-and-kamma, apaṇṇaka MN 60) showed:

- YouTube returns 20+ ranked results per topic when queried in English with
  Pāḷi sutta name + numeric reference as anchors.
- Serious channels (Bhante Suddhāso / Empty Cloud, Clear Mountain Monastery,
  Bhikkhu Dhammānanda, Candana Bhikkhu) recur across topics — a curated
  allowlist is high leverage.
- AI-narrated slop channels ("Buddha's Wisdom", "Buddhism Podcast", "Buddha
  Speaks") also recur — without filtering, search quality is degraded.
- Transcripts contain Pāḷi terms only as auto-caption mishears
  ("Suddhāso" → "saso", "Apaṇṇaka" → "apaka"); they are useful for **topic
  discovery and locating the right time-window** in a talk, but NOT for
  verbatim Pāḷi quotation.

## What it should do

1. Expose two new helpers and two new CLI subcommands:
   - `search_youtube(query, channels=None, limit=N)` → list of `YouTubeHit`
     (video_id, title, channel, channel_id, duration, url).
   - `fetch_youtube_transcript(video_id)` → `YouTubeTranscript` with timestamped
     segments; caches to `data/youtube_cache/<video_id>.json`.
   - CLI: `search-youtube`, `fetch-transcript`.
2. Maintain a human-editable channel allowlist at
   `data/youtube_channels.md` with three tiers:
   - **trusted** — proven good across multiple runs.
   - **probationary** — surfaced in searches, not yet evaluated. *Default for
     new channels.*
   - **excluded** — known noise (AI-narrated, clickbait, off-topic).
   Filtering rule: a search returning channels in `excluded` strips them;
   `probationary` and `trusted` pass through; never exclude up-front, only
   on evidence.
3. Update `SKILL.md`:
   - Split Phase 4 into 4a (web) and 4b (YouTube).
   - Hard rule: query YouTube in English + preserve Pāḷi sutta name and
     numeric reference.
   - Hard rule: auto-caption Pāḷi terms are unreliable; paraphrase, never
     quote verbatim from auto-captions.
   - Citation form: `[Channel — Title](https://youtu.be/<id>?t=<seconds>) —
     fetched YYYY-MM-DD (auto-captions; paraphrase)`.
   - Note template gains a `## YouTube Evidence` section.
   - Run-reflection template gains a "channel tuning" bullet.
4. Run an end-to-end probe on one prior research topic; cache the fetched
   transcripts; populate `data/youtube_channels.md` from real evidence
   (channels that produced relevant hits go to `trusted`; everything else
   stays `probationary`).

## Assumptions & uncertainties

- **Tooling split.** `yt-dlp` (system-installed `2024.04.09`) for search via
  `ytsearchN:` — confirmed working; **`youtube-transcript-api`** (just added
  as a project dep) for transcript fetch — confirmed working on the same
  video where `yt-dlp` failed with "Did not get any data blocks".
- **No channel-wide sweeps in v1.** Building a full local FTS index over
  curated channels was considered (option B in the design discussion) but
  deferred. v1 builds the corpus *passively* by caching every transcript
  it fetches; once the cache has real depth, an indexed search across the
  cache becomes a follow-up thread.
- **English-only search.** The probe data is unambiguous: Pāḷi-heavy queries
  return zero results, English queries with Pāḷi anchors return 20+. We
  ship English-only and revisit only if a future run shows a counter-example.
- **Caption-quality flag.** The pipeline distinguishes human-uploaded
  captions from auto-captions, and the note must annotate which is which
  in the citation. `is_auto` comes from `youtube-transcript-api` metadata.
- **Channel IDs vs. names.** YouTube channel display names can change;
  channel IDs (`UC...`) are stable. Allowlist stores both for resilience.
- **Possibly wrong:** the probationary tier may become noisy if every search
  adds dozens of new channels and nothing ever gets promoted. Mitigation:
  the reflection step forces explicit promotion / demotion calls per run.

## Constraints

- No new system packages; only Python deps via `uv add`.
- Helper module stays stdlib + `youtube-transcript-api` (newly added). No
  network calls at import time.
- CLI subcommands must follow the existing pattern (JSON to stdout).
- Don't touch SKILL.md sections unrelated to web search and the report /
  reflection step.
- Touch only files this thread requires (per Kamma scope rule).

## How we'll know it's done

- `uv run tools/research_sources.py search-youtube "<English query>"` returns
  a JSON array of hits.
- `uv run tools/research_sources.py fetch-transcript <video_id>` returns
  JSON segments AND writes a cache file to `data/youtube_cache/<id>.json`.
- A second call to `fetch-transcript` on the same `video_id` reads from
  cache (verified by mtime or a log line).
- `data/youtube_channels.md` exists, lists ≥6 channels with tier assignments
  seeded from the probe data, and has a documented format.
- `SKILL.md` includes a Phase 4b section, a YouTube hard rule, a citation
  form, and an updated reflection template — and contains zero remaining
  references to `python -c` heredocs for YouTube work.
- `uv run pytest` still passes (14 existing tests + any new ones).
- One transcript from a real channel is cached under `data/youtube_cache/`
  as evidence the end-to-end flow works.

## What's not included

- Channel-wide sweeps and a local FTS index over transcripts.
- Whisper / better ASR re-transcription of auto-captioned talks.
- A `/vicaya-tune` skill that mines reflection files into SKILL.md diffs.
- Resolving the older `MN 02 §23 (mūla)` → `MN 1 Mūlapariyāyasutta §23`
  citation upgrade (separate open thread in handoff.md).
- Any change to existing helpers (`search_vault`, `search_canon`,
  `search_calibre`, `gemini_cross_check`, `resolve_citation`).
