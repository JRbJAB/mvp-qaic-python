# R21N Local Cockpit Preview - No Runtime

```text
R21N_LOCAL_COCKPIT_PREVIEW_NO_RUNTIME=READY
SOURCE_R21K_CONTRACT_BOUND=True
SOURCE_R21L_MODEL_BINDING_BOUND=True
SOURCE_R21M_VISUAL_PLANNING_BOUND=True
LOCAL_PREVIEW_RENDERER=True
NO_COMMITTED_HTML_OUTPUT=True
PREVIEW_OUTPUT_RUN_REPORT_ONLY=True
NO_RUNTIME=True
NO_DOCKER=True
NO_REFLEX_RUN=True
NO_PROVIDER_CALL=True
NO_BROKER_ORDER_SIZING=True
NO_SHEET_BQ_WRITE=True
NO_05_EXPORTS=True
NEXT=R21O_QAIC_REVIEW_PACKET_FINAL_NO_RUNTIME
```

R21N renders a local static cockpit preview from the R21K cockpit queue data
contract, the R21L cockpit queue model binding, and the R21M cockpit queue
visual planning model.

The renderer is a preview-only artifact generator. It does not start a UI
process, does not call providers, does not touch broker/order/sizing paths, does
not write Sheets or BigQuery, and does not create committed HTML output.

Preview writes are restricted to `_RUN_REPORTS` output paths. Repository paths,
`docs`, `public`, and `05_EXPORTS` targets are rejected.

Required cockpit traces:

```text
BRAND_CONFIG_TRACE_COCKPIT_READY=True
UI_TRACKER_TRACE_COCKPIT_READY=True
TOOL_REGISTRY_CDC_TRACE_COCKPIT_READY=True
CDC_CONTRACT_TRACE_COCKPIT_READY=True
QAIC_BRIDGE_TRACE_COCKPIT_READY=True
```

Brand/config preview coverage:

```text
QAIT_CHARTE_TEMPLATE=BOUND
MVP_QAIC_LOGO_VALIDATED=BOUND
preserve_q_candlesticks_signal_line=True
NO_GENERATED_PREVIEW_REPLACES_VALIDATED_LOGO=True
```
