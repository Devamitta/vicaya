## Overview
Add a Vicaya tool attribution to every research note produced by the /vicaya
skill — both in the YAML frontmatter and in the footer line at the end of the
note.

## What it should do
1. Every note's YAML frontmatter gains a `tool` field (before `agent`) whose
   value is the bare GitHub URL: `https://github.com/bdhrs/vicaya`
2. The italic footer line at the end of every note is updated from:
     *Researched by <Model> on YYYY-MM-DD.*
   to:
     *Researched by [Vicaya](https://github.com/bdhrs/vicaya) using <Model> on YYYY-MM-DD HH:MM.*
3. The `agent` field (model identity) is unchanged; `tool` is a separate field
   for the research framework, ordered before `agent`.

## Assumptions & uncertainties
- GitHub repo URL is `https://github.com/bdhrs/vicaya` (confirmed from git remote).
- Obsidian renders a bare URL in a property field as a clickable hyperlink.
- The footer line is rendered as markdown inside the vault note, so a markdown
  link `[Vicaya](url)` is correct there.

## Constraints
- Only `skill/vicaya/SKILL.md` is modified; no Python files touched.
- No existing vault notes are retroactively edited.

## How we'll know it's done
- SKILL.md frontmatter template: `tool` before `agent`
- SKILL.md footer template: new Vicaya-first format with HH:MM
- Rule F5 description: updated inline example
- Rule F6: new rule documenting `tool` field
- Correct frontmatter example block: updated

## What's not included
- Retroactive edits to previously written vault notes.
- Changes to Python helpers or tests.
