param(
  [switch]$SelfTest,
  [switch]$Build,
  [string]$Repo = "C:\JRb_TRADING_OS\MVP_QAIC_PY",
  [string]$ReportBase = "C:\JRb_TRADING_OS\_RUN_REPORTS\MVP_QAIC_PY"
)

$ErrorActionPreference = "Stop"

$RunnerName = "P_R16F2H8B_REFLEX_DOCKER_BUILD_SELECTOR_NO_RUNTIME"
$PinnedImage = "jrb-reflex-pinned-hub:py312-node22-reflex096p1"
$DockerfileRel = "docker\reflex-pinned-hub\Dockerfile"
$ContextRel = "docker\reflex-pinned-hub"
$PolicyId = "R16F2H4_REFLEX_RUNTIME_POLICY_LOCK"

function New-H8BReportRoot {
  param([string]$BasePath)
  if ([string]::IsNullOrWhiteSpace($BasePath)) {
    throw "ReportBase is empty"
  }
  $stamp = Get-Date -Format "yyyyMMdd_HHmmss"
  $root = Join-Path $BasePath "${RunnerName}_$stamp"
  [System.IO.Directory]::CreateDirectory($root) | Out-Null
  return $root
}

function Write-H8BTextFile {
  param(
    [string]$Path,
    [string[]]$Lines
  )
  $encoding = New-Object System.Text.UTF8Encoding($false)
  [System.IO.File]::WriteAllLines($Path, $Lines, $encoding)
}

function Test-H8BSelf {
  $script:SelfTestExitCode = 0
  $scriptPath = $PSCommandPath
  if ([string]::IsNullOrWhiteSpace($scriptPath)) {
    throw "Self path is empty"
  }
  $source = [System.IO.File]::ReadAllText($scriptPath)
  $forbidden = @(
    ("git add" + " ."),
    ("git " + "reset"),
    ("docker" + " run"),
    ("reflex" + " run"),
    ("Start" + "-Process"),
    ("clasp" + " push"),
    ("Remove" + "-Item")
  )
  $hits = New-Object System.Collections.Generic.List[string]
  foreach ($pattern in $forbidden) {
    if ($source.Contains($pattern)) {
      $hits.Add($pattern) | Out-Null
    }
  }
  if ($hits.Count -gt 0) {
    Write-Output "SELF_TEST_OK=False"
    foreach ($hit in $hits) {
      Write-Output "FORBIDDEN_PATTERN=$hit"
    }
    $script:SelfTestExitCode = 1
    return
  }
  Write-Output "SELF_TEST_OK=True"
  Write-Output "NO_RUNTIME=True"
  Write-Output "DEFAULT_DRY_RUN=True"
}

if ($SelfTest) {
  Test-H8BSelf
  exit $script:SelfTestExitCode
}

$reportRoot = $null
$statusPath = $null
$auditPath = $null
$runnerOk = $true
$buildSelectorStatus = "DRY_RUN_NO_BUILD"
$sourceBuildPathStatus = "UNKNOWN"
$pinnedImageStatus = "UNKNOWN"
$finalStatus = "PASS"
$nextRequiredAction = "OPERATOR_REVIEW_AND_OPTIONAL_EXPLICIT_BUILD_FLAG"
$buildExitCode = $null
$buildCommand = "docker build -f $DockerfileRel -t $PinnedImage $ContextRel"

