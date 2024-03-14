# Scrapy settings for the Clutter project
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from __future__ import annotations

import os

os.environ["DJANGO_SETTINGS_MODULE"] = "panso.settings"


import django

django.setup()

BOT_NAME = "clutter"

SPIDER_MODULES: list[str] = ["clutter.spiders"]
NEWSPIDER_MODULE = "clutter.spiders"
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 3 * 60 * 60  # 3 hours
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
USER_AGENT = "Clutter (+http://www.panso.se)"
DEFAULT_REQUEST_HEADERS: dict[str, str] = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en",
    "DNT": "1",
}
