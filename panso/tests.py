from __future__ import annotations

from typing import TYPE_CHECKING, cast

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.test import Client, TestCase
from django.urls import reverse

if TYPE_CHECKING:
    from django.http import HttpResponse


class TestAdminPage(TestCase):
    def setUp(self) -> None:
        """Create a test user and log in."""
        self.client = Client()
        self.user: User = User.objects.create_user(username="testuser", email="test@panso.se", password="testpassword")  # noqa: S106
        self.client.login(username="testuser", password="testpassword")  # noqa: S106

    def test_admin_page(self) -> None:
        """Test if the admin page is accessible."""
        response: HttpResponse = self.client.get(reverse("admin:index"))
        assert response.status_code == 302
        response = cast(HttpResponseRedirect, response)
        assert response.url == "/admin/login/?next=/admin/"
        self.client.logout()

        response: HttpResponse = self.client.get(reverse("admin:index"), follow=True)
        assert response.status_code == 200
        self.client.logout()


class TestIndexPage(TestCase):
    def test_index_page(self) -> None:
        """Test if the index page is accessible."""
        response: HttpResponse = self.client.get(reverse("index"))
        assert response.status_code == 200

        response: HttpResponse = self.client.get("/")
        assert response.status_code == 200


class TestRobotsTxt(TestCase):
    def test_robots_txt(self) -> None:
        """Test if the robots.txt page is accessible."""
        response: HttpResponse = self.client.get("/robots.txt")
        assert response.status_code == 200
        assert response.content == b"User-agent: *\nDisallow: /admin\n\nSitemap: https://panso.se/sitemap.xml"
        response: HttpResponse = self.client.get(reverse("robots_txt"))
        assert response.status_code == 200
        assert response.content == b"User-agent: *\nDisallow: /admin\n\nSitemap: https://panso.se/sitemap.xml"
