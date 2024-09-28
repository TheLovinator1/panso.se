from __future__ import annotations

import sys

from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns: list = [
    path(route="admin/", view=admin.site.urls),
    path(route="accounts/", view=include(arg="allauth.urls")),
    path(route="", view=TemplateView.as_view(template_name="home.html")),
    path(route="__reload__/", view=include(arg="django_browser_reload.urls")),
]

# Don't include debug_toolbar when running tests
if "test" not in sys.argv:
    urlpatterns = [*urlpatterns, *debug_toolbar_urls()]
