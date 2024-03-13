from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.template import loader


def index(request: HttpRequest) -> HttpResponse:
    """/ index page."""
    template = loader.get_template(template_name="index.html")
    canonical_url: str = "https://panso.se/"
    context: dict[str, str] = {"canonical_url": canonical_url}
    return HttpResponse(content=template.render(context=context, request=request))


def robots_txt(request: HttpRequest) -> HttpResponse:  # noqa: ARG001
    """robots.txt page."""
    robots_txt_content = "User-agent: *\nDisallow: /admin\n\nSitemap: https://panso.se/sitemap.xml"
    return HttpResponse(robots_txt_content, content_type="text/plain")
