# P107-R1 — Canonical WebApp Binding + Admin Monitor

## Status
CREATED_LOCAL_PENDING_GATE

## Decision
- The validated WebApp Index.html remains canonical.
- Python must not generate or overwrite Index.html.
- Python may generate local admin/suivi HTML as admin/ADMIN_MONITOR.html.

## Generated files
- data packs for the canonical WebApp
- binding contract
- admin status
- admin/ADMIN_MONITOR.html

## Safety
- NO_REVOLUTX_REAL_ACCESS
- NO_BROKER
- NO_ORDER
- NO_CANCEL
- NO_REPLACE_ORDER
- NO_AUTO_SIZING
- NO_SECRET_LOG
- NO_SHEET_WRITE
- NO_APPS_SCRIPT_EXECUTION
- NO_CLASP
- NO_PUBLIC_DEPLOY

## Next
P108_UI_POLISH_USING_CANONICAL_INDEX_OR_PUBLIC_DEPLOY_DECISION_GATE
