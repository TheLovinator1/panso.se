from __future__ import annotations

import os
from typing import TYPE_CHECKING

from django.core.asgi import get_asgi_application

if TYPE_CHECKING:
    from django.core.handlers.asgi import ASGIHandler

os.environ.setdefault(key="DJANGO_SETTINGS_MODULE", value="config.settings")

application: ASGIHandler = get_asgi_application()
