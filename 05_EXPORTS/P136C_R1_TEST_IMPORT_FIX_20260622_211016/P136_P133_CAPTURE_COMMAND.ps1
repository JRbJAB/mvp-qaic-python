$ErrorActionPreference = "Stop"
chcp 65001 | Out-Null
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

$GitExe = (Get-Command git.exe -ErrorAction SilentlyContinue).Source
$RepoRoot = $null

if ($GitExe) {
  try {
    $maybeRoot = (& $GitExe rev-parse --show-toplevel 2>$null)
    if ($LASTEXITCODE -eq 0 -and $maybeRoot) {
      $maybeRoot = $maybeRoot.Trim()
      if ((Split-Path -Leaf $maybeRoot) -eq "MVP_QAIC_PY") {
        $RepoRoot = $maybeRoot
      }
    }
  } catch {}
}

if (-not $RepoRoot) {
  $people = [string]::Concat([char]0xD83D, [char]0xDC65)
  $chart  = [string]::Concat([char]0xD83D, [char]0xDCC8)
  $RepoRoot = "G:\Mon Drive\$people JULIEN [Perso]\$chart Trading JRb\Solutions & Dev (Trading JRb)\MVP_QAIC_PY"
}

if (-not (Test-Path -LiteralPath $RepoRoot)) {
  throw "Repo introuvable: $RepoRoot"
}

Set-Location -LiteralPath $RepoRoot

$responseText = 'G:\Mon Drive\👥 JULIEN [Perso]\📈 Trading JRb\Solutions & Dev (Trading JRb)\MVP_QAIC_PY\05_EXPORTS\P136C_R1_TEST_IMPORT_FIX_20260622_211016\P136_IMPORTED_GEM_RESPONSE.md'
$outputDir = 'G:\Mon Drive\👥 JULIEN [Perso]\📈 Trading JRb\Solutions & Dev (Trading JRb)\MVP_QAIC_PY\05_EXPORTS\P136C_R1_TEST_IMPORT_FIX_20260622_211016\P133_FROM_P136_REAL_RESPONSE_IMPORT'
New-Item -ItemType Directory -Path $outputDir -Force | Out-Null

python -m mvp_qaic_py.gem_multimodal_response_capture_gate `
  --response-text $responseText `
  --output-dir $outputDir `
  --run-id 'P136C-R1-TEST-IMPORT-FIX-20260622-P133-GATE' `
  --generated-at-utc '2026-06-22T00:00:00Z'

Write-Host "P133_OUTPUT_DIR=$outputDir"
Write-Host "OPEN_FIRST=$(Join-Path $outputDir 'P133_GEM_RESPONSE_HUMAN_REVIEW.md')"
Write-Host "OPEN_JSON=$(Join-Path $outputDir 'P133_GEM_RESPONSE_PRETTY.json')"
