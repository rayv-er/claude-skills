---
name: vault-search
description: >
  Apply when searching or answering questions from the Obsidian vault:
  "search my vault", "search my notes", "what did I write about X",
  "when did I last work on Y", "what does my vault say about Z", "find my
  note on X", or any question whose answer lives in personal/project notes
  rather than code. Do not apply to codebase searches (use Grep/Glob) or
  to writing notes (/note writes, this skill only reads).
---

# Vault search

Query the Obsidian vault at `/Volumes/rayv/obsidian-vault` through
`/Users/admin/code/personal/obsidian/bin/vault-query.sh`. It is read-only.

## Subcommands

```
vault-query.sh search <query>     full-text search, returns file list
vault-query.sh read <path>        print a note (vault-relative path)
vault-query.sh backlinks <file>   notes linking to <file>
vault-query.sh tags               tag usage counts
vault-query.sh tasks              open tasks across the vault
vault-query.sh daily [date]       print a daily note (default today)
```

## Q&A pattern

1. `search` for the user's terms (try 2-3 phrasings if the first is thin).
2. `read` the most promising hits, newest first when dates are in play.
3. `backlinks` on a central note to find related material.
4. Answer from what the notes actually say, citing each source as a
   `[[wikilink]]` (e.g. `[[Projects/sync/log]]`, `[[Daily/2026-08-15]]`)
   so the user can jump to it in Obsidian.

## Vault geography

- `Daily/YYYY-MM-DD.md`: per-day session log, `## Notes` captures, agenda.
- `Projects/<name>/log.md` and `commands.md`: per-repo session history and
  captured shell commands. `<name>` matches the repo directory in `~/code`.
- `Areas/`, `Reference/`, `People/`, `Meetings/`, `Weekly/`: the
  human-authored PARA layer.
- `Archive/`: frozen pre-2026-05 material (CFTA, homelab, old memory).

## Degraded modes

- Exit 3 means the rayv drive is not mounted. Say so; do not retry.
- A stderr banner about grep fallback means the Obsidian app is closed and
  results came from `rg`, not the live index. Results are still valid.
  In an interactive session you MAY offer to `open -a Obsidian`, wait ~5
  seconds, and retry for index-backed results, but only if the user says
  yes. Never launch the app unprompted, and never from a headless context.
