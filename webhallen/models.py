from __future__ import annotations

import logging
import re
import time
from typing import TYPE_CHECKING

import httpx
from django.conf import settings
from django.db import models
from django.utils import timezone

if TYPE_CHECKING:
    from httpx import Response

logger: logging.Logger = logging.getLogger(__name__)

HTTP_STATUS_TOO_MANY_REQUESTS = 429


class WebhallenProductJSON(models.Model):
    """A single product from Webhallen."""

    webhallen_id = models.PositiveIntegerField(unique=True, help_text="Webhallen product ID")
    data = models.JSONField(null=True, help_text="JSON data from Webhallen API")

    created_at = models.DateTimeField(auto_now_add=True, editable=False, help_text="When the data was fetched")
    updated_at = models.DateTimeField(auto_now=True, editable=False, help_text="When the data was last updated")

    class Meta:
        verbose_name: str = "Webhallen data"
        verbose_name_plural: str = "Webhallen data"

    def __str__(self) -> str:
        return f"{self.webhallen_id} - (https://www.webhallen.com/se/product/{self.webhallen_id})"

    def fetch_data(self: WebhallenProductJSON) -> None:
        """Fetch data from Webhallen API."""
        # Don't fetch data if we already have it or it has been more than 24 hours since last fetch
        if self.data and (timezone.now() - self.updated_at).days < 1:
            logger.info("Data already exists for %s", self)
            return

        client: httpx.Client = settings.HISHEL_CLIENT
        url: str = f"https://www.webhallen.com/api/product/{self.webhallen_id}"
        response: httpx.Response = client.get(url=url, extensions={"cache_metadata": True})
        try:
            response.raise_for_status()
        except httpx.HTTPError as exc:
            # Retry the request if we get a 429 because we are rate limited
            if response.status_code == HTTP_STATUS_TOO_MANY_REQUESTS:
                logger.exception("403: Access forbidden for URL: %s. Retrying in 30 seconds...", exc.request.url)
                time.sleep(30)

                # Retry the request
                retry_response: Response = client.get(url=url, extensions={"cache_metadata": True})
                try:
                    retry_response.raise_for_status()  # Check if retry succeeds
                except httpx.HTTPStatusError:
                    logger.exception("Retry failed to fetch data for %s", self)
                    return

            logger.exception("Failed to fetch data for %s", self)
            return

        self.data = response.json()
        self.save()
        logger.info("Fetched data for %s", self)

    @classmethod
    def fetch_data_for_webhallen_ids(cls: type[WebhallenProductJSON], webhallen_ids: list[int]) -> None:
        """Fetch data from Webhallen API for multiple products."""
        for webhallen_id in webhallen_ids:
            instance: WebhallenProductJSON = cls.objects.get(webhallen_id=webhallen_id)
            logger.info("Fetching data for %s", instance)
            instance.fetch_data()


class SitemapHome(models.Model):
    """Saves https://www.webhallen.com/sitemap.home.xml to the database."""

    sitemap = models.TextField(help_text="The sitemap XML")

    created_at = models.DateTimeField(auto_now_add=True, editable=False, help_text="When the data was fetched")
    updated_at = models.DateTimeField(auto_now=True, editable=False, help_text="When the data was last updated")

    class Meta:
        verbose_name: str = "Webhallen Sitemap - home"
        verbose_name_plural: str = "Webhallen Sitemap - home"

    def __str__(self) -> str:
        return f"webhallen.com/sitemap.home.xml - {self.updated_at}"

    def fetch_sitemap(self: SitemapHome) -> None:
        """Fetch sitemap from Webhallen."""
        client: httpx.Client = settings.HISHEL_CLIENT
        response: httpx.Response = client.get(
            url="https://www.webhallen.com/sitemap.home.xml",
            extensions={"cache_metadata": True},
        )
        response.raise_for_status()
        self.sitemap = response.text
        self.save()
        logger.info("Fetched sitemap home")


