---
name: wine-deploy
description: >
  Apply when deploying theme code to the Crested Butte Wine + Food Festival
  staging or production site. Triggers include: "deploy to staging", "push to
  production", "deploy the changes", "update the live site", or any request
  to get code from the git repo onto Cloudways.
---

# CBWFF Cloudways Deploy

You deploy the `cfta-theme` repository to staging or production on Cloudways.
Always confirm which environment before deploying. Default to staging unless
the user explicitly says production.

## Environments

| Environment | App ID | System User | Branch | Domain |
|---|---|---|---|---|
| Production | `6269576` | `nyuqcdfzjc` | `main` | shop.cbwineandfood.com |
| Staging | `6387528` | `ftqmvtkprb` | `staging` | wordpress-1599060-6387528.cloudwaysapps.com |

**Server ID** (same for both): `1599060`
**SSH master user**: `cfta-brett@143.198.110.93`

## Git repository

- Remote: `git@github.com:rayv-er/cfta-theme.git`
- Local clone: `/Users/admin/code/cfta/cfta-theme/`
- Production branch: `main`
- Staging branch: `staging`

## Deploy workflow

### Step 1 — Confirm what's being deployed

Before deploying, show the user what commits are ahead:
```bash
cd /Users/admin/code/cfta/cfta-theme
git log origin/main..staging --oneline   # for staging→prod merge
git log origin/staging..HEAD --oneline   # for local→staging push
```

### Step 2 — Push to the right branch

```bash
git push origin staging   # for staging deploy
git push origin main      # for production deploy
```

### Step 3 — Trigger Cloudways Git pull

**Important**: Cloudways does NOT auto-deploy on push. The Git pull must be
manually triggered via the Cloudways MCP tool `mcp__cloudways__git_pull`.

Use the Cloudways MCP `git_pull` tool with:
- `server_id`: `1599060`
- `app_id`: `6387528` (staging) or `6269576` (production)

### Step 4 — Verify the deploy

SSH into the server and spot-check a recently modified file:
```bash
# Check that a known change is present (e.g., a CSS value or PHP string)
ssh -o StrictHostKeyChecking=no cfta-brett@143.198.110.93 \
  "grep -n 'YOUR_KNOWN_STRING' /home/SYSUSER/public_html/wp-content/themes/cfta-theme/cfta-festival.css | head -3"
```

Replace `SYSUSER` with `nyuqcdfzjc` (prod) or `ftqmvtkprb` (staging).
WP theme path: `/home/{sys_user}/public_html/wp-content/themes/cfta-theme/`

### Fallback — SSH direct file push

If the Cloudways Git pull doesn't trigger or fails, push individual files
directly via SSH:

```bash
cat /Users/admin/code/cfta/cfta-theme/cfta-festival.css | \
  ssh -o StrictHostKeyChecking=no cfta-brett@143.198.110.93 \
  "cat > /home/nyuqcdfzjc/public_html/wp-content/themes/cfta-theme/cfta-festival.css"
```

Use this sparingly — it bypasses Git history on the server side. Always
make sure the local file is committed and pushed to the remote first.

## Staging → Production promotion

When all staging changes are approved and ready for production:

```bash
cd /Users/admin/code/cfta/cfta-theme
git checkout main
git merge staging
git push origin main
# Then trigger Cloudways git_pull for production app 6269576
```

Always ask the user to confirm before merging staging → main and deploying
to production. Summarize what commits will land before proceeding.

## Safety rules

- Never deploy directly to production without asking first.
- Never force-push to `main`.
- If a deploy to production fails or the verification check doesn't match,
  do not attempt a workaround — surface the error to the user.
- After any production deploy, always verify at least one changed file on
  the live server before declaring success.
