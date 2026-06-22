# P134 — NiceGUI Prompt Cockpit Local Private

## Statut

- Status : `NICEGUI_PROMPT_COCKPIT_LOCAL_PRIVATE_READY`
- Version : `MVP_QAIC_P134_NICEGUI_PROMPT_COCKPIT_LOCAL_PRIVATE_0_1_0_SAFE`
- URL locale : `http://127.0.0.1:8088`
- Host : `127.0.0.1`
- Port : `8088`

## Sources détectées

- Prompt P132-R2 : `G:\Mon Drive\👥 JULIEN [Perso]\📈 Trading JRb\Solutions & Dev (Trading JRb)\MVP_QAIC_PY\05_EXPORTS\P132_R2_PRETTY_JSON_PROMPT_SYNC_20260622_184031\P132_GEM_MULTIMODAL_PORTFOLIO_PROMPT.md`
- Gate P133 : `G:\Mon Drive\👥 JULIEN [Perso]\📈 Trading JRb\Solutions & Dev (Trading JRb)\MVP_QAIC_PY\05_EXPORTS\P133_GEM_MULTIMODAL_RESPONSE_CAPTURE_IMAGE_USAGE_GATE_20260622_181633\P133_GEM_RESPONSE_CAPTURE_GATE.json`
- Rapport P133 : `G:\Mon Drive\👥 JULIEN [Perso]\📈 Trading JRb\Solutions & Dev (Trading JRb)\MVP_QAIC_PY\05_EXPORTS\P133_GEM_MULTIMODAL_RESPONSE_CAPTURE_IMAGE_USAGE_GATE_20260622_181633\P133_GEM_RESPONSE_HUMAN_REVIEW.md`
- Pretty JSON P133 : `G:\Mon Drive\👥 JULIEN [Perso]\📈 Trading JRb\Solutions & Dev (Trading JRb)\MVP_QAIC_PY\05_EXPORTS\P133_GEM_MULTIMODAL_RESPONSE_CAPTURE_IMAGE_USAGE_GATE_20260622_181633\P133_GEM_RESPONSE_PRETTY.json`

## Workflow opérateur

1. Open cockpit locally on 127.0.0.1.
2. Copy latest P132-R2 prompt from cockpit.
3. Attach Revolut X screenshot manually in GEM.
4. Paste GEM response back into local cockpit or save it as a local file.
5. Run P133 response capture gate locally.
6. Open P133 human review markdown and pretty JSON.

## Sécurité

- Local privé uniquement : `127.0.0.1` ou `localhost`.
- Aucun public deploy.
- Aucun tunnel.
- Aucun broker, ordre, sizing, auto-apply.
- Aucun write Sheets/BigQuery/Apps Script.

## Commande de lancement cockpit

```powershell
python -m mvp_qaic_py.nicegui_prompt_cockpit_local_private --launch --exports-dir 05_EXPORTS
```

Si NiceGUI n’est pas installé, le module reste utilisable en mode export/runbook :

```powershell
python -m mvp_qaic_py.nicegui_prompt_cockpit_local_private --output-dir 05_EXPORTS\P134_TEST --dry-run-export
```
