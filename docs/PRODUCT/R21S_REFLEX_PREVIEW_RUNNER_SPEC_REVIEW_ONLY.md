# R21S Reflex Preview Runner Spec - Review Only

Status: `R21S_REFLEX_PREVIEW_RUNNER_SPEC=READY`

R21S is a review-only runner specification. It is not a runtime runner, does not
create a PowerShell runner, does not launch Reflex execution, does not use
Docker, does not call providers, does not touch broker/order/sizing paths, does
not write Sheets or BigQuery, does not emit HTML, and does not create export
artifacts.

## Source Binding

```text
R21S_REFLEX_PREVIEW_RUNNER_SPEC=READY
SOURCE_R21R_PREVIEW_STRATEGY_BOUND=True
RUNNER_SPEC_REVIEW_ONLY=True
RUNNER_EXECUTED=False
REFLEX_RUNTIME_STATUS=PAUSED
REFLEX_RUNTIME_RUNNER_CHAIN=STOPPED_UNTIL_HUMAN_APPROVAL
```

## Human Approval Gate

```text
HUMAN_APPROVED_PRIVATE_PREVIEW_REQUIRED=True
REFLEX_CLI_HELP_CAPTURE_REQUIRED=True
REFLEX_VERSION_CAPTURE_REQUIRED=True
NO_FRONTEND_HOST_FLAG=True
```

R21T may only happen after explicit human approval. R21T must capture CLI
version and help evidence before any private preview attempt. R21S does not
capture live help or version output.

## Runner Shape Requirements

```text
PS51_COMPATIBLE=True
PROMPT_MD_REQUIRED=True
RUNNER_SHORT_REQUIRED=True
NO_GIANT_CONSOLE_PROMPT=True
TARGETED_STAGING_ONLY=True
```

Required review phases:

```text
RUNNER_PREFLIGHT
EVIDENCE_COLLECTION
VALIDATION
SUMMARY
```

## Source Hygiene Requirements

```text
NO_GIT_ADD_DOT=True
NO_RESET=True
DIRTY_START_STOP_NO_WRITE=True
FAILED_TESTS_NO_COMMIT_NO_TAG_NO_PUSH=True
```

Dirty start evidence stops source writes. Failed tests stop commit, tag, and push
actions.

## Preview Evidence Gates

```text
HTTP_FRONTEND_NON_EMPTY_REQUIRED=True
TCP_ONLY_NOT_PREVIEW_READY=True
PREVIEW_ONLY_AFTER_HTTP_PASS=True
HTTP_FAIL_STOP_AND_DIAG=True
```

TCP-only evidence is never preview-ready. HTTP frontend evidence must pass and
must be non-empty before any private preview can be reviewed.

## Safety Locks

```text
NO_PUBLIC_DEPLOY=True
NO_REFLEX_DEPLOY=True
NO_RUNTIME=True
NO_DOCKER=True
NO_REFLEX_RUN=True
NO_PROVIDER_CALL=True
NO_BROKER_ORDER_SIZING=True
NO_SHEET_BQ_WRITE=True
NO_HTML_OUTPUT=True
```

## Audit Decision

- R21S is not a runtime authorization.
- R21S is not a private preview attempt.
- R21S does not create a `.ps1` runtime runner.
- R21S does not capture live CLI help or version output.
- R21T is blocked until explicit human approval.
- R21T must capture version and help evidence before any private preview attempt.
- Public release and deployment through Reflex stay closed.
- Provider, broker/order/sizing, Sheet/BQ write, HTML output, and export output
  paths stay closed.

## Files

- `mvp_qaic_py/reflex_preview_runner_spec_r21s.py`
- `tests/test_r21s_reflex_preview_runner_spec.py`
- `docs/PRODUCT/R21S_REFLEX_PREVIEW_RUNNER_SPEC_REVIEW_ONLY.md`

## Next

`NEXT=R21T_HUMAN_APPROVED_PRIVATE_PREVIEW_ATTEMPT_ONLY`
