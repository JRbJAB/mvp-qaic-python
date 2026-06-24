$ErrorActionPreference = "Stop"
$repo = "C:\Users\Julie\Documents\JRb-Dev\MVP_QAIC_PY_WORK_20260623_192901"
Set-Location -LiteralPath $repo
Write-Host "REPO=$repo"
Write-Host "HEAD=$(git rev-parse --short HEAD)"
Write-Host "STATUS:"
git status --short --branch
Write-Host "PORT_8080:"
Get-NetTCPConnection -LocalPort 8080 -State Listen -ErrorAction SilentlyContinue | Format-Table -AutoSize
