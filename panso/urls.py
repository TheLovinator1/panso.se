from __future__ import annotations

from typing import TYPE_CHECKING

from django.urls import path

from . import views

if TYPE_CHECKING:
    from django.urls.resolvers import URLPattern

urlpatterns: list[URLPattern] = [
    path(route="", view=views.IndexView.as_view(), name="index"),
]
