# Coaching log

One line per suggestion, so coaching compounds instead of repeating itself. A suggestion that was
declined is not raised again; a suggestion that was adopted becomes the assumed standard and stops being
mentioned. Status is one of: introduced, practising, adopted, declined.

Read this before offering anything. Add to it when something is offered, and update the status when it
changes.

| Date | Curriculum item | Suggestion | Status |
|---|---|---|---|
| 2026-09-22 | 1. State before acting | Before a DELETE or UPDATE, check the table has a key, run it as a SELECT and read the count, keep a copy in the same transaction. Now enforced by the database guard. | introduced |
| 2026-09-22 | 1. State before acting | Diff a deployed file against the local one before overwriting it; the server's copy is sometimes ahead. Now enforced by the deploy guard. | introduced |
| 2026-09-22 | 8. The read-only path | Ask question-shaped things in chat with the tool server rather than opening a session. Six finance tools added so it reaches the finance work. | introduced |
| 2026-09-22 | 2. Branch discipline | The sync repository is on a feature branch, one ahead of the default and eight behind, with 25 uncommitted files. Worth an hour to land or drop. | introduced |
| 2026-09-22 | (agent defect) | Email bodies were hard-wrapped, twice. Fixed in tooling rather than by instruction: email-wrap-guard.py blocks a wrapped body on the mail tools, and brett-prose carries the rule. | adopted |
| 2026-09-22 | (agent defect) | Told Brett the 13:45 inbox triage would reach him, from the file being fixed rather than from the scheduler. It had already run at 07:45, because /etc/cron.d/cfta-sync declares a timezone Ubuntu's cron ignores. Claiming a delivery time needs the job's own last log line, not the crontab's comment. | introduced |
