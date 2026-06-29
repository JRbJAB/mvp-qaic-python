from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = {
    "docs_scope": "mvp_qaic",
    "public_scope": "mvp-qaic",
    "brand": "MVP QAIC",
    "index_json": "mvp-qaic-web-assets-index.json",
    "public_logo": "logo-mvp-qaic-official-name.png",
    "charte_v0": "mvp-qaic-charte-graphique-v0.png",
    "required_public": [
        "logo-mvp-qaic-official-name.png",
        "logo-mvp-qaic-icon-only.png",
        "favicon.ico",
        "favicon.svg",
        "favicon-16x16.png",
        "favicon-32x32.png",
        "favicon-96x96.png",
        "apple-touch-icon.png",
        "android-chrome-192x192.png",
        "android-chrome-384x384.png",
        "android-chrome-512x512.png",
        "maskable-icon-192x192.png",
        "maskable-icon-512x512.png",
        "mstile-150x150.png",
        "site.webmanifest",
        "browserconfig.xml",
        "meta-tags.html",
        "og-mvp-qaic-brand-preview-1200x630.png",
        "charte-graphique.png",
        "charte/mvp-qaic-charte-graphique-v0.png",
        "brand-assets.html",
        "charte/index.html",
        "mvp-qaic-web-assets-index.json"
    ],
    "required_docs": [
        "README.md",
        "logos/mvp-qaic-logo-official-name-v0.png",
        "logos/mvp-qaic-logo-icon-only-v0.png",
        "charte_graphique/mvp-qaic-charte-graphique-v0.png",
        "source/mvp-qaic-logo-validated-source.png",
        "source/README_SOURCE.md",
        "web/WEB_INTEGRATION.md"
    ]
}
DOCS = ROOT / "docs" / "brand_assets" / DATA["docs_scope"]
PUBLIC = ROOT / "public" / "brand" / DATA["public_scope"]


def _size(path: Path) -> int:
    return path.stat().st_size


def _rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def test_brand_assets_required_files_exist() -> None:
    required = [PUBLIC / item for item in DATA["required_public"]]
    required += [DOCS / item for item in DATA["required_docs"]]
    required += [ROOT / "docs" / "dev_tracking"]
    missing = [_rel(path) for path in required if not path.exists()]
    assert missing == []


def test_brand_assets_are_not_empty() -> None:
    files = [PUBLIC / item for item in DATA["required_public"]]
    files += [DOCS / item for item in DATA["required_docs"]]
    empty = [_rel(path) for path in files if _size(path) <= 0]
    assert empty == []


def test_charte_matches_qait_template_sections() -> None:
    charte = PUBLIC / "charte-graphique.png"
    assert charte.exists()
    assert _size(charte) > 180_000
    html = (PUBLIC / "charte" / "index.html").read_text(encoding="utf-8")
    assert "Format aligné sur la charte QAIT validée" in html
    assert DATA["charte_v0"] in html


def test_public_html_references_logo_icon_charte() -> None:
    html = (PUBLIC / "brand-assets.html").read_text(encoding="utf-8")
    assert DATA["public_logo"] in html
    assert "icon-only" in html
    assert "charte-graphique.png" in html
    assert DATA["index_json"] in html


def test_manifest_and_asset_index_contract() -> None:
    manifest = json.loads((PUBLIC / "site.webmanifest").read_text(encoding="utf-8"))
    index = json.loads((PUBLIC / DATA["index_json"]).read_text(encoding="utf-8"))
    assert manifest["name"] == DATA["brand"]
    assert index["brand"] == DATA["brand"]
    assert index["no_new_logo_invented"] is True
    icon_names = {item["src"] for item in manifest["icons"]}
    assert "android-chrome-192x192.png" in icon_names
    assert "android-chrome-512x512.png" in icon_names


def test_no_desktop_ini_in_brand_scopes() -> None:
    paths = list(DOCS.rglob("*")) + list(PUBLIC.rglob("*"))
    bad = [_rel(path) for path in paths if path.name.lower() == "desktop.ini"]
    assert bad == []
