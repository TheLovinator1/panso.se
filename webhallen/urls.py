from django.urls import path
from django.urls.resolvers import URLPattern

from .views import WebhallenProductsView, WebhallenProductView

app_name: str = "webhallen"

urlpatterns: list[URLPattern] = [
    path(route="", view=WebhallenProductsView.as_view(), name="webhallen_products"),
    path(route="<int:product_id>/", view=WebhallenProductView.as_view(), name="webhallen_product"),
]
