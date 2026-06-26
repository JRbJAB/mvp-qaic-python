# Matrice globale de migration — Sheets / Apps Script / Python / Reflex / BigQuery

- Status: `GLOBAL_MIGRATION_MATRIX_READY_FOR_OPERATOR_REVIEW`
- Generated at: `2026-06-26T09:54:52+00:00`
- Politique statuts: statuts machine en anglais + libellés français en UI.

## Synthèse

- `total_rows`: `2794`
- `by_scope`: `{'APPS_SCRIPT_FUNCTION': 2738, 'APPS_SCRIPT_FILE': 22, 'SHEETS_COCKPIT': 19, 'FEATURE_CLUSTER': 10, 'FUTURE_ARCHITECTURE': 5}`
- `by_status`: `{'PYTHON_REWRITE': 1594, 'MIGRATE_NOW': 1048, 'KEEP_AS_EXPORT_SOURCE': 114, 'REVIEW_REQUIRED': 18, 'RETIRE_NO_VALUE': 7, 'BIGQUERY_FUTURE_CANDIDATE': 5, 'MIGRATE_LATER': 4, 'NO_MIGRATION_NEEDED': 2, 'REFLEX_UI_BINDING': 1, 'KEEP_SHEETS_MANUAL': 1}`
- `by_target_layer`: `{'PYTHON_SERVICE + READONLY_EXPORT': 1594, 'PYTHON + REFLEX_UI': 964, 'PYTHON + LOCAL_EXPORT + FUTURE_BIGQUERY': 78, 'LOCAL_DOCS + REFLEX_UI': 66, 'LOCAL_CSV + REFLEX_UI': 48, 'PYTHON_REWRITE_OR_RETIRE': 9, 'REFLEX_NATIVE_UI': 7, 'REFLEX_UI': 5, 'BIGQUERY': 5, 'LOCAL_EXPORT': 5, 'REFLEX_UI_OR_RETIRE': 3, 'REFLEX_UI + LOCAL_DOCS': 2, 'REFLEX_UI + DOCS': 2, 'TECHNICAL': 2, 'REFLEX_UI + PYTHON': 1, 'SHEETS_EXPORT + FUTURE_PYTHON': 1, 'SHEETS_MANUAL': 1, 'PYTHON_SERVICE': 1}`
- `by_module_family`: `{'QAIC_BRIDGE': 1594, 'PROMPT_ENGINE': 749, 'KNOWLEDGE_SEARCH': 213, 'JOURNAL': 77, 'AUDIT_INVENTORY': 66, 'SCRIPT_REGISTRY': 47, 'SHEETS_OR_TARGET_PLATFORM': 19, 'SETUP_FOUNDATION': 10, 'FORMATTING': 7, 'IMPORT_SEEDS': 5, 'FUTURE_PLATFORM': 5, 'MANIFEST': 2}`
- `source_csv_rows`: `3235`
- `script_inventory_count`: `22`
- `function_index_count`: `2738`

## Légende statuts

- `MIGRATE_NOW` / À migrer maintenant — Important pour le MVP privé Reflex/Python.
- `MIGRATE_LATER` / À migrer plus tard — Utile mais non bloquant.
- `KEEP_SHEETS_MANUAL` / Garder dans Sheets en contrôle manuel — Sheets garde une valeur de revue humaine/export.
- `KEEP_AS_EXPORT_SOURCE` / Garder comme source d’export lecture seule — Alimente Python/Reflex sans mutation automatique.
- `PYTHON_REWRITE` / Réécrire en Python — Sortir la logique d’Apps Script.
- `REFLEX_UI_BINDING` / Brancher dans l’interface Reflex — Créer route/panneau/filtre UI.
- `BIGQUERY_FUTURE_CANDIDATE` / Candidat BigQuery futur — Logs, historiques, snapshots, analytics.
- `RETIRE_NO_VALUE` / Ne pas migrer / sans intérêt confirmé — Legacy, doublon ou faible valeur.
- `NO_MIGRATION_NEEDED` / Pas de migration nécessaire — Fichier technique ou déjà couvert.
- `REVIEW_REQUIRED` / Revue nécessaire — Risque/couverture/dépendance à vérifier.

## Premières lignes à revoir