try {
  $reportRoot = New-H8BReportRoot -BasePath $ReportBase
  $statusPath = Join-Path $reportRoot "STATUS.json"
  $auditPath = Join-Path $reportRoot "BUILD_SELECTOR_AUDIT.md"

  if (-not (Test-Path -LiteralPath $Repo -PathType Container)) {
    throw "Repo does not exist: $Repo"
  }
  $repoPath = (Resolve-Path -LiteralPath $Repo).Path
  $dockerfilePath = Join-Path $repoPath $DockerfileRel
  $contextPath = Join-Path $repoPath $ContextRel

  if ((Test-Path -LiteralPath $dockerfilePath -PathType Leaf) -and
      (Test-Path -LiteralPath $contextPath -PathType Container)) {
    $sourceBuildPathStatus = "PRESENT_RECOVERED_REPLACEMENT"
  } else {
    $sourceBuildPathStatus = "MISSING"
    $finalStatus = "BLOCKED_BY_SOURCE_BUILD_PATH"
    $nextRequiredAction = "RESTORE_DOCKERFILE_AND_CONTEXT_PATH"
  }

  $docker = Get-Command docker -ErrorAction SilentlyContinue
  if ($docker -and -not [string]::IsNullOrWhiteSpace($docker.Source)) {
    $inspectStdout = Join-Path $reportRoot "docker_image_inspect.stdout.txt"
    $inspectStderr = Join-Path $reportRoot "docker_image_inspect.stderr.txt"
    $dockerConfig = Join-Path $reportRoot "docker-config"
    [System.IO.Directory]::CreateDirectory($dockerConfig) | Out-Null
    $previousErrorPreference = $ErrorActionPreference
    $previousDockerConfig = $env:DOCKER_CONFIG
    $ErrorActionPreference = "Continue"
    try {
      $env:DOCKER_CONFIG = $dockerConfig
      & $docker.Source image inspect $PinnedImage 1>$inspectStdout 2>$inspectStderr
      $inspectExitCode = $LASTEXITCODE
    } finally {
      $ErrorActionPreference = $previousErrorPreference
      $env:DOCKER_CONFIG = $previousDockerConfig
    }
    if ($inspectExitCode -eq 0) {
      $pinnedImageStatus = "PRESENT"
    } else {
      $inspectError = ""
      if (Test-Path -LiteralPath $inspectStderr -PathType Leaf) {
        $inspectError = [System.IO.File]::ReadAllText($inspectStderr)
      }
      if ($inspectError -like "*Access is denied*") {
        $pinnedImageStatus = "DOCKER_ACCESS_DENIED"
      } else {
        $pinnedImageStatus = "ABSENT"
      }
    }

    if ($Build) {
      if ($sourceBuildPathStatus -ne "PRESENT_RECOVERED_REPLACEMENT") {
        throw "Cannot build without recovered source path"
      }
      $buildSelectorStatus = "EXPLICIT_BUILD_REQUESTED"
      & $docker.Source build -f $dockerfilePath -t $PinnedImage $contextPath
      $buildExitCode = $LASTEXITCODE
      if ($buildExitCode -ne 0) {
        $finalStatus = "BLOCKED_BY_BUILD_FAILURE"
        $nextRequiredAction = "FIX_DOCKER_BUILD_FAILURE_WITHOUT_RUNTIME"
      } else {
        $buildSelectorStatus = "EXPLICIT_BUILD_COMPLETED"
        $nextRequiredAction = "REVIEW_REPORT_AND_IMAGE_METADATA"
      }
    }
  } else {
    $pinnedImageStatus = "DOCKER_NOT_FOUND"
    if ($Build) {
      $finalStatus = "BLOCKED_BY_DOCKER_UNAVAILABLE"
      $nextRequiredAction = "INSTALL_OR_START_DOCKER_BEFORE_EXPLICIT_BUILD"
      $buildSelectorStatus = "EXPLICIT_BUILD_NOT_STARTED"
    }
  }

  $status = [ordered]@{
    runner_name = $RunnerName
    runner_ok = $runnerOk
    final_status = $finalStatus
    next_required_action = $nextRequiredAction
    report_root = $reportRoot
    repo = $repoPath
    policy_id = $PolicyId
    reflex_policy_guard_required = $true
    pinned_image = $PinnedImage
    pinned_image_status = $pinnedImageStatus
    source_build_path_status = $sourceBuildPathStatus
    build_selector_status = $buildSelectorStatus
    default_dry_run = (-not $Build)
    no_runtime = $true
    build_command = $buildCommand
    build_exit_code = $buildExitCode
    original_provenance_proven = $false
    recovered_replacement_source_path = $true
  }
  $status | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $statusPath -Encoding UTF8

  $audit = @(
    "# H8B Reflex Docker Build Selector - No Runtime",
    "",
    "REPORT_ROOT=$reportRoot",
    "POLICY_ID=$PolicyId",
    "REFLEX_POLICY_GUARD_REQUIRED=True",
    "PINNED_IMAGE=$PinnedImage",
    "SOURCE_BUILD_PATH_STATUS=$sourceBuildPathStatus",
    "BUILD_SELECTOR_STATUS=$buildSelectorStatus",
    "PINNED_IMAGE_STATUS=$pinnedImageStatus",
    "FINAL_STATUS=$finalStatus",
    "NEXT_REQUIRED_ACTION=$nextRequiredAction",
    "",
    "## Provenance",
    "",
    "ORIGINAL_PROVENANCE_PROVEN=False",
    "RECOVERED_REPLACEMENT_SOURCE_PATH=True",
    "",
    "## Build Command",
    "",
    $buildCommand
  )
  Write-H8BTextFile -Path $auditPath -Lines $audit

  Write-Output "FINAL_STATUS=$finalStatus"
  Write-Output "REPORT_ROOT=$reportRoot"
  Write-Output "PINNED_IMAGE_STATUS=$pinnedImageStatus"
  Write-Output "SOURCE_BUILD_PATH_STATUS=$sourceBuildPathStatus"
  Write-Output "BUILD_SELECTOR_STATUS=$buildSelectorStatus"
  Write-Output "BUILD_COMMAND=$buildCommand"
  exit 0
} catch {
  $runnerOk = $false
  if ($null -eq $reportRoot) {
    $finalStatus = "ABORTED_BY_PREFLIGHT"
    $nextRequiredAction = "REPORT_ROOT_NOT_WRITABLE"
  } elseif ($finalStatus -eq "PASS") {
    $finalStatus = "BLOCKED_BY_RUNNER_DEFECT"
    $nextRequiredAction = "FIX_H8B_SELECTOR"
  }
  if ($null -ne $statusPath) {
    $status = [ordered]@{
      runner_name = $RunnerName
      runner_ok = $runnerOk
      final_status = $finalStatus
      next_required_action = $nextRequiredAction
      report_root = $reportRoot
      error = "$($_.Exception.GetType().Name):$($_.Exception.Message)"
    }
    $status | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $statusPath -Encoding UTF8
  }
  Write-Output "FINAL_STATUS=$finalStatus"
  Write-Output "REPORT_ROOT=$reportRoot"
  Write-Output "ERROR=$($_.Exception.Message)"
  exit 1
}
