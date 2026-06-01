# Vicaya skill improvements — work in progress

This file replaces the run-by-run reflection backlog. All 30 prior reflections
are in `runs/processed/`. The full prioritized issue list came from two passes
over those runs (one by Claude, one by another agent). What follows is what
remains after the work captured in commits up to and including the citation
verification feature.

## Done

| Issue | Status | Commit |
|---|---|---|
| #1 Scratch file not written before compaction | done | `feat: structural scratch-dossier system with per-phase gates + autolog` |
| #2 Calibre lock / multi-agent contention | done | `fix: serialize concurrent calibredb calls with cross-process flock` |
| #4 Cross-check AI hallucinations | done | `feat: verify Pāḷi citations from cross-check output against dpd.db sutta_info` |
| Chinese column always emitted in canon hits (user request, mid-session) | done | Same commit as #1 |
| Thematic runs forced to hand-skip Phase 2.5 / 3b gates (5 unprocessed runs) | done | `scratch-init --class thematic` auto-skips 2.5/3b in `scratch_gate` |
| `VICAYA_SCRATCH`/`VICAYA_PHASE` re-export tax every Bash call (3 unprocessed runs) | done | `data/scratch/.active` state file; `scratch-gate` auto-advances phase |
| `calibre-check` "ok" while `search-calibre` dies on GUI lock (3 unprocessed runs) | done | `calibre-check` runs the real search path; `search-calibre` returns a structured `unavailable` sentinel |

## Remaining — prioritized

### High severity

**#3 Canon / SQLite search failures.** Multiple sub-issues:
- NFD/NFC Unicode encoding breaks diacritic-heavy Pāḷi searches in some books
- Empty `paranum` in continuation rows — formulas like `bhavanirodho nibbānaṃ`
  in AN10.7 live in a row with empty paranum; requires id-range scan
- Stem-search false positives: `pāram` returns 20+ noise hits
  (pariyāpuṇanti, paramparā, rūpārammaṇa)
- Visuddhimagga (`e0101n_mul`) diacritic issue — `appamān` returns 0
- AN6.115 misref from misleading snippet
- Arrow wound near-misattribution to Thanissaro
- sqlite column names doc inconsistent with CLI output names

**#5 Skill too long / prescriptive.** SKILL.md is 2056 lines. Other agents
complained the skill is so long that they comply with stale instructions while
missing more important ones. Suggested fix: split into short mandatory
execution checklist + long reference. Scratch-gate / scratch-verify already
addresses *some* of this by making phase exits structural.

**#6 Agent failure checklist before final response.** A mandatory self-check:
did I overweight easy sources, underweight user seeds, stop after enough
evidence, confuse artifact creation with workflow completion, follow a stale
secondary instruction mechanically? Could be a `scratch-self-audit`
subcommand that prints a fixed checklist into scratch and refuses Phase 7
gate unless ticked.

### Medium severity

**#7 Phase exit criteria missing for non-scratch dimensions.** Partly
addressed by `scratch-gate <phase>` enforcing canonical evidence per phase,
but the gate's checklist is currently tick-by-agent. A stronger version would
*check* — e.g. Phase 2 gate verifies that at least N canon-search auto-log
entries appear in the phase section before allowing the gate to pass.

**#8 Scope lock for user-named seeds.** Before Phase 5, list every user-named
seed (URL, vault note, video) and confirm processed-or-deferred. A run missed
the long "Being Untangled" video transcript because the seed was never
explicitly gated. Could ride on the existing scratch-gate system as a new
phase or a Phase 5 pre-gate check.

**#9 YouTube transcript fetch failures / hangs.** No timeout, no fallback to
cached transcripts. `fetch-transcript` needs explicit timeout + a check for
cached transcripts under a known path before fetching.

**#10 Obsidian CLI bypass.** Agents write directly to vault filesystem,
breaking YAML indexing, links, graph. Should make Obsidian CLI primary and
filesystem write an explicit fallback that the final report must declare.
SKILL.md already says this but the rule gets ignored. Structural fix: a
helper `vault-write` subcommand that wraps Obsidian CLI with filesystem
fallback and writes the chosen path to scratch for Phase 7 hard-gate to read.

