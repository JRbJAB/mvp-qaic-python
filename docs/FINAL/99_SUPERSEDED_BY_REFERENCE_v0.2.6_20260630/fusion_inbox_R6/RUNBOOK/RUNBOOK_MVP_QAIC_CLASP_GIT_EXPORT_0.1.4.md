# 🛠️ MVP QAIC — Runbook CLASP + Git + Export Scripts 0.1.4

Version: `MVP_QAIC_CLASP_GIT_EXPORT_0.1.4_LIVE_TREE_ALIGNED_SAFE`  
Date: 2026-06-11  
Statut: `READY_FOR_LIVE_TREE_RUN`

## Objectif

Mettre en place une routine régulière :

1. `clasp pull` read-only vers `03_APPS_SCRIPT/apps_script`.
2. Export complet des scripts Apps Script.
3. CSV consolidé importable dans Google Sheets : `MVPQAIC_CLASP_IMPORTS_ALL.csv`.
4. Backup ZIP du miroir.
5. Logs + résumé JSON.
6. Import manuel du CSV dans `⬇️ MVPQAIC_CLASP_IMPORTS`.
7. Enrichissement de `MVPQAIC_SCRIPT_REGISTRY` via Apps Script.

## Arborescence live respectée

- Script PowerShell à la racine : `MVPQAIC_CLASP_GIT_EXPORT_ANALYSIS.ps1`
- CSV Sheets : `02_SHEETS/EXPORTS_CSV/`
- Miroir CLASP : `03_APPS_SCRIPT/apps_script/`
- Copies sources : `03_APPS_SCRIPT/SOURCE/`
- Backups ZIP : `03_APPS_SCRIPT/BACKUPS/`
- ZIP/archives scripts : `03_APPS_SCRIPT/ZIP/`

## Commande régulière

```powershell
$PROJECT_ROOT = "G:\Mon Drive\👥 JULIEN [Perso]\📈 Trading JRb\Solutions & Dev (Trading JRb)\📈 QAIC\🛠️ MVP QAIC — Crypto Signal OS"
$SCRIPT_ID = "1OnXtyDAAiQI1_1mkX3AbLiJfRHfWhXdSoi1xwjMpKbrZzqSwWHvbQfIB"

Set-Location -LiteralPath $PROJECT_ROOT

.\MVPQAIC_CLASP_GIT_EXPORT_ANALYSIS.ps1 `
  -ProjectRoot $PROJECT_ROOT `
  -ScriptId $SCRIPT_ID `
  -InitGit `
  -Pull `
  -Commit
```

## Sorties attendues

- `02_SHEETS/EXPORTS_CSV/MVPQAIC_CLASP_IMPORTS_ALL.csv`
- `02_SHEETS/EXPORTS_CSV/MVPQAIC_FUNCTION_GUARD_AUDIT.csv`
- `02_SHEETS/EXPORTS_CSV/RUN-*/MVPQAIC_CLASP_IMPORTS_ALL.csv`
- `02_SHEETS/EXPORTS_CSV/RUN-*/MVPQAIC_CLASP_EXPORT_SUMMARY.json`
- `02_SHEETS/EXPORTS_CSV/RUN-*/clasp_pull_output.txt`
- `02_SHEETS/EXPORTS_CSV/RUN-*/git_status_after_export.txt`
- `03_APPS_SCRIPT/BACKUPS/MVPQAIC_APPS_SCRIPT_MIRROR_*.zip`

## Apps Script

Ajouter le fichier complet :

```text
03_APPS_SCRIPT/SOURCE/mvpqaic_20_script_registry_maintenance_core.gs
```

Fonctions à lancer :

```javascript
MVPQAIC_ScriptRegistry_CoreVersion()
MVPQAIC_ScriptRegistry_CoreRepairAll()
MVPQAIC_ScriptRegistry_CoreStatus()
```

Après import CSV dans `⬇️ MVPQAIC_CLASP_IMPORTS` :

```javascript
MVPQAIC_ScriptRegistry_RunAllFast()
MVPQAIC_ScriptRegistry_CleanupAuditRun()
```

## Sécurité

- Aucun `clasp push`.
- Aucun `clasp clone`.
- Aucune exécution Apps Script depuis PowerShell.
- Aucune écriture Sheet depuis PowerShell.
- Aucun ordre, sizing, broker, secret.
- Cleanup audit-only : pas de suppression, masquage, menu ou trigger mutation.