- `SHEET_COCKPIT_001` `SHEETS_COCKPIT` **Mission Control** → `REFLEX_UI_BINDING` (Brancher dans l’interface Reflex) → `REFLEX_UI` — Déjà présent partiellement ; compléter liens et statuts.
- `SHEET_COCKPIT_002` `SHEETS_COCKPIT` **Dev Tracking** → `MIGRATE_NOW` (À migrer maintenant) → `REFLEX_UI + LOCAL_DOCS` — À alimenter depuis Git, 05_EXPORTS et seal reports.
- `SHEET_COCKPIT_003` `SHEETS_COCKPIT` **CDC Tracker** → `MIGRATE_NOW` (À migrer maintenant) → `REFLEX_UI + DOCS` — Conserver JSON machine + affichage lisible.
- `SHEET_COCKPIT_004` `SHEETS_COCKPIT` **Migration Tracker** → `MIGRATE_NOW` (À migrer maintenant) → `REFLEX_UI + DOCS` — Doit devenir la vue globale enrichie par CSV CLASP.
- `SHEET_COCKPIT_005` `SHEETS_COCKPIT` **Auto-update Trackers** → `MIGRATE_NOW` (À migrer maintenant) → `REFLEX_UI` — Fondation posée en P12E-R2G.
- `SHEET_COCKPIT_006` `SHEETS_COCKPIT` **Prompt Cockpit** → `MIGRATE_NOW` (À migrer maintenant) → `REFLEX_UI + PYTHON` — Cœur MVP privé.
- `SHEET_COCKPIT_007` `SHEETS_COCKPIT` **Benchmark AI Trade** → `MIGRATE_LATER` (À migrer plus tard) → `PYTHON + REFLEX_UI` — Secondaire après migration globale.
- `SHEET_COCKPIT_008` `SHEETS_COCKPIT` **Decision Journal** → `MIGRATE_NOW` (À migrer maintenant) → `PYTHON + LOCAL_EXPORT + FUTURE_BIGQUERY` — Préparer export/BigQuery futur.
- `SHEET_COCKPIT_009` `SHEETS_COCKPIT` **Prompt History Library** → `MIGRATE_LATER` (À migrer plus tard) → `PYTHON + REFLEX_UI` — Audit prompt et régression.
- `SHEET_COCKPIT_010` `SHEETS_COCKPIT` **Response Draft** → `MIGRATE_LATER` (À migrer plus tard) → `PYTHON + REFLEX_UI` — Boucle de correction humaine.
- `SHEET_COCKPIT_011` `SHEETS_COCKPIT` **Lexique / Knowledge Base** → `MIGRATE_NOW` (À migrer maintenant) → `PYTHON + REFLEX_UI` — Valeur MVP publique future.
- `SHEET_COCKPIT_012` `SHEETS_COCKPIT` **Runtime Cockpit** → `MIGRATE_NOW` (À migrer maintenant) → `REFLEX_UI` — Essentiel opérateur privé.
- `SHEET_COCKPIT_013` `SHEETS_COCKPIT` **Runtime Bridge Status** → `MIGRATE_NOW` (À migrer maintenant) → `REFLEX_UI + LOCAL_DOCS` — À lier aux trackers auto-update.
- `SHEET_COCKPIT_014` `SHEETS_COCKPIT` **WebApp Readiness** → `MIGRATE_NOW` (À migrer maintenant) → `REFLEX_UI` — Checklist release privée.
- `SHEET_COCKPIT_015` `SHEETS_COCKPIT` **Revolut X Readonly Views** → `KEEP_SHEETS_MANUAL` (Garder dans Sheets en contrôle manuel) → `SHEETS_EXPORT + FUTURE_PYTHON` — Pas d’ordre/sizing ; revue/export seulement.
- `SHEET_COCKPIT_016` `SHEETS_COCKPIT` **Legacy Script Registry** → `KEEP_AS_EXPORT_SOURCE` (Garder comme source d’export lecture seule) → `LOCAL_CSV + REFLEX_UI` — Source inventaire jusqu’à fermeture migration.
- `SHEET_COCKPIT_017` `SHEETS_COCKPIT` **Legacy Sheets Control Tabs** → `REVIEW_REQUIRED` (Revue nécessaire) → `SHEETS_MANUAL` — Ne rien supprimer sans preuve.
- `SHEET_COCKPIT_018` `SHEETS_COCKPIT` **BigQuery Historical Snapshots** → `BIGQUERY_FUTURE_CANDIDATE` (Candidat BigQuery futur) → `BIGQUERY` — Volumétrie, audit et backtests.
- `SHEET_COCKPIT_019` `SHEETS_COCKPIT` **BigQuery Decision Facts** → `BIGQUERY_FUTURE_CANDIDATE` (Candidat BigQuery futur) → `BIGQUERY` — Audit décisionnel long terme.
- `FUTURE_ARCH_001` `FUTURE_ARCHITECTURE` **BigQuery event log** → `BIGQUERY_FUTURE_CANDIDATE` (Candidat BigQuery futur) → `BIGQUERY` — Logs runs/gates/erreurs/smokes.
- `FUTURE_ARCH_002` `FUTURE_ARCHITECTURE` **BigQuery decision facts** → `BIGQUERY_FUTURE_CANDIDATE` (Candidat BigQuery futur) → `BIGQUERY` — Journal décisionnel et validations humaines.
- `FUTURE_ARCH_003` `FUTURE_ARCHITECTURE` **BigQuery historical snapshots** → `BIGQUERY_FUTURE_CANDIDATE` (Candidat BigQuery futur) → `BIGQUERY` — Historique pour backtests/audit.
- `FUTURE_ARCH_004` `FUTURE_ARCHITECTURE` **Python migration service** → `MIGRATE_LATER` (À migrer plus tard) → `PYTHON_SERVICE` — Conversion fonctions Apps Script vers modules Python.
- `FUTURE_ARCH_005` `FUTURE_ARCHITECTURE` **Reflex migration workbench** → `MIGRATE_NOW` (À migrer maintenant) → `REFLEX_UI` — Interface de tri opérateur des décisions migration.
- `APPS_SCRIPT_FILE_016` `APPS_SCRIPT_FILE` **mvpqaic_23_gpt_response_intake_core.js** → `PYTHON_REWRITE` (Réécrire en Python) → `PYTHON_SERVICE + READONLY_EXPORT` — Logique métier à sortir d’Apps Script. Risque élevé : revue stricte avant retrait ou migration.
- `APPS_SCRIPT_FILE_012` `APPS_SCRIPT_FILE` **mvpqaic_11_p1_prompt_quality_core.js** → `MIGRATE_NOW` (À migrer maintenant) → `PYTHON + REFLEX_UI` — Cœur prompt/human-review MVP. Risque élevé : revue stricte avant retrait ou migration.
- `APPS_SCRIPT_FILE_020` `APPS_SCRIPT_FILE` **mvpqaic_50_p5_webapp_readiness_core.js** → `PYTHON_REWRITE` (Réécrire en Python) → `PYTHON_SERVICE + READONLY_EXPORT` — Logique métier à sortir d’Apps Script. Risque élevé : revue stricte avant retrait ou migration.
- `APPS_SCRIPT_FILE_018` `APPS_SCRIPT_FILE` **mvpqaic_41_phase4_closure_cdc_tracker_core.js** → `PYTHON_REWRITE` (Réécrire en Python) → `PYTHON_SERVICE + READONLY_EXPORT` — Logique métier à sortir d’Apps Script. Risque élevé : revue stricte avant retrait ou migration.
- `APPS_SCRIPT_FILE_013` `APPS_SCRIPT_FILE` **mvpqaic_20_script_registry_maintenance_core.js** → `KEEP_AS_EXPORT_SOURCE` (Garder comme source d’export lecture seule) → `LOCAL_CSV + REFLEX_UI` — Inventaire utile. Risque élevé : revue stricte avant retrait ou migration.
- `APPS_SCRIPT_FILE_017` `APPS_SCRIPT_FILE` **mvpqaic_31_lexique_master_search_cockpit_core.js** → `MIGRATE_NOW` (À migrer maintenant) → `PYTHON + REFLEX_UI` — KB/Lexique dans WebApp. Risque élevé : revue stricte avant retrait ou migration.
- `APPS_SCRIPT_FILE_008` `APPS_SCRIPT_FILE` **mvpqaic_06_p0b4_gpt_revolutx_bridge.js** → `PYTHON_REWRITE` (Réécrire en Python) → `PYTHON_SERVICE + READONLY_EXPORT` — Logique métier à sortir d’Apps Script. Risque élevé : revue stricte avant retrait ou migration.
- `APPS_SCRIPT_FILE_007` `APPS_SCRIPT_FILE` **mvpqaic_05_p0b3_institutional_readiness.js** → `PYTHON_REWRITE` (Réécrire en Python) → `PYTHON_SERVICE + READONLY_EXPORT` — Logique métier à sortir d’Apps Script. Risque élevé : revue stricte avant retrait ou migration.
- `APPS_SCRIPT_FILE_006` `APPS_SCRIPT_FILE` **mvpqaic_04_p0b2_expansion.js** → `PYTHON_REWRITE` (Réécrire en Python) → `PYTHON_SERVICE + READONLY_EXPORT` — Logique métier à sortir d’Apps Script. Risque élevé : revue stricte avant retrait ou migration.
- `APPS_SCRIPT_FILE_009` `APPS_SCRIPT_FILE` **mvpqaic_07_p0b5_trade_plan_methods_trailing.js** → `PYTHON_REWRITE` (Réécrire en Python) → `PYTHON_SERVICE + READONLY_EXPORT` — Logique métier à sortir d’Apps Script. Risque élevé : revue stricte avant retrait ou migration.
- `APPS_SCRIPT_FILE_010` `APPS_SCRIPT_FILE` **mvpqaic_08_full_signal_mapping_50_50.js** → `PYTHON_REWRITE` (Réécrire en Python) → `PYTHON_SERVICE + READONLY_EXPORT` — Logique métier à sortir d’Apps Script. Risque élevé : revue stricte avant retrait ou migration.
- `APPS_SCRIPT_FILE_005` `APPS_SCRIPT_FILE` **mvpqaic_03_import_csv_seeds.js** → `REVIEW_REQUIRED` (Revue nécessaire) → `LOCAL_EXPORT` — Import seed souvent one-shot. Risque élevé : revue stricte avant retrait ou migration.
- `APPS_SCRIPT_FILE_014` `APPS_SCRIPT_FILE` **mvpqaic_21_sheet_inventory_cross_audit_core.js** → `KEEP_AS_EXPORT_SOURCE` (Garder comme source d’export lecture seule) → `LOCAL_DOCS + REFLEX_UI` — Audit et preuves. Risque élevé : revue stricte avant retrait ou migration.
- `APPS_SCRIPT_FILE_019` `APPS_SCRIPT_FILE` **mvpqaic_42_response_intake_consolidation_audit_core.js** → `KEEP_AS_EXPORT_SOURCE` (Garder comme source d’export lecture seule) → `LOCAL_DOCS + REFLEX_UI` — Audit et preuves. Risque élevé : revue stricte avant retrait ou migration.
- `APPS_SCRIPT_FILE_011` `APPS_SCRIPT_FILE` **mvpqaic_09_p1_journal_core.js** → `MIGRATE_NOW` (À migrer maintenant) → `PYTHON + LOCAL_EXPORT + FUTURE_BIGQUERY` — Journal décision traçable hors Sheets. Risque élevé : revue stricte avant retrait ou migration.
- `APPS_SCRIPT_FILE_002` `APPS_SCRIPT_FILE` **mvpqaic_00_setup_p0.js** → `REVIEW_REQUIRED` (Revue nécessaire) → `PYTHON_REWRITE_OR_RETIRE` — Fondation legacy à vérifier. Risque élevé : revue stricte avant retrait ou migration.
- `APPS_SCRIPT_FILE_015` `APPS_SCRIPT_FILE` **mvpqaic_22_frontend_sheet_rename_migration_core.js** → `PYTHON_REWRITE` (Réécrire en Python) → `PYTHON_SERVICE + READONLY_EXPORT` — Logique métier à sortir d’Apps Script.
- `APPS_SCRIPT_FILE_022` `APPS_SCRIPT_FILE` **mvpqaic_91_webapp_sheets_sync.js** → `PYTHON_REWRITE` (Réécrire en Python) → `PYTHON_SERVICE + READONLY_EXPORT` — Logique métier à sortir d’Apps Script.
- `APPS_SCRIPT_FILE_003` `APPS_SCRIPT_FILE` **mvpqaic_01_knowledge_engine.js** → `MIGRATE_NOW` (À migrer maintenant) → `PYTHON + REFLEX_UI` — KB/Lexique dans WebApp.
- `APPS_SCRIPT_FILE_004` `APPS_SCRIPT_FILE` **mvpqaic_02_formatting.js** → `RETIRE_NO_VALUE` (Ne pas migrer / sans intérêt confirmé) → `REFLEX_NATIVE_UI` — Mise en forme Sheets non migrée telle quelle.
- `APPS_SCRIPT_FILE_001` `APPS_SCRIPT_FILE` **appsscript.json** → `NO_MIGRATION_NEEDED` (Pas de migration nécessaire) → `TECHNICAL` — Fichier technique Apps Script.
- `APPS_SCRIPT_FILE_021` `APPS_SCRIPT_FILE` **mvpqaic_90_webapp_entrypoint.js** → `PYTHON_REWRITE` (Réécrire en Python) → `PYTHON_SERVICE + READONLY_EXPORT` — Logique métier à sortir d’Apps Script.
