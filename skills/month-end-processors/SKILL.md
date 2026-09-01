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

**Deferred sweep (MANDATORY, added 2026-08-30):** before closing the month,
pull the FULL ledger of 2100.11 Deferred Revenue:Ticket Sales and release
EVERY line whose event occurred on or before month-end — from ANY platform,
not just Humanitix. The Humanitix engine only releases its own events;
Stripe-side deferrals (e.g. `2026-07-highnote-def`) and one-off Deposits
slip through. Lesson: High Note Tour de Fork 27,900 (event 8/6) and a
150.00 Azaria deposit (event 12/27/25) sat unreleased until the 8/31 sweep
(JE 2026-08-defrel, Id 34483). Release mirrors the deferral's structure
(High Note was 50/50 Earned 104 / Contributed 96 per the W+FF split).
After the sweep, every remaining 2100.11 dollar must belong to a FUTURE
event; decompose and note the per-event remainders in the close memo.
Snapshot caveat: the month-end JE is built from the morning warehouse
sync, so orders placed after the snapshot are deferred one month late —
the cumulative recompute self-corrects, but note the gap if issuing
statements (8/31/26: ≥1,135 late).

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
50/50 Earned 104 / Contributed 96, entity+class per the festival. **The 50/50
fundraiser-ticket split is CBO-set policy (affirmed 2026-08-30) — apply it,
never re-derive it from FMV math. FY25 used 35.6%, so line-level YoY needs an
on-paper FY25 restatement (~36K), not an FY26 change.** True-up the
prior month's pre-posted catch JE.
Target: 1610 balance ≈ Stripe pending (~2 days of payouts). Note: only ONE of
two Stripe accounts is synced — check both if the residual is off.

**CASH CUTOFF — run the ET payment list to the LAST DAY of the month**
(added 2026-08-31). Never cut at a mid-month payout date: JE 34438 stopped
at 8/19 and stranded 12,072.00 of ET Stripe receipts with no QBO landing
on either side (fixed by JE 34490 `2026-08-stripe-cutoff`). The cutoff
entry mirrors the ET cash-application template with ONE difference:

- Dr 1610 net + Dr 1018 Stripe fees (derived) — same as always;
- **Cr 2100.12 / 2400 by customer, NOT AR:Event Temple.** The monthly
  `YYYY-MM-temple` gross-up trues AR:ET to the ET OPEN book, so fully-paid
  invoices are already excluded from it — crediting AR drives it negative.
  Guard the entry: abort if AR:ET has moved off the gross-up figure.
- Split deposit content to 2400 per §3.8's component map.

Fee derivation when the payouts are not yet booked: ET carries no fee
data and the main CFTA Stripe account is not in the warehouse, so derive
at the effective rate observed on the SAME rail that month (JE 34438:
812.68 / 23,619.75 = 3.441%), not a generic 2.9% + $0.30 — and memo it as
derived pending true-up. Assertion: ET payments for the month with no QBO
landing must be ZERO.

## 3. Clover — batch tie-out (deposits are GROSS, no fee netting)

Bar JEs (per event, Payment Method lines) debit 1100.14 gross incl. card
tips; Clover "BANKCARD-8600 BTOT DEP" deposits arrive at FULL GROSS 1-3
days later — fees are NOT netted from deposits (verified June 2026: every
batch tied to the penny). Fees bill separately: "BANKCARD-8600 MTOT DISC"
ACH debit on the 1st (prior month's processing fees, e.g. 7/1 $3,626.44
for June) + mid-month "CLOVER FEES" SaaS debit — both code straight to
Processing Fees from the feed. So month-end 1100.14 work is a BATCH
TIE-OUT, not a fee accrual: match each event's card total to its BTOT DEP
(batches can split across days — a 5/29-30 batch settled 987.85 on 6/1 +
1,192.85 inside a 6/8 deposit); residual should be settlement-lag only.
A stubborn residual usually means a miscoded JE line — Cash lines go to
Bar Banks (acct 73), Debit/Credit Card lines to 1100.14 with entity
AR - Clover (2917); three June 2026 JEs had them swapped. Optional
strict-accrual: Dr fees / Cr 2030 at month-end for the coming MTOT DISC,
reverse on the 1st.

**Tips Payable check**: after each payroll the balance should be ~0 (only
undistributed recent pools remain). Nightly bar JEs accrue CC tips only; the
22% dev-comp gratuities accrue via /tips Step 4 (`tipcomp-YYYYMMDD`: Dr 322
Tips Paid / Cr Tips Payable, cls 3 - Development). A negative balance means a
comp gratuity was paid without its accrual — see the FY26 audit
(cfta/data docs/tips-payable-audit-fy26.md, corrected by JE 34448 at 8/31).

