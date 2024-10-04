from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from django.test import Client
from django.urls import reverse

if TYPE_CHECKING:
    from django.http import HttpResponse


@pytest.mark.django_db
def test_index_view() -> None:
    """Test the index view to ensure it returns the correct status code and context data."""
    client = Client()
    response: HttpResponse = client.get(reverse("index"))

    assert response.status_code == 200
    assert "title" in response.context
    assert response.context["title"] == "Panso.se - Jämför priser"
    assert "description" in response.context
    assert response.context["description"] == (
        "Panso.se hjälper dig jämföra priser över 1000+ produkter och butiker i Sverige. "
        "Hitta de bästa erbjudandena för GPU:er, CPU:er, RAM och mer."
    )
