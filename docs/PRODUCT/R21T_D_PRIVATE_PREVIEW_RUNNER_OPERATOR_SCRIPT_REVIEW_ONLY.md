# R21T-D Private Preview Runner Operator Script - Review Only

Status: `R21T_D_PRIVATE_PREVIEW_RUNNER_OPERATOR_SCRIPT_REVIEW=READY`

R21T-D describes the future private preview operator script sections as
metadata only. It does not create a script file, launch runtime work, use
Docker, use ports, open a browser, call providers, touch broker/order/sizing
paths, write Sheets or BigQuery, emit HTML, create export artifacts, or claim
preview readiness.

## Source Binding

```text
R21T_D_PRIVATE_PREVIEW_RUNNER_OPERATOR_SCRIPT_REVIEW=READY
SOURCE_R21T_C_BUILD_REVIEW_BOUND=True
```

R21T-D is bound to:

- `docs/PRODUCT/R21T_C_PRIVATE_PREVIEW_RUNNER_BUILD_REVIEW_ONLY.md`
- `docs/PRODUCT/R21T_B_OPERATOR_APPROVED_HELP_VERSION_CAPTURE_REVIEW_ONLY.md`
- `docs/RUNTIME/REFLEX_CLI_CONTRACT_H8I.md`
- `docs/RUNTIME/REFLEX_READINESS_ANTI_LOOP_POLICY_R16F2H6.md`
- `docs/RUNTIME/REFLEX_RUNNER_HARDENING_POLICY_R16F2H7I.md`
- `docs/FINAL/R21B_REFLEX_RUNTIME_CLOSURE_STRATEGY_AND_INSTRUCTIONS_MEMO_20260701.md`

## Inherited Evidence

```text
REFLEX_VERSION=0.9.6.post1
HELP_VERSION_CAPTURE_PASSED=True
HELP_FORBIDDEN_FRONTEND_HOST_FOUND=False
NO_FRONTEND_HOST_FLAG=True
```

The help/version capture passed in R21T-B. R21T-D reuses that evidence as
review input only and does not repeat the capture.

## Review-Only Boundary

```text
OPERATOR_SCRIPT_REVIEW_ONLY=True
SCRIPT_FILE_CREATED=False
PS1_CREATED=False
SCRIPT_EXECUTED=False
RUNNER_EXECUTED=False
RUNTIME_EXECUTION_ALLOWED=False
NO_RUNTIME_EXECUTION=True
NO_DOCKER_CALL=True
NO_REFLEX_APP_START=True
NO_PREVIEW_ATTEMPT=True
NO_PORTS=True
NO_BROWSER=True
REFLEX_RUNTIME_STATUS=PAUSED
REFLEX_RUNTIME_RUNNER_CHAIN=STOPPED_AFTER_OPERATOR_SCRIPT_REVIEW
```

## Future Operator Script Sections

The later operator script may be dry-built in R21T-E only after this metadata
gate. R21T-D records the expected sections without command lines:

- `STRICT_PREFLIGHT`
- `HARD_TIMEOUT_NATIVE_CALLS`
- `PINNED_IMAGE_CHECK`
- `PRIVATE_PORT_CHECKS`
- `FULL_HEAD_COPY_BY_ARCHIVE_TAR`
- `POLICY_GUARD_CHECKS`
- `HELP_VERSION_EVIDENCE_REUSE`
- `PREVIEW_READINESS_PROBES`
- `FAILURE_STOP_DIAGNOSTICS`
- `SUMMARY`

The future source copy strategy must use a full tracked-source snapshot outside
the source repository through an archive/tar approach. This document does not
provide executable command text.

## Operator Script Requirements

```text
PS51_COMPATIBLE=True
PROMPT_MD_REQUIRED=True
RUNNER_SHORT_REQUIRED=True
NO_GIANT_CONSOLE_PROMPT=True
HARD_TIMEOUT_REQUIRED=True
IMAGE_PREFLIGHT_REQUIRED=True
PORT_PREFLIGHT_REQUIRED=True
GIT_ARCHIVE_HEAD_COPY_REQUIRED=True
POLICY_GUARDS_REQUIRED=True
TRANSIENT_REPORTS_UNDER_RUN_REPORTS=True
```

## Private Preview Readiness Boundary

```text
PRIVATE_MAPPING_REQUIRED=True
HTTP_FRONTEND_NON_EMPTY_REQUIRED=True
TCP_ONLY_NOT_PREVIEW_READY=True
PREVIEW_ONLY_AFTER_HTTP_PASS=True
```

R21T-D does not claim preview readiness. A later reviewed dry build must still
require non-empty HTTP frontend evidence before any preview can be considered
ready. TCP evidence alone is not preview readiness.

## Safety Locks

```text
TARGETED_STAGING_ONLY=True
NO_GIT_ADD_DOT=True
NO_RESET=True
NO_PUBLIC_DEPLOY=True
NO_REFLEX_DEPLOY=True
NO_PROVIDER_CALL=True
NO_BROKER_ORDER_SIZING=True
NO_SHEET_BQ_WRITE=True
NO_HTML_OUTPUT=True
```

## Audit Decision

- R21T-D is metadata only.
- R21T-D is bound to R21T-C runner build review metadata.
- R21T-D reuses R21T-B help/version capture evidence.
- R21T-D does not create a script file.
- R21T-D does not execute a script or runner.
- R21T-D does not start runtime work.
- R21T-D does not attempt private preview.
- R21T-D does not use ports, a browser, Docker, providers, broker/order/sizing,
  Sheets, BigQuery, HTML output, export output, public release, or Reflex
  release paths.
- R21T-D does not claim preview readiness.
- Public release paths stay closed.

## Files

- `mvp_qaic_py/reflex_private_preview_operator_script_review_r21t_d.py`
- `tests/test_r21t_d_private_preview_operator_script_review.py`
- `docs/PRODUCT/R21T_D_PRIVATE_PREVIEW_RUNNER_OPERATOR_SCRIPT_REVIEW_ONLY.md`

## Next

`NEXT=R21T_E_PRIVATE_PREVIEW_OPERATOR_SCRIPT_DRY_BUILD_NO_RUN`
