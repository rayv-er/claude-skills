#!/usr/bin/env python3
"""side-nudge.py — a one-line nudge when Brett is using the wrong side of Claude.

WHY THIS EXISTS. Brett, 2026-09-26: "can you nudge me when im using one side or the other in an incorrect way before
answering". The two sides do different jobs. The chat side is for questions, drafts, and decisions. The code side,
where this hook runs, is for building, fixing, and scheduling things on the server, the databases, the repositories,
and the schedules. The costly mistakes seen so far run both ways: one code session carrying dozens of unrelated
questions until it compacts, and recurring work kept in chats, like the AP collector, a scheduled chat that stalled on
almost half its runs and still read "succeeded". A written instruction to watch for this would fade after the first
compaction. A hook puts the rule in front of the agent on every message.

WHAT IT DOES. A UserPromptSubmit hook. It never blocks. It adds a short rule to the agent's context, plus two facts
it can measure: how many messages Brett has typed in this session, and whether the message uses the language of
repeated work. The agent judges whether a nudge applies. When one does, the reply opens with a single line starting
"Side check:" and then answers the request anyway. When none applies, nothing is said. A nudge Brett has heard and
carried on past is not repeated in the same session.

The chat side has no hooks. Its half of the rule is a paragraph in Brett's personal preferences in the Claude app
(the text is coach/chat-preferences.txt; pasting it is Brett's step).

Exit 0 always. Output is JSON with hookSpecificOutput.additionalContext.
"""
import json
import os
import re
import sys

LONG_SESSION = 25          # typed messages; past this, a new unrelated topic deserves a fresh session
SCAN_LIMIT = 40_000_000    # bytes; beyond this the transcript is long by definition and is not scanned

REPEAT = re.compile(
    r"\b(every (day|morning|week|weekday|month|monday|tuesday|wednesday|thursday|friday|quarter|year)|each (week|month)"
    r"|weekly|monthly|again|like last (time|week|month)|same as last|as usual|for (this|last) month"
    r"|tips for|check deposit|month.?end|stripe clearing|ira deposit|ach briefing|board packet|reconcil\w*)\b",
    re.I)

RULE = """SIDE CHECK. Brett asked on 2026-09-26 to be nudged, before the answer, when he uses the wrong side of Claude.
This is the code side: it builds, fixes, and schedules things on the server, the databases, the repositories, and the
schedules. Before answering, decide whether this message belongs somewhere else:
- a one-off question or advice with nothing to build, fix, or schedule: the chat side answers it as well, with less at stake
- a new topic unrelated to this session's work, in a session that is already long: a fresh session
- work that repeats, a recipe run by hand again: make it routine, an entry on the recurring list (for CFTA, cfta-sync
  deploy/recurring.toml) and a job on the server, so it stops depending on a chat
If one applies, open the reply with one line that starts "Side check:", names the better place in plain words, and
says why in a clause. Then answer the request anyway. If none applies, say nothing about sides. Replies to your own
questions ("yes", "go ahead") never earn a nudge. Never repeat a side check Brett has already heard in this session
and carried on past."""


def typed_messages(path: str) -> int | None:
    """Messages Brett typed in this session; None when the transcript is missing or too large to scan."""
    try:
        if os.path.getsize(path) > SCAN_LIMIT:
            return None
        n = 0
        with open(path, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                if '"type":"user"' not in line or '"tool_result"' in line:
                    continue
                o = json.loads(line)
                if o.get("isMeta") or o.get("isCompactSummary"):
                    continue
                c = o.get("message", {}).get("content")
                text = c if isinstance(c, str) else " ".join(
                    x.get("text", "") for x in (c or []) if isinstance(x, dict) and x.get("type") == "text")
                if text.strip() and not text.lstrip().startswith("<"):
                    n += 1
        return n
    except (OSError, ValueError):
        return None


def context(prompt: str, transcript: str | None) -> str | None:
    p = (prompt or "").strip()
    if not p or p.startswith("/"):
        return None                                   # slash commands and empty prompts are left alone
    signals = []
    n = typed_messages(transcript) if transcript else None
    if n is None and transcript and os.path.exists(transcript):
        signals.append("this session's transcript is very large, so it is long")
    elif n is not None and n > LONG_SESSION:
        signals.append(f"this session is long: Brett has typed {n} messages in it")
    m = REPEAT.search(p)
    if m:
        signals.append(f'the message uses the language of repeated work ("{m.group(0)}")')
    return RULE + ("\nMeasured this turn: " + "; ".join(signals) + "." if signals else "")


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except ValueError:
        return
    ctx = context(data.get("prompt", ""), data.get("transcript_path"))
    if ctx:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": ctx}}))


if __name__ == "__main__":
    main()
