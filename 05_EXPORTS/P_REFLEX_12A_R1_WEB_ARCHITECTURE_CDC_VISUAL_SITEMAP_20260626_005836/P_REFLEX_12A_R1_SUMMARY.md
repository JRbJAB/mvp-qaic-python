# P_REFLEX_12A-R1 — Web Architecture CDC + Visual Sitemap Schema

Status: `OK_P_REFLEX_12A_R1_WEB_ARCHITECTURE_CDC_VISUAL_SITEMAP_SCHEMA`

Base:

`P11D_BROWSER_LOCALSTORAGE_THEME_PERSISTENCE`

Implemented:

- Professional SVG schema at the top of `/architecture-web`
- Source artifacts:
  - `docs/WEB_ARCHITECTURE_CDC.md`
  - `docs/WEB_ARCHITECTURE_SITEMAP.json`
  - `docs/WEB_ARCHITECTURE_SCHEMA.svg`
  - `assets/mvp_qaic_web_architecture_schema.svg`
- CDC tracker with route links, status, cockpit, evidence and progress percent
- Essential cockpit registry
- Dedicated `/sitemap` route
- SitemapPlugin kept explicit in `rxconfig.py`

Safety:

- server started by batch: `false`
- public deploy: `false`
- broker/order/sizing: `false`
- Sheet write: `false`
- BigQuery write: `false`

Manual preview:

`RUN_P_REFLEX_12A_R1_LOCAL_PREVIEW.ps1`

Next:

`P_REFLEX_12B_RUNTIME_VISUAL_SMOKE_ARCHITECTURE_WEB`
