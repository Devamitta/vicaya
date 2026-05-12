# Probe notes — YouTube pipeline, first run (2026-05-12)

First end-to-end exercise of the new YouTube source. Captures the data on which the
seed allowlist was built, and the gotchas worth knowing for future runs.

## Queries that worked

- `apannaka sutta MN 60` → 20 hits, several substantive (Bhante Suddhāso multi-part
  sutta study, Clear Mountain Monastery 10-min summary, Candana Bhikkhu, Dharma robe).
- `paticcasamuppada dependent origination` → 20 hits, mixed — three monastic-tradition
  channels surfaced (Bhikkhu Dhammānanda, Yuttadhammo Bhikkhu, plus a Bhikkhu Bodhi
  talk re-hosted on a generic channel) and several AI-narrated channels.
- `arahant kamma after enlightenment` → 20 hits, decent (Wisdom Park, Theravada
  Buddhism Learning, Buddha Tube).

## Queries that returned nothing

- `paticcasamuppada` (term alone, Pāḷi only) — same Pāḷi-heaviness reason.
- `arahant kamma parinibbana ahosi` — too many Pāḷi terms, no English anchor.
- `apannaka sutta safe bet wager rebirth` — long English gloss with no numeric ref.

Confirms Hard Rule #8: English + Pāḷi sutta name + numeric reference. Short.

## Transcript quality

Fetched Bhante Suddhāso MN 60 talk (`R0vhivplJuM`): 1433 segments, `is_auto: true`.
Pāḷi terms predictably mangled — `Apaṇṇaka` → `apaka`, `Majjhima Nikāya` → `Maj Manaya`,
`Suddhāso` → `saso`. Useful for locating the timestamp where a topic is discussed; not
for verbatim quotation. Hard Rule #7 is load-bearing.

## Channels promoted to trusted (with reason)

- **Buddhist Insights @ Empty Cloud** — Bhante Suddhāso's multi-part MN 60 sutta study
  is exactly the depth that justifies promotion. Saw across one topic; reasonable bet.
- **Bhikkhu Dhammānanda** — recognised monastic teacher; animation/explanation of
  paṭiccasamuppāda surfaced as a substantive hit.
- **Yuttadhammo Bhikkhu** — well-known Theravāda monk with a long-running channel.

## Channels left probationary

Everything else from the three probes. Some are obvious AI-narrated channels
("Buddha's Wisdom", "Buddhism Podcast", "Mind Podcast (Buddhism)") but per user
instruction we do not exclude on hunch. They stay probationary until a real run
produces concrete evidence of noise — a citation that turned out wrong, a quote that
misrepresented a source, a transcript with low signal density.

## Channels excluded

None. Per user instruction: only exclude on concrete evidence. The category exists
and the pipeline supports it; it stays empty until a real noise event is documented.

## Open follow-ups for the next run

- Run a real `/vicaya` on a fresh topic so the reflection template gets exercised
  end-to-end (writing the run reflection + applying the Channel tuning section).
- Watch whether `Yuttadhammo Bhikkhu` surfaces on multiple topics; if so the trust
  is well-placed. If only paṭiccasamuppāda surfaced him, treat as topic-specific.
- The 14k Calibre FTS index is still building in the background — orthogonal but a
  reminder that the corpus story will be deeper once that finishes.
