from __future__ import annotations

import datetime
import logging
import re
from typing import TYPE_CHECKING, Any, ClassVar

import scrapy
from asgiref.sync import sync_to_async

from webhallen.models import WebhallenJSON, WebhallenProduct

if TYPE_CHECKING:
    from collections.abc import Generator

    from scrapy.http import TextResponse, XmlResponse

logger: logging.Logger = logging.getLogger(__name__)


class WebhallenSpider(scrapy.Spider):
    name: str = "webhallen"
    allowed_domains: ClassVar[list[str]] = ["webhallen.com"]

    def start_requests(self: WebhallenSpider) -> Generator[scrapy.Request, Any, None]:
        """Start requests by fetching the sitemap."""
        yield scrapy.Request(url="https://www.webhallen.com/sitemap.product.xml", callback=self.parse_sitemap)

    def parse_sitemap(self: WebhallenSpider, response: XmlResponse) -> Generator[scrapy.Request, Any, None]:
        """Parse the sitemap to get product URLs."""
        locs: list[str] = response.xpath('//*[local-name()="loc"]/text()').extract()
        if not locs:
            logger.info("[red]No locs found in sitemap[/red]")

        for loc in locs:
            match: re.Match[str] | None = re.search(r"/product/(\d+)", loc)
            if match:
                product_id: str = str(match.group(1))
                api_url: str = f"https://www.webhallen.com/api/product/{product_id}"

                logger.info("Processing product %s", product_id)

                yield scrapy.Request(
                    url=api_url,
                    callback=self.parse_json,
                    meta={"product_id": product_id, "scraped_url": loc},
                    errback=self.error_callback,
                )

    async def error_callback(self: WebhallenSpider, failure) -> None:  # noqa: ANN001, PLR6301
        """Handle request errors."""
        request = failure.request
        product_id = int(request.meta["product_id"])
        scraped_url = request.meta["scraped_url"]
        error_message = str(failure.value)

        logger.error("Error processing product %s from %s: %s", product_id, scraped_url, error_message)

        await sync_to_async(WebhallenProduct.objects.update_or_create)(
            product_id=product_id,
            defaults={
                "last_exception": error_message,
            },
        )

    async def parse_json(self: WebhallenSpider, response: TextResponse) -> None:  # noqa: PLR6301
        """Parse the JSON response from the product API."""
        product_id: int = int(response.meta["product_id"])
        scraped_url: str = str(response.meta["scraped_url"])
        json_data = response.json()
        product_data = json_data.get("product", {})  # type: ignore  # noqa: PGH003
        product_name = str(product_data.get("name"))

        logger.info("Processed product %s from %s", product_id, scraped_url)

        product, _created = await sync_to_async(WebhallenProduct.objects.update_or_create)(
            product_id=product_id,
            defaults={
                "last_scraped_json_at": datetime.datetime.now(tz=datetime.UTC),
                "name": product_name,
                "url": scraped_url,
                "last_exception": "",
            },
        )

        await sync_to_async(WebhallenJSON.objects.update_or_create)(
            product=product,
            scraped_url=scraped_url,
            json=json_data,
        )
