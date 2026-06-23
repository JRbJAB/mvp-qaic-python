$ErrorActionPreference = "Stop"
chcp 65001 | Out-Null
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

# MVP QAIC P151 — local launch smoke command
# Vérification seulement : aucun Sheet write, aucun public deploy, aucun broker/order/sizing.

$app = "G:\Mon Drive\👥 JULIEN [Perso]\📈 Trading JRb\Solutions & Dev (Trading JRb)\MVP_QAIC_PY\05_EXPORTS\P147_OPERATOR_POLISH_20260623_130332\P147_NICEGUI_OPERATOR_POLISH_APP.py"
if (-not (Test-Path -LiteralPath $app)) { throw "App NiceGUI introuvable: $app" }
Write-Host "LOCAL_PRIVATE_APP=$app"
Write-Host "Launch manually with: python `"$app`""
# Décommenter volontairement la ligne suivante seulement pour lancer l'UI locale.
# & python "$app"
