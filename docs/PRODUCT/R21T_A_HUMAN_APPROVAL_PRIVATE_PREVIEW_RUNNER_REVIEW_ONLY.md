# R21T-A Human Approval Private Preview Runner - Review Only

Status: `R21T_A_HUMAN_APPROVAL_PRIVATE_PREVIEW_RUNNER_REVIEW=READY`

R21T-A is an approval gate and review-only runner boundary. It does not create a
PowerShell runtime runner, launch Reflex execution, use Docker, call providers,
touch broker/order/sizing paths, write Sheets or BigQuery, emit HTML, or create
export artifacts.

## Source Binding

```text
R21T_A_HUMAN_APPROVAL_PRIVATE_PREVIEW_RUNNER_REVIEW=READY
SOURCE_R21S_PREVIEW_RUNNER_SPEC_BOUND=True
```

## Human Approval Gate

```text
HUMAN_APPROVED_PRIVATE_PREVIEW=False
HUMAN_APPROVED_PRIVATE_PREVIEW_REQUIRED=True
EXPLICIT_OPERATOR_MARKER_REQUIRED=True
REQUIRED_OPERATOR_MARKER=HUMAN_APPROVED_PRIVATE_PREVIEW_TRUE
```

The required operator marker remains absent in R21T-A. No private preview
authorization is granted by this document or by the review-only Python payload.

## Review-Only Boundary

```text
RUNNER_REVIEW_ONLY=True
RUNNER_EXECUTED=False
RUNTIME_EXECUTION_ALLOWED=False
REFLEX_RUNTIME_STATUS=PAUSED
REFLEX_RUNTIME_RUNNER_CHAIN=STOPPED_UNTIL_EXPLICIT_OPERATOR_MARKER
```

## Help And Preview Evidence Gate

```text
REFLEX_CLI_HELP_CAPTURE_REQUIRED=True
REFLEX_VERSION_CAPTURE_REQUIRED=True
HELP_VERSION_CAPTURE_BEFORE_PREVIEW=True
NO_FRONTEND_HOST_FLAG=True
HTTP_FRONTEND_NON_EMPTY_REQUIRED=True
TCP_ONLY_NOT_PREVIEW_READY=True
PREVIEW_ONLY_AFTER_HTTP_PASS=True
HTTP_FAIL_STOP_AND_DIAG=True
```

R21T-A does not capture live help or version output. Capture remains required
before any later private preview evidence review.

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

Dirty start evidence stops source writes. Failed tests stop commit, tag, and
push actions.

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

- R21T-A is not a runtime authorization.
- R21T-A is not a private preview attempt.
- R21T-A does not create a `.ps1` runtime runner.
- R21T-A does not capture live CLI help or version output.
- The explicit operator marker remains required and absent.
- `HUMAN_APPROVED_PRIVATE_PREVIEW` remains `False`.
- R21T-B may proceed only after the required operator marker is provided.
- Public release paths stay closed.
- Provider, broker/order/sizing, Sheet/BQ write, HTML output, and export output
  paths stay closed.

## Files

- `mvp_qaic_py/reflex_private_preview_approval_review_r21t_a.py`
- `tests/test_r21t_a_private_preview_approval_review.py`
- `docs/PRODUCT/R21T_A_HUMAN_APPROVAL_PRIVATE_PREVIEW_RUNNER_REVIEW_ONLY.md`

## Next

`NEXT=R21T_B_OPERATOR_APPROVED_HELP_VERSION_CAPTURE_REVIEW_ONLY`
