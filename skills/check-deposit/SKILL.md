---
name: check-deposit
description: >
  Apply when Brett scans a batch of checks to deposit: build the QBO deposit
  with correctly coded lines, entities, and classes, and attach the check
  images. Triggers: attached check-scan PDFs, "add these as a deposit",
  "deposit I'll make today", "code these checks".
---

# Check Deposit Day (CFTA)

Turn a folder/batch of scanned check PDFs into a complete QBO deposit with
attached images. Reference workflow from DEP-33870 (7/16/26, 15 checks $69,700).

## Workflow

1. **Read every PDF** (Read tool, `pages: "1"`). Extract per check: payer name
   (incl. fund names on foundation checks), date, amount, check number, memo.
   Foundation checks (CFGV, Raymond James, Fidelity, Schwab, LPL, Jackson,
   IRA custodians) — the DONOR is in the memo/fund line, not the payer bank.

2. **Identify each check** before coding:
   - Open AB invoice for the donor? → note "apply to AB20xx" (see step 4).
   - `INV-000xx` memo → Event Temple invoice payment.
   - Painting/art memo → Gallery sale, NOT a pledge payment.
   - Match against Bloomerang recent transactions and the AES unpaid list.
   - Unidentifiable foundation checks → code to 4040 Unrestricted with
     "donor/purpose TBD" in the description; flag to Brett.

3. **Coding rules** (account ids in the qbo-fix skill):
   | Check type | Account | Entity | Class |
   |---|---|---|---|
   | Arts Ball paddle/gala donation | 101 (4010.12) | `AB - ...` customer (create + parent under 2950 if missing) | 3-Development |
   | General donation | 4040.13 | donor customer | 3-Development |
   | Event Temple INV-xxx | 100.16 | AR - Event Temple (3850) | 2-Programming |
   | Gallery/art sale | 112 (4140.11) | — | 2-Programming |

4. **Invoice-paying checks**: if the donor has an open invoice, do NOT code the
   line to income — Brett receives it against the invoice in the UI, or code to
   the AR account + entity so it nets. Ask if ambiguous; income-coding a check
   that pays an invoice double-counts revenue.

5. **Create the deposit** via direct API (`qbo_auth.py`): DepositToAccountRef
   323 (Operating), TxnDate = today, PrivateNote = "Check deposit M/D/YY - N
   checks $TOTAL", one line per check with description
   `"Check NNN Payer - purpose (AES bid # if any)"`.

6. **Attach every PDF**: POST `{BASE_URL}/upload` multipart per file —
   `file_metadata_01` = JSON `{"AttachableRef":[{"EntityRef":{"type":"Deposit","value":DEP_ID}}],
   "FileName":"check-Payer-amount.pdf","ContentType":"application/pdf"}`,
   `file_content_01` = the bytes. Name files descriptively (payer-checknum-amount).

7. **Report**: deposit slip line — "N items, $TOTAL.00" — plus the coding table
   and any TBD lines for Brett. Remind: when this hits the bank feed, **MATCH
   it to the deposit — never add** (prevents double-booking).
