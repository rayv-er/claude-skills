---
name: month-end-processors
description: >
  Apply at month end (and the 10/31 FYE) to build/true-up the Humanitix,
  Stripe, and Clover processor entries in QBO from platform data. Triggers:
  "month end", "close [month]", "true up the humanitix/stripe JE",
  "processor recon", start of a new month.
---

# Month-End Processor Close (CFTA)

The processor model reconciled 2026-07-16 (see memory: qbo-processor-clearing-model).
Fiscal year Nov 1–Oct 31. All data from `mcp cfta-data run_sql` /
`ssh cfta-vm "sudo runuser -u postgres -- psql -d cfta_data"`.

## 1. Humanitix — two JEs (mirror docs: 2026-06-humanitix, 2026-07-humanitix-def)

**JE B — recognition** (`YYYY-MM-humanitix`, dated month-end):
Dr 1100.15 (entity AR - Humanitix 1978) / Cr ticket income by program.
Amount = **online-channel ONLY** net sales for events occurring that month:
```sql
SELECT e.name, ROUND(SUM(o.net_sales)::numeric,2)
FROM humanitix.orders o JOIN humanitix.events e ON e.id=o.event_id
WHERE date_trunc('month', e.start_date) = 'YYYY-MM-01'
  AND o.sales_channel != 'manual'
  AND COALESCE(o.status,'') NOT IN ('cancelled','refunded')
GROUP BY e.name;
```
NEVER include `sales_channel='manual'` (tables/comps paid by check — their cash
is coded on deposit; including them double-counts revenue, $95K lesson 7/16).
For events already deferred (JE A below), the debit for that slice is
2100.11 Deferred, not AR.

**JE A — deferral** (`YYYY-MM-humanitix-def`): Dr 1100.15 / Cr 2100.11 Deferred
= this month's NEW online net sales for FUTURE-month events (same query with
`o.order_date` in the month and `e.start_date` after month-end).

**True up pre-posted JEs**: the current month's JEs are often pre-posted mid-month
("thru M/D — update at month end" in the memo) — recompute and edit amounts.

**Applications**: generate the $0-payment FIFO schedule (JE debits vs payout
deposits) — the API cannot write deposit-credit applications; hand Brett the
schedule to click in the UI (pattern: scratchpad humanitix_apply.py).

## 2. Stripe — connector completeness check

The connector books each charge as SalesReceipt (Dr UDF / Cr 449 Deferred) and
sweeps payouts; recognition at festival by JE (e.g. 2026-07-wff-recognize).
Every "STRIPE TRANSFER" ACH codes to **1610 Stripe Clearing** — never AR.

Gap check (charges the connector missed):
```sql
-- QBO receipt pi ids: from SalesReceipts' "Transaction ID: pi_..." descriptions
-- vs stripe.payment_intents. Missing set = catch-up JE.
```
Catch-up JE (`YYYY-MM-stripe-catch`, ≤21 chars): Dr 1610 net + Dr 1018 Stripe
fees / Cr 449 Deferred (gross). Recognition companion moves Deferred → income
50/50 Earned 104 / Contributed 96, entity+class per the festival. True-up the
prior month's pre-posted catch JE.
Target: 1610 balance ≈ Stripe pending (~2 days of payouts). Note: only ONE of
two Stripe accounts is synced — check both if the residual is off.

## 3. Clover — fee accrual

Bar JEs (per event, Payment Method lines) debit 1100.14 gross incl. tips;
Clover deposits credit it net of fees. Month-end: book
Dr credit-card fees / Cr 1100.14 for the accumulated fee residual so the
account returns to ≈ settlement-lag only. Verify July-style timing gaps
(JEs pending vs deposits landed) before calling a residual "fees".

## 4. FYE (10/31) extras

- 1100.15 negative at 10/31 (fall presales paid out early) → present as
  2100.11 Deferred, reversing 11/1.
- Never touch anything before the prior 11/1.
