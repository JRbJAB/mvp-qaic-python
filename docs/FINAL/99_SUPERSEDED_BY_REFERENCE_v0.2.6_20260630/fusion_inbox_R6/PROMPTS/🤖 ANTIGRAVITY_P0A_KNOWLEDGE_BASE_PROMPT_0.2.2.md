# 🤖 Antigravity Prompt — P0-A Knowledge Base CSV

> **Projet :** 🛠️ MVP QAIC — Crypto Signal OS Web App  
> **Version :** `ANTIGRAVITY_P0A_PROMPT_0.2.2`  
> **Date :** 2026-06-11  
> **Statut :** `READY_TO_RUN_AFTER_USER_VALIDATION`

## Prompt à coller dans Antigravity

```text
You are working on the MVP QAIC — Crypto Signal OS Web App.

Goal:
Build P0 Knowledge Base from the provided Markdown files.

Priority:
The MVP must first deliver a usable Web App focused on:
- crypto lexicon
- trading methods
- signal library
- risk playbooks
- daily checklists
- decision journal

Long-term direction:
This MVP will later become a Web App / UI IDE layer for the final QAIC system. Do not integrate the final QAIC engine yet. Prepare stable IDs and clean mappings only.

Do not implement automatic trading.
Do not implement broker execution.
Do not create live market integrations yet.
Do not invent trading rules that are not present in the source documents.
If a field is uncertain, use REVIEW_REQUIRED.

Input files:
- source/architecture_mvp_crypto_stitch_antigravity_google_lexique_first.md
- source/lexique_crypto_methodes_signaux_trading_pro.md
- source/synthese_lexique_mvp_crypto_project_context.md
- docs/CDC_MVP_QAIC_WEB_APP_LEXIQUE_FIRST_0.2.2.md
- docs/PLANNING_MVP_QAIC_WEB_APP_TRANSITION_QAIC_0.2.2.md
- docs/INSTRUCTIONS_PROJET_MVP_QAIC_0.2.2.md

Tasks:
1. Extract structured rows from the lexicon and project docs.
2. Create machine-readable CSV seed files for:
   - KNOWLEDGE_TERMS
   - METHOD_LIBRARY
   - SIGNAL_LIBRARY
   - RISK_PLAYBOOK
   - CHECKLISTS
   - DECISION_TEMPLATES
   - GLOSSARY_TAGS
3. Every row must include stable IDs, category, title, tags, priority, risk notes, related terms, source file, source section, and validation status when available.
4. Generate a Markdown schema document describing every table and column.
5. Generate a manifest listing all files created.
6. Use UTF-8 CSV.
7. Do not create files outside these folders:
   - schemas/
   - csv_seed/
   - exports/
8. Do not use BigQuery, Cloud Run, brokers, order execution, or secrets.

Output:
- schemas/MVP_QAIC_SHEETS_SCHEMA_P0_0.2.2.md
- csv_seed/KNOWLEDGE_TERMS.csv
- csv_seed/METHOD_LIBRARY.csv
- csv_seed/SIGNAL_LIBRARY.csv
- csv_seed/RISK_PLAYBOOK.csv
- csv_seed/CHECKLISTS.csv
- csv_seed/DECISION_TEMPLATES.csv
- csv_seed/GLOSSARY_TAGS.csv
- exports/MVP_QAIC_P0_KNOWLEDGE_BASE_SEED_0.2.2.zip
- MANIFEST_P0A_0.2.2.md

Acceptance criteria:
- No invented trading rule.
- No automatic order logic.
- IDs are stable and human-readable.
- CSV columns are simple and AppSheet-friendly.
- Uncertain entries are flagged REVIEW_REQUIRED.
- The manifest lists every created file.
```