## 3.6 Bar sales-tax carve-out (standing month-end step, added 2026-08-30)

The bar rings tax-inclusive and the nightly bar JEs book gross sales, so
every month needs a carve-out JE or 2500 Sales Tax Payable drifts negative
as remittances hit it. Doc `YYYY-MM-bartax`, dated month-end:

```
Dr  Earned Revenue:Bar Income:Bar Sales     (tax component)
    Cr  2500 Sales Tax Payable (Id 259)     same
```
Class `2 - Programming` on both lines.

**Amount**: rate is 9.4% combined on tax-inclusive sales — carve-out =
taxable bar sales x 9.4/109.4 (Town of CB 4.5% remitted direct; CO
DOR-administered 4.9% covers state+county). Filings happen ~20th of the
following month; when the filed amounts are known, true the JE to actuals
(origin-month policy: edit the month's JE while the period is open).
Cross-check the split: Town/State payment ratio runs ~0.92.

**Feeds and offsets**: the ACH debits ("CO DEPT REVENUE TAXPAYMENT",
"TownofCrestedBut PURCHASE") code straight to 2500 from the bank feed.
Alpenglow food-vendor tax checks collected by CFTA also credit 2500 on
deposit — net them against that month's carve-out (June 2026 precedent:
826.70).

**Health check**: after the prior month's payments clear, 2500 should equal
just the current month's accrual. A debit balance means a missed carve-out;
a growing credit means a missed filing. History: Nov 2025–Jul 2026 were
back-filled 2026-08-30 (JEs 34466–34473, sized to actual remittances; see
cfta/data docs/bar-sales-tax-carveout-2026-08-30.md).

## 3.7 Payroll event attribution + Gusto reclass (standing, added 2026-08-30)

Monthly JE `YYYY-MM-evtstaff` dated month-end (continues the Nov-Apr series;
May-Aug 2026 back-filled as JEs 34475-34478). NO classes on any line
(payroll is classless by design; functional allocation stays at reporting).

Build from Homebase: clocked timecards intersected with shift windows
(the /tips cross-timecard join) x `timecards.wage_rate`, grouped by
role -> sub-account and event -> QBO customer:

- 6330.11 Bar: Bartender, Bar Lead, Barback, floaters, gala bartenders
- 6330.14 Event: Event Staff, EventStaff/Security, Event Captain,
  Hospitality, Merch, Security Lead, Arts Ball Setup/Breakdown
- 6330.19 Rentals: Amanda Bade (EM) | 6330 parent: Rebecca Vehik (EM)
- 6330.20 Set Up / Transition: Setup/Breakdown, Theater Transition,
  Setup Crew Lead, W+FF set-up crews
- 6330.21 Tech | 6330.22 Tipped: W+FF service/wine/BOH/seminar crews
- excluded: `homebase.non_event_roles` (Training, Facility, Programming,
  Sales, Operations, Bar Prep/Inventory, Marquee)

JE shape (Gusto era): Dr subs per event (entity = event customer;
no-entity rows for unmapped hours) + Dr 6350.12 Salaried Pay (salaried
regular by check month: gross less fixed comps less PTO-hours x
annual/2080) / Cr 6300 Payroll lump. OT pair inside 6330.17: per-event
debits pro-rata to event cost vs one no-entity credit (monthly OT from GL).

**CHECK-DATE basis (CBO directive 2026-08-30):** group hourly shifts by
the month of the paycheck that pays them, not the month worked. Gusto is
biweekly; map each shift date through the pay-period calendar (period end
+ 5 days = check date, e.g. 6/1-6/14 -> 6/18 check -> June JE;
8/10-8/23 -> 8/28 -> August). Shifts after the last period end of the
month DEFER to the next month's JE (they are in next month's lump).
This matches the FY25 QBO-payroll methodology (expense on check date) and
guarantees each month's Cr never exceeds that month's actual Gusto lump —
the 6300 parent must stay >= 0 in every month after the JE posts (the
residual is non-event roles + Homebase-vs-Gusto wage variance). The
work-month cut used originally left June 2026 at -8,553 and was re-cut
2026-08-30 (Jun/Jul/Aug lump credits 33,432.01 / 141,480.64 / 87,446.85;
2,164.96 of 8/24-8/31 shifts deferred to the September JE).

Gusto already posts Holiday->6340.14, Sick->6340.16, Vacation->6350.13,
and OT->6330.17 on check dates; no reclass needed for those. Reference
build: cfta/data scripts/qbo/qbo_evtstaff.py (original attribution logic)
+ qbo_evtstaff2.py (check-date regrouping — use this shape going forward).

