from __future__ import annotations

import pathlib
import subprocess


ROOT = pathlib.Path(__file__).resolve().parents[1]


def _git_ls_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    decoded = result.stdout.decode("utf-8", errors="replace")
    return [entry.strip() for entry in decoded.split("\0") if entry.strip()]


def test_desktop_ini_is_ignored() -> None:
    gitignore = ROOT / ".gitignore"
    assert gitignore.exists()
    text = gitignore.read_text(encoding="utf-8", errors="replace")
    assert any(line.strip().lower() == "desktop.ini" for line in text.splitlines())


def test_no_desktop_ini_is_tracked() -> None:
    tracked = _git_ls_files()
    offenders = [p for p in tracked if pathlib.PurePosixPath(p).name.lower() == "desktop.ini"]
    assert offenders == []


def test_tool_registry_and_root_lock_docs_exist() -> None:
    assert (ROOT / "docs" / "TOOL_REGISTRY_CDC.md").exists()
    assert (ROOT / "docs" / "TOOL_REGISTRY_SCHEMA.md").exists()
    assert (ROOT / "docs" / "TOOL_REGISTRY_CHANGELOG.md").exists()
    assert (ROOT / "docs" / "P237C_ROOT_LOCK_EXPORT_HYGIENE_POLICY.md").exists()
    assert (ROOT / "data" / "tool_registry" / "tools_global.json").exists()
    assert (ROOT / "data" / "tool_registry" / "tools_project_mvp_qaic.json").exists()


def test_p237c_does_not_create_reflex_tools_page() -> None:
    suspicious_paths = [
        ROOT / "pages" / "tools.py",
        ROOT / "mvp_qaic_reflex_ui" / "pages" / "tools.py",
    ]
    assert [path for path in suspicious_paths if path.exists()] == []
