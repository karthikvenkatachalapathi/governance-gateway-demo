# Governance Gateway Demo

Static, sanitized demo for the Google Workspace Governance Gateway control plane.

This repository is intended for Cloudflare Pages.

## Cloudflare Pages

| Setting | Value |
|---|---|
| Framework preset | None / Static HTML |
| Build command | leave blank |
| Build output directory | `/` |

One-off deploy:

```bash
npx wrangler pages deploy . --project-name governance-gateway-demo
```

## Safety

The demo uses mock data only:

- no Google API calls
- no OAuth flow
- no tokens
- no backend dependency
- no real accounts

## Regenerate screenshots

```bash
python3 scripts/generate_demo_screenshots.py
```
