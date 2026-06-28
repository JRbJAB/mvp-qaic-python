# REFLEX_FAST_GATE.ps1
# MVP QAIC Reflex Fast Gate R6A
# Validates route, source, fresh HEAD runtime, optional server start and HTTP probe.
# Local/private only. No deploy, no broker/order/sizing, no Sheet/BQ write.

[CmdletBinding()]
param(
  [string]$RepoRoot = "",
  [string]$Route = "/cdc-dev-tracker",
  [int]$FrontendPort = 3000,
  [int]$BackendPort = 8000,
  [int]$TimeoutSec = 240,
  [switch]$NoRuntimeStart,
  [switch]$NoKillPorts
)

$ErrorActionPreference = "Stop"
chcp 65001 | Out-Null
[Console]::OutputEncoding = [Text.Encoding]::UTF8
$OutputEncoding = [Text.Encoding]::UTF8

Remove-Item Env:\PYTHONNOUSERSITE -ErrorAction SilentlyContinue
$env:NO_PUBLIC_DEPLOY = "true"
$env:NO_LIVE_ACTION = "true"
$env:NO_BROKER_ORDER_SIZING = "true"
$env:NO_SHEET_WRITE = "true"
$env:NO_BIGQUERY_WRITE = "true"
$env:HUMAN_REVIEW_ONLY = "true"
$env:BROWSER = "none"
$env:PYTHONUTF8 = "1"
$env:REFLEX_USE_NPM = "true"
$env:NPM_CONFIG_INCLUDE = "optional"
$env:NPM_CONFIG_AUDIT = "false"
$env:NPM_CONFIG_FUND = "false"
Remove-Item Env:\NPM_CONFIG_OPTIONAL -ErrorAction SilentlyContinue

if (-not $RepoRoot) {
  $people = [char]::ConvertFromUtf32(0x1F465)
  $chart  = [char]::ConvertFromUtf32(0x1F4C8)
  $RepoRoot = [IO.Path]::Combine(
    "G:\Mon Drive",
    "$people JULIEN [Perso]",
    "$chart Trading JRb",
    "Solutions & Dev (Trading JRb)",
    "MVP_QAIC_PY"
  )
}

if (-not [IO.Directory]::Exists($RepoRoot)) {
  throw "RepoRoot not found: $RepoRoot"
}

$runtimeName = "HEAD_REFLEX_FAST_GATE_R6A"
$runtimeRoot = [IO.Path]::Combine($env:LOCALAPPDATA, "MVP_QAIC_REFLEX_RUNTIME", $runtimeName)
$archivePath = [IO.Path]::Combine($env:TEMP, "MVP_QAIC_REFLEX_FAST_GATE_R6A_HEAD.zip")
$startScript = [IO.Path]::Combine($RepoRoot, "scripts", "START_REFLEX_LOCAL_SAFE.ps1")
$stopScript = [IO.Path]::Combine($RepoRoot, "scripts", "STOP_REFLEX_LOCAL_SAFE.ps1")

function Write-Step([string]$Text) {
  Write-Host "===== $Text ====="
}

function Test-PortOpen {
  param([int]$Port)
  try {
    $client = New-Object Net.Sockets.TcpClient
    $iar = $client.BeginConnect("127.0.0.1", $Port, $null, $null)
    $ok = $iar.AsyncWaitHandle.WaitOne(800, $false)
    if ($ok) { $client.EndConnect($iar) }
    $client.Close()
    return [bool]$ok
  } catch {
    return $false
  }
}

function Stop-PortOwners {
  param([int[]]$Ports)
  foreach ($port in $Ports) {
    try {
      $owners = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue |
        Select-Object -ExpandProperty OwningProcess -Unique
      foreach ($ownerPid in $owners) {
        if ($ownerPid -and $ownerPid -ne $PID) {
          $proc = Get-Process -Id $ownerPid -ErrorAction SilentlyContinue
          if ($proc -and $proc.ProcessName -match '^(python|pythonw|node|bun|reflex)$') {
            Stop-Process -Id $ownerPid -Force -ErrorAction SilentlyContinue
            Write-Host "STOPPED_PORT=$port PID=$ownerPid PROCESS=$($proc.ProcessName)"
          }
        }
      }
    } catch {}
  }
}

Write-Step "R6A REFLEX FAST GATE"
Write-Host "REPO=$RepoRoot"
Write-Host "ROUTE=$Route"
Write-Host "NO_RUNTIME_START=$NoRuntimeStart"
Write-Host "RUNTIME_ROOT=$runtimeRoot"

