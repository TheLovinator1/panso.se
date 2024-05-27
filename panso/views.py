from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View


class IndexView(View):
    template_name: str = "index.html"
    canonical_url: str = "https://panso.se/"

    def get(self: IndexView, request: HttpRequest) -> HttpResponse:
        context: dict[str, str] = {"canonical_url": self.canonical_url}
        return render(request=request, template_name=self.template_name, context=context)


class RobotsTxtView(View):
    robots_txt_content: str = "User-agent: *\nDisallow: /admin\n\nSitemap: https://panso.se/sitemap.xml"

    def get(self: RobotsTxtView, request: HttpRequest) -> HttpResponse:  # noqa: ARG002
        return HttpResponse(content=self.robots_txt_content, content_type="text/plain")
