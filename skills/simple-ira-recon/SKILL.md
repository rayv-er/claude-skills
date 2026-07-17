---
name: simple-ira-recon
description: >
  Apply monthly to reconcile the employee SIMPLE IRA plan: payroll
  withholdings + employer match accrued in QBO liability 2300.16 vs
  American Funds ACH remittances, per-employee tie-out, and deposit-timing
  compliance. Triggers: "ira reconciliation", "IRA liability", "simple ira",
  "did the retirement money go out", month-end close.
---

# Monthly SIMPLE IRA Reconciliation (CFTA)

Plan: **SIMPLE IRA at American Funds** (+ a ROTH option since 7/2026).
Liability: **2300.16 Payroll Liabilities:IRA** (QBO id 366). Expense:
6310.14 Simple IRA - Employer Contribution. Payroll: **Gusto** since the
6/18/2026 check date (QBO Payroll before that). Remittances arrive as
**"PREAUTHORIZED ACH DEBIT AMERICAN FUNDS"** expenditures against 2300.16.

## The identity to prove each month

```
Opening 2300.16 balance
+ employee deferrals withheld this month (all check dates)
+ employer match this month
− American Funds ACH pulls this month
= Ending balance = deferrals not yet remitted (should be ≤ ~1 payroll cycle)
```

## 1. Pull the GL activity

/qbo-fix auth → GeneralLedger report on account 366 for the month
(pattern: this session's scratchpad pull). Two eras, handle both:

- **Pre-6/18/2026 (QBO Payroll)**: per-employee "Payroll Check" lines,
  memo `Simple IRA - Employee Contribution` (employee) and `... - C`
  (Company match). Per-employee recon possible straight from GL.
- **6/18/2026+ (Gusto)**: summary JEs only — memo
  `Benefit Liabilities For Simple IRA` / `For ROTH IRA`. One JE per check
  date, combining employee + employer. No names in QBO.

## 2. Per-employee detail (Gusto era)

The Gusto MCP (`list_payrolls`/`get_payroll`) returns only payroll-wide
totals (`totals.employee_benefits_deductions` + `totals.benefits` — and
those include health, not IRA alone). Per-employee IRA amounts are NOT in
the MCP. Get them from:
1. **Gusto Reports UI** (Brett's Chrome, claude-in-chrome): Reports →
   Payroll journal or Benefits report, CSV per check date; or
2. **American Funds plan sponsor portal** — per-participant deposits
   (ultimate truth for what actually got invested).
Match each Gusto benefit JE in QBO to its check date's Gusto report total
before trusting the summary numbers.

## 3. Tie remittances — the sheet workflow (discovered 7/17/26)

Remittance is MANUAL: Brett emails an "IRA contribution sheet" (.xls,
per-employee, American Funds account numbers) to **Katy Murtaugh
<katym@shondeckfinancial.com>** (Shondeck Financial, Gunnison — also the
health-insurance broker; Gary Shondeck = plan advisor). Katy keys the
contributions; the ACH pull hits 0–2 days later for EXACTLY the sheet
total. Sheets live on Brett's Mac (`~/Desktop`, `~/Downloads`,
`IRA-contribution-YYYY.MM.DD.xls`; template `2026-IRA-template.xls`) and
as Gmail attachments to katym@. Proven ties: 3/3 sheet $13,667.90 → 3/4
ACH; 4/22 → 4/23 $8,781.78; 6/29 → 7/1 $6,724.10.

Each sheet ≈ un-remitted check dates at send time, but NOT exactly —
sheets have included catch-ups (see Drive "Loki IRA catchup") and have
MISSED people (Arvin Ramgoolam: withheld since Jan 2026, never on any
sheet — no American Funds account). Always diff the sheet roster against
the GL/Gusto roster.

## 4. Compliance checks (the point of the exercise)

- **Deposit timing**: DOL safe harbor for small plans = employee deferrals
  deposited within **7 business days** of the check date (IRS outer limit
  30 days after month-end). Flag any check date whose deferrals waited
  longer — May/June 2026 deferrals waited 4–6 weeks (Gusto migration
  disruption); verify the American Funds auto-pull is re-established.
- **Annual limits**: SIMPLE deferral limit per calendar year (+ catch-up
  50+); Brett's $754.17/check ≈ max pace — watch Q4.
- **Match formula**: employer match should track the plan's elected %
  (typically 3% of comp) — spot-check one employee per quarter.
- **Never touch anything before 11/1/2025.**

## 5. Output

Table per check date: date | source (QBO Payroll lines / Gusto JE) |
employee $ | employer $ | remitted via which ACH pull | days-to-deposit |
flag. Plus the month-end identity above proved to the penny, and any
un-remitted balance aged. Escalate: deferrals > 30 days un-remitted, GL
JE ≠ Gusto report total, or a missing monthly American Funds pull.
