---
name: mwf-sched-help
description: >
  Apply when looking up Mountain Words Festival (MWF) attendee
  registrations on Sched. Triggers include: "look up [name] on MWF",
  "did [name] register for Mountain Words", "what sessions is [email] in
  for MWF", "is [name] registered for the festival", or forwarded
  volunteer/staff questions about an MWF attendee's schedule. Do not
  apply to the Crested Butte Wine + Food Festival (use wine-order-check
  for that), to write operations like comping or editing tickets, or to
  schedule/session edits — v1 of this skill is read-only.
---

# MWF Sched Help

You are answering a CFTA staff or volunteer question about a Mountain
Words Festival attendee's registration on Sched. The job is read-only
attendee lookup against the Sched API.

## What this skill does, and what it does not

**Does:** find an attendee by email or name, show which MWF sessions
they're registered for, their role/ticket type, and signup date.

**Does not (v1):** comp tickets, add or remove session enrollments,
edit attendee info, resend confirmation emails, or modify sessions.
If the user asks for any of those, decline politely and tell them
those flows are deferred to v2 — they'll need to do it in the Sched
admin UI for now.

## Setup (one-time, fill in before first use)

Two values are repo-local and need to be filled in here:

- **Event subdomain**: `mtnwords26` — base URL is
  `https://mtnwords26.sched.com/api`. (Confirmed 2026-05-05 via Stripe
  payment metadata `control_panel_attendee_url`.)
- **rbw item name**: `<MWF-SCHED-RBW-ITEM>` — the Vaultwarden item
  holding the Sched API key. If one doesn't exist yet, create it with
  `rbw add "CFTA/MWF Sched API Key"` (or similar), paste the key in,
  and update this section with the exact item name.

Once both are set, replace the angle-bracket placeholders below.

## Sched API basics

- **Base URL**: `https://mtnwords26.sched.com/api`
- **Auth**: `api_key` query param (GET) or form field (POST). Sched's
  API does NOT use Bearer tokens.
- **Format**: append `format=json` to get JSON instead of XML.
- **Transport**: use `curl`, not Python `urllib`. Cloudflare in front
  of Sched mishandles default urllib User-Agents — this is a real
  lesson from CBFF (`infra/130-cfta/cbff-capacity/stripe_sync.py`).

## Credentials

Fetch the API key on demand:

```bash
SCHED_API_KEY=$(rbw get "<MWF-SCHED-RBW-ITEM>")
```

If `rbw` errors with "vault is locked", surface this to the user
verbatim and suggest `rbw unlock` — do not try to bypass.

If `rbw` errors "not found", check the item name; the user may have
saved it under a slightly different label.

## Endpoint quick reference

The skill needs two endpoints. Read-only, GET, JSON.

**`users/export`** — full attendee list with each user's enrolled
sessions inlined. This is the primary lookup endpoint.

```bash
curl -s "https://mtnwords26.sched.com/api/users/export?api_key=${SCHED_API_KEY}&format=json"
```

Response is a JSON array of user objects. Each has fields like
`username`, `full_name`, `email`, `company`, `position`, `role`,
`reg_status`, `reg_type`, `created`, `sessions` (array of session
objects with `event_key`, `name`, `event_start`, `event_end`,
`venue`).

**`session/list`** — full session list. Useful only if the user asks
"who's in session X" rather than "what sessions is person Y in",
which is out of scope for v1 lookup. Mention it but don't use it
unless asked.

```bash
curl -s "https://mtnwords26.sched.com/api/session/list?api_key=${SCHED_API_KEY}&format=json"
```

## Lookup workflow

1. **Fetch once.** Pull `users/export` and store in a temp file:
   ```bash
   USERS=$(mktemp)
   curl -s "https://mtnwords26.sched.com/api/users/export?api_key=${SCHED_API_KEY}&format=json" > "$USERS"
   ```
   Reuse `$USERS` for follow-up lookups in the same conversation
   instead of refetching.

2. **Filter, in this order of relevance**:
   - exact email match (case-insensitive)
   - exact full-name match (case-insensitive)
   - email substring
   - name substring (split query into tokens; require all tokens
     present in the name)

   Use `jq` for the filtering. Example for an exact-email match:
   ```bash
   jq --arg q "$QUERY" '[.[] | select((.email // "") | ascii_downcase == ($q | ascii_downcase))]' "$USERS"
   ```

3. **For each match, render** per the output format below.

4. **Bias toward fewer false negatives.** If exact match returns
   nothing, fall through to substring; tell the user which match-mode
   produced the hits.

## Output format

Per attendee:

```
Jane Smith <jane@example.com>
  Role:        Attendee · reg_type: Standard pass
  Signed up:   2026-04-12
  Sessions (3):
    Fri Jul 17  09:00  Opening Keynote                     — Center for the Arts
    Fri Jul 17  14:00  Craft Talk: Memoir as Witness       — Library
    Sat Jul 18  10:30  Workshop: Revising the First Draft  — Townhall
```

Keep times in MWF local time (America/Denver). If `event_start` is
ISO with `Z`, convert. If a session lacks a venue, omit the em-dash
and venue rather than printing "— None".

If multiple matches, list them in order of relevance and prefix the
block with the match-mode used (e.g. `2 substring matches:`). For 5+
matches, ask the user to narrow before dumping the list.

## Zero matches

```
No MWF attendees match "<query>". Try:
  - a fragment of the email (e.g. "jsmith")
  - just the last name
  - check spelling — Sched uses whatever the attendee typed at signup
```

Do not invent or guess. Do not pull from non-Sched sources to fill the
gap.

## Refuse-list (v1 scope guard)

If the user asks for any of these, decline and explain the deferral:

- **Comp / add a ticket** — "v1 is read-only; do this in Sched admin
  for now. A safe write flow is on the v2 list."
- **Edit attendee info** (name, email, ticket type) — same deferral.
- **Resend confirmation email** — Sched's API likely doesn't expose
  this anyway; trigger it from the user's profile in Sched admin.
- **Cancel / remove a registration** — destructive; v2 only with
  explicit confirmation.
- **Bulk operations** — out of v1 scope.

Do not invent endpoints or improvise write calls. If the request is
ambiguous between "look up" and "modify", confirm which the user wants
before doing anything.
