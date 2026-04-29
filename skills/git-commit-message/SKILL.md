---
name: git-commit-message
description: >
  Apply when writing a git commit message. Do not apply to PR descriptions,
  changelogs, release notes, or any prose that is not a commit message. The
  trigger is: "write a commit message" or "commit these changes" or drafting
  the message that goes into `git commit -m`.
---

# Git commit message format

## Subject line

50 characters or fewer. No period at the end.

Format: `<type>: <what>`

Valid types:

- `feat` -- new feature or capability
- `fix` -- bug fix
- `refactor` -- restructuring without behavior change
- `docs` -- documentation only
- `chore` -- maintenance, dependencies, tooling
- `test` -- tests only
- `revert` -- reverting a prior commit

Use imperative mood, present tense: "add", "fix", "remove", "update", not
"added", "fixed", "removed", "updated".

## Body (when needed)

Separate from subject with a blank line. Wrap at 72 characters.

The body explains WHY, not WHAT. The diff shows what changed. The commit
message explains why that change was necessary or what problem it solves.

Reference issue or ticket numbers at the end of the body if applicable.

## What not to write

Do not write vague subjects. These are all bad:

- `fix things`
- `misc updates`
- `WIP`
- `update stuff`
- `bug fix`
- `changes`

If the commit fixes a bug, name the specific symptom, not "bug fix".

## Examples

Good subjects:

```
fix: prevent duplicate ntfy alerts when spider retries
feat: add caddy-site lint check to make lint-inventory
chore: pin all container images to digest hashes
refactor: extract vault lookup into shared helper
docs: add deployment sequence to infra-ops README
```

Good commit with body:

```
fix: stop caddy reload on config parse error

The previous behavior reloaded even when the generated Caddyfile had
a syntax error, which took down all proxied sites. Now the deploy
target validates the config with `caddy validate` before reloading.

Closes #42
```

Bad:

```
update stuff
fixed the thing
WIP
misc
```
