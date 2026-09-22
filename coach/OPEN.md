# Open items

Things handed back and not yet closed. One line each, with an owner, the date it opened, what closing it
looks like, and where possible a command that answers "is this still open" without asking anyone.

The rule that makes this worth keeping: **an item leaves this list by being done or by being decided
against, and both are closures.** An item nobody will ever do, left open, is what turns a list like this
into noise. Move it to Closed with `dropped` and the reason.

Reviewed every Monday morning by the `coach-open-items` scheduled task, which runs the verify commands,
closes what it can prove is done, and reports only what is genuinely still open.

## Open

| Opened | Item | Owner | Closed when | Verify |
|---|---|---|---|---|
| 2026-09-22 | The n8n workflow `sync-wine-woocommerce` is still active although it was deactivated in the interface. Its work moved to the `wine` module, so it only errors every six hours. | Brett | `active` reads false, or the workflow is deleted | `ssh cfta-vm "sudo runuser -u postgres -- psql -d n8n -At -c \"select active from workflow_entity where id='Gw1fSCbgey3ICOc1'\""` → expect `f` |
| 2026-09-22 | Credential rotation has not started. Order is in `docs/runbooks/credential-rotation.md`, with the Google service-account key first because it reads every mailbox, then the vendor keys, then the database roles. The `dbt_runner` password is also a literal in the sync repository's `deploy/dbt-run.sh`. | Brett and admin | every credential in the runbook rotated and the store re-encrypted | manual: ask, and check `git log -1 --format=%as -- secrets/` in cfta-data |
| 2026-09-22 | Eleven pipelines read stale in `ops.v_sync_health`. Several may only need their threshold cleared rather than a fix; `bar` at 310 hours feeds bar cost of goods and the sales-tax carve-out. | Brett to triage, then me | the stale count is what you meant it to be, with thresholds set deliberately | `ssh cfta-vm "sudo runuser -u postgres -- psql -d cfta_data -At -c \"select count(*) from ops.v_sync_health where status='stale'\""` → was 11 |
| 2026-09-22 | Seventeen `wine.ticket_sales` rows belong to orders that were cancelled, abandoned, or failed, four of them marked paid. They hold no seats any more. Removing them is a decision nobody has made. | Brett | rows removed, or decided to keep them and this line dropped | `ssh cfta-vm "sudo runuser -u postgres -- psql -d cfta_data -At -c \"select count(*) from wine.ticket_sales ts join wordpress.passes p on p.pass_key=ts.pass_key join wordpress.orders o on o.id=p.order_id where o.status in ('checkout-draft','failed','cancelled')\""` → was 17 |

## Closed

| Opened | Closed | Item | How |
|---|---|---|---|
| 2026-09-21 | 2026-09-22 | The board companion disagreed with the working workbook on eleven figures. | Rebuilt; the consistency check prints clean across every surface. |
| 2026-09-05 | 2026-09-22 | The wine pipeline had been failing since on or before 2026-09-05 on a stale password. | Ported to the `wine` module in cfta-sync, scheduled daily at noon, monitor healthy. |
| 2026-09-22 | 2026-09-22 | 186 seat reservations held by orders that were never sales, inflating 17 sessions. | Migration 086 removed them, with a copy kept; the sync and the monitor now exclude those order statuses. |
