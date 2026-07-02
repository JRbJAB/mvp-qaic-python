# R21R Reflex Publication Preview Strategy Audit - Docs Only

Status: `R21R_REFLEX_PUBLICATION_PREVIEW_STRATEGY_AUDIT=READY`

R21R binds the R21Q product continuation final seal to a publication preview
strategy audit. This artifact is documentation and deterministic metadata only.
It does not create a runtime runner, start Reflex execution, use Docker, call
providers, touch broker/order/sizing paths, write Sheets or BigQuery, emit HTML,
or create export artifacts.

## Source Binding

```text
R21R_REFLEX_PUBLICATION_PREVIEW_STRATEGY_AUDIT=READY
SOURCE_R21Q_PRODUCT_CONTINUATION_BOUND=True
REFLEX_RUNTIME_STATUS=PAUSED
REFLEX_RUNTIME_RUNNER_CHAIN=STOPPED
FALLBACK_STATIC_WYSIWYG_ALLOWED=True
REFLEX_ALLOWED_NEXT_ONLY_AFTER_HUMAN_RUNNER_REVIEW=True
```

## Preview Strategy Boundary

```text
NO_DOCS_NO_ACTION=True
NO_HELP_NO_RUNTIME=True
HELP_FLAG_MISSING_COMMAND_FORBIDDEN=True
TCP_ONLY_NOT_PREVIEW_READY=True
HTTP_FAIL_STOP_AND_DIAG=True
PREVIEW_ONLY_AFTER_HTTP_PASS=True
HTTP_FRONTEND_NON_EMPTY_REQUIRED=True
REFLEX_CLI_HELP_CAPTURE_REQUIRED=True
REFLEX_VERSION_CAPTURE_REQUIRED=True
NO_FRONTEND_HOST_FLAG=True
```

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

- R21R is not a runtime authorization.
- R21R is not a preview attempt.
- R21R does not capture live CLI help or version output.
- R21S must require CLI help capture and version capture before any private
  preview attempt can be reviewed.
- TCP-only evidence is insufficient for preview readiness.
- HTTP frontend evidence must pass and be non-empty before any preview review.
- Static or WYSIWYG fallback remains allowed for visual review without runtime.

## Files

- `mvp_qaic_py/reflex_publication_preview_strategy_r21r.py`
- `tests/test_r21r_reflex_publication_preview_strategy.py`
- `docs/PRODUCT/R21R_REFLEX_PUBLICATION_PREVIEW_STRATEGY_AUDIT_DOCS_ONLY.md`

## Next

`R21S_REFLEX_PREVIEW_RUNNER_SPEC_REVIEW_ONLY`