## 3.8 Rentals recognition (standing, added 2026-08-31)

**ONE JE per month**, doc `YYYY-MM-rentals`, dated month-end (June 2026's
pair was merged and 33733/33734 deleted 2026-08-31 — never run parallel
series again). Dr 2100.12 Deferred Revenue:Rental Fees / Cr per-event
lines, class 2 - Programming:

- 4150.13 facility/venue + 4150.15 staffing fees, per EVENT-MONTH (never
  cash month; future-event cash stays in 2100.12 — the Robson lesson).
- 4110.12 Hosted Bar Sales at ET BASE (pre-tax, pre-gratuity); 4110.13
  only for genuinely-kept fees (Mobile Bar Setup, Custom Cocktail,
  Special Alcohol Order). The 22% client gratuities are NEVER revenue —
  they fund tips via Tips Payable (/tips Step 4 + settlement rail).
- Exclude refundable security deposits and ET-billed sales-tax components.
- Build from eventtemple invoices/line_items (events held that month);
  descriptions `YYYY.MM.DD - Event - what (ET INV-000xx)`.
- **Every revenue line carries Entity = Customer** (the CBO pulls a P&L
  by Customer). Assignment rule, in order: (1) the customer on the QBO AR
  doc for that event; (2) the customer matching the ET account; (3) the
  existing `Events:YYYY.MM.DD - Name` job; (4) the person record matching
  the ET contact; (5) only then create. SEARCH THE FULL customer tree
  (all parents, inactive included, aliases/emails) before any create —
  two proposed creates in the 2026-08-31 pass were duplicates found only
  by email match. Recurring renters (School of Dance, Wild Hare, Life
  Drawing, Trailhead, PPF, MetRec) use ONE customer across months.
  Genuinely unattributable amounts go to `General:General Rentals`
  (3260), never blank — that keeps them out of "Not Specified" and makes
  them visible FYE true-up items.
**SPLIT EVERY ET INVOICE INTO COMPONENTS before anything touches 2100.12**
(added 2026-08-31 after 11,025 of refundable deposits were found buried in
deferred revenue; JE 34489 fixed it). 2100.12 is the RESIDUAL bucket for
genuine future-event rental revenue only — nothing lands there by default:

| ET component | Goes to |
|---|---|
| Refundable security / alcohol deposit | **2400** (Id 266) — never 2100.12, never released to income |
| Facility, staffing, add-ons, incidentals | 4150 family, EVENT month |
| Hosted bar consumption | 4110.12 at BASE (divide the ET total by 1.22) |
| Kept/retained bar service fee | 4110.13 |
| 22% client gratuity | Tips Payable rail; or 4110.14 Tips Received as the recovery leg where Tips Paid is already accrued |
| Sales tax 9.4% | 2500 **parent** (Id 259) — 2500.11/.12 are QBO tax-agency accounts and REJECT journal entries |
| Everything else | 2100.12 |

Deposit mechanics: CREDIT 2400 when billed or collected, whichever first;
DEBIT 2400 when the ET invoice shows a negative deposit line (applied) or
a refund is paid. Roll forward per customer — opening + collected −
applied − refunded = closing — and that roll-forward IS the 2400
supporting schedule.

TWO root causes to keep fixed: (1) QBO item 4 'Facility Rental Deposit'
and item 45 'Alcohol Deposit' post to 2100.12 while item 35 posts to 2400,
and every connector receipt/refund uses item 4 — repoint them; (2) since
2026-05-29 ET cash lands directly in AR:Event Temple and the monthly
temple gross-up credits it wholly to 2100.12 BY CONSTRUCTION — **splitting
the gross-up credit is the real control**, the item fix alone is not
enough.

- Cross-check after posting: monthly 4110.12 must equal the ET bar base
  for events held that month; 2100.12 must never be drawn below the
  collected-cash + AR gross-up attributable to recognized events; 2400 by
  customer must equal the ET held-deposit roll-forward; no ET line with
  revenue_category 'Security Deposit' may appear in any 2100.12 posting;
  and ET payments for the month with no QBO landing must be ZERO (run the
  cash cutoff to the LAST day of the month — an 8/19 cutoff stranded
  20,872 in August).
- The `YYYY-MM-temple`/`-temple-clr` AR gross-up pair re-trues 100.16 vs
  the ET open book (see the stripe-clearing-recon skill §4.3).

## 4. FYE (10/31) extras

- 1100.15 negative at 10/31 (fall presales paid out early) → present as
  2100.11 Deferred, reversing 11/1.
- Never touch anything before the prior 11/1.
