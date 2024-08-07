# Scrapy settings for the Clutter project
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from __future__ import annotations

import os

from django.conf import settings

os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"


from typing import TYPE_CHECKING

import django

if TYPE_CHECKING:
    from pathlib import Path

django.setup()

data_dir: Path = settings.DATA_DIR
if not data_dir.exists():
    msg: str = f"Data directory {data_dir} does not exist. This means Django is not set up correctly."
    raise FileNotFoundError(msg)

BOT_NAME = "clutter"

SPIDER_MODULES: list[str] = ["clutter.spiders"]
NEWSPIDER_MODULE = "clutter.spiders"
HTTPCACHE_ENABLED = True
HTTPCACHE_DIR: str = str(data_dir / "httpcache")
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
USER_AGENT = "Clutter (+http://www.panso.se)"
DEFAULT_REQUEST_HEADERS: dict[str, str] = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en",
    "DNT": "1",
}
CLOSESPIDER_ERRORCOUNT = 1
DOWNLOAD_DELAY = 2
