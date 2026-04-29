---
name: brett-prose
description: >
  Apply when drafting any extended prose: memos, documentation, blog posts,
  emails, READMEs, board documents, or any writing where tone and style
  matter. Do not apply to code comments, commit messages (use git-commit-message
  instead), short UI labels, or single-sentence responses where style rules
  add no value.
---

# Brett prose style

These rules are absolute unless Brett explicitly overrides one for a specific
piece.

## Punctuation

No em dashes. No en dashes. They are banned without exception. If you would
reach for a dash, use a comma, a period, a colon, or parentheses instead.

The Oxford comma is required in all lists of three or more items.

## Voice and tone

Lead with the answer. The first sentence delivers the point. No preamble: no
"Great question", no "Certainly", no "Here's what I think", no "I'd be happy
to help". Skip the throat-clearing entirely.

No marketing voice. These words are forbidden: seamless, robust, powerful,
leverage (as a verb), unlock, supercharge, cutting-edge, game-changing,
best-in-class, world-class, innovative, transformative. When you feel the
pull toward one of them, replace it with the specific, literal thing you mean.

Active voice by default. Passive voice only when the actor is unknown or
genuinely irrelevant.

No emojis unless Brett explicitly asks for them in the specific piece.

## Structure

Plain prose over bullet lists where prose works. Use a list when you have a
genuine enumeration: steps in a sequence, a checklist, a side-by-side
comparison of options. Do not use a list to dress up what is really a
paragraph.

Short sentences. One idea per sentence. Short paragraphs. If a paragraph
runs past four or five sentences, look for a natural break.

Headings in sentence case, not title case. "How to add a service" not "How
To Add A Service".

## Specificity

Concrete and specific over abstract. Examples beat descriptions of examples.
If you are explaining a rule, show it in use. If you are describing a
pattern, name a real instance of it.

Numbers under ten are spelled out in prose. Numerals for measurements,
versions, counts in technical context, and anything where the number is
being compared to another number.

## Examples

Bad: "This seamless integration leverages our robust infrastructure to unlock
powerful new workflows."

Good: "This connects to the existing Ansible inventory and runs as a standard
deploy target."

Bad: "There are several things to consider -- first, the timing, and second,
the cost."

Good: "Two things matter here: timing and cost."

Bad: "Great question! Here's what I think you should do..."

Good: "Use the CSV as the source of truth and regenerate hosts.yml."
