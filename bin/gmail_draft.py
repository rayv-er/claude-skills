#!/usr/bin/env python3
"""Create a Gmail draft in brett@'s mailbox through the Workspace service account, built so nothing can re-wrap it.

    gmail_draft.py --to a@x.org[,b@y.org] --subject "Re: ..." --body body.txt [--reply-to MESSAGE_ID] [--attach FILE ...]

Why this exists. The Gmail connector's create_draft runs behind email-wrap-guard.py; the service-account route
(needed whenever a draft carries attachments) does not. On 2026-09-25 three drafts built with
EmailMessage.set_content(text) went to Brett's Drafts folded at 70 characters, one hard return per fold, which
is the thing he asked never to see again. This helper sends the plain text as base64 (no folding is possible)
and the same paragraphs as HTML <p> tags, which is what Gmail renders.

Body file: one paragraph per line, blank line between paragraphs; a signature block keeps its own lines.
Never send from here; drafts only.
"""
import argparse
import base64
import html
import mimetypes
import os
import sys
from email.message import EmailMessage

sys.path.insert(0, os.path.expanduser("~/code/clients/cfta/sync"))
os.environ.setdefault("SA_KEY_PATH", os.path.expanduser("~/Projects.local/cfta/cfta-sync/credentials/cfta-admin-sa.json"))
from auth import get_credentials                                      # noqa: E402
from googleapiclient.discovery import build                           # noqa: E402

BRETT = "brett@crestedbuttearts.org"
WRAP_LIMIT = 100   # a line this long followed by another prose line inside one paragraph is a hard wrap


def to_html(text: str) -> str:
    paras = [p.strip("\n") for p in text.strip().split("\n\n") if p.strip()]
    blocks = ["<p>" + "<br>".join(html.escape(l) for l in p.split("\n")) + "</p>" for p in paras]
    return '<div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;color:#000;">' + "".join(blocks) + "</div>"


def check_unwrapped(text: str) -> None:
    """Refuse a body wrapped at a fixed width: two consecutive prose lines inside a paragraph, the first a long one."""
    for p in text.strip().split("\n\n"):
        lines = [l for l in p.split("\n") if l.strip()]
        for a, b in zip(lines, lines[1:]):
            if len(a) >= WRAP_LIMIT and not a.rstrip().endswith((":", ".", "!", "?")) \
                    and not b.lstrip().startswith(("-", "*", "•")):
                raise SystemExit(f"ABORT: body looks hard-wrapped at:\n  {a[:80]}...\n  {b[:80]}...\nOne paragraph is one line.")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--to", required=True)
    ap.add_argument("--cc", default="")
    ap.add_argument("--subject", required=True)
    ap.add_argument("--body", required=True, help="text file, one paragraph per line")
    ap.add_argument("--reply-to", help="Gmail message id to reply to (sets the thread and In-Reply-To)")
    ap.add_argument("--attach", nargs="*", default=[])
    a = ap.parse_args()
    body = open(a.body, encoding="utf8").read()
    check_unwrapped(body)
    creds = get_credentials(["https://www.googleapis.com/auth/gmail.readonly",
                             "https://www.googleapis.com/auth/gmail.compose"], BRETT)
    gmail = build("gmail", "v1", credentials=creds, cache_discovery=False)
    msg = EmailMessage()
    msg["From"] = BRETT
    msg["To"] = a.to
    msg["Subject"] = a.subject
    if a.cc:
        msg["Cc"] = a.cc
    thread_id = None
    if a.reply_to:
        m = gmail.users().messages().get(userId="me", id=a.reply_to, format="metadata",
                                         metadataHeaders=["Message-ID", "References"]).execute()
        h = {x["name"].lower(): x["value"] for x in m["payload"]["headers"]}
        thread_id = m["threadId"]
        if h.get("message-id"):
            msg["In-Reply-To"] = h["message-id"]
            msg["References"] = (h.get("references", "") + " " + h["message-id"]).strip()
    msg.set_content(body.strip() + "\n", cte="base64")          # base64: the decoded lines cannot be folded
    msg.add_alternative(to_html(body), subtype="html", cte="base64")
    for path in a.attach:
        ctype = mimetypes.guess_type(path)[0] or "application/octet-stream"
        main_t, sub_t = ctype.split("/", 1)
        msg.add_attachment(open(path, "rb").read(), maintype=main_t, subtype=sub_t, filename=os.path.basename(path))
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    payload = {"message": {"raw": raw}}
    if thread_id:
        payload["message"]["threadId"] = thread_id
    d = gmail.users().drafts().create(userId="me", body=payload).execute()
    print(f"draft {d['id']} on thread {d['message']['threadId']} to {a.to}"
          + (f" with {len(a.attach)} attachment(s)" if a.attach else ""))


if __name__ == "__main__":
    main()
