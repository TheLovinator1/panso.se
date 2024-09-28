import os

from django.core.asgi import get_asgi_application
from django.core.handlers.asgi import ASGIHandler

os.environ.setdefault(key="DJANGO_SETTINGS_MODULE", value="config.settings")

application: ASGIHandler = get_asgi_application()
