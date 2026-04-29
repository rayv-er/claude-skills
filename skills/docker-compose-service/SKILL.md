---
name: docker-compose-service
description: >
  Apply when adding a new Docker Compose service to the homelab: creating a
  new LXC, scaffolding a new compose file, or wiring a new service end-to-end
  into infra-ops. Do not apply when making minor edits to an existing compose
  file (changing an env var, bumping an image tag), debugging container
  issues on an existing service, or working with Docker outside the homelab
  context.
---

# New homelab Docker Compose service

## Image pinning

Container images must be pinned to a specific tag. Never use `:latest`. If
the upstream only publishes `:latest`, pin to the digest hash instead:

```yaml
image: ghcr.io/owner/app@sha256:abc123...
```

## Provisioning sequence

For a brand-new service with no existing LXC:

```bash
# 1. Add to service-inventory.csv first
# 2. Provision the LXC
make provision-lxc vmid=<id> name=<slug> ip=<ip>
# 3. Scaffold the project
make new-project name=<slug> image=<img:tag> port=<n> password=<pw>
```

Then follow the standard change sequence: diff, deploy, commit.

For a service that already has a Makefile target but needs changes, skip to
the infra-ops-workflow change sequence.

## Wiring checklist

A new public-facing service needs all of these:

- Row in `service-inventory.csv` (machine, IP, port, description)
- Row in `caddy-sites.csv` (hostname, upstream, access_tier)
- Entry in Vaultwarden (credentials, any generated passwords)
- Uptime Kuma monitor via `make sync-uptime-kuma`
- Authentik/Authelia application if auth-gated

## Compose file conventions

Per-project Postgres is the standard pattern. Ship the database in the
compose file alongside the app. The shared `cfta_data` warehouse on VM 107
is the exception, used only for cross-project analytics.

Notifications go through ntfy on LXC 125. Topic convention:
`homelab-<service>` for infrastructure services, `cfta-<service>` for
CFTA-related services.

See `assets/compose.example.yml` for a minimal working template.

## Restart policy

All services use `restart: unless-stopped`. Never `restart: always` (it
fights manual stops during maintenance) and never no restart policy (services
should survive reboots).

## Scripts in compose files

If your service uses entrypoint scripts or healthcheck scripts, apply the
bash-script conventions: `set -euo pipefail`, stderr capture, no
`2>/dev/null` on primary actions.
