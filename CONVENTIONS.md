# Conventions

This document specifies how skills in this repo are structured. Follow it
when adding a new skill.

## Directory naming

Each skill lives in its own directory under `skills/`. The directory name
must be kebab-case and must match the `name:` field in the frontmatter
exactly. Example: a skill named `bash-script` lives at `skills/bash-script/`.

## Files

`SKILL.md` is required. It contains the frontmatter and the skill body.

`README.md` is optional. Use it for human-facing notes about the skill: why
it exists, what prompted it, known gaps. It is not read by Claude.

`assets/` is optional. Put referenced files here (example configs, templates,
etc.). Reference them by relative path from within SKILL.md.

## SKILL.md frontmatter

Every SKILL.md begins with YAML frontmatter:

```yaml
---
name: kebab-case-name
description: >
  One paragraph. Describe when to use this skill and when not to. Be specific
  about triggers (what the user says or does that activates the skill) and
  anti-triggers (what looks similar but should not activate it). Claude uses
  this field to route, so vague descriptions lead to missed activations or
  false positives.
---
```

The `description` field is the most important part of the frontmatter. Write
it so Claude can answer "should I use this skill right now?" accurately.

## SKILL.md body

Write the body as direct guidance. Prose works well for style rules and
principles. Lists work well for checklists, sequences, and option
enumerations. Do not mix formats where one will do.

Include concrete examples when the skill defines a style or pattern. An
example is more useful than a description of the example.

Length target: 30 to 200 lines. If the skill grows past 300 lines, split it
into two skills with narrower scopes.

## Style rules that apply to every file in this repo

These rules apply to SKILL.md files, README files, and CONVENTIONS.md itself.

- No em dashes or en dashes. Substitute: comma, period, colon, or
  parentheses.
- No emojis.
- No marketing voice ("seamless", "powerful", "robust", "leverage").
- Lead with the answer. No preamble.
- Sentence case for headings.
- Oxford comma in lists.
- Plain prose over bullet lists where prose works.
