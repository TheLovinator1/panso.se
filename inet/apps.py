from __future__ import annotations

from typing import Literal

from django.apps import AppConfig


class InetConfig(AppConfig):
    """Inet app configuration."""

    default_auto_field: Literal["django.db.models.BigAutoField"] = "django.db.models.BigAutoField"
    name: Literal["inet"] = "inet"
