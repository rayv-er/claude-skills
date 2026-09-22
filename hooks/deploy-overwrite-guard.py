#!/usr/bin/env python3
"""deploy-overwrite-guard.py — no overwriting a deployed file without a backup.

WHY THIS EXISTS. On 2026-09-22 a module was about to be deployed to cfta-vm by
copying the local orchestrator.py over the deployed one. The deployed copy
carried a fix the checkout did not have, a guard that stops non-ascii alert
titles being silently dropped, and the copy would have reintroduced that bug
with no sign anything had been lost. The deployed file was patched in place
instead. Nothing in the tooling would have caught the other outcome.

The general case: a server's copy of a file is not always behind yours. It is
sometimes ahead, because someone fixed it there and never got it back into the
repository. Overwrite blind and the fix disappears silently.

WHAT IT DOES. A PreToolUse hook on Bash. If a command writes INTO a deployment
path and the same command takes no backup, it blocks. Reading, listing,
diffing, and copying OUT of those paths are untouched.

Written in Python because which side of the command the path is on is the whole
question. `cp /opt/a /tmp/b` is a read, `cp a /opt/b` is a deploy, and
`cat x | ssh host "tee /opt/b"` begins with the word cat and is a deploy. A
regular expression that gets all three right is harder to read than this.

Exit 0 allows. Exit 2 blocks and returns the message to the agent.
"""
import json
import re
import sys

DEPLOY = r'/(opt|etc|srv|usr/local|var/lib|var/www)/'
COPY_VERBS = ("cp", "mv", "rsync", "scp", "install")

MESSAGE = """BLOCKED: writing to a deployment path without a backup in the same command.

The server's copy is not always behind yours. On 2026-09-22 the deployed
orchestrator on cfta-vm carried a fix the checkout did not have, and copying
over it would have silently removed it.

Two steps first:

  1. Diff what is there against what you are about to send.
         ssh HOST "sudo cat /opt/path/file" | diff - local/path/file
     If the remote has something the repository does not, patch it in place and
     get that difference back into the repository rather than overwriting it.
  2. Back the file up in the same command, so the restore path exists before
     the risk does:
         ssh HOST "sudo cp /opt/path/file /opt/path/file.bak-$(date +%Y%m%d)"

Then re-issue. Any command that takes a backup passes this guard automatically,
and GUARD_OK overrides it on the record."""


def writes_into_deployment(cmd: str) -> bool:
    # Redirection: > /opt/... or >> /etc/...
    if re.search(r'>>?\s*["\']?' + DEPLOY, cmd):
        return True
    # tee, with or without -a
    if re.search(r'\btee\b\s+(-a\s+)?["\']?' + DEPLOY, cmd):
        return True
    # dd's destination is named, not positional
    if re.search(r'\bdd\b[^|;&]*\bof=["\']?' + DEPLOY, cmd):
        return True
    # Copy-like verbs: only the destination counts, so take the last path
    # argument of each occurrence rather than any path in the command.
    for verb in COPY_VERBS:
        for m in re.finditer(r'\b' + verb + r'\b([^|;&]*)', cmd):
            args = [a.strip('"\'') for a in m.group(1).split() if not a.startswith("-")]
            if args and re.search(DEPLOY, args[-1]):
                return True
    return False


def main() -> int:
    try:
        cmd = (json.load(sys.stdin).get("tool_input") or {}).get("command", "")
    except Exception:
        return 0                      # never block because the hook itself failed
    if not cmd or not re.search(DEPLOY, cmd):
        return 0
    # An explicit acknowledgement, or a backup taken in the same command.
    if re.search(r'GUARD_OK|\.bak|\.backup|\.orig|backup-|\btar\b[^|]*\s-?c', cmd, re.I):
        return 0
    if not writes_into_deployment(cmd):
        return 0
    print(MESSAGE, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
