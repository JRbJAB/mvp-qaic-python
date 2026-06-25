# MVP QAIC — Web Architecture CDC

Status: `P_REFLEX_12A_R1_WEB_ARCHITECTURE_CDC_VISUAL_SITEMAP_READY`

## Architecture artifacts

- `docs/WEB_ARCHITECTURE_CDC.md`
- `docs/WEB_ARCHITECTURE_SITEMAP.json`
- `docs/WEB_ARCHITECTURE_SCHEMA.svg`
- `assets/mvp_qaic_web_architecture_schema.svg`

## Reflex integration

- Main page: `/architecture-web`
- Visual sitemap route: `/sitemap`
- Sitemap plugin: `SitemapPlugin` explicit in `rxconfig.py`
- Schema displayed first on Architecture Web page

## Global CDC progress

- Average progress: `56.67%`
- CDC rows: `15`
- Sitemap nodes: `17`
- Cockpits tracked: `8`

## CDC tracker

| ID | Section | Title | Route | Cockpit | Status | Progress | Next |
|---|---|---|---|---|---|---:|---|
| CDC-001 | Landing | Home / Mission Control | `/` | Mission Control | PRIVATE_READY | 85% | Brancher indicateurs réels MVP. |
| CDC-002 | Tracking | Dev Tracking | `/dev-tracking` | Dev Cockpit | STRUCTURE_READY | 45% | Connecter historique lots/tags/exports. |
| CDC-003 | CDC | CDC Tracker | `/cdc-tracker` | CDC Cockpit | STRUCTURE_READY | 60% | Ajouter décisions, owners, blockers. |
| CDC-004 | Architecture | Architecture Web | `/architecture-web` | Architecture Cockpit | ACTIVE | 70% | Finaliser flux data et contrats. |
| CDC-005 | Sitemap | Visual Sitemap | `/sitemap` | Sitemap Cockpit | ACTIVE | 65% | Review visuelle et enrichissement liens. |
| CDC-006 | Documentation | Documentation Registry | `/documentation-registry` | Docs Registry | STRUCTURE_READY | 45% | Indexer docs et exports utiles. |
| CDC-007 | Registry | Architecture & Registry | `/architecture-registry` | Registry Cockpit | TO_STRUCTURE | 45% | Finaliser registry routes/modules/docs. |
| CDC-008 | Admin | Admin Center | `/admin` | Admin Cockpit | PRIVATE_READY | 75% | Ajouter contrôle qualité runtime détaillé. |
| CDC-009 | Admin | Runtime Admin | `/admin/runtime` | Runtime Cockpit | PRIVATE_READY | 80% | Ajouter smoke history et incidents. |
| CDC-010 | Admin | Theme Admin | `/admin/theme` | Theme Cockpit | PRIVATE_READY | 85% | Runtime persistence smoke. |
| CDC-011 | Prompt | Prompt Lab | `/prompt-lab` | Prompt Cockpit | STRUCTURE_READY | 45% | Brancher prompts P132/P133/P157. |
| CDC-012 | GEM | GEM Portfolio | `/gem-portfolio` | GEM Review Cockpit | STRUCTURE_READY | 35% | Brancher import capture et revue JSON. |
| CDC-013 | Lexique | Lexique Knowledge | `/lexique-knowledge` | Knowledge Cockpit | STRUCTURE_READY | 40% | Brancher lexique validé et méthode publique. |
| CDC-014 | Bridge | QAIC Bridge | `/qaic-bridge` | QAIC Bridge Cockpit | REVIEW_ONLY | 25% | Contrat read-only uniquement. |
| CDC-015 | Safety | Settings Safety | `/settings-safety` | Safety Cockpit | STRUCTURE_READY | 50% | Centraliser limites public/privé. |

## Essential cockpits

| Cockpit | Route | Priority | Status | Purpose |
|---|---|---|---|---|
| Mission Control | `/` | P0 | PRIVATE_READY | Pilotage opérateur global. |
| Architecture Cockpit | `/architecture-web` | P0 | ACTIVE | Schéma, sitemap, CDC et architecture cible. |
| CDC Cockpit | `/cdc-tracker` | P0 | STRUCTURE_READY | Exigences, avancement, blockers, décisions. |
| Docs Registry | `/documentation-registry` | P0 | STRUCTURE_READY | Inventaire docs, exports, prompts, preuves. |
| Admin Cockpit | `/admin` | P0 | PRIVATE_READY | Runtime, thème, routes, data binding. |
| Prompt/GEM Cockpit | `/prompt-lab` | P1 | STRUCTURE_READY | Prompt workflows et revue GEM. |
| Lexique Cockpit | `/lexique-knowledge` | P1 | STRUCTURE_READY | Concepts, méthode, pédagogie publique future. |
| QAIC Bridge Cockpit | `/qaic-bridge` | P1 | REVIEW_ONLY | Pont futur read-only vers QAIC privé. |

## Safety

- No public deploy
- No broker execution
- No auto order
- No sizing
- No Sheet write
- No BigQuery write
