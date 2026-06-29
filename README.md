# MVP QAIC PY — Benchmark Layer

Python = moteur / source de vérité / scoring / audit.

Google Sheets = cockpit décisionnel, un seul onglet :
`🎛️ BENCHMARK_AI_TRADE`.

Safety:
- HUMAN_REVIEW_ONLY
- NO_BROKER
- NO_ORDER
- NO_SIZING
- NO_AUTO_SIGNAL_COPY
<!-- MVP_QAIC_RUNNER_STANDARD_START -->

## Runner quality standard

Active standard: `docs/dev_tracking/runner_quality/RUNNER_REFERENCE_STANDARD_R1.md`.

Future runner packs must follow `AGENTS.md` and the R1 runner contract:

- no interactive Python;
- no Git without subcommand;
- no silent empty args;
- no `New-Item -LiteralPath` for folder creation;
- no untested generic Git/Python wrappers;
- informational metrics do not block;
- runner preflight required;
- stop and audit after repeated shell-glue defects.

<!-- MVP_QAIC_RUNNER_STANDARD_END -->
