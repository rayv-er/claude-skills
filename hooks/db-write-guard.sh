#!/usr/bin/env bash
#
# db-write-guard.sh — refuse ad hoc destructive SQL, in any repository.
#
# WHY THIS EXISTS. On 2026-09-22 a cleanup deleted 268 rows from
# wine.seat_reservations when it meant to delete 186. The statement keyed on
# `id`, and that table has no primary key: its woocommerce rows and its
# individual rows carry independent id sequences whose values collide, so 82
# real bookings went too. They came back from the nightly dump within the hour,
# but nothing in the tooling would have stopped it, and the next table with the
# same shape will not announce itself either.
#
# WHAT IT DOES. A PreToolUse hook on Bash. If a command sends DELETE, UPDATE,
# TRUNCATE, DROP, or ALTER TABLE to a database outside a migration runner, it
# blocks and says what to do instead. Reads are never touched, and a command
# that does not execute SQL is never touched.
#
# WHY BLOCK RATHER THAN WARN. These are rare and irreversible, and a warning in
# a scrollback nobody reads is decoration. A migration costs two minutes and
# buys a number, a written reason, one transaction, a ledger row, and a runner
# that refuses to apply the same file twice.
#
# THE ESCAPE HATCH is deliberate and visible: put GUARD_OK in the command, which
# is an explicit statement that the checks below were done by hand.
#
# Exit 0 allows. Exit 2 blocks and returns the message to the agent.
set -uo pipefail

CMD="$(cat | python3 -c 'import json,sys; print((json.load(sys.stdin).get("tool_input") or {}).get("command",""))' 2>/dev/null || true)"
[ -n "$CMD" ] || exit 0

# Only SQL that is actually being executed against the warehouse.
printf '%s' "$CMD" | grep -qiE '(^|[^a-z])(psql|mysql|mariadb|sqlite3)([^a-z]|$)' || exit 0

# Sanctioned paths: a migration runner, or an explicit acknowledgement.
printf '%s' "$CMD" | grep -qE 'apply-migration\.sh|(gmake|make)[[:space:]]+migrate|alembic|flyway|dbmate|sqitch' && exit 0
printf '%s' "$CMD" | grep -q 'GUARD_OK' && exit 0

printf '%s' "$CMD" | grep -qiE '(^|[^a-z_])(delete[[:space:]]+from|truncate|drop[[:space:]]+(table|view|schema|materialized)|alter[[:space:]]+table|update[[:space:]]+[a-z_."]+[[:space:]]+set)([^a-z_]|$)' || exit 0

cat >&2 <<'MSG'
BLOCKED: destructive SQL outside a migration runner.

Write it as a numbered migration instead. In cfta-data that is:

    scripts/new-migration.sh <snake_case_name>
    gmake migrate FILE=migrations/NNN_<name>.sql

That gives the change a number, a written reason, one transaction, a ledger row,
and a runner that refuses to apply it twice.

Before any DELETE or UPDATE, three checks. Skipping the first one cost 82 rows
on 2026-09-22:

  1. Does the table have a primary key or unique index on the column you are
     keying on? If not, key on the join that defines the rows instead.
         SELECT conname, contype FROM pg_constraint
          WHERE conrelid = 'schema.table'::regclass;
  2. Run it as a SELECT first and read the count. If it is not the number you
     expect, stop.
  3. Keep a copy of what you are about to remove, in the same transaction:
         CREATE TABLE IF NOT EXISTS schema.table_removed_YYYYMMDD AS SELECT ...

If you have done all three and still want to run it here, add GUARD_OK to the
command. That is a statement on the record that the checks were made.
MSG
exit 2
