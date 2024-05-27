from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import ListView

from .models import WebhallenProduct

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


class WebhallenProductsView(ListView):
    model = WebhallenProduct
    paginate_by = 100
    template_name: str = "webhallen/products.html"
    context_object_name: str = "products"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:  # noqa: ANN401
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["canonical_url"] = "https://panso.se/webhallen/"
        context["products_length"] = WebhallenProduct.objects.count()
        return context


class WebhallenProductView(View):
    model = WebhallenProduct
    template_name: str = "webhallen/product.html"

    def get(self: WebhallenProductView, request: HttpRequest, product_id: int) -> HttpResponse:
        product: WebhallenProduct = get_object_or_404(self.model, product_id=product_id)
        context: dict[str, Any] = {"canonical_url": f"https://panso.se/webhallen/{product_id}/", "product": product}
        return render(request=request, template_name=self.template_name, context=context)
