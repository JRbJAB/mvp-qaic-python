from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Sequence, Any

CONTRACT_VERSION = "mvp_qaic.migration_contracts.v1"

MIGRATION_SAFETY_MARKERS: tuple[str, ...] = (
    "MIGRATION_READONLY",
    "SCHEMA_VALIDATION_ONLY",
    "NO_GOOGLE_LIVE_WRITE",
    "NO_SHEET_WRITE",
    "NO_BROKER",
    "NO_ORDER",
    "NO_SIZING",
    "NO_SECRET",
)


@dataclass(frozen=True)
class ContractField:
    name: str
    required: bool = True
    allow_empty: bool = False
    description: str = ""


@dataclass(frozen=True)
class ContractSpec:
    contract_id: str
    version: str
    source_kind: str
    fields: tuple[ContractField, ...]
    safety_markers: tuple[str, ...] = MIGRATION_SAFETY_MARKERS


@dataclass(frozen=True)
class ContractValidationResult:
    contract_id: str
    version: str
    status: str
    missing_fields: tuple[str, ...] = field(default_factory=tuple)
    empty_fields: tuple[str, ...] = field(default_factory=tuple)
    unexpected_fields: tuple[str, ...] = field(default_factory=tuple)
    row_count: int = 1
    valid_row_count: int = 0
    invalid_row_count: int = 0
    blockers: tuple[str, ...] = field(default_factory=tuple)
    safety_markers: tuple[str, ...] = MIGRATION_SAFETY_MARKERS


def _field_names(spec: ContractSpec) -> tuple[str, ...]:
    return tuple(field_spec.name for field_spec in spec.fields)


def _required_field_names(spec: ContractSpec) -> tuple[str, ...]:
    return tuple(field_spec.name for field_spec in spec.fields if field_spec.required)


def _empty_forbidden_field_names(spec: ContractSpec) -> tuple[str, ...]:
    return tuple(
        field_spec.name
        for field_spec in spec.fields
        if field_spec.required and not field_spec.allow_empty
    )


def _is_empty(value: object) -> bool:
    return value is None or (isinstance(value, str) and value.strip() == "")


TRADE_PLAN_INPUT_CONTRACT = ContractSpec(
    contract_id="trade_plan_input.v1",
    version=CONTRACT_VERSION,
    source_kind="sheet_or_csv_row",
    fields=(
        ContractField("signal_id", description="Stable signal identifier."),
        ContractField("risk_guard", description="Safety posture markers."),
        ContractField("asset", description="Asset symbol."),
        ContractField("current_price", description="Observed current price."),
        ContractField("entry_price", description="Human-provided entry price."),
        ContractField("tp1", description="Human-provided first target."),
        ContractField("tp2", description="Human-provided second target."),
        ContractField("tp3", description="Human-provided third target."),
        ContractField("stop_loss", description="Human-provided stop loss."),
        ContractField("invalidation_level", description="Human invalidation level."),
        ContractField("requested_action", required=False, allow_empty=True),
    ),
)

PUBLIC_MARKET_SNAPSHOT_CONTRACT = ContractSpec(
    contract_id="public_market_snapshot.v1",
    version=CONTRACT_VERSION,
    source_kind="python_provider_snapshot",
    fields=(
        ContractField("provider_version"),
        ContractField("provider"),
        ContractField("asset"),
        ContractField("symbol"),
        ContractField("current_price"),
        ContractField("quote_currency"),
        ContractField("status"),
        ContractField("live_readonly"),
        ContractField("network_called"),
        ContractField("broker_called"),
        ContractField("order_created"),
        ContractField("sizing_created"),
        ContractField("source_url", required=False, allow_empty=True),
        ContractField("missing_data", required=False, allow_empty=True),
        ContractField("blockers", required=False, allow_empty=True),
    ),
)

DECISION_JOURNAL_CONTRACT = ContractSpec(
    contract_id="decision_journal.v1",
    version=CONTRACT_VERSION,
    source_kind="sheet_or_csv_row",
    fields=(
        ContractField("run_id"),
        ContractField("signal_id"),
        ContractField("asset"),
        ContractField("decision_status"),
        ContractField("human_decision_only"),
        ContractField("no_order_no_sizing"),
        ContractField("risk_guard"),
        ContractField("timestamp"),
        ContractField("missing_data", required=False, allow_empty=True),
        ContractField("blockers", required=False, allow_empty=True),
        ContractField("notes", required=False, allow_empty=True),
    ),
)

RUNTIME_OUTPUT_CONTRACT = ContractSpec(
    contract_id="runtime_output.v1",
    version=CONTRACT_VERSION,
    source_kind="python_runtime_json",
    fields=(
        ContractField("runtime_version"),
        ContractField("decision_status"),
        ContractField("missing_data", required=False, allow_empty=True),
        ContractField("blockers", required=False, allow_empty=True),
        ContractField("human_decision_only"),
        ContractField("no_order_no_sizing"),
        ContractField("safety_markers"),
        ContractField("live_readonly"),
        ContractField("broker_called"),
        ContractField("order_created"),
        ContractField("sizing_created"),
    ),
)


