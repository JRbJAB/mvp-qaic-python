# MVP QAIC — Runner Reference Standard R1

Status: `ACTIVE`
Version: `R1`
Scope: MVP QAIC / Reflex / UI Tracker / local execution packs
Date: 2026-06-29
Owner: MVP QAIC

## 1. Purpose

This document is the mandatory reference for every future MVP QAIC runner pack.

It exists because the R2A Reflex private preflight proved that the project evidence was good while multiple shell runners produced false blockers. A runner must measure the project state. It must not create artificial failures.

## 2. Mandatory contract

No future runner pack may be delivered unless it respects this contract.

1. No interactive Python launch is allowed.
2. No Git launch without an explicit Git subcommand is allowed.
3. Empty argument arrays must fail before execution.
4. Do not use `New-Item -LiteralPath` to create folders.
5. Do not use untested generic wrappers for Git or Python.
6. Logs must show exact command intent, exit code, and business status.
7. One runner must have one goal.
8. Informational metrics must not block.
9. Every runner must run its own preflight before touching the project.
10. Do not launch a new full run when the previous run already proved the business point.
11. No commit, tag, or push may occur after failed tests.
12. No generated runner pack may be delivered without a self-test.
13. ZIP payload paths must not contain emoji filenames.
14. Do not use long inline PowerShell patches; use tracked scripts or small reviewed patches.
15. After two repeated failures on the same workstream, Codex is required before another attempt.

## 3. Required runner structure

Every runner must contain four clear phases:

```text
RUNNER_PREFLIGHT
EVIDENCE_COLLECTION
VALIDATION
SUMMARY
```

### RUNNER_PREFLIGHT

Checks the runner itself before touching the project:

```text
- paths are non-empty
- repo exists
- Python exists when Python is required
- Git exists when Git is required
- Python receives a script path or module mode
- Git receives a subcommand
- report folder can be created with a PowerShell 5.1 and PS7 safe method
```

### EVIDENCE_COLLECTION

Collects evidence without repository write unless the pack explicitly announces a controlled write.

### VALIDATION

Separates business gates from informational metrics.

### SUMMARY

The final status must separate:

```text
EVIDENCE_OK=True|False
RUNNER_OK=True|False
FINAL_STATUS=...
```

A runner defect must never be presented as a project failure.

## 4. Python rule

Forbidden patterns:

```text
python
python.exe
& $Python
Start-Process $Python
```

Allowed only when the first argument is explicit:

```text
python tools/some_gate.py --out ... --repo ...
python -m pytest ...
python -m ruff check .
```

Mandatory guard logic:

```text
- reject empty args
- accept first arg only when it is '-m' or a .py script
- never allow Python REPL from a runner
```

## 5. Git rule

Forbidden patterns:

```text
git
& $Git
```

Allowed only with an explicit subcommand:

```text
git -C <repo> status --short
git -C <repo> log -1 --oneline --decorate
git -C <repo> tag --points-at HEAD
```

Mandatory guard logic:

```text
- reject empty Git args
- log the intended Git operation
- do not infer CLEAN_GIT from Git help output
```

## 6. PowerShell compatibility rule

Do not use `New-Item -LiteralPath` for folder creation.

Use this cross-version pattern:

```text
[System.IO.Directory]::CreateDirectory($Report) | Out-Null
```

All runners must be Windows PowerShell 5.1 and PowerShell 7 safe unless the runner states `PS7_ONLY=True`.

## 7. Reflex `.web` rule

Reflex `.web` can contain thousands of generated files. Total file count is informational only.

Informational:

```text
WEB_TOTAL_FILE_COUNT
```

Blocking only when true or greater than zero:

```text
FORBIDDEN_SHIM_FILE_COUNT
FORBIDDEN_ORACLE_DRIFT
FORBIDDEN_PUBLIC_DEPLOY
```

## 8. Status taxonomy

Allowed final statuses:

```text
PASS
BLOCKED_BY_PROJECT_EVIDENCE
BLOCKED_BY_RUNNER_DEFECT
ABORTED_BY_PREFLIGHT
```

A generic `BLOCKED` without cause is forbidden.

## 9. R2A incident audit summary

### R2A

Cause: `ui_tracker_route_binding_gate.py` was called with an obsolete `--approved-oracle` argument.

Classification: runner defect.

### R2A-R2

Cause: Python could be launched with empty args and enter REPL.

Classification: runner defect.

### R2A-R3

Cause: total `.web` file count was treated as a blocker.

Classification: validation-design defect.

### R2A-R5

Cause: Git was called without a subcommand, printed Git help, and produced a false `CLEAN_GIT=False`.

Classification: wrapper defect.

### R2A-R6

Cause: invalid folder creation pattern using `New-Item -LiteralPath`.

Classification: PowerShell compatibility defect.

## 10. Stop rule

If a runner fails twice because of shell glue, stop the run loop. Do not keep generating patch packs. First produce:

```text
- root-cause audit
- standard update
- smallest missing proof only
```

## 11. Pack delivery checklist

Before any ZIP delivery:

```text
[ ] RUNNER_PREFLIGHT exists.
[ ] Python cannot start interactively.
[ ] Git cannot run without a subcommand.
[ ] Arguments are explicit and non-empty.
[ ] Report folder creation is PowerShell 5.1 and PowerShell 7 safe.
[ ] Informational metrics cannot block.
[ ] Final status separates evidence from runner health.
[ ] No commit, tag, push, public deploy, or broker action occurs unless explicitly requested.
[ ] No commit, tag, or push occurs after a failed test gate.
[ ] Generated runner pack self-test passed.
[ ] ZIP payload paths contain no emoji filenames.
[ ] No long inline PowerShell patch is embedded in the runner.
[ ] Codex handoff is required after two repeated failures on the same workstream.
[ ] Double-click command targets the intended script.
[ ] Report path includes the pack version.
```

## 12. Assistant and Codex instruction

Future assistant/Codex work must treat this document as binding. If a proposed pack violates this standard, the pack must not be delivered.
