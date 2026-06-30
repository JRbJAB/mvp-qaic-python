# 🛠️ MVP QAIC — Reflex Runtime & Process Live Reference

Live version: v0.2.7
Policy ID: R16F2H4_REFLEX_RUNTIME_POLICY_LOCK
Readiness Policy ID: R16F2H6_REFLEX_READINESS_ANTI_LOOP_POLICY
Updated: 2026-06-30 23:41:31 UTC

## 🔒 Runtime lock

Reflex preview is locked to Docker pinned + full tracked HEAD copy outside repo + Reflex dev mode.

```text
Container frontend: 3000
Container backend: 8000
Windows preview frontend: 3055
Windows preview backend: 8055
```

## 🧯 Anti-loop readiness lock

Future runners must not loop indefinitely on repeated log tails.

```text
MAX_WAIT_SECONDS=420
MAX_IDENTICAL_LOG_TAIL_REPEATS=2
APP_RUNNING_MARKER_REQUIRED=True
INTERNAL_PORT_DIAGNOSTIC_REQUIRED=True
STOP_CONTAINER_ON_FAILURE=True
```

## 🧭 Documentation fusion lock

For every validated technical process:

1. generate a reference `.md` document;
2. update the relevant `docs/FINAL` live deliverable;
3. use emoji headings in final-facing markdown when useful;
4. keep transient reports under `_RUN_REPORTS`;
5. commit only after guards/tests/staged review.

## ✅ Current validated evidence

- H4 runtime policy was sealed and pushed.
- H5B baseline preview passed with HTTP root ready and route gate OK.
- H6 readiness policy passed guard and tests.

## 🚫 Explicitly forbidden

- NiceGUI fallback for this Reflex chain.
- `.web` source patch as a validation strategy.
- `--env prod`, `--single-port`, `reflex export`, or minimal allowlist as primary preview.
- unbounded log polling.
- reports written into final docs folders without explicit promotion.
