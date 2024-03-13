"""URL configuration for panso project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/

Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib import admin
from django.urls import URLPattern, path

if TYPE_CHECKING:
    from django.urls.resolvers import URLResolver

from panso.views import panso

app_name: str = "panso"

urlpatterns: list[URLResolver | URLPattern] = [
    path(route="", view=panso.index, name="index"),
    path(route="admin/", view=admin.site.urls),
    path(route="robots.txt", view=panso.robots_txt, name="robots_txt"),
]
