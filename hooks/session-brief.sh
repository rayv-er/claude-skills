#!/usr/bin/env bash
#
# session-brief.sh — three lines of ground truth at the start of a session.
#
# WHY THIS EXISTS. Most of the expensive mistakes in this setup start with a
# wrong assumption about state rather than a wrong command: work committed onto
# a feature branch that is not the default, a checkout carrying someone else's
# uncommitted files, commits that were never pushed, a worktree left behind
# months ago. None of that is visible unless asked for, so it gets asked for
# after the mistake instead of before.
#
# Local git only, and no network, so it costs nothing and never delays a
# session. The deeper review is `/checkup`, which is invoked deliberately.
#
# Output goes to stdout, which the agent reads as context for the session.
set -uo pipefail

cd "${CLAUDE_PROJECT_DIR:-$PWD}" 2>/dev/null || exit 0
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0

BRANCH="$(git branch --show-current 2>/dev/null)"
[ -n "$BRANCH" ] || BRANCH="(detached)"
DIRTY="$(git status --porcelain 2>/dev/null | wc -l | tr -d '[:space:]')"
[ -n "$DIRTY" ] || DIRTY=0

# The default branch as the remote actually reports it, not an assumption.
DEFAULT="$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null | sed 's|^origin/||')"
[ -n "$DEFAULT" ] || DEFAULT="$(git config --get init.defaultBranch 2>/dev/null || echo main)"

UPSTREAM="$(git rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>/dev/null || true)"
if [ -n "$UPSTREAM" ]; then
  AHEAD="$(git rev-list --count "${UPSTREAM}..HEAD" 2>/dev/null | tr -d '[:space:]')"
  [ -n "$AHEAD" ] || AHEAD=0
else
  AHEAD="$(git rev-list --count "origin/${DEFAULT}..HEAD" 2>/dev/null | tr -d '[:space:]')"
  [ -n "$AHEAD" ] || AHEAD=0
fi

printf 'Repository state: on %s' "$BRANCH"
[ "$BRANCH" != "$DEFAULT" ] && printf ' (default is %s)' "$DEFAULT"
printf ', %s uncommitted file(s), %s commit(s) not pushed.\n' "$DIRTY" "$AHEAD"

# The traps that have actually bitten, surfaced only when they apply.
if [ "$DIRTY" -gt 8 ]; then
  printf 'Note: %s files are already modified here. Stage explicitly by path so unrelated work is not swept into a commit.\n' "$DIRTY"
fi
if [ "$BRANCH" != "$DEFAULT" ] && [ "$AHEAD" -gt 0 ]; then
  printf 'Note: these commits are on %s, not %s. Check where they belong before pushing.\n' "$BRANCH" "$DEFAULT"
fi

# Coaching focus, if one is set. Kept to one line so it informs without nagging.
FOCUS="$HOME/code/claude-skills/coach/FOCUS.txt"
[ -s "$FOCUS" ] && printf 'Coaching focus: %s\n' "$(head -1 "$FOCUS")"
exit 0
