from __future__ import annotations

import sys

from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import include, path

urlpatterns: list = [
    path(route="admin/", view=admin.site.urls),
    path(route="accounts/", view=include(arg="allauth.urls")),
    path(route="__reload__/", view=include(arg="django_browser_reload.urls")),
    path(route="", view=include(arg="panso.urls")),
]

# Don't include debug_toolbar when running tests
if "test" not in sys.argv:
    urlpatterns = [*urlpatterns, *debug_toolbar_urls()]
