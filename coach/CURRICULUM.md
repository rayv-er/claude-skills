# Mastering this setup: the order that pays

Eight things, ordered by what they are worth here, not by how advanced they sound. Each one names what
good looks like and how you know it landed. Work one at a time. The current one is in `FOCUS.txt`, and
what has been introduced, adopted, or declined is in `LOG.md`.

The setup is already unusual: a warehouse, an agent with a shell, twenty-one skills, hooks, worktrees,
a private mirror, and a read-only tool server. The gaps are not in the software. They are in the habits
around it, which is where the expensive mistakes have come from.

## 1. Establish state before acting

Almost every costly mistake here began with a wrong assumption about state, not a wrong command. A
delete keyed on a column that was not unique. An overwrite of a server file that was ahead of the
checkout. A commit onto a branch that was not the default.

Good looks like: before anything that changes something, one cheap command that proves the assumption.
Does this table have a key. What is actually deployed there. Which branch is this. How many rows will
this touch. Say the expected number out loud first, then compare.

You know it landed when: a destructive step is always preceded by its own dry run, and you notice
yourself asking "how would I know if I am wrong about this" before acting rather than after.

## 2. Branch and commit discipline

The sync repository is on a feature branch that is one commit ahead of the default and eight behind,
carrying twenty-five modified files nobody committed. That is not a disaster, it is a slow tax: every
future change has to be untangled from it first, and work committed there does not reach production's
branch.

Good looks like: know which branch is the default before committing, stage by explicit path when a
checkout is dirty, and never let a checkout carry more than a day's uncommitted work.

You know it landed when: `git status` in any repository fits on one screen, and no branch is both ahead
and behind by more than a few commits.

## 3. Plan mode for anything touching more than three files

The September review was done in plan mode and it worked: scope agreed, staged, approved stage by stage,
and every stage landed. Nothing else this month used it.

Good looks like: for a multi-file or multi-step change, plan first, approve the plan, then execute. For a
one-file fix, skip it; ceremony on small work is its own waste.

You know it landed when: you can point at the plan that a week of changes came from, and the stages match
the commits.

## 4. Verification you can re-run

Until 2026-09-22 this platform had no automated test. It now has ten, plus `gmake check`, `gmake
migrations-check`, `gmake budget-mirror-ok`, and two monitors. That is the difference between believing
something works and being able to show it does, repeatedly, after the next change.

Good looks like: anything you checked by eye once becomes a command. The check runs before the thing it
guards, not after the incident.

You know it landed when: a change to the close tooling is followed by `gmake test` without being asked,
and a failed check is treated as information rather than an obstacle.

## 5. Close the loop, in writing

Several things this month were handed back and left open: a workflow to deactivate, a rotation to start,
eleven stale pipelines, a decision about seventeen rows. None of them are hard. They are open because
nothing carries an owner and a date.

Good looks like: anything handed back gets a name and a date in the same sentence, and lands somewhere
that will be read again, a runbook, an issue, or the review document.

You know it landed when: the open items at the end of a month are the ones you chose to defer, not the
ones that quietly fell off.

## 6. Delegate the searching

Reading twenty files to answer one question is what subagents are for. They read in parallel and return
the conclusion instead of the file dumps, and they do not spend your session's context.

Good looks like: "search the whole repository for every caller of this" goes to an agent; the decision
about what to do with the answer stays with you.

You know it landed when: long searches stop pushing the useful part of a session out of view.

## 7. Repository hygiene

Nine worktrees, forty-four branches on one remote and sixteen on its mirror, and a stale checkout that
the desktop client was running the server from. Each is small; together they are why "which copy is
real" keeps being a question.

Good looks like: worktrees removed when the work merges, branches deleted when they land, one canonical
checkout per repository, and the deployed copy reconciled with the repository rather than drifting.

You know it landed when: the answer to "where does this run from" takes one command, not three.

## 8. The read-only path

The tool server is read-only, capped, and safe by construction. The shell is neither. Questions belong
on the first path, changes on the second. Six finance tools were added on 2026-09-22 so the first path
now reaches the work you actually do.

Good looks like: "what is the balance", "which series have posted", "who owes us" asked in chat; "change
this", "deploy that", "rebuild the packet" done here.

You know it landed when: a question you would have opened a session for gets answered from your phone.
