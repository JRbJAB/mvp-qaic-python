
# P127 Operator Run Shortcut
# LOCAL ONLY / HUMAN REVIEW ONLY / NO SHEET WRITE / NO BROKER / NO ORDER / NO SIZING

$ErrorActionPreference = "Stop"
chcp 65001 | Out-Null
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

function Fail($Message) { throw "[P127 SHORTCUT BLOCKED] $Message" }

$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$CandidateRepo = Resolve-Path -LiteralPath (Join-Path $Here "..\..") -ErrorAction SilentlyContinue
if (-not $CandidateRepo) { Fail "Cannot resolve repo root from shortcut location" }

$RepoRoot = $CandidateRepo.Path
$PyProject = Join-Path $RepoRoot "pyproject.toml"
$PackageDir = Join-Path $RepoRoot "mvp_qaic_py"
if (-not (Test-Path -LiteralPath $PyProject)) { Fail "pyproject.toml not found" }
if (-not (Test-Path -LiteralPath $PackageDir)) { Fail "mvp_qaic_py package not found" }

Set-Location -LiteralPath $RepoRoot

$PythonExe = (Get-Command python.exe -ErrorAction Stop).Source
$ExportsDir = Join-Path $RepoRoot "05_EXPORTS"
$Stamp = Get-Date -Format "yyyyMMdd_HHmmss"

$P124Dir = Join-Path $ExportsDir ("P127_RUN_P124_INPUT_" + $Stamp)
$P125Dir = Join-Path $ExportsDir ("P127_RUN_P125_REVIEW_" + $Stamp)
$P126Dir = Join-Path $ExportsDir ("P127_RUN_P126_REGISTRY_" + $Stamp)

[System.IO.Directory]::CreateDirectory($P124Dir) | Out-Null
[System.IO.Directory]::CreateDirectory($P125Dir) | Out-Null
[System.IO.Directory]::CreateDirectory($P126Dir) | Out-Null

$OldPythonPath = $env:PYTHONPATH
$env:PYTHONPATH = $RepoRoot

& $PythonExe -m mvp_qaic_py.gem_loop_input_helper `
  --output-dir $P124Dir `
  --run-id ("P127-P124-" + $Stamp) `
  --generated-at-utc "2026-06-22T00:00:00Z" `
  --notes "P127 shortcut created local P124 input folder. Operator must fill portfolio and GEM response manually."

if ($LASTEXITCODE -ne 0) { Fail "P124 input helper failed" }

Write-Host ""
Write-Host "P124 folder created:"
Write-Host $P124Dir
Write-Host ""
Write-Host "ACTION REQUIRED:"
Write-Host "1. Fill portfolio_input.txt"
Write-Host "2. Run the P118 prompt command from P124_OPERATOR_COMMANDS.md"
Write-Host "3. Paste GEM answer into gem_response.txt"
Write-Host "4. Run P125 and P126 commands below manually."
Write-Host ""
Write-Host "P125 review command:"
Write-Host "python -m mvp_qaic_py.gem_manual_test_review_pack --output-dir `"$P125Dir`" --p124-run-dir `"$P124Dir`" --run-id P127-P125-$Stamp"
Write-Host ""
Write-Host "P126 registry command:"
Write-Host "python -m mvp_qaic_py.daily_run_registry --output-dir `"$P126Dir`" --exports-dir `"$ExportsDir`" --run-id P127-P126-$Stamp"
Write-Host ""
Write-Host "SAFETY: HUMAN_REVIEW_ONLY / NO_SHEET_WRITE / NO_BROKER / NO_ORDER / NO_SIZING / NO_AUTO_APPLY_GEM_RESPONSE / NO_REVOLUTX_REAL_ACCESS_FROM_MVP"

$env:PYTHONPATH = $OldPythonPath
