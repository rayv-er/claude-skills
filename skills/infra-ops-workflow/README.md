# infra-ops-workflow

Homelab control plane discipline. Covers the CSV-as-contract pattern,
diff-before-deploy discipline, secrets hygiene, and the provisioning sequence.

The "state vs. intent" rule near the bottom is easy to get wrong during
migrations. When in doubt: set the CSV to reality, document intent elsewhere.
