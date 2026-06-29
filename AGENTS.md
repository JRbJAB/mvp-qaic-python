# MVP QAIC — Agent Instructions

These instructions apply to AI assistants, Codex sessions, and automation work on this repository.

## Active runner standard

Follow:

`docs/dev_tracking/runner_quality/RUNNER_REFERENCE_STANDARD_R1.md`

## Non-negotiable runner rules

- Do not ship a runner that can launch Python interactively.
- Do not call Git without an explicit subcommand.
- Do not silently accept empty argument arrays.
- Do not use `New-Item -LiteralPath` for folder creation.
- Do not use untested generic wrappers for Git/Python.
- Do not let informational metrics block a run.
- Do not relaunch a full runner when prior evidence already proves the business point.
- After two shell-glue defects, stop and audit before producing another runner.

## MVP QAIC safety rules

- No broker action.
- No order action.
- No sizing action.
- No public deploy unless explicitly authorized.
- Human review only for trading/portfolio outputs.

## Required reporting

Every runner must report:

```text
EVIDENCE_OK=True|False
RUNNER_OK=True|False
FINAL_STATUS=<PASS|BLOCKED_BY_PROJECT_EVIDENCE|BLOCKED_BY_RUNNER_DEFECT|ABORTED_BY_PREFLIGHT>
```
