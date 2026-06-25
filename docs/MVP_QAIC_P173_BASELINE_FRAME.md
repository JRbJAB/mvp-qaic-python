# MVP QAIC — P173 baseline frame

## Décision corrigée

`mvp_qaic_py/p173_nicegui_private_local_runner.py` n’est pas l’interface officielle finale.

C’est la trame de départ récupérée, à améliorer selon les suggestions d’audit UI.

## Lancement correct

```powershell
python -m mvp_qaic_py.p173_nicegui_private_local_runner --project-root . --host 127.0.0.1 --port 8088 --serve-private
```

## Règles

- Ne pas lancer P173 en fichier direct avec `python .\mvp_qaic_py\p173...py`.
- Lancer en module avec `python -m`.
- Utiliser `--serve-private` pour ouvrir l’interface.
- Host local uniquement : `127.0.0.1`.
- Pas de broker, pas d’ordre, pas de sizing, pas d’appel provider live, pas d’écriture Sheets.
- P173 sert de base visuelle pour appliquer l’audit, pas de final figé.

## Audit-driven polish

- Garder la trame visuelle récupérée.
- Ajouter des accès rapides clairs.
- Clarifier les pages Base Python et Google Sheets.
- Améliorer progressivement les contenus sans réécrire un nouveau shell.

## Next

`P219E2_P173_APPLY_AUDIT_UI_CONTENT_FAST_FUSE`