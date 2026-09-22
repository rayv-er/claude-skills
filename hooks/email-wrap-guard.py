#!/usr/bin/env python3
"""email-wrap-guard.py — no hard-wrapped paragraphs in an email body.

WHY THIS EXISTS. Brett has twice received drafts with line breaks scattered
through the middle of sentences. The cause both times was the same: the plain
text body was wrapped at a fixed width, the way a file or a commit message is
wrapped. A file is read at the width it was written. An email is not. Every
break typed into the body is a real break in the sent mail, so it reflows
badly on a phone, in a narrow reading pane, and in anyone's quoted reply.

THE RULE. One paragraph is one unwrapped line. Blank lines separate
paragraphs. Let the reader's client do the wrapping, because only it knows
how wide the window is. Where the tool takes a rich text body as well, send
the same content as paragraph tags so the plain body is only ever the
fallback.

WHAT IT DOES. A PreToolUse hook on the mail tools. It looks at the plain text
body, finds paragraphs broken across several short lines, and blocks. Lists,
signature blocks, addresses, and quoted history are left alone, because those
are lines by intent rather than by wrapping.

Exit 0 allows. Exit 2 blocks and returns the message to the agent.
"""
import json
import re
import sys

MAIL_TOOL = re.compile(
    r'(create_draft|update_draft|send_message|send_mail|create_reply|reply|forward)',
    re.I)

# A wrapped line is long enough to be prose but stops well short of the width a
# client would use. Signature and address lines sit below this floor.
WRAP_MIN, WRAP_MAX = 40, 95

LIST_MARKER = re.compile(r'^\s*([-*•>]|\d+[.)]|[a-z][.)])\s')
ENDS_CLAUSE = re.compile(r'[.!?:;]["\')\]]?\s*$')

MESSAGE = """BLOCKED: the plain text body is hard-wrapped, which is how the last two
drafts arrived with breaks through the middle of sentences.

An email is not a file. Every line break in the body is a real break in the
sent mail, so a body wrapped at a fixed width reflows badly on a phone, in a
narrow reading pane, and inside anyone's quoted reply.

Rewrite the body so that:

  1. Each paragraph is ONE line, however long, with no breaks inside it.
  2. Paragraphs are separated by a blank line.
  3. Lists and signature lines stay on their own lines, which is fine; they
     are lines by intent rather than by wrapping.

If the tool takes a rich text body too, send the same content there as
paragraph tags, so the plain body is only ever the fallback.

GUARD_OK anywhere in the body overrides this, for the rare message that
genuinely needs fixed-width lines."""


def wrapped_lines(body: str) -> list:
    """Lines that look like prose broken by a writer rather than by a reader."""
    hits, paragraphs = [], re.split(r'\n\s*\n', body)
    for para in paragraphs:
        lines = [l for l in para.splitlines() if l.strip()]
        if len(lines) < 2:
            continue
        for i, line in enumerate(lines[:-1]):          # the last line may be short
            s = line.strip()
            if LIST_MARKER.match(s) or LIST_MARKER.match(lines[i + 1].strip()):
                continue
            if not (WRAP_MIN <= len(s) <= WRAP_MAX):
                continue
            if ENDS_CLAUSE.search(s):                  # a deliberate short sentence
                continue
            hits.append(s)
    return hits


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0                                   # never block on a hook failure
    if not MAIL_TOOL.search(payload.get("tool_name", "")):
        return 0
    body = (payload.get("tool_input") or {}).get("body") or ""
    if not body or "GUARD_OK" in body:
        return 0
    hits = wrapped_lines(body)
    if len(hits) < 2:                              # one short line is not a pattern
        return 0
    print(MESSAGE, file=sys.stderr)
    print("\nLines that look wrapped:", file=sys.stderr)
    for h in hits[:4]:
        print(f"    {h}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
