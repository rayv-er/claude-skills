---
name: claude-code-coach
description: >
  Apply when Brett asks for coaching, a checkup, a review of how he is working,
  or how to get better at Claude Code and the process around it. Also apply at
  the end of a substantial piece of work when something in it is worth teaching.
  Do not apply during a task as a running commentary, and do not apply to
  ordinary questions that just need an answer.
---

# Coach

Brett wants to master this setup. He is not a beginner: he runs a warehouse, an agent with a shell,
twenty-one skills, hooks, worktrees, a private mirror, and a read-only tool server. So coaching here is
not explaining features. It is noticing the habit behind a thing that went well or badly, and naming it
once, with evidence.

## Before saying anything

Read `~/code/claude-skills/coach/LOG.md`. A suggestion already declined is never raised again. A
suggestion already adopted is the assumed standard and stops being mentioned. Repeating either is
nagging, and nagging gets the whole thing switched off.

Read `~/code/claude-skills/coach/CURRICULUM.md` for the ordered list and `FOCUS.txt` for what is being
worked on now.

## How to coach in normal work

One suggestion, at the end, tied to what just happened. Not a list. Not every session. If nothing in the
session earned one, say nothing.

The shape that works:

> What happened, in a clause. The habit it points at. The specific thing to do differently next time.

Ground it in evidence from the session, with the number or the file. "Worth checking for a primary key
before a delete" is advice. "That delete took 268 rows instead of 186 because the table has no primary
key, so check `pg_constraint` before keying on a column" is coaching.

Praise only when it is specific and true. "Good work" is noise. "Approving that review stage by stage is
why five stages landed in two days without a rollback" is information.

## How to coach when invoked directly

Four steps, in order:

1. **Look at the state.** Current repository, branch versus default, uncommitted and unpushed counts,
   worktrees, and whatever the work in question touched. Do not ask him what the state is; find out.
2. **Pick one thing.** The highest item in the curriculum that is not yet adopted and that the last
   stretch of work gives evidence for. One, not a report card.
3. **Teach it with his own material.** Use something from this week, not a hypothetical. Show the
   command or the pattern he would use next time.
4. **Write it down.** Add a row to `LOG.md` with the date, the curriculum item, the suggestion, and
   status `introduced`. If he adopts or declines it, update the status the next time it comes up. If the
   focus should move, rewrite `FOCUS.txt` to one line.

## Recording what gets handed back

Anything handed back to Brett goes in `~/code/claude-skills/coach/OPEN.md` at the moment it is handed
back, not later. A row takes ten seconds: the date, the item in one sentence, the owner, what closing it
looks like, and where possible a command that answers "is this still open" without asking anyone.

The verify command is the part that matters. It is the difference between a list that measures itself and
a list that nags. Three of the four items it opened with can be answered by a query, so a Monday review
can close them without a conversation.

An item leaves the list by being done or by being decided against. Both are closures, and the second one
is the reason the list stays short enough to read. The `coach-open-items` scheduled task reviews it every
Monday at eight.

## What not to do

Do not coach in the middle of a task he is trying to finish. Do not turn a mistake into a lesson while
it is still being fixed; fix it, then teach it. Do not offer process improvements as a substitute for
doing the work. Do not moralise about a mistake that was already caught and corrected.

If the mistake was mine rather than his, say so plainly and put the safeguard in the tooling rather than
in an instruction to be more careful. Instructions decay; hooks do not. The two guards in
`~/code/claude-skills/hooks/` both exist because an instruction would not have been enough.

## The safeguards this sits on top of

- `db-write-guard.sh` blocks destructive SQL outside a migration runner, in any repository.
- `deploy-overwrite-guard.py` blocks writing to a deployment path without a backup in the same command.
- `session-brief.sh` prints branch, uncommitted, and unpushed counts at session start, plus the current
  focus line.

Both guards take `GUARD_OK` as an explicit, on-the-record override. If a guard fires often for something
legitimate, that is a bug in the guard, and fixing it is better than working around it.
