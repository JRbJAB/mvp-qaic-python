"""Runnable local Reflex app for MVP QAIC."""

from __future__ import annotations

__all__ = ["app"]


def __getattr__(name: str) -> object:
    if name != "app":
        raise AttributeError(name)

    from .mvp_qaic_reflex_ui import app

    return app
