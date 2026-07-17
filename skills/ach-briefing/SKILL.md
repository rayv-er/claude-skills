---
name: ach-briefing
description: >
  Apply when identifying ACH/wire items in the QBO bank feed: scan synced
  email for grant, payout, and payment notifications and map each expected
  feed item to its coding or invoice application. Triggers: "scan my email
  for the ach payments", "what's in the bank feed", "what's this deposit",
  unidentified PREAUTHORIZED ACH credits.
---

# Bank Feed ACH Briefing (CFTA)

Answer "what is each ACH in the feed and where does it go" from synced email
evidence. Email source: `workspace.gmail_messages` (subjects/snippets) with
full bodies at `/var/lib/docker/volumes/cfta_cfta_sync_data/_data/gmail/<user>/<id>.txt`
on cfta-vm (path in the `local_path` column). Sync lands ~6:15 AM daily.

## Query pattern

```sql
SELECT to_char(date,'MM/DD HH24:MI'), from_address, subject, LEFT(snippet,160)
FROM workspace.gmail_messages
WHERE user_email = 'brett@crestedbuttearts.org'   -- also jillian@ for donor intent
  AND date >= now() - interval '5 days'
  AND (subject ~* 'ach|wire|transfer|grant|deposit|payment|payout|remittance'
    OR from_address ~* 'paypal|fmr.com|vanguard|nptrust|ghcf|stripe|clover|bank|ubs|morgan|raymondjames')
ORDER BY date DESC;
```

## Known sender fingerprints

| Sender / subject | Feed item | Coding |
|---|---|---|
| donorservices@ghcf.org "ACH Notification" | GHCF grant ACH — body names the FUND and amount (read the body file!) | 101 + AB entity, or apply to AB invoice |
| fcgf@fmr.com FIDELITYSECURE | Fidelity Charitable grant — amount in secure portal; ACH memo "FIDELITY INVESTM GrantPaymt" | per donor |
| service@paypal.com "grant from [NPT/Vanguard]" | DAF grant paid via PayPal → "PAYPAL TRANSFER" ACH 1–2 days later | apply to the donor's AB invoice |
| notifications@stripe.com "Your $X payout for **[account]**" | the subject names WHICH Stripe account: shop.cbwineandfood.org → 1610 Stripe Clearing; **Event Temple → 100.16** (client portal payments, net of fees) | see /month-end-processors |
| app@clover.com Closeout Report | Clover settlement ACH 1–3 days later | credit 1100.14 |
| AES FUNDING | Auction Conductor settlement | see /aes-recon |
| quickbooks@notification.intuit.com Bill Pay | OUTGOING — match to bills; watch for "We weren't able to schedule 1 payment" failures |
| paul.gerardi@ubs.com / MSSB memos | donor wires — "MSSB C/F <name>" is the DONOR's brokerage, verify against donor emails (a Ronai wire was misread as Burke once) |

## Output

A table: feed item → amount → identity (with the email evidence) → action
("match to DEP-x", "apply to AB20xx", "code to acct Y + entity Z"). Flag:
double-payment risks (card captured AND check en route), failed Bill Pays, and
anything unmatched. Always remind: **match feed items to existing deposits,
never add duplicates**. DAF-funded invoices are never sent to donors.
