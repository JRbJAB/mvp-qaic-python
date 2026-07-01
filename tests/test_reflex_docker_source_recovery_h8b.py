from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCKERFILE = ROOT / "docker" / "reflex-pinned-hub" / "Dockerfile"
README = ROOT / "docker" / "reflex-pinned-hub" / "README.md"
SELECTOR = ROOT / "scripts" / "H8B_REFLEX_DOCKER_BUILD_SELECTOR_NO_RUNTIME.ps1"
PINNED_IMAGE = "jrb-reflex-pinned-hub:py312-node22-reflex096p1"
POLICY_ID = "R16F2H4_REFLEX_RUNTIME_POLICY_LOCK"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_recovered_docker_source_path_is_reviewable_and_explicit() -> None:
    assert DOCKERFILE.is_file()
    assert README.is_file()
    dockerfile = _text(DOCKERFILE)
    readme = _text(README)
    combined = dockerfile + "\n" + readme
    assert PINNED_IMAGE in combined
    assert POLICY_ID in combined
    assert "recovered" in combined.lower()
    assert "original provenance" in combined.lower()
    assert "not proven" in combined.lower() or "not asserted" in combined.lower()


def test_dockerfile_pins_expected_contract_without_runtime_startup() -> None:
    dockerfile = _text(DOCKERFILE)
    assert "FROM python:3.12" in dockerfile
    assert "ARG NODE_MAJOR=22" in dockerfile
    assert "ARG REFLEX_VERSION=0.9.6.post1" in dockerfile
    assert re.search(r"reflex==\$\{REFLEX_VERSION\}", dockerfile)
    assert not re.search(r"(?im)^\s*(CMD|ENTRYPOINT)\b", dockerfile)


def test_selector_defaults_to_dry_run_and_requires_explicit_build_flag() -> None:
    selector = _text(SELECTOR)
    assert "[switch]$Build" in selector
    assert "default_dry_run" in selector
    assert "DRY_RUN_NO_BUILD" in selector
    assert "EXPLICIT_BUILD_REQUESTED" in selector
    assert "[System.IO.Directory]::CreateDirectory" in selector
    assert "New-Item -LiteralPath" not in selector
    assert "C:\\JRb_TRADING_OS\\_RUN_REPORTS\\MVP_QAIC_PY" in selector


def test_h8b_files_static_no_forbidden_runtime_or_destructive_tokens() -> None:
    forbidden = [
        "git add" + " .",
        "git " + "reset",
        "docker" + " run",
        "reflex" + " run",
        "Start" + "-Process",
        "clasp" + " push",
        "Remove" + "-Item",
    ]
    paths = [DOCKERFILE, README, SELECTOR]
    hits: list[str] = []
    for path in paths:
        text = _text(path)
        for token in forbidden:
            if token in text:
                hits.append(f"{path.relative_to(ROOT)}::{token}")
    assert hits == []
