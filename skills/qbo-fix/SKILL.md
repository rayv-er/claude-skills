---
name: qbo-fix
description: >
  Apply when editing CFTA's QuickBooks Online books programmatically: repointing
  deposit lines or JE lines between accounts, fixing entities/classes/descriptions,
  creating AB- customers, building invoices, or any "change the actual entries"
  request. Triggers: "fix the coding on", "repoint", "recode this deposit",
  "edit the JE", "create an invoice for", "clean up [account]".
---

# QBO Entry Surgery (CFTA)

Direct Intuit API editing of CFTA's QuickBooks Online file. Brett prefers
**editing actual entries over posting reclass JEs**. HARD RULE: **never touch
anything dated before 2025-11-01** (FY25 is closed; fiscal year = Nov 1–Oct 31).

## Auth — READ THIS FIRST (token rotation)

Realm ID: `9130350131931956`. Credentials live in `~/.config/cfta/qbo_creds.json`:
```json
{"client_id": "...", "client_secret": "...", "refresh_token": "..."}
```
Intuit **rotates refresh tokens**. Every token call may return a NEW
refresh_token; if you don't persist it, the stored one dies within hours
(this killed a session on 2026-07-17). ALWAYS use `qbo_auth.py` in this skill
directory — it refreshes AND writes back the rotated token. Never hardcode the
refresh token in scratch scripts.

If the refresh token is dead (`invalid_grant`): fall back to the **QBO MCP
connector** (qbo_* tools — it manages its own OAuth) for customers/invoices,
and tell Brett the direct-API creds need re-auth for deposit/JE editing.

## Account map (ids are QBO internal)

| Id | Account | Use |
|---|---|---|
| 323 | Operating Cash:Operating - 1139 | the bank account; deposits go here |
| 101 | 4010.12 Fundraiser Contributions | Arts Ball paddle raises / gala donations |
| 96 | 4010.13 Fundraisers:Tickets | gala table/ticket income |
| 104 | 4140.13 Earned:Ticket Sales | programming ticket income |
| 112 | 4140.11 Gallery Sales | art/exhibit sales |
| 31/32 | 4040 / 4040.13 Unrestricted | general donations (.13 = Individual) |
| 449 | 2100.11 Deferred Revenue:Ticket Sales | presale liability |
| 1150040028 | 1100.15 AR:Humanitix | Humanitix cycle ONLY |
| 1150040024 | 1100.14 AR:POS | Clover cycle ONLY |
| 1150040034 | 100.16 AR:Event Temple | ET issued-invoice AR |
| 1150040035 | 1610 Stripe Clearing | ALL Stripe payout coding |
| 275 | 1100.13 AR:Operating | genuine operating receivables ONLY — keep processors out |
| 1018 | Stripe fees (COGS) | stripe fee expense |

Classes: `2100000000000153449` 1-Administration · `2100000000001501760` 2-Programming ·
`2100000000000153452` 3-Development · `2100000000001505933` 4-Building.
**Arts Ball + donations → 3-Development; rentals (Event Temple) → 2-Programming.**

## Customer conventions

- `AB - First & First Last` = Arts Ball invoices/payments. MUST be a sub-customer
  of parent **"Arts Ball" id 2950** (FQN `OPERATIONS:Arts Ball`). The MCP
  create-customer tool can't set a parent — create, then sparse-update via API:
  `{"Id", "SyncToken", "sparse": true, "Job": true, "ParentRef": {"value": "2950"}}`.
- `FR -` = Front Row / capital campaign pledges. `CC -` = capital campaign. Never
  mix gala pledges onto these.
- Processor entities: AR - Humanitix (1978), AR - Event Temple (3850), AR - Clover,
  AR - Stripe (legacy, accounts deactivated 7/16 — don't revive).

## Editing patterns

Always **dry-run first** (print current state), then `--apply`. Pattern scripts
from 2026-07-16 live in the session scratchpad style; canonical skeleton:
fetch entity → modify in place → POST full object back (QBO full-update).

Gotchas learned the hard way:
- `DocNumber` max **21 chars** (invoice/JE).
- Account sparse update requires `Name` field even when unchanged.
- **Payments API cannot apply Deposit-type credits** ("Amount Received plus
  credits..." error) — $0 apply-payments are UI-only. Generate the schedule,
  Brett clicks it.
- GL reports do NOT show entity names on JE lines — never conclude a JE lacks
  a customer from GL output; fetch the JE itself.
- `Stale Object Error ... Brett Henderson` = Brett is editing in the UI right
  now. Re-fetch for a fresh SyncToken and retry once; if it persists, pause and
  tell him which transaction.
- Bank-feed arrivals must be **matched** to existing manual deposits, never
  added fresh (a $51K Fidelity deposit got double-booked this way once).
- DAF-funded invoices (GHCF/NPT/Vanguard/Fidelity payers) are internal AR
  trackers — **never send** them to the donor.

## Verification

After any batch: re-query `Account.CurrentBalance` for touched accounts and
state before/after. For invoices use the MCP `qbo_sales_get_invoices`.
