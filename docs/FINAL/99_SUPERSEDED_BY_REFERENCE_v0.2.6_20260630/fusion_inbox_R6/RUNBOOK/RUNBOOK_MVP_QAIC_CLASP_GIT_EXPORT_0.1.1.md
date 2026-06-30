# 🛠️ RUNBOOK — MVP QAIC CLASP/Git Export 0.1.1

## Commande recommandée

```powershell
$PROJECT_ROOT = "G:\Mon Drive\👥 JULIEN [Perso]\📈 Trading JRb\Solutions & Dev (Trading JRb)\📈 QAIC\🛠️ MVP QAIC — Crypto Signal OS"
$SCRIPT_ID = "COLLER_ICI_LE_SCRIPT_ID_APPS_SCRIPT"

Set-Location -LiteralPath $PROJECT_ROOT
.	ools\MVPQAIC_CLASP_GIT_EXPORT_ANALYSIS.ps1 `
  -ProjectRoot $PROJECT_ROOT `
  -ScriptId $SCRIPT_ID `
  -Commit
```

## Variante sans pull

```powershell
.	ools\MVPQAIC_CLASP_GIT_EXPORT_ANALYSIS.ps1 -ProjectRoot $PROJECT_ROOT -SkipClaspPull -Commit
```

## Résultats attendus

- `02_EXPORTS/CLASP/RUN-*/MVPQAIC_CLASP_IMPORTS_ALL.csv`
- `02_EXPORTS/CLASP/MVPQAIC_CLASP_IMPORTS_ALL.csv`
- `02_EXPORTS/CLASP/RUN-*/MVPQAIC_FUNCTION_GUARD_AUDIT.csv`
- `02_EXPORTS/CLASP/RUN-*/MVPQAIC_CLASP_EXPORT_SUMMARY.json`
- `00_ADMIN/BACKUPS_CLASP/MVPQAIC_APPS_SCRIPT_MIRROR_*.zip`

## Après export

Importer `MVPQAIC_CLASP_IMPORTS_ALL.csv` dans `⬇️ MVPQAIC_CLASP_IMPORTS`, puis lancer :

```javascript
MVPQAIC_ScriptRegistry_RunAllFast()
MVPQAIC_ScriptRegistry_CleanupAuditRun()
```
