"""No-runtime operator workflow preview for MVP QAIC R21C.

This module is intentionally pure stdlib and offline-only. It renders a static
operator workboard that keeps the MVP-to-QAIC bridge usable while Reflex runtime
is paused.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
import html
import json
from pathlib import Path
from typing import Any


POLICY_FLAGS: dict[str, bool | str] = {
    "reflex_runtime_paused": True,
    "no_runtime": True,
    "no_docker": True,
    "no_provider_call": True,
    "no_broker_order_sizing": True,
    "no_sheet_bq_write": True,
    "human_review_required": True,
    "qaic_execution_allowed": False,
    "handoff_mode": "review_only_local_handoff",
}


@dataclass(frozen=True)
class WorkflowStep:
    order: int
    title: str
    owner: str
    status: str
    output: str


@dataclass(frozen=True)
class OperatorWorkflowModel:
    title: str
    version: str
    route_reference: str
    bridge_contract: str
    status: str
    policy_flags: dict[str, bool | str]
    steps: tuple[WorkflowStep, ...]


def build_workflow_model() -> OperatorWorkflowModel:
    """Build the R21C no-runtime operator workflow model."""
    return OperatorWorkflowModel(
        title="MVP QAIC Operator Workflow - No Runtime Preview",
        version="R21C",
        route_reference="/qaic-bridge",
        bridge_contract="MVP_QAIC_TO_QAIC_BRIDGE_R1",
        status="READY_FOR_PRODUCT_WORK_WITHOUT_REFLEX_RUNTIME_BLOCKING",
        policy_flags=dict(POLICY_FLAGS),
        steps=(
            WorkflowStep(1, "Prepare operator input", "Operator", "ready", "portfolio text, notes, or image transcription"),
            WorkflowStep(2, "Generate GEM prompt", "MVP QAIC", "ready", "copy-paste prompt payload"),
            WorkflowStep(3, "Capture GEM response", "Operator", "ready", "raw response and structured review queue"),
            WorkflowStep(4, "Human review decision", "Operator", "required", "approved, blocked, or correction-needed decision"),
            WorkflowStep(5, "Create QAIC handoff", "MVP QAIC", "review-only", "local JSON handoff for QAIC review"),
            WorkflowStep(6, "QAIC review", "QAIC", "execution-disabled", "technical review without broker/order/sizing"),
        ),
    )


def model_to_dict(model: OperatorWorkflowModel) -> dict[str, Any]:
    """Serialize the model to a JSON-friendly dict."""
    return {
        "title": model.title,
        "version": model.version,
        "route_reference": model.route_reference,
        "bridge_contract": model.bridge_contract,
        "status": model.status,
        "policy_flags": model.policy_flags,
        "steps": [asdict(step) for step in model.steps],
    }


def render_static_preview(model: OperatorWorkflowModel | None = None) -> str:
    """Render a static HTML workboard for visual/operator review."""
    if model is None:
        model = build_workflow_model()

    flags = "\n".join(
        f"<li><strong>{html.escape(str(key))}</strong>: {html.escape(str(value))}</li>"
        for key, value in sorted(model.policy_flags.items())
    )
    rows = "\n".join(
        "<tr>"
        f"<td>{step.order}</td>"
        f"<td>{html.escape(step.title)}</td>"
        f"<td>{html.escape(step.owner)}</td>"
        f"<td>{html.escape(step.status)}</td>"
        f"<td>{html.escape(step.output)}</td>"
        "</tr>"
        for step in model.steps
    )

    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>{html.escape(model.title)}</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 0; background: #0f172a; color: #e5e7eb; }}
    header {{ padding: 28px 36px; background: #111827; border-bottom: 1px solid #334155; }}
    main {{ padding: 28px 36px; max-width: 1180px; margin: auto; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; }}
    .card {{ background: #111827; border: 1px solid #334155; border-radius: 14px; padding: 18px; }}
    .pill {{ display: inline-block; padding: 6px 10px; border-radius: 999px; background: #1e293b; border: 1px solid #475569; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 12px; }}
    th, td {{ border-bottom: 1px solid #334155; padding: 10px; text-align: left; vertical-align: top; }}
    th {{ color: #93c5fd; }}
    code {{ background: #020617; padding: 2px 6px; border-radius: 6px; }}
    .warn {{ color: #facc15; }}
    .ok {{ color: #86efac; }}
  </style>
</head>
<body>
  <header>
    <h1>{html.escape(model.title)}</h1>
    <p><span class=\"pill\">{html.escape(model.version)}</span> <span class=\"pill\">Route reference: {html.escape(model.route_reference)}</span></p>
  </header>
  <main>
    <section class=\"grid\">
      <div class=\"card\">
        <h2>Status</h2>
        <p class=\"ok\">{html.escape(model.status)}</p>
        <p>Bridge contract: <code>{html.escape(model.bridge_contract)}</code></p>
      </div>
      <div class=\"card\">
        <h2>Reflex runtime</h2>
        <p class=\"warn\">Paused. This preview is static and no-runtime.</p>
        <p>No Docker, no Reflex run, no provider call, no broker/order/sizing.</p>
      </div>
      <div class=\"card\">
        <h2>Next product focus</h2>
        <p>Continue cockpit, operator workflow, prompt/GEM portfolio, and QAIC review-only handoff without blocking on Reflex runtime.</p>
      </div>
    </section>

    <section class=\"card\" style=\"margin-top: 16px;\">
      <h2>Workflow steps</h2>
      <table>
        <thead><tr><th>#</th><th>Step</th><th>Owner</th><th>Status</th><th>Output</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </section>

    <section class=\"card\" style=\"margin-top: 16px;\">
      <h2>Safety flags</h2>
      <ul>{flags}</ul>
    </section>
  </main>
</body>
</html>
"""


def write_preview(output_dir: Path) -> tuple[Path, Path]:
    """Write HTML and manifest preview artifacts."""
    model = build_workflow_model()
    output_dir.mkdir(parents=True, exist_ok=True)
    html_path = output_dir / "index.html"
    manifest_path = output_dir / "preview_manifest.json"
    html_path.write_text(render_static_preview(model), encoding="utf-8")
    manifest_path.write_text(
        json.dumps(model_to_dict(model), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return html_path, manifest_path


if __name__ == "__main__":
    write_preview(Path("05_EXPORTS") / "R21C_OPERATOR_WORKFLOW_STATIC_PREVIEW")
