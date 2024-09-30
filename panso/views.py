from __future__ import annotations

from typing import Any

from django.views.generic import TemplateView


class IndexView(TemplateView):
    """IndexView renders the index.html template with context data."""

    template_name = "index.html"

    def get_context_data(self, **kwargs: dict) -> dict:
        """Add context data for the index template.

        Adds the following context data:
        - title: The title of the page.
        - description: A brief description of the application.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            dict: The context data.
        """
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["title"] = "Panso.se - Jämför priser"
        context["description"] = (
            "Panso.se hjälper dig jämföra priser över 1000+ produkter och butiker i Sverige. Hitta de bästa erbjudandena för GPU:er, CPU:er, RAM och mer."  # noqa: E501
        )
        return context
