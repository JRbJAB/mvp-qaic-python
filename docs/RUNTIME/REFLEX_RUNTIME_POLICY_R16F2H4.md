# R16F2H4 - Reflex Runtime Policy Lock

Policy ID: R16F2H4_REFLEX_RUNTIME_POLICY_LOCK

## Locked decision

Authorized MVP QAIC Reflex UI preview:

python -m reflex run --env dev --backend-host 0.0.0.0 --backend-port 8000 --frontend-port 3000

Docker preview mapping:
host 3055 -> container 3000
host 8055 -> container 8000

Docker reference mapping:
host 3035 -> container 3000
host 8035 -> container 8000

## Forbidden for primary UI preview

Forbidden: --env prod, --single-port, reflex export as primary preview, minimal allowlist runtime copy, silent dynamic port fallback, patching the real repo before preview, commit/tag/push before DOM + PNG + human validation, NiceGUI, .web source patch.

## Required gate

Every future Reflex runner must execute:
python tools\reflex_runtime_policy_guard.py --repo C:\JRb_TRADING_OS\MVP_QAIC_PY

and display:
REFLEX_POLICY_GUARD_OK=True
POLICY_ID=R16F2H4_REFLEX_RUNTIME_POLICY_LOCK
REFLEX_POLICY_GUARD_REQUIRED=True

## Official Reflex docs binding

The assistant must check official Reflex CLI/config docs before proposing any new Reflex command or config change.

Locked preview strategy:
Docker pinned + full tracked HEAD copy outside repo + Reflex dev mode + container frontend/backend 3000/8000 + host preview ports 3055/8055 + no real repo patch before visual validation.