def migration_contract_registry() -> dict[str, ContractSpec]:
    contracts = (
        TRADE_PLAN_INPUT_CONTRACT,
        PUBLIC_MARKET_SNAPSHOT_CONTRACT,
        DECISION_JOURNAL_CONTRACT,
        RUNTIME_OUTPUT_CONTRACT,
    )
    return {contract.contract_id: contract for contract in contracts}


def list_contract_ids() -> tuple[str, ...]:
    return tuple(sorted(migration_contract_registry()))


def get_contract(contract_id: str) -> ContractSpec:
    registry = migration_contract_registry()
    try:
        return registry[contract_id]
    except KeyError as exc:
        raise KeyError(f"unknown migration contract: {contract_id}") from exc


def validate_contract_record(
    record: Mapping[str, Any],
    contract: ContractSpec,
    *,
    allow_unexpected_fields: bool = True,
) -> ContractValidationResult:
    expected_fields = set(_field_names(contract))
    required_fields = _required_field_names(contract)
    empty_forbidden = set(_empty_forbidden_field_names(contract))

    missing = tuple(field_name for field_name in required_fields if field_name not in record)
    empty = tuple(
        field_name
        for field_name in required_fields
        if field_name in empty_forbidden and field_name in record and _is_empty(record[field_name])
    )
    unexpected = tuple(
        sorted(str(field_name) for field_name in record if str(field_name) not in expected_fields)
    )

    blockers: list[str] = []
    if missing:
        blockers.append("MISSING_REQUIRED_FIELDS")
    if empty:
        blockers.append("EMPTY_REQUIRED_FIELDS")
    if unexpected and not allow_unexpected_fields:
        blockers.append("UNEXPECTED_FIELDS")

    status = "PASS" if not blockers else "REVIEW_REQUIRED"

    return ContractValidationResult(
        contract_id=contract.contract_id,
        version=contract.version,
        status=status,
        missing_fields=missing,
        empty_fields=empty,
        unexpected_fields=unexpected,
        row_count=1,
        valid_row_count=1 if status == "PASS" else 0,
        invalid_row_count=0 if status == "PASS" else 1,
        blockers=tuple(blockers),
    )


def validate_contract_records(
    records: Sequence[Mapping[str, Any]],
    contract: ContractSpec,
    *,
    allow_unexpected_fields: bool = True,
) -> ContractValidationResult:
    if not records:
        return ContractValidationResult(
            contract_id=contract.contract_id,
            version=contract.version,
            status="REVIEW_REQUIRED",
            row_count=0,
            valid_row_count=0,
            invalid_row_count=0,
            blockers=("NO_ROWS",),
        )

    missing: set[str] = set()
    empty: set[str] = set()
    unexpected: set[str] = set()
    valid_count = 0
    invalid_count = 0
    blockers: set[str] = set()

    for record in records:
        result = validate_contract_record(
            record,
            contract,
            allow_unexpected_fields=allow_unexpected_fields,
        )
        missing.update(result.missing_fields)
        empty.update(result.empty_fields)
        unexpected.update(result.unexpected_fields)
        blockers.update(result.blockers)
        if result.status == "PASS":
            valid_count += 1
        else:
            invalid_count += 1

    status = "PASS" if invalid_count == 0 and not blockers else "REVIEW_REQUIRED"

    return ContractValidationResult(
        contract_id=contract.contract_id,
        version=contract.version,
        status=status,
        missing_fields=tuple(sorted(missing)),
        empty_fields=tuple(sorted(empty)),
        unexpected_fields=tuple(sorted(unexpected)),
        row_count=len(records),
        valid_row_count=valid_count,
        invalid_row_count=invalid_count,
        blockers=tuple(sorted(blockers)),
    )


def contract_spec_to_dict(spec: ContractSpec) -> dict[str, object]:
    return {
        "contract_id": spec.contract_id,
        "version": spec.version,
        "source_kind": spec.source_kind,
        "fields": [
            {
                "name": field_spec.name,
                "required": field_spec.required,
                "allow_empty": field_spec.allow_empty,
                "description": field_spec.description,
            }
            for field_spec in spec.fields
        ],
        "safety_markers": list(spec.safety_markers),
    }


def contract_validation_result_to_dict(
    result: ContractValidationResult,
) -> dict[str, object]:
    return {
        "contract_id": result.contract_id,
        "version": result.version,
        "status": result.status,
        "missing_fields": list(result.missing_fields),
        "empty_fields": list(result.empty_fields),
        "unexpected_fields": list(result.unexpected_fields),
        "row_count": result.row_count,
        "valid_row_count": result.valid_row_count,
        "invalid_row_count": result.invalid_row_count,
        "blockers": list(result.blockers),
        "safety_markers": list(result.safety_markers),
    }
