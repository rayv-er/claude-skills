---
name: ira-qcd-recon
description: >
  Apply monthly (or on request) to reconcile IRA/QCD charitable distribution
  gifts: match custodian checks to donors, age promised-but-unarrived IRA
  gifts, and track QCD acknowledgment compliance. Triggers: "ira
  reconciliation", "QCD", "IRA checks", "who promised an IRA gift",
  month-start finance routines.
---

# Monthly IRA / QCD Reconciliation (CFTA)

Donors 70½+ give via IRA Qualified Charitable Distributions. The checks come
from CUSTODIANS with the donor buried in FBO/memo lines, the money often
arrives weeks after the promise, and the acknowledgment letter has special
IRS language. This skill closes the loop monthly.

## 1. Find custodian payments received this month

Sweep both systems for custodian-pattern payments:
- **QBO deposits** (direct API, /qbo-fix auth): line descriptions/attachments
  matching `IRA|FBO|401k|RMD|QCD` or custodian names.
- **Bloomerang**: `bloomerang.transactions` method='Check'/'Eft' joined to
  constituents; custodian checks are often logged under the DONOR already —
  verify against the check image on the QBO deposit attachment.

Known custodian fingerprints (grow this list):
| Payer on check | Donor identification |
|---|---|
| "IRA FBO <name>" (Cetera, BNY Mellon) | FBO name IS the donor (e.g. Samuel David McKenney & Barbie Adams) |
| LPL Financial | memo line (e.g. "Barnhart - painting donation") |
| Jackson National Life | "DONOR:" line (e.g. Karen Miller) |
| Fidelity/Schwab/Vanguard brokerage checks | memo or accompanying letter; do NOT confuse with DAF grants (Fidelity **Charitable** = DAF, different rules) |
| Raymond James | fund/foundation name in memo |

**QCD vs DAF matters**: DAF grants (GHCF, Fidelity Charitable, NPT, Vanguard
Charitable) are NOT QCDs — different acknowledgment rules (see §3) and DAF
invoices are never sent to donors.

## 2. Age the promises

Email intent mining (`workspace.gmail_messages`, jillian@ + brett@, bodies on
cfta-vm volume): `snippet ~* 'from (my|her|his) (IRA|401k)|required minimum|QCD'`.
Cross with open AB/pledge invoices. Output an aging table:

| Donor | Amount | Promised (date/source) | Invoice | Days waiting | Status |
Known open examples (7/2026): Tim Fretthold $5,000 (AB2044, "week or two"
from 7/15); Bill & Doris Altman $5,100 (AB2037, IRA/401k check promised 7/10).
Escalate anything > 30 days to Jillian for a gentle nudge.

## 3. Acknowledgment compliance (the audit item)

- **QCD receipts** must state: gift received from the custodian on behalf of
  the donor, date + amount, **no goods or services provided**, and must NOT
  call it tax-deductible (it's pre-tax money). No standard "deductible to the
  extent allowed" language.
- **DAF grants**: thank the recommending donor, no tax language at all
  (the sponsor already receipted them; grant letters certify no benefits and
  no binding-pledge fulfillment).
- Track in the register: received date, custodian, donor, amount, QBO deposit
  ref, acknowledgment sent Y/N. Bloomerang `acknowledgement_status` column
  holds their letter state — flag mismatches.

## 4. Output

Monthly artifact/table: (a) QCDs received this month w/ deposit refs,
(b) promise aging, (c) acknowledgment gaps, (d) YTD QCD register (fiscal year
Nov 1–Oct 31). Post follow-ups to the team sheet if one is active.
