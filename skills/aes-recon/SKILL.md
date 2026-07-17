---
name: aes-recon
description: >
  Apply for Auction Conductor (AES) event reconciliation: tying CC deposit
  batches to the bank, extracting balance-due lists, building supporting docs,
  tracking AuthOnly captures. Triggers: "reconcile the [event] payments",
  "AES", "auction conductor", "who still owes from the ball", post-event
  wrap-up emails from AES (David Bolding).
---

# AES / Auction Conductor Reconciliation (CFTA)

Site: auctionconductor.com (use Brett's logged-in Chrome via claude-in-chrome;
account shows as Jillian Liebl). AES rep: David Bolding, david.bolding@aesauctions.com.

## Money model (from the Datacap how-to)

- Each CC settlement batch gets a **Deposit ID**; its net (fees pre-deducted)
  arrives as an "AES FUNDING" ACH — match Deposit ID net total to the bank
  credit exactly.
- Status path: Approved → In Queue → Funded (2 business days); statuses sync
  once daily. **AuthOnly** = authorized, NOT captured — auths expire ~7 days;
  capture via "Apply to Accounts" (password-protected) in the Payments tab.
- QBO coding of an AES FUNDING deposit: donor gross lines to 101 (or apply to
  AB invoices if invoiced) + one negative fee line; fee = gross − net residual,
  never sum of per-txn fees (float drift).

## Data extraction tricks

- **Payments grid** is AG Grid: columns virtualize — row text scrapes come back
  empty; use per-cell `[col-id=...]` queries or filter the Status dropdown
  (select value 11 = Auth Only) and screenshot.
- **Invoice Summary report** (Reports → Post Event Reports → Invoice Summary)
  renders in PDF.js — extract all pages via
  `PDFViewerApplication.pdfDocument.getPage(i).getTextContent()` in the
  dialogIframe. Strip emails/phones before returning (data filter).
  Parse `#bid Name ... BALANCE DUE $x` per bidder.
- **Sale/Payment CSV export** (Post Event Reports) = sales-side join; its
  per-deposit totals differ from the Payments grid (drops cover-my-fees rows).
  The GRID is bank-authoritative.
- Edit Payment modal lives in `#dialogIframe`; buttons only clickable via JS
  inside the iframe. The Continue→Yes flow EDITS payment details — it does NOT
  capture charges.

## Standard jobs

1. **Deposit batch tie-out**: per Deposit ID — transactions, gross, fees, net;
   verify net = bank ACH; build/refresh the reconciliation artifact.
2. **Balance-due → AR**: extract per-bidder balances (total must equal the
   "N Unpaid Bidders Owe $X" header), cross-check payments received elsewhere
   (use /donor-paid), then build AB invoices per /qbo-fix conventions.
   Watch households: AES bills one member; pick the AB household record.
3. **AuthOnly watch**: list pending auths with dates; warn before expiry;
   after capture, expect a new Deposit ID settling in ~2 days and apply the
   funding deposit against the AuthOnly-tracker invoices.
4. **Wrap-up package** (zip from David): the "UNPAID guests" xlsx is
   authoritative for billing person + amounts; reconcile against our AR list
   to the penny before trusting either.
