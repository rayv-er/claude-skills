# bash-script

Bash scripting conventions for scripts that get committed and re-run.

The stderr suppression rule (`2>/dev/null` on primary actions) is the one
that causes the most incidents. A swallowed error that only shows up 12 days
later under load is far worse than a noisy exit. This skill enforces the
distinction between acceptable suppression (existence checks) and dangerous
suppression (primary actions).
