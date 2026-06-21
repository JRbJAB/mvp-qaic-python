# MVP QAIC — P98D Runtime Cockpit Extended Module Local

Status: `OK_P98D_RUNTIME_COCKPIT_EXTENDED_MODULE_LOCAL_READY`

Scope:
- build the extended local cockpit module from P98C scope audit
- include journal workflow, benchmark, prompt quality, lexique, methods, signals, risk, portfolio, and Revolut read-only
- no live write in P98D
- no Decision Journal write in P98D
- no Apps Script execution
- no CLASP push
- no broker/order/sizing

Extended cockpit sections:
1. Runtime & journal pipeline
2. Quality, prompts & benchmark
3. Knowledge, methods, signals & risk
4. Portfolio & broker read-only

Extended cockpit cards:
- benchmark_status
- latest_payload_status
- run_queue_status
- response_intake_status
- journal_queue_status
- decision_journal_status
- prompt_quality_status
- prompt_improvement_backlog
- prompt_library_readiness
- lexique_readiness
- method_library_status
- signal_library_coverage
- risk_guard_status
- trade_plan_methods_status
- revolut_readonly_status
- portfolio_snapshot_status
- runtime_bridge_status

Next:
- `P98E_COCKPIT_UI_EXPORT_OR_P99_MVP_FREEZE_RELEASE_HANDOFF`
