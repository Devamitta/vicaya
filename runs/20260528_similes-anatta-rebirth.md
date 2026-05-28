# Run Reflection — similes-anatta-rebirth — 2026-05-28

## Run summary
- **Question**: Similes for anattā and rebirth across three tiers (canonical, commentarial, modern)
- **Vault note**: `2026-05-28 - similes-anatta-rebirth.md` (committed cf0d11b)
- **Scratch**: `data/scratch/20260528_similes-anatta-rebirth.md`
- **Session**: Resumed from compacted context; phases 0–2 partial results recovered from summary

## What worked well
- Direct SQL fallback (sqlite3) essential — helper CLI returned empty for Pāḷi compound queries
- Cross-checker caught the SN 22.100 misidentification immediately (plantain passage is within SN 22.95, not a separate sutta)
- The three-tier structure cleanly separated doctrinal functions: T1 = the teaching itself, T2 = the philosophical problem-solving apparatus, T3 = living pedagogical application
- EBC catalogue grep was efficient for finding thematically related suttas (SN 35.234, AN 3.133)

## Errors and corrections
1. **SN 22.100 misidentification**: Initially labeled the kadali passage as a separate sutta. Cross-checker flagged correctly. Fixed before vault note.
2. **Milinda §-numbering**: Used DB paranum values (§2, §4, §5) as section refs; cross-checker noted these are non-standard. Switched to descriptive labels + "Miln." PTS page refs where known.
3. **Arrow wound attribution**: Nearly attributed the simile to Ṭhānissaro's own invention; cross-checker noted it's MN 63. Clarified.
4. **Context compaction**: Phases 1-2 results existed only in conversation context after compaction; had to reconstruct from session summary. Scratch discipline would have prevented this — should write to scratch at end of each phase, not batch at the end.

## What to improve in future runs
- Write to scratch immediately after each search query, not just at phase boundaries
- For Milinda research: look up PTS Miln. page numbers at research time, not during note-writing
- When canon rows show no paranum in a given row, always check nearby rows first before assuming the passage is in a different sutta
- Consider checking Ud and Iti as default T1 sources for any doctrinal topic — often have relevant material not in the main Nikāyas

## Sources not used / considered and dropped
- SN 12 (Nidāna-vagga): searched but rebirth similes there were about feeding a fire (craving) not rebirth itself
- Calibre locked mid-session (main app running) — metadata search unavailable after initial hits; core material adequate without it
- YouTube search not run — web sources and texts provided sufficient modern-teacher coverage
- SN 35.239: cross-checker confirmed it does not contain the chariot simile (chariot-maker sutta only)
