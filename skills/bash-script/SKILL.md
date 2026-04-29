---
name: bash-script
description: >
  Apply when writing a new bash script or doing a substantive review of an
  existing one. Do not apply to one-liners run interactively at the shell,
  Makefile recipes, or scripts in other languages (Python, etc.). The trigger
  is writing a file that will be committed and run as a script.
---

# Bash scripting conventions

## Safety header

Every script opens with this line, no exceptions:

```bash
set -euo pipefail
```

`-e` exits on error. `-u` treats unset variables as errors. `-o pipefail`
catches failures in pipes. Together they turn silent failures into loud ones.

## Stderr handling

Capture stderr on failure paths. Never use `2>/dev/null` on a primary action.
That suppression turns a transient bug into a mystery that persists for days.

Use `2>/dev/null` only for expected noise on non-critical operations:

```bash
# OK: suppressing expected noise on an existence check
mkdir -p "$dir" 2>/dev/null || true

# NOT OK: suppressing stderr on a primary action
docker compose up -d 2>/dev/null
```

When a command fails and you want to print a message before exiting, redirect
to stderr:

```bash
echo "error: could not connect to $host" >&2
exit 1
```

## Quoting

Quote all variable expansions. Every time. No exceptions.

```bash
# correct
echo "$var"
"$EDITOR" "${file:-/dev/null}"

# wrong
echo $var
$EDITOR $file
```

Use `$(...)` for command substitution. Never backticks.

## Structure

Functions before main logic. `main()` at the bottom, called as `main "$@"`.
This makes the script readable top-to-bottom and makes the entry point
explicit.

```bash
#!/bin/bash
set -euo pipefail

do_thing() {
    local input="$1"
    ...
}

main() {
    do_thing "$1"
}

main "$@"
```

Use `local` for all variables inside functions.

## Exit codes

Exit 0 on success. Exit non-zero on failure. Be explicit about which code
means what if the caller cares. Do not rely on implicit exit codes from the
last command unless that is the intended behavior.

## Idempotency

Write scripts to be safe to run more than once. Check state before mutating:

```bash
if [ ! -d "$target" ]; then
    mkdir -p "$target"
fi
```

## Announcing mutations

For scripts that mutate remote state, print what the script is about to do
before doing it:

```bash
echo "deploying $service to $host..."
ssh "$host" "docker compose -f $compose_file up -d"
```

This makes logs useful and makes dry-run debugging possible.
