"""R21H no-runtime binding between operator workflow and reference registries.

The module is deliberately offline and side-effect free. It does not render a
preview, start Reflex, call providers, write Sheets/BQ, or use broker/order
interfaces. It exposes a deterministic binding model from the existing CDC,
UI tracker, and tool registry sources located by R21G.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


POLICY_FLAGS: dict[str, bool | str] = {
    "drive_first_reference_lock_applied": True,
    "source_references_from_r21g_audit": True,
    "no_runtime": True,
    "no_reflex_run": True,
    "no_docker": True,
    "no_provider_call": True,
    "no_broker_order_sizing": True,
    "no_sheet_bq_write": True,
    "no_apps_script_exec": True,
    "no_html_preview_output": True,
    "human_review_required": True,
    "qaic_execution_allowed": False,
    "binding_mode": "review_only_reference_binding",
}


@dataclass(frozen=True)
class ReferenceBinding:
    """A single source-to-operator-workflow binding."""

    key: str
    route: str
    surface: str
    source_path_hint: str
    source_suffix: str
    required_terms: tuple[str, ...]
    operator_use: str


@dataclass(frozen=True)
class SourceValidation:
    """Validation result for one binding source."""

    key: str
    exists: bool
    resolved_path: str
    required_terms_ok: bool
    missing_terms: tuple[str, ...]


@dataclass(frozen=True)
class OperatorReferenceBindingModel:
    """R21H binding model for local operator review."""

    workflow: str
    version: str
    status: str
    policy_flags: dict[str, bool | str]
    bindings: tuple[ReferenceBinding, ...]
    source_validations: tuple[SourceValidation, ...]


REFERENCE_BINDINGS: tuple[ReferenceBinding, ...] = (
    ReferenceBinding(
        key="cdc_dev_tracker",
        route="/cdc-dev-tracker",
        surface="CDC + Dev Tracker cockpit",
        source_path_hint="docs/dev_tracking/TRACKER_RENDER_REFERENCE_REGISTRY.md",
        source_suffix="TRACKER_RENDER_REFERENCE_REGISTRY.md",
        required_terms=("cdc_dev_tracker", "/cdc-dev-tracker", "tool_registry_cdc"),
        operator_use="show combined CDC and development tracker status in operator workflow",
    ),
    ReferenceBinding(
        key="dev_tracker",
        route="/dev-tracking",
        surface="Development lifecycle tracker",
        source_path_hint="docs/dev_tracking/TRACKER_RENDER_REFERENCE_REGISTRY.md",
        source_suffix="TRACKER_RENDER_REFERENCE_REGISTRY.md",
        required_terms=("dev_tracker", "/dev-tracking"),
        operator_use="surface product/dev lifecycle stage, status, priority, and evidence",
    ),
    ReferenceBinding(
        key="tool_registry_cdc",
        route="/tool-registry-cdc",
        surface="Tool Registry CDC cockpit",
        source_path_hint="docs/dev_tracking/TRACKER_RENDER_REFERENCE_REGISTRY.md",
        source_suffix="TRACKER_RENDER_REFERENCE_REGISTRY.md",
        required_terms=("tool_registry_cdc", "/tool-registry-cdc"),
        operator_use="bind tool registry coverage to operator review without inventing registry semantics",
    ),
    ReferenceBinding(
        key="cdc_tracker",
        route="/cdc-tracker",
        surface="CDC readiness tracker",
        source_path_hint="docs/dev_tracking/TRACKER_RENDER_REFERENCE_REGISTRY.md",
        source_suffix="TRACKER_RENDER_REFERENCE_REGISTRY.md",
        required_terms=("cdc_tracker", "/cdc-tracker"),
        operator_use="expose CDC readiness and source coverage in operator workflow",
    ),
    ReferenceBinding(
        key="ui_tracker_tool_manifest",
        route="/dev-tracking",
        surface="UI tracker tool manifest",
        source_path_hint="docs/dev_tracking/ui_tracker_tool_manifest.json",
        source_suffix="ui_tracker_tool_manifest.json",
        required_terms=("tracker",),
        operator_use="link UI tracker tooling metadata to the workflow binding model",
    ),
    ReferenceBinding(
        key="tracker_visual_contract",
        route="/cdc-dev-tracker",
        surface="Tracker visual contract",
        source_path_hint="docs/dev_tracking/TRACKER_UI_VISUAL_CONTRACT.md",
        source_suffix="TRACKER_UI_VISUAL_CONTRACT.md",
        required_terms=("TRACKER",),
        operator_use="keep visual semantics tied to the approved tracker contract",
    ),
    ReferenceBinding(
        key="tool_registry_export",
        route="/tool-registry-cdc",
        surface="Tool registry export",
        source_path_hint="data/tool_registry/tool_registry_export.csv",
        source_suffix="tool_registry_export.csv",
        required_terms=("tool",),
        operator_use="use the current tool registry data export as source evidence",
    ),
    ReferenceBinding(
        key="tool_registry_snapshot",
        route="/tool-registry-cdc",
        surface="Tool registry snapshot",
        source_path_hint="data/tool_registry/tool_registry_snapshot.json",
        source_suffix="tool_registry_snapshot.json",
        required_terms=("tool",),
        operator_use="use the current tool registry snapshot as source evidence",
    ),
    ReferenceBinding(
        key="cdc_final_contract",
        route="/cdc-tracker",
        surface="Final CDC contract",
        source_path_hint="docs/FINAL/*MVP_QAIC_CDC_CONTRACT_FINAL_FUSED_v0.2.6.md",
        source_suffix="MVP_QAIC_CDC_CONTRACT_FINAL_FUSED_v0.2.6.md",
        required_terms=("CDC", "MVP_QAIC"),
        operator_use="anchor CDC semantics to the sealed final CDC contract",
    ),
    ReferenceBinding(
        key="r21d_qaic_bridge_status",
        route="/qaic-bridge",
        surface="QAIC bridge status model",
        source_path_hint="docs/PRODUCT/R21D_OPERATOR_WORKFLOW_QAIC_BRIDGE_STATUS_NO_RUNTIME.md",
        source_suffix="R21D_OPERATOR_WORKFLOW_QAIC_BRIDGE_STATUS_NO_RUNTIME.md",
        required_terms=("/qaic-bridge", "NO_RUNTIME"),
        operator_use="keep QAIC bridge status visible in the no-runtime workflow",
    ),
    ReferenceBinding(
        key="r21e_decision_journal_handoff",
        route="/qaic-bridge",
        surface="Decision journal handoff",
        source_path_hint="docs/PRODUCT/R21E_OPERATOR_DECISION_JOURNAL_HANDOFF_NO_RUNTIME.md",
        source_suffix="R21E_OPERATOR_DECISION_JOURNAL_HANDOFF_NO_RUNTIME.md",
        required_terms=("decision journal", "QAIC"),
        operator_use="connect operator decision journal handoff to QAIC review-only consumption",
    ),
)


def _repo_root_or_cwd(repo_root: str | Path | None) -> Path:
    return Path.cwd() if repo_root is None else Path(repo_root)


def _read_text_lossy(path: Path) -> str:
    for encoding in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_bytes().decode("utf-8", errors="ignore")


def resolve_binding_source(binding: ReferenceBinding, repo_root: str | Path | None = None) -> Path | None:
    """Resolve a binding source by direct path first, then by suffix search."""
    root = _repo_root_or_cwd(repo_root)
    direct = root / binding.source_path_hint
    if direct.exists():
        return direct

    matches = [path for path in root.rglob("*") if path.is_file() and path.name.endswith(binding.source_suffix)]
    if len(matches) == 1:
        return matches[0]

    # Prefer non-archive matches when multiple suffix matches exist.
    active_matches = [path for path in matches if "ARCHIVE" not in {part.upper() for part in path.parts}]
    if len(active_matches) == 1:
        return active_matches[0]

    return None


def validate_reference_sources(repo_root: str | Path | None = None) -> tuple[SourceValidation, ...]:
    """Validate that R21G-located reference sources still exist and contain anchor terms."""
    validations: list[SourceValidation] = []
    for binding in REFERENCE_BINDINGS:
        resolved = resolve_binding_source(binding, repo_root)
        if resolved is None:
            validations.append(
                SourceValidation(
                    key=binding.key,
                    exists=False,
                    resolved_path="",
                    required_terms_ok=False,
                    missing_terms=binding.required_terms,
                )
            )
            continue

        text = _read_text_lossy(resolved)
        text_lower = text.lower()
        missing = tuple(term for term in binding.required_terms if term.lower() not in text_lower)
        validations.append(
            SourceValidation(
                key=binding.key,
                exists=True,
                resolved_path=str(resolved),
                required_terms_ok=not missing,
                missing_terms=missing,
            )
        )
    return tuple(validations)


def build_operator_reference_binding_model(repo_root: str | Path | None = None) -> OperatorReferenceBindingModel:
    """Build the R21H no-runtime reference binding model."""
    validations = validate_reference_sources(repo_root)
    all_valid = all(item.exists and item.required_terms_ok for item in validations)
    return OperatorReferenceBindingModel(
        workflow="R21H_BIND_UI_TRACKER_TOOL_REGISTRY_CDC_TO_OPERATOR_WORKFLOW_NO_RUNTIME",
        version="R21H",
        status="READY_FOR_OPERATOR_REVIEW_BINDING" if all_valid else "REFERENCE_BINDING_REVIEW_REQUIRED",
        policy_flags=dict(POLICY_FLAGS),
        bindings=REFERENCE_BINDINGS,
        source_validations=validations,
    )


def model_to_dict(model: OperatorReferenceBindingModel) -> dict[str, Any]:
    """Serialize the binding model for tests or local handoff."""
    return {
        "workflow": model.workflow,
        "version": model.version,
        "status": model.status,
        "policy_flags": model.policy_flags,
        "bindings": [asdict(binding) for binding in model.bindings],
        "source_validations": [asdict(validation) for validation in model.source_validations],
    }


def render_binding_markdown(model: OperatorReferenceBindingModel | None = None) -> str:
    """Render a markdown-only operator summary. No HTML is produced."""
    if model is None:
        model = build_operator_reference_binding_model()

    lines = [
        "# R21H Operator Workflow Reference Binding",
        "",
        f"Status: {model.status}",
        "",
        "## Policy flags",
    ]
    for key, value in sorted(model.policy_flags.items()):
        lines.append(f"- `{key}` = `{value}`")

    lines.extend(["", "## Bindings"])
    for binding in model.bindings:
        lines.append(
            f"- `{binding.key}` -> `{binding.route}` | source `{binding.source_path_hint}` | use: {binding.operator_use}"
        )

    lines.extend(["", "## Source validation"])
    for validation in model.source_validations:
        missing = ", ".join(validation.missing_terms) if validation.missing_terms else "none"
        lines.append(
            f"- `{validation.key}` exists={validation.exists} terms_ok={validation.required_terms_ok} missing={missing}"
        )

    return "\n".join(lines) + "\n"
