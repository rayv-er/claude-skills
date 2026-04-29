# claude-skills

Custom skills for Claude Code, the Claude desktop app, and the Claude web UI.
Each skill is a directory under `skills/` containing a `SKILL.md` file that
Claude reads to shape its behavior for a specific task type.

## How skills work

Claude Code loads skills from `~/.claude/skills/`. Each subdirectory there is
a skill. Claude reads the `SKILL.md` in each skill directory and uses the
frontmatter description to decide when to apply it.

## Installation

Clone this repo to `~/code/claude-skills`, then run:

```bash
./install.sh
```

This symlinks each directory under `skills/` into `~/.claude/skills/`. The
script is idempotent: run it again after adding new skills and it will link
only the new ones.

To install on another machine, clone the repo there and run `./install.sh`
again.

## Adding a skill

1. Create a new directory under `skills/` using a kebab-case name.
2. Add a `SKILL.md` with the required frontmatter (see CONVENTIONS.md).
3. Run `./install.sh` to link it.
4. For desktop or web UI use, upload the `SKILL.md` through the respective UI.

See [CONVENTIONS.md](CONVENTIONS.md) for the full format specification.

## Skills in this repo

| Skill | Purpose |
|---|---|
| brett-prose | Writing style guide for prose: no em dashes, lead with the answer, no marketing voice |
| board-memo | Board-level communications: executive summary first, explicit ask, no operational detail |
| bash-script | Bash scripting conventions: set -euo pipefail, stderr capture, no silent swallows |
| git-commit-message | Commit message format: imperative mood, type prefix, why not what in body |
| infra-ops-workflow | Homelab control plane discipline: CSV-as-contract, diff before deploy, no hand-editing hosts.yml |
| caddy-site | Adding a new public hostname: CSV entry, Authelia decision, Uptime Kuma, Vaultwarden |
| docker-compose-service | New homelab service scaffold: pinned images, per-project Postgres, full wiring checklist |
| cfta-staff-comms | Internal CFTA staff communications: direct, plain, no urgency theater |