class SitemapSection(models.Model):
    """Saves https://www.webhallen.com/sitemap.section.xml to the database."""

    sitemap = models.TextField(help_text="The sitemap XML")

    created_at = models.DateTimeField(auto_now_add=True, editable=False, help_text="When the data was fetched")
    updated_at = models.DateTimeField(auto_now=True, editable=False, help_text="When the data was last updated")

    class Meta:
        verbose_name: str = "Webhallen Sitemap - section"
        verbose_name_plural: str = "Webhallen Sitemap - section"

    def __str__(self) -> str:
        return f"webhallen.com/sitemap.section.xml - {self.updated_at}"

    def fetch_sitemap(self: SitemapSection) -> str:
        """Fetch sitemap from Webhallen.

        Returns:
            str: The sitemap XML.
        """
        client: httpx.Client = settings.HISHEL_CLIENT
        response: httpx.Response = client.get(
            url="https://www.webhallen.com/sitemap.section.xml",
            extensions={"cache_metadata": True},
        )
        response.raise_for_status()
        self.sitemap = response.text
        self.save()
        logger.info("Fetched sitemap section")

        return self.sitemap


class SitemapCategory(models.Model):
    """Saves https://www.webhallen.com/sitemap.category.xml to the database."""

    sitemap = models.TextField(help_text="The sitemap XML")

    created_at = models.DateTimeField(auto_now_add=True, editable=False, help_text="When the data was fetched")
    updated_at = models.DateTimeField(auto_now=True, editable=False, help_text="When the data was last updated")

    class Meta:
        verbose_name: str = "Webhallen Sitemap - category"
        verbose_name_plural: str = "Webhallen Sitemap - category"

    def __str__(self) -> str:
        return f"webhallen.com/sitemap.category.xml - {self.updated_at}"

    def fetch_sitemap(self: SitemapCategory) -> str:
        """Fetch sitemap from Webhallen.

        Returns:
            str: The sitemap XML.
        """
        client: httpx.Client = settings.HISHEL_CLIENT
        response: httpx.Response = client.get(
            url="https://www.webhallen.com/sitemap.category.xml",
            extensions={"cache_metadata": True},
        )
        response.raise_for_status()
        self.sitemap = response.text
        self.save()
        logger.info("Fetched sitemap category")

        return self.sitemap


class SitemapCampaign(models.Model):
    """Saves https://www.webhallen.com/sitemap.campaign.xml to the database."""

    sitemap = models.TextField(help_text="The sitemap XML")

    created_at = models.DateTimeField(auto_now_add=True, editable=False, help_text="When the data was fetched")
    updated_at = models.DateTimeField(auto_now=True, editable=False, help_text="When the data was last updated")

    class Meta:
        verbose_name: str = "Webhallen Sitemap - campaign"
        verbose_name_plural: str = "Webhallen Sitemap - campaign"

    def __str__(self) -> str:
        return f"webhallen.com/sitemap.campaign.xml - {self.updated_at}"

    def fetch_sitemap(self: SitemapCampaign) -> str:
        """Fetch sitemap from Webhallen.

        Returns:
            str: The sitemap XML.
        """
        client: httpx.Client = settings.HISHEL_CLIENT
        response: httpx.Response = client.get(
            url="https://www.webhallen.com/sitemap.campaign.xml",
            extensions={"cache_metadata": True},
        )
        response.raise_for_status()
        self.sitemap = response.text
        self.save()
        logger.info("Fetched sitemap campaign")

        return self.sitemap


class SitemapInfoPages(models.Model):
    """Saves https://www.webhallen.com/sitemap.infoPages.xml to the database."""

    sitemap = models.TextField(help_text="The sitemap XML")

    created_at = models.DateTimeField(auto_now_add=True, editable=False, help_text="When the data was fetched")
    updated_at = models.DateTimeField(auto_now=True, editable=False, help_text="When the data was last updated")

    class Meta:
        verbose_name: str = "Webhallen Sitemap - info pages"
        verbose_name_plural: str = "Webhallen Sitemap - info pages"

    def __str__(self) -> str:
        return f"webhallen.com/sitemap.infoPages.xml - {self.updated_at}"

    def fetch_sitemap(self: SitemapInfoPages) -> str:
        """Fetch sitemap from Webhallen.

        Returns:
            str: The sitemap XML.
        """
        client: httpx.Client = settings.HISHEL_CLIENT
        response: httpx.Response = client.get(
            url="https://www.webhallen.com/sitemap.infoPages.xml",
            extensions={"cache_metadata": True},
        )
        response.raise_for_status()
        self.sitemap = response.text
        self.save()
        logger.info("Fetched sitemap info pages")

        return self.sitemap


