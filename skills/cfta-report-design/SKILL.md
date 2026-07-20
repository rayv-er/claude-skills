---
name: cfta-report-design
description: >
  Apply when building or restyling any CFTA branded document: finance
  committee reports, board packets, one-pagers, or PDF deliverables.
  Triggers: "finance report", "committee report", "make it on brand",
  "brand guidelines", "rebuild the report", monthly reporting cycles.
  Contains the full brand design system, embedded fonts/logo, and the
  working finance-report builder.
---

# CFTA Report Design System

Distilled from the CFTA Brand Guidelines 2025 + Brett's directives
(July 2026 Finance Committee report build). The working builder and all
embedded assets live in `assets/` beside this file.

## Brand system (Brett-confirmed variants)

**Colors**
- Body text near-black `#1c1c1c`; headings pure black.
- **Dominant accent: royal navy `#0A3A82`** (sampled from the brand
  pattern set's `#003A8B`/`#023C8C` family). Brett explicitly prefers
  navy-dominant over the brand teal (`#016469`/`#014134`) and sunshine
  (`#FED208`) for finance documents.
- Cerise `#A7182F` ONLY for unfavorable/negative callouts.
- Tints: backgrounds `#f2f6fb` / `#eef3fb` / `#f4f7fc`, borders
  `#d5e0f0` / `#c2d2ec`.

**Typography — two roles, never a third**
- **Flama Condensed** (Black/Bold/Book, embedded as base64 OTF):
  everything that LABELS — h1/h2/h3, table headers (`tr.hd`), KPI
  labels, eyebrows. Uppercase + letter-spacing on structural labels.
- **IBM Plex Serif** (Reg/Semi, embedded): everything you READ **and
  every numeral** — body, table figures, KPI values — always with
  `font-variant-numeric: tabular-nums`.
- **NO monospace ever** (Libertad Mono is in the brand kit but Brett
  banned it from reports: "i dont want to use monotype fonts").
- Sizes via classes, not inline: body 9.5px, `.note` 8.5px `#555`,
  `.tcap` 8px Flama uppercase navy caption, `.fine` 7.5px `#999`.

**Layout**
- Letter, `@page` margins 0.55in / 0.65in, print via headless Chrome.
- Header: square `center_main_logo.png` (embedded b64) left, Flama
  masthead, uppercase sub, 3px black rule.
- `h2` uppercase, 2px black bottom border. `.lede` intro boxes: navy
  4px left border on `#f2f6fb`. `.kpis` = 4 flex cards per row.
- Table classes: `tr.hd` (uppercase Flama header, 1.5px black rule),
  `tr.b` (bold subtotal, `#eef3fb` fill), `td.n` (right-aligned serif
  tabular numerals), `.pb` page break.

## The builder

`assets/build_report.py` — self-contained f-string generator
(fonts + logo embedded; ~630KB). Emits `finance_report_v2.html`.

```bash
python3 build_report.py
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="$HOME/Downloads/<date> - Finance Committee - Report.pdf" \
  "file://$PWD/finance_report_v2.html"
```

GOTCHA: the HTML is one big Python f-string — any literal CSS/JS `{}`
inside it must be doubled `{{}}`. The @font-face block is already
escaped; keep new CSS braces doubled.

## Report structure (July 2026 edition — the approved shape)

Executive Summary (lede + Arts Ball block + Favorable/Unfavorable
bullets, vs-budget then vs-prior-year, Cash & Balance Sheet, Other
Updates) → Statement of Activities (KPI cards + 7-col table) →
Statement of Financial Position (parent lines only — no cash/AR
sub-lines) → Statement of Cash Flows w/ YoY → Programming Planned vs
Actual (+ per-event Bar column + consolidated direct P&L) → Bar &
Concessions (full-year GL + POS ops + Alpenglow YoY) → Rentals (budget
line items from the workbook's Rental Schedule tab + forward pipeline
breakouts incl. FY27 contracted) → Donor Intelligence (aggregate only:
pyramid, retention, concentration + CRM-completeness bridge) →
Forward-Looking Outlook.

## Data conventions (see memory files for full detail)

- Budget = QBO Budget object "FY26 - Consolidated" id 1000000031,
  phased monthly — sum actual months, never prorate
  (memory: qbo-fy26-budget-source).
- Prior-year comparability: restate FY25 W+FF recognized-as-sold
  revenue out of YTD columns; never touch FY25 books
  (memory: wff-recognition-restatement).
- Arts Ball spans 4010 full-year + 4140.13 + 4030.12; 4010.13 in July
  is WFF, never AB (memory: arts-ball-revenue-structure).
- Donor section: aggregates only — no names, no wealth detail in
  emailed documents; $25k+ pyramid band = Front Row installment
  timing. CRM counts are floors (entry backlog vs books).
- Tone: Brett/Bob Valentine style — condensed chart of accounts,
  "Total Net Revenue" bottom line, accrual basis, Favorable/
  Unfavorable narrative bullets, no dashes in emails.

## Sibling builders

`assets/build_strategy_report.py` — the Strategic Plan KPI Report
(7-page mid-year edition + single-page scorecard). It extracts the
style block and STEDDY/SEAT/ROOF/mark assets from build_report.py at
build time, so restyling build_report.py restyles both reports. Data:
strategy.v_kpi_scorecard + the plan workbook's mid-year checks; update
the values in the section strings on refresh.

`assets/build_programming_report.py` — the Programming Report
(finance x strategic plan blend: per-event P&L, consolidated direct
contribution, audience/experience KPIs, plan-alignment matrix, forward
book with presales). Same extraction pattern; adds .aligntbl for
multi-line prose tables.

`assets/build_operations_report.py` — the Operations Report
(cost & labor discipline, bar operations, facility & building
utilization, people & plan alignment). Same extraction pattern.

## Refresh cadence

Each month: update the A/B/P dicts from QBO (actuals + budget object +
prior-year on the restated basis), balance-sheet dicts, and the
narrative numbers; rebuild; verify page-by-page before sending.