Push-Location -LiteralPath $RepoRoot
try {
  $head = git rev-parse --short=12 HEAD
  Write-Host "HEAD=$head"

  Write-Step "GATE 1 ROUTE STRING IN HEAD SOURCE"
  $uiDir = [IO.Path]::Combine($RepoRoot, "mvp_qaic_reflex_ui")
  if (-not [IO.Directory]::Exists($uiDir)) {
    throw "Missing mvp_qaic_reflex_ui directory"
  }

  $routePattern = [regex]::Escape($Route)
  $routeHits = Get-ChildItem -LiteralPath $uiDir -Filter "*.py" -Recurse |
    Select-String -Pattern $routePattern -ErrorAction SilentlyContinue

  if (-not $routeHits) {
    Write-Host "ROUTE_FOUND=False"
    throw "Route string not found in source: $Route"
  }
  Write-Host "ROUTE_FOUND=True"
  $routeHits | Select-Object Path,LineNumber,Line | Format-Table -AutoSize

  Write-Step "GATE 2 PYTHON COMPILE"
  $pyFiles = @(
    [IO.Path]::Combine($uiDir, "mvp_qaic_reflex_ui.py")
  )
  $routePage = [IO.Path]::Combine($uiDir, "cdc_dev_tracker_reflex_page.py")
  if ([IO.File]::Exists($routePage)) { $pyFiles += $routePage }

  foreach ($file in $pyFiles) {
    if ([IO.File]::Exists($file)) {
      & "C:\Python314\python.exe" -m py_compile $file
      if ($LASTEXITCODE -ne 0) { throw "py_compile failed: $file" }
      Write-Host "PY_COMPILE_OK=$file"
    }
  }

  Write-Step "GATE 3 BUILD FRESH HEAD RUNTIME"
  if ([IO.Directory]::Exists($runtimeRoot)) {
    Remove-Item -LiteralPath $runtimeRoot -Recurse -Force
  }
  if ([IO.File]::Exists($archivePath)) {
    Remove-Item -LiteralPath $archivePath -Force
  }

  git archive --format=zip -o $archivePath HEAD
  if ($LASTEXITCODE -ne 0) { throw "git archive failed" }

  [IO.Directory]::CreateDirectory($runtimeRoot) | Out-Null
  Expand-Archive -LiteralPath $archivePath -DestinationPath $runtimeRoot -Force

  Write-Step "GATE 4 ROUTE STRING IN FRESH RUNTIME"
  $runtimeUiDir = [IO.Path]::Combine($runtimeRoot, "mvp_qaic_reflex_ui")
  $runtimeHits = Get-ChildItem -LiteralPath $runtimeUiDir -Filter "*.py" -Recurse |
    Select-String -Pattern $routePattern -ErrorAction SilentlyContinue

  if (-not $runtimeHits) {
    throw "Route string not found in fresh runtime: $Route"
  }
  Write-Host "RUNTIME_ROUTE_FOUND=True"

  if ($NoRuntimeStart) {
    Write-Step "FINAL_OK NO RUNTIME START"
    Write-Host "STATUS=OK_R6A_REFLEX_FAST_GATE_SOURCE_AND_RUNTIME_READY_NO_RUN"
    Write-Host "HEAD=$head"
    Write-Host "RUNTIME_ROOT=$runtimeRoot"
    exit 0
  }

  Write-Step "GATE 5 STOP OLD LOCAL SERVERS"
  if (-not $NoKillPorts) {
    if ([IO.File]::Exists($stopScript)) {
      powershell -NoProfile -ExecutionPolicy Bypass -File $stopScript -KillLocalRuntimeChildren
    } else {
      Stop-PortOwners -Ports @($FrontendPort, $BackendPort)
    }
  }

  Write-Step "GATE 6 START FRESH RUNTIME"
  if (-not [IO.File]::Exists($startScript)) {
    throw "Missing START_REFLEX_LOCAL_SAFE.ps1: $startScript"
  }

  $args = @(
    "-NoProfile",
    "-ExecutionPolicy", "Bypass",
    "-NoExit",
    "-File", $startScript,
    "-RuntimeRoot", $runtimeRoot,
    "-CleanWeb",
    "-MaxRestarts", "1",
    "-FrontendPort", [string]$FrontendPort,
    "-BackendPort", [string]$BackendPort
  )
  Start-Process -FilePath "powershell.exe" -ArgumentList $args

  Write-Step "GATE 7 HTTP PROBE"
  $ok = $false
  $rootStatus = "NA"
  $routeStatus = "NA"
  $deadline = (Get-Date).AddSeconds($TimeoutSec)

  while ((Get-Date) -lt $deadline) {
    Start-Sleep -Seconds 2
    try {
      $rootResp = Invoke-WebRequest -Uri ("http://127.0.0.1:{0}/" -f $FrontendPort) -UseBasicParsing -TimeoutSec 3
      $rootStatus = [string]$rootResp.StatusCode
    } catch {
      $rootStatus = "PENDING"
    }

    foreach ($candidate in @($Route, ($Route.TrimEnd("/") + "/"))) {
      $url = "http://127.0.0.1:{0}{1}" -f $FrontendPort, $candidate
      try {
        $resp = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 3
        $routeStatus = [string]$resp.StatusCode
        if ($resp.StatusCode -ge 200 -and $resp.StatusCode -lt 400) {
          Write-Host "ROUTE_OK=$url STATUS=$($resp.StatusCode)"
          $ok = $true
          break
        }
      } catch {
        if ($_.Exception.Response) {
          $routeStatus = [string]([int]$_.Exception.Response.StatusCode)
        } else {
          $routeStatus = "PENDING"
        }
      }
    }

    Write-Host "PROBE ROOT=$rootStatus ROUTE=$routeStatus"
    if ($ok) { break }

    if ($rootStatus -eq "200" -and $routeStatus -eq "404") {
      throw "Root is served but route is 404. Patch app route registry/app.add_page, not server."
    }
  }

  if (-not $ok) {
    throw "Route probe failed. ROOT_LAST=$rootStatus ROUTE_LAST=$routeStatus"
  }

  Write-Step "FINAL_OK"
  Write-Host "STATUS=OK_R6A_REFLEX_FAST_GATE_RUNTIME_ROUTE_UP"
  Write-Host "HEAD=$head"
  Write-Host "ROUTE=$Route"
  Write-Host "RUNTIME_ROOT=$runtimeRoot"
} finally {
  Pop-Location
}