from __future__ import annotations

from typing import Literal

from django.apps import AppConfig


class WebhallenConfig(AppConfig):
    """Configuration for the Webhallen app."""

    default_auto_field: Literal["django.db.models.BigAutoField"] = "django.db.models.BigAutoField"
    name: Literal["webhallen"] = "webhallen"
