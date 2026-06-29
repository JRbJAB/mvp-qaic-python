# Tracker Render Reference Registry

R1C2 tracks the render reference types used by CDC and Dev Tracker surfaces. These entries are source contracts for static preview generation and Reflex component mapping.

| Render reference type | Concerned cockpit/page/surface | Preview command/path policy |
|---|---|---|
| `migration_tracker_reference` | Migration Tracker visual reference surface; shared tracker progress, badge, route, and evidence semantics | Use `python tools/render_tracker_preview.py --out <run_report_preview_dir>` and keep output under `C:\JRb_TRADING_OS\_RUN_REPORTS\MVP_QAIC_PY`. |
| `cdc_dev_tracker` | `/cdc-dev-tracker` combined CDC + Dev Tracker cockpit | Use the common renderer preview before deployment; no runtime/frontend proof is claimed by this static artifact. |
| `dev_tracker` | `/dev-tracking` Dev Tracker surface and development lifecycle grouping | Use the common renderer preview and verify blue progress bars, percentages, statuses, priorities, and evidence text. |
| `tool_registry_cdc` | Tool Registry CDC cockpit/surface and registry contract coverage | Use the common renderer preview when registry CDC rows are surfaced; path policy remains run-report-only. |
| `cdc_tracker` | `/cdc-tracker` CDC-only readiness surface | Use the common renderer preview to verify route readiness, source coverage, progress, and CDC phase state. |
| `migration_tracker_oracle` | Legacy R1B alias for the migration tracker visual oracle | Kept for import and test compatibility; new work should bind to `migration_tracker_reference`. |
| `tool_registry_tracker` | Legacy R1B alias for tool registry tracker coverage | Kept for import and test compatibility; new work should bind to `tool_registry_cdc`. |

Static preview command:

```powershell
python tools/render_tracker_preview.py --out C:\JRb_TRADING_OS\_RUN_REPORTS\MVP_QAIC_PY\<run>\preview
```

Visual gate:

Visual tests are mandatory before Reflex deployment. R1C2 does not run Bun, npm, Reflex runtime, a browser, or deploy.
