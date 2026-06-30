# ✅ Antigravity P0-A — Critères de validation

> **Version :** `ANTIGRAVITY_P0A_ACCEPTANCE_CRITERIA_0.2.2`  
> **Date :** 2026-06-11  
> **Statut :** `READY`

## Validation obligatoire

| Critère | Statut attendu |
|---|---|
| Tous les CSV existent | Obligatoire |
| Schéma Markdown généré | Obligatoire |
| Manifest généré | Obligatoire |
| IDs stables | Obligatoire |
| Colonnes AppSheet-friendly | Obligatoire |
| Source file / source section | Obligatoire |
| `REVIEW_REQUIRED` si doute | Obligatoire |
| Pas de règle inventée | Obligatoire |
| Pas de broker / ordre / secret | Obligatoire |
| ZIP final | Recommandé |

## Stop immédiat si

- création d’un ordre automatique ;
- mention de clés API ou secrets ;
- ajout BigQuery/Cloud Run ;
- suppression de fichiers ;
- règles non sourcées ;
- CSV illisibles ;
- colonnes trop complexes pour AppSheet.
