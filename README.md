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