class SitemapProduct(models.Model):
    """Saves https://www.webhallen.com/sitemap.product.xml to the database."""

    sitemap = models.TextField(help_text="The sitemap XML")

    created_at = models.DateTimeField(auto_now_add=True, editable=False, help_text="When the data was fetched")
    updated_at = models.DateTimeField(auto_now=True, editable=False, help_text="When the data was last updated")

    class Meta:
        verbose_name: str = "Webhallen Sitemap - product"
        verbose_name_plural: str = "Webhallen Sitemap - product"

    def __str__(self) -> str:
        return f"webhallen.com/sitemap.product.xml - {self.updated_at}"

    def fetch_sitemap_from_webhallen(self: SitemapProduct, *, force: bool = False) -> str:
        """Fetch sitemap from Webhallen.

        Args:
            force (bool): Whether to force fetch the sitemap.

        Returns:
            str: The sitemap XML.
        """
        if not self.sitemap or force:
            client: httpx.Client = settings.HISHEL_CLIENT
            response: httpx.Response = client.get(
                url="https://www.webhallen.com/sitemap.product.xml",
                extensions={"cache_metadata": True},
            )
            response.raise_for_status()
            self.sitemap = response.text
            self.save()
            logger.info("Fetched sitemap product")

        return self.sitemap

    @staticmethod
    def convert_loc_to_id(loc: str) -> int:
        """Convert a URL to a Webhallen product ID.

        Example URL:
            https://www.webhallen.com/se/product/364071-ASUS-ProArt-GeForce-RTX-4070-12GB-GDDR6X-OC-Edition

        Args:
            loc (str): The URL to convert.

        Returns:
            int: The Webhallen product ID.
        """
        regex_pattern: str = r"https://www.webhallen.com/se/product/(\d+)-"
        match: re.Match[str] | None = re.search(pattern=regex_pattern, string=loc)
        if match:
            return int(match.group(1))
        return 0


class SitemapManufacturer(models.Model):
    """Saves https://www.webhallen.com/sitemap.manufacturer.xml to the database."""

    sitemap = models.TextField(help_text="The sitemap XML")

    created_at = models.DateTimeField(auto_now_add=True, editable=False, help_text="When the data was fetched")
    updated_at = models.DateTimeField(auto_now=True, editable=False, help_text="When the data was last updated")

    class Meta:
        verbose_name: str = "Webhallen Sitemap - manufacturer"
        verbose_name_plural: str = "Webhallen Sitemap - manufacturer"

    def __str__(self) -> str:
        return f"webhallen.com/sitemap.manufacturer.xml - {self.updated_at}"

    def fetch_sitemap(self: SitemapManufacturer) -> str:
        """Fetch sitemap from Webhallen.

        Returns:
            str: The sitemap XML.
        """
        client: httpx.Client = settings.HISHEL_CLIENT
        response: httpx.Response = client.get(
            url="https://www.webhallen.com/sitemap.manufacturer.xml",
            extensions={"cache_metadata": True},
        )
        response.raise_for_status()
        self.sitemap = response.text
        self.save()
        logger.info("Fetched sitemap manufacturer")

        return self.sitemap


class SitemapArticle(models.Model):
    """Saves https://www.webhallen.com/sitemap.article.xml to the database."""

    sitemap = models.TextField(help_text="The sitemap XML")

    created_at = models.DateTimeField(auto_now_add=True, editable=False, help_text="When the data was fetched")
    updated_at = models.DateTimeField(auto_now=True, editable=False, help_text="When the data was last updated")

    class Meta:
        verbose_name: str = "Webhallen Sitemap - article"
        verbose_name_plural: str = "Webhallen Sitemap - article"

    def __str__(self) -> str:
        return f"webhallen.com/sitemap.article.xml - {self.updated_at}"

    def fetch_sitemap(self: SitemapArticle) -> str:
        """Fetch sitemap from Webhallen.

        Returns:
            str: The sitemap XML.
        """
        client: httpx.Client = settings.HISHEL_CLIENT
        response: httpx.Response = client.get(
            url="https://www.webhallen.com/sitemap.article.xml",
            extensions={"cache_metadata": True},
        )
        response.raise_for_status()
        self.sitemap = response.text
        self.save()
        logger.info("Fetched sitemap article")

        return self.sitemap
