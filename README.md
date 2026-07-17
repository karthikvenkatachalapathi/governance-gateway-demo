# Google Workspace Governance Gateway Demo

Static Cloudflare Pages demo of the Google Workspace Governance Control UI.

Important: this demo copies the production Control UI HTML/CSS/JavaScript from `google_governance_control_plane.py`; only the API responses are mocked in-browser. The layout, navigation, tabs, settings rail, tables, modals, and responsive behavior should match the real control plane.

## Cloudflare Pages

- Framework preset: `None` / static HTML
- Build command: leave blank
- Build output directory: `/`

## Local preview

```bash
python3 -m http.server 8787
```

Then open `http://127.0.0.1:8787/`.

## Screenshots

These screenshots are generated from the same static demo page. They are not separate mockups.

| View | Screenshot |
| --- | --- |
| Login | ![Login](assets/screenshots/01-login.png) |
| ACL rules | ![ACL rules](assets/screenshots/02-acl-rules.png) |
| Approvals | ![Approvals](assets/screenshots/03-approvals.png) |
| Access logs | ![Access logs](assets/screenshots/04-access-logs.png) |
| MCP tools | ![MCP tools](assets/screenshots/05-mcp-tools.png) |
| Gateway Setup — MCP Authorization | ![Gateway Setup MCP Authorization](assets/screenshots/06-gateway-setup-mcp-authorization.png) |
| Gateway Setup — Workspace Configuration | ![Workspace Configuration](assets/screenshots/07-workspace-configuration.png) |
| Gateway Setup — Channel Configuration | ![Channel Configuration](assets/screenshots/08-channel-configuration.png) |
| Admin Settings — Runtime Status | ![Runtime Status](assets/screenshots/09-runtime-status.png) |
| Admin Settings — Runtime Backups | ![Runtime Backups](assets/screenshots/10-runtime-backups.png) |

## Regenerating screenshots

```bash
python3 scripts/capture_screenshots.py
```
