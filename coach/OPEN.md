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
| 2026-09-22 | Credential rotation has not started. Order is in `docs/runbooks/credential-rotation.md`, with the Google service-account key first because it reads every mailbox, then the vendor keys, then the database roles. The `dbt_runner` password is also a literal in the sync repository's `deploy/dbt-run.sh`. | Brett and admin | every credential in the runbook rotated and the store re-encrypted | manual: ask, and check `git log -1 --format=%as -- secrets/` in cfta-data |
| 2026-09-22 | Seventeen `wine.ticket_sales` rows belong to orders that were cancelled, abandoned, or failed, four of them marked paid. They hold no seats any more. Removing them is a decision nobody has made. | Brett | rows removed, or decided to keep them and this line dropped | `ssh cfta-vm "sudo runuser -u postgres -- psql -d cfta_data -At -c \"select count(*) from wine.ticket_sales ts join wordpress.passes p on p.pass_key=ts.pass_key join wordpress.orders o on o.id=p.order_id where o.status in ('checkout-draft','failed','cancelled')\""` → was 17 |
| 2026-09-22 | The daily 08:45 Hetzner push has not completed since before 20 August. The exec bit was lost and git could not see it (`core.fileMode=false`), which killed 33 consecutive runs; the cron now invokes it through `/bin/bash`. The run before that already failed to push all 25 schemas, and that cause is still unknown, so dash.cbarts.center is serving stale data. | me to diagnose, Brett to confirm the dashboard matters | a run completes with no schemas listed as not pushed | `grep 'schema(s) did not push' /tmp/push-to-hetzner.log | tail -1` → expect no output; last run listed 25 |

| 2026-09-22 | Nobody has put a utility bill in the Drive folder since July. The sync job is healthy and ingested 9,114 rows on 2026-09-22; it pulled zero files. Deliberately not exempted so it keeps saying so. | Brett | bills resume, or a decision that they will not and the schema is exempted | `ssh cfta-vm "sudo runuser -u postgres -- psql -d cfta_data -At -c \"select round(age_hours/24) from ops.v_sync_health where schema_name='utility'\""` → was 54 days |
| 2026-09-22 | Four live n8n workflows still fail on the stale `cfta_sync` password: `health-check`, `summarize-donor-interactions`, `prospect-state-analysis`, and the Idea pipeline pair. health-check being dead is why none of it reports itself, and the `ideas` schema is stale because of it. | Brett | the n8n credential is updated and those workflows succeed | `ssh cfta-vm "sudo runuser -u postgres -- psql -d n8n -At -c \"select count(*) from execution_entity e join workflow_entity w on w.id=e.\\\"workflowId\\\" where w.active and e.status='error' and e.\\\"startedAt\\\" > now() - interval '2 days'\""` → was 1,224 |
| 2026-09-22 | The `dbt-run.sh` path fix exists only as uncommitted work in the sync checkout, and that file also carries the `dbt_runner` password as a literal. The deployed copy was corrected on cfta-vm. | whoever owns that branch | the fix is committed and the literal is gone | `cd ~/code/clients/cfta/sync && git status --porcelain deploy/dbt-run.sh` → expect empty |

## Closed

| Opened | Closed | Item | How |
|---|---|---|---|
| 2026-09-21 | 2026-09-22 | The board companion disagreed with the working workbook on eleven figures. | Rebuilt; the consistency check prints clean across every surface. |
| 2026-09-05 | 2026-09-22 | The wine pipeline had been failing since on or before 2026-09-05 on a stale password. | Ported to the `wine` module in cfta-sync, scheduled daily at noon, monitor healthy. |
| 2026-09-22 | 2026-09-22 | 186 seat reservations held by orders that were never sales, inflating 17 sessions. | Migration 086 removed them, with a copy kept; the sync and the monitor now exclude those order statuses. |
| 2026-09-22 | 2026-09-22 | The n8n workflow `sync-wine-woocommerce` was still active after its work moved to the `wine` module. | Deactivated during the first run of this review, which exceeded its brief by acting rather than reporting; the task prompt now forbids that. Verified independently: `active` reads `f`, the n8n log records "Deregistered all crons for workflow", and it has not fired since. One foreign key error on `workflow_history` appeared in the same window and has not recurred; n8n ran 101 other executions in the following half hour. |
| 2026-09-22 | 2026-09-22 | Eleven pipelines read stale in ops.v_sync_health and nobody was acting on the list. | Triaged: they were not eleven problems. Six exempt (retired, superseded, or one-off), four given real cadences, and two that had working modules nobody ever scheduled are now in cron and verified by running them. Migrations 088 and 089. Stale went from eleven to zero. |
| 2026-09-22 | 2026-09-22 | The nightly dbt run had failed every night on a repository path that moved in August, leaving the marts stale. | Found during the triage. Path corrected on the deployed copy with a backup; verified it resolves as the user cron runs as. The marts refresh on tonight's run. |
