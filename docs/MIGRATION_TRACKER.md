# MVP QAIC — Migration Tracker

Status: `READY_COMPACT_MISSION_PANEL`

- Rows: `15`
- Average progress: `45.67%`
- Scope: Sheets + Apps Script + exported docs
- Display: compact Mission Control panel

| ID | Type | Source | Target | Status | Progress | Next |
|---|---|---|---|---|---:|---|
| MIG-001 | SHEET_TAB | LEXIQUE_CRYPTO_APPROVED | `/lexique-knowledge` | STRUCTURE_READY | 40% | Brancher export lexique validé + catégories + recherche. |
| MIG-002 | SHEET_TAB | GPT_QUALITY_DASHBOARD | `/prompt-lab` | TO_MIGRATE | 30% | Migrer métriques qualité prompt/GEM en cockpit Reflex. |
| MIG-003 | SHEET_TAB | PROMPT_IMPROVEMENT_QUEUE | `/prompt-lab` | TO_MIGRATE | 30% | Lister corrections, statuts, priorités et human review. |
| MIG-004 | SHEET_TAB | DECISION_JOURNAL | `/cdc-tracker` | PARTIAL | 45% | Créer journal web read-only avec décisions, blockers, evidence. |
| MIG-005 | SHEET_TAB | QAIC_RUNTIME_COCKPIT_VIEW | `/admin/runtime` | PARTIAL | 70% | Brancher historique smoke/runtime et incidents. |
| MIG-006 | SHEET_TAB | QAIC_RUNTIME_BRIDGE_STATUS | `/qaic-bridge` | REVIEW_ONLY | 35% | Contrat read-only, pas de broker/order/sizing. |
| MIG-007 | SHEET_TAB | 🎛️ BENCHMARK_AI_TRADE | `/prompt-lab` | TO_MIGRATE | 30% | Migrer benchmark en lecture locale avec scoring compact. |
| MIG-008 | APPS_SCRIPT_FILE | mvpqaic_09_p1_journal_core.gs | `/cdc-tracker` | PARTIAL | 50% | Porter logique idempotence/journal en Python local review-only. |
| MIG-009 | APPS_SCRIPT_FUNCTION | Decision journal append / duplicate guard | `/cdc-tracker` | PARTIAL | 45% | Formaliser tests duplicate guard côté Python. |
| MIG-010 | FUNCTIONALITY | P132/P133 GEM portfolio multimodal prompt | `/gem-portfolio` | STRUCTURE_READY | 55% | UI import capture + réponse GEM + revue humaine. |
| MIG-011 | FUNCTIONALITY | Prompt correction loop P153/P154/P155/P159 | `/prompt-lab` | STRUCTURE_READY | 50% | Brancher actions correction + apply gate review-only. |
| MIG-012 | FUNCTIONALITY | Safety gates no-order/no-sizing/no-public-deploy | `/settings-safety` | PRIVATE_READY | 80% | Centraliser affichage et audit sécurité. |
| MIG-013 | DOC_EXPORT | WEB_ARCHITECTURE_CDC.md / SITEMAP.json / SCHEMA.svg | `/architecture-web` | ACTIVE | 85% | Review visuelle + enrichissement data contracts. |
| MIG-014 | INVENTORY | MVPQAIC_CLASP_IMPORTS_ALL.csv | `/architecture-registry` | TO_BIND | 20% | Importer inventaire scripts/fonctions pour tracker exhaustif. |
| MIG-015 | INVENTORY | MVPQAIC_CLASP_IMPORTS_ALL_HEADERS.csv | `/architecture-registry` | TO_BIND | 20% | Mapper headers Sheets vers contrats Reflex/Python. |
