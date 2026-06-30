from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "mvp_qaic_reflex_ui" / "mvp_qaic_reflex_ui.py"
WEB_ROUTES = ROOT / ".web" / "app" / "routes"


def test_r16b_app_is_not_r15_static_preview_shell() -> None:
    text = APP.read_text(encoding="utf-8", errors="replace")
    forbidden = ["PRIVATE REFLEX PREVIEW", "R15H", "R15J", "Real module cockpit"]
    assert not any(marker in text for marker in forbidden)


def test_r16b_reflex_shell_sources_exist() -> None:
    required = [
        ROOT / "mvp_qaic_reflex_ui" / "pages_landing.py",
        ROOT / "mvp_qaic_reflex_ui" / "theme.py",
        ROOT / "mvp_qaic_reflex_ui" / "visual_theme.py",
        ROOT / "mvp_qaic_reflex_ui" / "web_architecture_cdc.py",
    ]
    for path in required:
        assert path.exists(), path


def test_r16b_web_static_preview_is_not_source_of_truth() -> None:
    if not WEB_ROUTES.exists():
        return
    static_preview_hits = []
    for path in WEB_ROUTES.glob("*.tsx"):
        text = path.read_text(encoding="utf-8", errors="replace")
        if "PRIVATE REFLEX PREVIEW" in text or "R15H" in text or "R15J" in text:
            static_preview_hits.append(path.name)
    assert static_preview_hits, "This test documents that .web is generated/disposable and must not be treated as source."
