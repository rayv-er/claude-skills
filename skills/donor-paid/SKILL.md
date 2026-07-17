---
name: donor-paid
description: >
  Apply when answering "did [donor] pay?" or reconciling a donor's pledges,
  tables, tickets, and payments across systems. Triggers: "did X pay",
  "is X reconciled", "what does X owe", "where is X's payment", donor names
  with amount questions.
---

# Donor Payment Lookup (CFTA)

Answer with EVIDENCE from every system a payment can hide in. One system is
never enough — the expensive lessons (Brown's "payment" was a painting; the
$11,800 "Ramsden" check was the King Family Foundation; McNeill pre-paid in
March) all came from cross-checking.

## Check sequence (all via mcp cfta-data run_sql unless noted)

1. **Bloomerang** — received money:
   `bloomerang.transactions JOIN constituents` by last name, date/amount/method.
   Caution: names can be misattributed; foundation checks may log under the
   signer or fund, not the donor.
2. **QBO invoices** — open AR: MCP `qbo_sales_get_invoices` (AB- customer) or
   `qbo.transactions` (local sync, line-level, daily 6:15 AM — may lag today).
3. **QBO deposits** — direct-coded money: scan deposit lines by entity name /
   description via API (local sync lacks most deposit-line detail).
4. **Humanitix** — `humanitix.orders` + `events`: CHECK `sales_channel` —
   `manual` orders are recorded-but-paid-by-check (tables, comps); `online`
   is real card money that arrives via payouts.
5. **AES** (if event-related) — balance due / payment status: /aes-recon.
6. **Email intent** — `workspace.gmail_messages` (jillian@ and brett@) for the
   donor's name: "will send check from IRA", "via my donor advised fund",
   "do not charge my card", wire confirmations. Full bodies on cfta-vm volume.

## Known patterns

- **Pre-payment**: major donors fund pledges MONTHS early (Feldberg $100K Jan,
  Popper $10K Mar, McNeill $30K Mar, Hogue-style). A pre-event payment matching
  a pledge amount is likely the pledge — but confirm with Brett before
  invoicing or waiving.
- **Households**: AES/QBO may bill either spouse (Kathy vs Clif Barnhart,
  Dalynn Trujillo vs Becky Frey); search both names + the AB household record.
- **DAF/foundation payers**: money arrives under GHCF/Fidelity/NPT/Vanguard/
  CFGV/Raymond James names — search the fund name AND the donor name.
- **Same-name traps**: verify amounts AND memos (Scott King ≠ Scott Ramsden).
- **Payment ≠ this pledge**: check memos ("Patrick Duke painting", "Table and
  Pass") before crediting a payment against a paddle raise.

## Output

Verdict + evidence table: what they owe (each pledge/purchase with source),
what's been received (date/method/where it landed in QBO), what's in transit,
and the net position. Cite transaction ids/DEP numbers so Brett can click in.
