$ErrorActionPreference = "Stop"
chcp 65001 | Out-Null
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

$SRC = "Q:\MVP_QAIC_PY"
$RUN_ROOT = Join-Path $env:LOCALAPPDATA "MVP_QAIC_REFLEX_RUNTIME"
$run = Get-ChildItem -LiteralPath $RUN_ROOT -Directory -Filter "P_REFLEX_06C_*" |
  Sort-Object LastWriteTime -Descending |
  Select-Object -First 1

if (-not $run) {
  throw "STOP: aucun runtime P_REFLEX_06C trouvé"
}

$RUN_DIR = $run.FullName
$WEB_DIR = Join-Path $RUN_DIR ".web"

Copy-Item -LiteralPath (Join-Path $SRC "rxconfig.py") -Destination (Join-Path $RUN_DIR "rxconfig.py") -Force
robocopy (Join-Path $SRC "mvp_qaic_reflex_ui") (Join-Path $RUN_DIR "mvp_qaic_reflex_ui") /E /NFL /NDL /NJH /NJS /NP /XF "desktop.ini" | Out-Host
if ($LASTEXITCODE -gt 7) { throw "STOP: robocopy UI failed" }
$global:LASTEXITCODE = 0

Set-Location -LiteralPath $WEB_DIR
$nodeArch = (& node -p "process.arch").Trim()
switch ($nodeArch) {
  "arm64" { $bindingPkg = "@rolldown/binding-win32-arm64-msvc" }
  "x64"   { $bindingPkg = "@rolldown/binding-win32-x64-msvc" }
  default { throw "STOP: architecture Node non gérée: $nodeArch" }
}

node -e "try { console.log(require.resolve('$bindingPkg')); process.exit(0); } catch (e) { process.exit(1); }"
if ($LASTEXITCODE -ne 0) {
  npm install --save-dev --include=optional --force $bindingPkg
  if ($LASTEXITCODE -ne 0) { throw "STOP: npm install binding failed" }
}

Set-Location -LiteralPath $RUN_DIR
Write-Host "============================================================"
Write-Host "P_REFLEX_07 LOCAL PRIVATE PREVIEW"
Write-Host "URL=http://localhost:3000/"
Write-Host "BACKEND=http://127.0.0.1:8000"
Write-Host "PUBLIC_DEPLOY=false"
Write-Host "BROKER_ORDER_SIZING=false"
Write-Host "============================================================"

python -m reflex run --env dev --backend-host 127.0.0.1 --frontend-port 3000
