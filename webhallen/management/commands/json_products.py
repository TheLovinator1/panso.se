from __future__ import annotations

import logging

from django.core.management.base import BaseCommand
from httpx import HTTPStatusError
from sitemap_parser import SiteMapParser, Url, UrlSet

from webhallen.models.scraped import WebhallenProductJSON
from webhallen.models.sitemaps import SitemapProduct

logger: logging.Logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Command to download JSON for products in the sitemap.

    You can pass the `--all` flag to download all products, even those not in the sitemap.

    Raises:
        CommandError: If the argument is "error".
    """

    help = "Download JSON for products in the sitemap"

    def handle(self, *args: tuple, **kwargs: dict) -> None:
        """Handles the command."""
        self.main(*args, **kwargs)

    def main(self, *args: tuple, **kwargs: dict) -> None:  # noqa: ARG002
        """Main function for the command.

        Args:
            args (tuple): The arguments for the command. (Unused)
            kwargs (dict): The keyword arguments for the command (Unused).
        """
        sitemap_product = SitemapProduct()
        sitemap: str = sitemap_product.fetch_sitemap_from_webhallen()

        parser: SiteMapParser = SiteMapParser(sitemap, is_data_string=True)
        if not parser.has_urls():
            logger.error("No URLs found in the sitemap")
            return

        urls: UrlSet = parser.get_urls()
        for url in urls:
            product_id: int = self.get_product_id(sitemap_product=sitemap_product, url=url)
            if not product_id:
                continue

            product: WebhallenProductJSON = self.get_or_create_product(product_id=product_id)
            self.fetch_data(product)

        logger.info("Successfully fetched data for all products")

    @staticmethod
    def get_or_create_product(product_id: int) -> WebhallenProductJSON:
        """Get or create a product.

        Args:
            product_id (int): The product ID.

        Returns:
            WebhallenProductJSON: The product.
        """
        product, created = WebhallenProductJSON.objects.get_or_create(webhallen_id=product_id)
        if created:
            logger.info("Product ID '%s' created", product_id)
        return product

    @staticmethod
    def fetch_data(product: WebhallenProductJSON) -> None:
        """Fetches the data for the product.

        Args:
            product (WebhallenProductJSON): The product.
        """
        try:
            product.fetch_data()
        except HTTPStatusError:
            logger.exception("Error fetching data for product ID '%s'", product.webhallen_id)
        logger.info("Successfully fetched data for product ID '%s'", product.webhallen_id)

    def get_product_id(self, sitemap_product: SitemapProduct, url: Url) -> int:
        """Get the product ID from the URL.

        Args:
            sitemap_product (SitemapProduct): The sitemap product.
            url (Url): The URL to get the product ID from.

        Returns:
            int: The product ID.
        """
        if not url.loc:
            logger.error("No loc found in the URL '%s'", url)
            return 0

        product_id: int = sitemap_product.convert_loc_to_id(url.loc)
        if product_id == 0:
            self.stdout.write(msg=self.style.ERROR(f"Product ID not found for URL '{url.loc}'"))

        return product_id