**#11 PDF generation failures / stale WeasyPrint.** The inline Python in
SKILL.md is fragile and creates temp-file drift. Replace with a named helper
subcommand (`generate-pdf <vault-path>`) so SKILL.md just calls it.

**#12 NFD/NFC Unicode encoding.** Diacritic-heavy terms return 0 hits when
the DB is NFD and the query is NFC (or vice versa). Add `unicodedata.normalize`
in `search_canon` before the LIKE.

**#13 Calibre query-syntax gotchas.** Apostrophes in author names cause
syntax errors; `--authors` is parsed as free-text `authors:` search;
empty-query-with-tags fails. Document or auto-escape.

**#14 Web search 403 / parameter failures.** Boolean operators break
search-web. Helper or doc note.

**#16 Tool failure operational rules.** Currently scattered across runs as
ad-hoc advice ("when X fails, do Y"). Consolidate into a single "When
something fails" reference, already partially present in SKILL.md — but make
each rule actionable rather than narrative.

**#17 Transcript-mining helper.** New subcommand:
`transcript-claims <video_id> --terms ... --window ...` that outputs
timestamped claim clusters from cached transcripts without dumping raw JSON.

**#18 Claim ledger output mode** for doctrinal/polemical audits — already
suggested in #6 territory. A `claim-ledger` subcommand that emits a
`| Claim | Source | Timestamp/page | Status | Counter-evidence |` table
into scratch.

**#19 Weak-model design — explicit control points.** Continue the structural
direction: anywhere the SKILL.md says "remember to X", replace with a
subcommand that does X or refuses to proceed without X.

**#20 Inline Python blocked by CLAUDE.md hook.** Agents end up writing
scripts to `temp/` to do ad-hoc work. Either document the temp/ workflow or
add subcommands for the most common one-off computations.

### Low severity

- **#21 sync_notes.py pull-rebase** fails on dirty working tree (the normal
  case); use stash-pull-pop-add-commit-push
- **#22 Obsidian vault path** assumptions inconsistent across machines
- **#23 Milinda paranum** references non-standard (PTS convention needed)
- **#24 CST Extra books** (0804/0810/1102) source identity unresolved
- **#25 wisdomlib.org** returning 404 — fallback path
- **#27 uv cache** needs escalated access (one-time setup; macOS)
- **#28 Movement-internal term mapping** (vossagga, paṭinissagga, sampajāna)
  when auditing modern method acronyms

### Content-specific guidance (lower urgency)

- **Phase 0b** — read user-provided vault note paths before angle triage
- **SN 12.15 (Kaccānagotta)** as standing pointer for any
  atthi/natthi/existence-language question; add to Devil's Advocate Q3
- **Ñāṇavīra Thera + pabhassara citta** as default search targets for
  Nibbāna-ontology questions
- **Niddesa** as systematiser for therapeutic bhāvanā pairings — pairings
  distributed across suttas, unified only in Niddesa/Abhidhamma
- **Two-note (English + Russian) frontmatter rule** — both share structure;
  Russian gets `topic:` in Russian, YAML keys stay English, Pāḷi refs
  verbatim
- **Cross-check correction logging** — when cross-check fixes a Pāḷi
  translation (`saha` = "simultaneous with" not "as soon as"), log the
  corrected rendering with the term in scratch verbatim

## Notes for the next session

1. The structural direction is working — `scratch-gate`, `scratch-verify`,
   `[REJECTED]` Phase 7 hard gate, and the cross-check auto-annotation all
   replace prose-instructions-that-get-ignored with code paths that refuse
   to proceed. Continue the same pattern.

2. The Phase 2 follow-up to citation verification is **Pāḷi-quote
   verification**: catch `asantasanto` mistaken for `asanta`, `saha` glossed
   wrongly, etc. This needs `search-canon` against the cited sutta and a
   fuzzy match on the quoted Pāḷi. Worth doing once content-level errors
   start mattering more than fabrication.

3. Several remaining issues (#5, #6, #19) point at the same root: the skill
   is structurally too long and relies on prose rules. The right move there
   is probably one big restructure (a short "execution kernel" section at
   the top, the rest moved into reference subsections that are loaded only
   when needed) rather than incremental edits.

4. Calibre Option B (HTTP content server) is still on the table if Option A
   (flock) starts feeling too serial. Punt until contention is the actual
   bottleneck.
