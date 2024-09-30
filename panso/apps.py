from __future__ import annotations

from typing import Literal

from django.apps import AppConfig


class PansoConfig(AppConfig):
    """Configuration for the Panso application."""

    default_auto_field: Literal["django.db.models.BigAutoField"] = "django.db.models.BigAutoField"
    name: Literal["panso"] = "panso"
