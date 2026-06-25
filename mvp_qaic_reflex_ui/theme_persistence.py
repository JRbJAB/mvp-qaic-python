"""Browser-local theme persistence for MVP QAIC Reflex."""

from __future__ import annotations

import reflex as rx


THEME_LOCAL_STORAGE_KEY = "mvp_qaic_ui_theme_preference_v1"
THEME_PERSISTENCE_MODE = "BROWSER_LOCAL_STORAGE"
THEME_ALLOWED_VALUES = ("light", "dark", "system")

THEME_PERSISTENCE_SCRIPT = f"""
(function () {{
  const KEY = "{THEME_LOCAL_STORAGE_KEY}";
  const VALID = ["light", "dark", "system"];

  function systemMode() {{
    if (window.matchMedia &&
        window.matchMedia("(prefers-color-scheme: dark)").matches) {{
      return "dark";
    }}
    return "light";
  }}

  function effectiveMode(mode) {{
    if (mode === "system") {{
      return systemMode();
    }}
    return mode === "dark" ? "dark" : "light";
  }}

  function updateStatus(mode) {{
    const effective = effectiveMode(mode);
    const status = document.getElementById("mvp-qaic-theme-persistence-status");
    if (status) {{
      status.textContent = "Persisted preference: " + mode + " / effective: " + effective;
    }}
  }}

  function applyTheme(mode) {{
    if (!VALID.includes(mode)) {{
      mode = "system";
    }}

    window.localStorage.setItem(KEY, mode);

    const effective = effectiveMode(mode);
    const root = document.documentElement;

    root.dataset.mvpQaicThemeMode = mode;
    root.dataset.mvpQaicEffectiveTheme = effective;
    root.style.colorScheme = effective;

    root.classList.toggle("mvp-qaic-dark", effective === "dark");
    root.classList.toggle("mvp-qaic-light", effective === "light");

    updateStatus(mode);
  }}

  function bindButton(id, mode) {{
    const button = document.getElementById(id);
    if (!button) {{
      return;
    }}
    button.addEventListener("click", function () {{
      applyTheme(mode);
    }});
  }}

  function boot() {{
    const stored = window.localStorage.getItem(KEY) || "system";
    applyTheme(VALID.includes(stored) ? stored : "system");

    bindButton("mvp-qaic-theme-persist-light", "light");
    bindButton("mvp-qaic-theme-persist-dark", "dark");
    bindButton("mvp-qaic-theme-persist-system", "system");
    bindButton("mvp-qaic-theme-persist-reset", "system");

    if (window.matchMedia) {{
      const media = window.matchMedia("(prefers-color-scheme: dark)");
      if (media.addEventListener) {{
        media.addEventListener("change", function () {{
          const current = window.localStorage.getItem(KEY) || "system";
          if (current === "system") {{
            applyTheme("system");
          }}
        }});
      }}
    }}

    window.MVP_QAIC_THEME_PERSISTENCE = {{
      key: KEY,
      allowed: VALID,
      get: function () {{
        return window.localStorage.getItem(KEY) || "system";
      }},
      apply: applyTheme,
      reset: function () {{
        applyTheme("system");
      }},
    }};
  }}

  if (document.readyState === "loading") {{
    document.addEventListener("DOMContentLoaded", boot);
  }} else {{
    boot();
  }}
}})();
"""


def build_theme_persistence_payload() -> dict[str, object]:
    return {
        "persistence_status": "READY_BROWSER_LOCAL_STORAGE",
        "storage_key": THEME_LOCAL_STORAGE_KEY,
        "persistence_mode": THEME_PERSISTENCE_MODE,
        "allowed_values": list(THEME_ALLOWED_VALUES),
        "default_value": "system",
        "server_write": False,
        "sheet_write": False,
        "bigquery_write": False,
        "public_deploy": False,
        "live_action": False,
        "human_review_approved": True,
    }


def theme_persistence_summary_rows() -> dict[str, object]:
    payload = build_theme_persistence_payload()
    return {
        "persistence_status": payload["persistence_status"],
        "storage_key": payload["storage_key"],
        "persistence_mode": payload["persistence_mode"],
        "default_value": payload["default_value"],
        "server_write": payload["server_write"],
        "sheet_write": payload["sheet_write"],
        "bigquery_write": payload["bigquery_write"],
    }


def theme_persistence_component() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading("Browser theme persistence", size="4"),
            rx.text(
                "Préférence stockée dans le navigateur local via localStorage. "
                "Aucune écriture serveur, Sheets ou BigQuery.",
                size="3",
            ),
            rx.hstack(
                rx.button(
                    "Persist Light",
                    id="mvp-qaic-theme-persist-light",
                    variant="soft",
                ),
                rx.button(
                    "Persist Dark",
                    id="mvp-qaic-theme-persist-dark",
                    variant="soft",
                ),
                rx.button(
                    "Persist System",
                    id="mvp-qaic-theme-persist-system",
                    variant="soft",
                ),
                rx.button(
                    "Reset",
                    id="mvp-qaic-theme-persist-reset",
                    variant="outline",
                ),
                spacing="2",
                wrap="wrap",
            ),
            rx.text(
                "Persisted preference: pending browser boot",
                id="mvp-qaic-theme-persistence-status",
                size="2",
                weight="bold",
            ),
            rx.code(THEME_LOCAL_STORAGE_KEY, size="2"),
            rx.script(
                THEME_PERSISTENCE_SCRIPT,
                id="mvp-qaic-theme-persistence-script",
            ),
            spacing="3",
            align="start",
            width="100%",
        ),
        border="1px solid var(--gray-6)",
        border_radius="16px",
        padding="1rem",
        width="100%",
        background="var(--gray-2)",
    )
