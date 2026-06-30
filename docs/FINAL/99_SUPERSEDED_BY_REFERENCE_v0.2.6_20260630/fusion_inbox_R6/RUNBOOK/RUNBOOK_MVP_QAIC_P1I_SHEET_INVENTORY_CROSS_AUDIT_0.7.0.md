# 🛠️ MVP QAIC — P1-I Sheet Inventory & Cross Audit — Runbook 0.7.0

## Objectif
Auditer les onglets live du Google Sheet avant la création des onglets P2-A Lexique / Méthodes / Signaux.

## Script
`mvpqaic_21_sheet_inventory_cross_audit_core.gs`

## Fonctions publiques
```javascript
MVPQAIC_SheetInventoryVersion()
MVPQAIC_SheetInventoryStatus()
MVPQAIC_SheetInventoryRepairSheets()
MVPQAIC_SheetInventoryRun()
MVPQAIC_SheetScriptCrossAuditRun()
MVPQAIC_SheetInventoryRunAllFast()
```

## Onglets créés / écrits
- `MVPQAIC_SHEET_INVENTORY`
- `MVPQAIC_SHEET_SCRIPT_CROSS_AUDIT`

## Onglet lu
- `MVPQAIC_SCRIPT_REGISTRY` si présent.

## Sécurité
- No CLASP depuis Apps Script.
- No external network call.
- No broker / order / sizing.
- No secret value read.
- No delete / hide / menu / trigger mutation.
- Écrit seulement les deux onglets d’audit P1-I.

## Ordre d’exécution conseillé
```javascript
MVPQAIC_SheetInventoryVersion()
MVPQAIC_SheetInventoryStatus()
MVPQAIC_SheetInventoryRunAllFast()
```

## Décision après run
Lire :
- `MVPQAIC_SHEET_INVENTORY`
- `MVPQAIC_SHEET_SCRIPT_CROSS_AUDIT`

Si les cinq cibles P2-A ressortent en `P2A_CREATE_ALLOWED`, P2-A peut créer les onglets après revue humaine.
