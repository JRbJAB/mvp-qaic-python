# P150B — Local Launch Commands

```powershell
$ErrorActionPreference = "Stop"
chcp 65001 | Out-Null
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# Depuis le repo MVP_QAIC_PY
python -m mvp_qaic_py.p147_operator_polish --help
# Les Apps NiceGUI exportées restent à lancer manuellement depuis 05_EXPORTS.
```

Rappel : pas de public deploy, pas de Sheet write, pas de broker/order/sizing.
