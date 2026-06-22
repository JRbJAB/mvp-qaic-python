# QAIC P3.82A - MVP Public Method Handoff

Status: READY_FOR_MVP_QAIC_PUBLIC_METHOD_HANDOFF
Generated at: 2026-06-22 13:25:19 +02:00
Repo: QAIC_PY
Branch: master
Source head: 5bb1ee847acf4027c854b1ae08f965b0c5f86251
Source tag: qaic-python-p3-81b-public-private-boundary-audit-20260622

## Purpose

This handoff defines what can be shared with MVP_QAIC from QAIC_PY.

MVP_QAIC remains the public product layer:
- lexicon
- knowledge base
- WebApp/public UX
- prompt methods
- public-safe signal explanation

QAIC remains the private technical backend:
- quantitative engine
- private portfolio logic
- Revolut X / broker integration
- execution-capable adapters locked behind human review
- secrets and private balances
- order payloads and real execution controls

## Public-safe scope for MVP

Allowed for MVP_QAIC:

```text
LEXICON_PUBLIC_METHOD
PROMPT_PUBLIC_METHOD
PUBLIC_SIGNAL_TAXONOMY
PUBLIC_SAFE_SCHEMA
PUBLIC_CONTRACT_REGISTRY
PUBLIC_METHOD_OVERVIEW
```

The public layer may explain methods, terminology, review workflow, and signal semantics.
It must not expose private execution data or broker mechanics.

## Hard exclusions

```text
REVOLUT_X_IN_MVP_PUBLIC=NO
QAIC_PRIVATE_BACKEND_ONLY=TRUE
NO_BROKER_SECRET_IN_PUBLIC=TRUE
NO_API_KEY_IN_PUBLIC=TRUE
NO_PRIVATE_KEY_IN_PUBLIC=TRUE
NO_ORDER_PAYLOAD_IN_PUBLIC=TRUE
NO_PORTFOLIO_BALANCE_IN_PUBLIC=TRUE
NO_REAL_ORDER_ALLOWED_IN_PUBLIC=TRUE
NO_AUTO_SIZING_ALLOWED_IN_PUBLIC=TRUE
NO_BROKER_ORDER_SIZING=TRUE
HUMAN_REVIEW_ONLY=TRUE
```

## Evidence files

```text
docs/public_method_contracts/registry/public_private_forbidden_content_review.csv
docs/public_method_contracts/registry/public_private_boundary_audit.csv
docs/public_method_contracts/registry/public_contract_manifest.csv
```

## MVP integration rule

MVP_QAIC can consume these contracts as documentation and schema guidance only.

It must not import QAIC private backend logic as public runtime.
It must not expose Revolut X execution.
It must not infer order sizing, real order intent, or private portfolio balances.

## Next

P3.82B_MVP_HANDOFF_REVIEW_OR_EXPORT.
