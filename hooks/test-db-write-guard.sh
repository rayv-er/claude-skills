#!/usr/bin/env bash
#
# test-db-write-guard.sh — feed db-write-guard.sh known commands and check the verdict.
#
# Each case is a Bash command wrapped in the PreToolUse JSON the hook reads on
# stdin. "allow" expects exit 0, "block" expects exit 2. Exits non-zero if any
# case disagrees.
#
# Usage: hooks/test-db-write-guard.sh   (HOOK=path to test another copy)
set -uo pipefail

HOOK="${HOOK:-$(cd "$(dirname "$0")" && pwd)/db-write-guard.sh}"
fail=0
n=0

check() {
    local want="$1" name="$2" cmd="$3" json code got
    json="$(CMD="$cmd" python3 -c 'import json,os; print(json.dumps({"tool_name":"Bash","tool_input":{"command":os.environ["CMD"]}}))')"
    printf '%s' "$json" | "$HOOK" >/dev/null 2>&1
    code=$?
    case "$code" in
        0) got=allow ;;
        2) got=block ;;
        *) got="exit $code" ;;
    esac
    n=$((n + 1))
    if [ "$got" = "$want" ]; then
        printf 'ok    %-5s  %s\n' "$want" "$name"
    else
        printf 'FAIL  want %s, got %s  %s\n' "$want" "$got" "$name"
        fail=$((fail + 1))
    fi
}

# The false positive from 2026-09-23.
check allow "grep over push-to-hetzner.sh (2026-09-23)" \
    "cd ~/code/clients/cfta/data && grep -n 'replace\|DROP SCHEMA\|drop schema\|pg_dump\|pg_restore\|psql\|ON_ERROR_STOP\|--clean\|if-exists\|reported an error' scripts/push-to-hetzner.sh | head -40"

# The three real cases that must stay blocked.
check block "ssh runuser psql -c DELETE" \
    "ssh cfta-vm \"sudo runuser -u postgres -- psql -d cfta_data -c 'DELETE FROM x.y WHERE id = 1'\""
check block "psql heredoc DROP TABLE" \
    "psql -d cfta_data <<'SQL'
BEGIN;
DROP TABLE wine.seat_reservations;
COMMIT;
SQL"
check block "ssh docker exec psql -c TRUNCATE" \
    "ssh host \"docker exec cfta-postgres psql -U postgres -d cfta_data -c 'TRUNCATE wine.orders'\""

# Readers that mention the words.
check allow "rg for DELETE FROM near psql" "rg -n 'psql.*DELETE FROM' scripts/"
check allow "git log --grep" "git log --oneline --grep='psql DROP TABLE'"
check allow "sed -n over a migration" "sed -n '1,40p' migrations/012_drop_table_psql.sql | grep -i 'alter table'"
check allow "cat piped to head" "cat notes.txt | grep psql | grep 'TRUNCATE'"

# Readers must not hide a real write next to them.
check block "grep then psql on the same line" "grep -c x f.sql; psql -c 'DELETE FROM a.b'"
check block "grep then psql on the next line" "grep -c x f.sql
psql -c 'DELETE FROM a.b'"
check block "psql inside grep's command substitution" "grep x \$(psql -Atc 'DELETE FROM a.b RETURNING id')"
check block "psql inside backticks in grep" "grep x \`psql -Atc 'DELETE FROM a.b RETURNING id'\`"
check block "cat heredoc piped to psql" "cat <<'SQL' | psql -d cfta_data
UPDATE wine.orders SET status = 'x';
SQL"
check block "echo piped to psql" "echo 'DROP SCHEMA staging CASCADE' | psql"
check block "unparseable quote falls back to blocking" "grep \"it's\" f; psql -c \"DELETE FROM a.b\" 'unclosed"

# Unchanged behavior.
check allow "plain SELECT" "psql -d cfta_data -c 'SELECT count(*) FROM wine.orders'"
check allow "GUARD_OK override" "psql -c 'DELETE FROM a.b WHERE id = 1' # GUARD_OK"
check allow "migration runner" "gmake migrate FILE=migrations/013_drop_old.sql && psql -c 'DROP TABLE x'"

echo
if [ "$fail" -eq 0 ]; then
    echo "all $n cases pass"
else
    echo "$fail of $n cases failed"
    exit 1
fi
