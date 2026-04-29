# docker-compose-service

New homelab service scaffold: end-to-end wiring checklist, image pinning
rules, and compose file conventions.

`assets/compose.example.yml` is a minimal working template with pinned
Postgres, a healthcheck-gated dependency, and `unless-stopped` restart policy.

The most common omission when adding a new service is forgetting one of the
five wiring steps (service-inventory, caddy-sites, Vaultwarden, Uptime Kuma,
Authelia). The checklist in the skill body covers all five.
