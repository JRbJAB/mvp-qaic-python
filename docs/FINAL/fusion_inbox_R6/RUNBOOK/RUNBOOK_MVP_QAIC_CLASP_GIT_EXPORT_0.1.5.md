# 🛠️ MVP QAIC — CLASP/Git Export + Drive CSV Import — 0.1.5

## Objectif
- PowerShell crée/met à jour `02_SHEETS/EXPORTS_CSV/MVPQAIC_CLASP_IMPORTS_ALL.csv`.
- Apps Script importe directement ce CSV depuis Drive dans `⬇️ MVPQAIC_CLASP_IMPORTS`.
- Apps Script reconstruit `MVPQAIC_SCRIPT_REGISTRY`.

## Ordre de run
1. PowerShell : `MVPQAIC_CLASP_GIT_EXPORT_ANALYSIS.ps1`
2. Apps Script : `MVPQAIC_ScriptRegistry_DriveCsvStatus()`
3. Apps Script : `MVPQAIC_ScriptRegistry_ImportLatestClaspCsvFromDrive()`
4. Apps Script : `MVPQAIC_ScriptRegistry_RunAllFast()`
5. Apps Script : `MVPQAIC_ScriptRegistry_CleanupAuditRun()`

## Si le dossier Drive ne se résout pas par chemin
Renseigner la Script Property `MVPQAIC_CLASP_DRIVE_FOLDER_ID` avec l’ID du dossier Drive `02_SHEETS/EXPORTS_CSV`.
