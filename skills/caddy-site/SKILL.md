---
name: caddy-site
description: >
  Apply when adding a new public hostname or reverse-proxy entry to the
  homelab. The trigger is: wiring up a new service so it is reachable via a
  *.rayv.dev hostname. Do not apply when modifying TLS or global Caddy
  settings, debugging an existing site, or adding an internal-only service
  that does not need a public hostname.
---

# Adding a new Caddy site

## The checklist

Work through these in order. Do not skip steps.

1. Add a row to `infra-ops/inventory/caddy-sites.csv`. Fields: hostname,
   upstream (host:port), access_tier, notes.

2. Run `make diff-caddy` to preview the generated Caddyfile change. Read it.

3. Run `make deploy-caddy` and confirm the interactive prompt.

4. Add the service to Uptime Kuma: `make sync-uptime-kuma`.

5. Add credentials to Vaultwarden under the service name.

6. If auth-gated: add the application to Authentik or Authelia, depending
   on which the service uses.

7. Verify: resolve the hostname and confirm the upstream responds.

## access_tier values

`access_tier` controls whether Authelia sits in front of the site. It does
not control network exposure.

- `public` -- no Authelia gate. Anyone on the network (Tailscale) can reach
  it directly.
- `private` -- Authelia-gated. Authentication required.

## Network posture

All sites use split-horizon DNS. Public DNS records for *.rayv.dev point to
private Tailscale IPs. The homelab is not reachable from the open internet
by default. Do not interpret `access_tier=public` as "internet-accessible."
Do not propose removing Cloudflare DNS entries. That would break the
split-horizon setup.

## caddy-sites.csv columns

| Column | Description |
|---|---|
| hostname | Full hostname, e.g. `app.rayv.dev` |
| upstream | Internal host:port the proxy forwards to |
| access_tier | `public` or `private` |
| notes | Short description for humans |

## After adding a site

Commit the CSV change to infra-ops and push. The Caddyfile on LXC 110 is
the deployed artifact; the CSV is the source of truth.
