from typing import Literal

from django.apps import AppConfig


class PansoConfig(AppConfig):
    default_auto_field: Literal["django.db.models.BigAutoField"] = "django.db.models.BigAutoField"
    name: Literal["panso"] = "panso"
