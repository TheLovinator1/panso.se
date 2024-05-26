import random
import string
from typing import TYPE_CHECKING

import pytest
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.test import Client
from django.test.utils import override_settings
from django.urls import reverse

if TYPE_CHECKING:
    from django.http import HttpResponse


password: str = "".join(random.choices(string.ascii_letters + string.digits, k=12))
username: str = "".join(random.choices(string.ascii_lowercase, k=8))
email: str = (
    "".join(random.choices(string.ascii_lowercase, k=5))
    + "@"
    + "".join(random.choices(string.ascii_lowercase, k=3))
    + "."
    + "".join(random.choices(string.ascii_lowercase, k=2))
)


@pytest.mark.django_db()
@pytest.mark.parametrize("debug_mode", [True, False], ids=["debug_mode_true", "debug_mode_false"])
@pytest.mark.parametrize(
    "url",
    ["/admin/", "/admin", lambda: reverse("admin:index")],
    ids=["url_admin", "url_admin_slash", "url_admin_reverse"],
)
def test_superuser_can_access_admin_page(client: Client, debug_mode: bool, url: str) -> None:
    """Test if a superuser can log in and access the admin page."""
    with override_settings(DEBUG=debug_mode):
        # Resolve the URL for the lambda function
        if callable(url):
            url = url()

        # Create a superuser and log in
        User.objects.create_superuser(username=username, email=email, password=password)
        client.login(username=username, password=password)

        # Access the admin page
        response: HttpResponse = client.get(url, follow=True)

        # Check if the response is as expected
        assert response.status_code == 200, f"Response status code: {response.status_code}"

        # Check if the response content is as expected
        assert "Site administration | Django site admin" in response.content.decode(
            "utf-8",
        ), f"Response content: {response.content.decode("utf-8")}"

        # Check if the username is in the response content
        assert username in response.content.decode("utf-8")


@pytest.mark.django_db()
@pytest.mark.parametrize("debug_mode", [True, False], ids=["debug_mode_true", "debug_mode_false"])
@pytest.mark.parametrize("url", ["/", lambda: reverse("panso:index")], ids=["url_index", "url_index_reverse"])
def test_index_page(client: Client, debug_mode: bool, url: str) -> None:
    """Test if the index page is accessible."""
    with override_settings(DEBUG=debug_mode):
        # Resolve the URL for the lambda function
        if callable(url):
            url = url()

        # Access the index page
        response: HttpResponse = client.get(url)

        # Check if the response is as expected
        assert response.status_code == 200, f"Response status code: {response.status_code}"

        # Check if the response content is as expected
        assert "Hello, world!" in response.content.decode(
            "utf-8",
        ), f"Response content: {response.content.decode("utf-8")}"


@pytest.mark.django_db()
@pytest.mark.parametrize("debug_mode", [True, False], ids=["debug_mode_true", "debug_mode_false"])
@pytest.mark.parametrize(
    "url",
    ["/robots.txt", lambda: reverse("panso:robots_txt")],
    ids=["url_robots_txt", "url_robots_txt_reverse"],
)
def test_robots_txt(client: Client, debug_mode: bool, url: str) -> None:
    """Test if the robots.txt page is accessible."""
    with override_settings(DEBUG=debug_mode):
        # Resolve the URL for the lambda function
        if callable(url):
            url = url()

        # Access the robots.txt page
        response: HttpResponse = client.get(url)

        # Check if the response is as expected
        assert response.status_code == 200

        # Check if the response content is as expected
        assert response.content == b"User-agent: *\nDisallow: /admin\n\nSitemap: https://panso.se/sitemap.xml"
