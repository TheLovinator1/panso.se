from __future__ import annotations

from typing import TYPE_CHECKING, cast

import pytest
from django.http import HttpResponseRedirect
from django.test import Client
from django.urls import reverse

if TYPE_CHECKING:
    from django.contrib.auth.models import User
    from django.http import HttpResponse


@pytest.mark.django_db
def test_admin_view() -> None:
    """Test the admin view to ensure it returns the correct status code and context data."""
    client = Client()
    response: HttpResponse = client.get(reverse(viewname="admin:index"))

    # Cast to HttpResponseRedirect to remove type error
    response = cast(HttpResponseRedirect, response)

    # Check if the response is a redirect to the login page
    assert response.status_code == 302
    assert response.url == "/admin/login/?next=/admin/"


@pytest.mark.django_db
def test_index_view() -> None:
    """Test the index view to ensure it returns the correct status code and context data."""
    client = Client()
    response: HttpResponse = client.get(reverse(viewname="index"))

    # Check if the response is 200 OK
    assert response.status_code == 200
    assert "Panso.se - Jämför priser" in response.content.decode()
    assert (
        "Panso.se hjälper dig jämföra priser över 1000+ produkter och butiker i Sverige." in response.content.decode()
    )


@pytest.mark.django_db
def test_admin_view_logged_in(admin_user: User) -> None:
    """Test the admin view when logged in to ensure it returns the correct status code."""
    client = Client()
    client.force_login(admin_user)
    response: HttpResponse = client.get(reverse(viewname="admin:index"))

    # Check if the response is 200 OK
    assert response.status_code == 200
