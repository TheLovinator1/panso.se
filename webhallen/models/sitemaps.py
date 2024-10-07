"""This module defines Django models for storing various sitemaps from Webhallen's website in the database.

Classes:
    SitemapHome: Stores https://www.webhallen.com/sitemap.home.xml.
    SitemapSection: Stores https://www.webhallen.com/sitemap.section.xml.
    SitemapCategory: Stores https://www.webhallen.com/sitemap.category.xml.
    SitemapCampaign: Stores https://www.webhallen.com/sitemap.campaign.xml.
    SitemapInfoPages: Stores https://www.webhallen.com/sitemap.infoPages.xml.
    SitemapProduct: Stores https://www.webhallen.com/sitemap.product.xml with a method to extract product IDs from URLs.
    SitemapManufacturer: Stores https://www.webhallen.com/sitemap.manufacturer.xml.
    SitemapArticle: Stores https://www.webhallen.com/sitemap.article.xml.
"""

from __future__ import annotations

import logging
import re
from typing import TYPE_CHECKING

import auto_prefetch
from django.conf import settings
from django.db import models

if TYPE_CHECKING:
    import httpx

logger: logging.Logger = logging.getLogger(__name__)


class SitemapHome(auto_prefetch.Model):
    """Saves https://www.webhallen.com/sitemap.home.xml to the database."""

    sitemap = models.TextField(help_text="The sitemap XML")

    created_at = models.DateTimeField(auto_now_add=True, editable=False, help_text="When the data was fetched")
    updated_at = models.DateTimeField(auto_now=True, editable=False, help_text="When the data was last updated")

    class Meta(auto_prefetch.Model.Meta):
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


class SitemapSection(auto_prefetch.Model):
    """Saves https://www.webhallen.com/sitemap.section.xml to the database."""

    sitemap = models.TextField(help_text="The sitemap XML")

    created_at = models.DateTimeField(auto_now_add=True, editable=False, help_text="When the data was fetched")
    updated_at = models.DateTimeField(auto_now=True, editable=False, help_text="When the data was last updated")

    class Meta(auto_prefetch.Model.Meta):
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


class SitemapCategory(auto_prefetch.Model):
    """Saves https://www.webhallen.com/sitemap.category.xml to the database."""

    sitemap = models.TextField(help_text="The sitemap XML")

    created_at = models.DateTimeField(auto_now_add=True, editable=False, help_text="When the data was fetched")
    updated_at = models.DateTimeField(auto_now=True, editable=False, help_text="When the data was last updated")

    class Meta(auto_prefetch.Model.Meta):
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


class SitemapCampaign(auto_prefetch.Model):
    """Saves https://www.webhallen.com/sitemap.campaign.xml to the database."""

    sitemap = models.TextField(help_text="The sitemap XML")

    created_at = models.DateTimeField(auto_now_add=True, editable=False, help_text="When the data was fetched")
    updated_at = models.DateTimeField(auto_now=True, editable=False, help_text="When the data was last updated")

    class Meta(auto_prefetch.Model.Meta):
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


class SitemapInfoPages(auto_prefetch.Model):
    """Saves https://www.webhallen.com/sitemap.infoPages.xml to the database."""

    sitemap = models.TextField(help_text="The sitemap XML")

    created_at = models.DateTimeField(auto_now_add=True, editable=False, help_text="When the data was fetched")
    updated_at = models.DateTimeField(auto_now=True, editable=False, help_text="When the data was last updated")

    class Meta(auto_prefetch.Model.Meta):
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


class SitemapProduct(auto_prefetch.Model):
    """Saves https://www.webhallen.com/sitemap.product.xml to the database."""

    sitemap = models.TextField(help_text="The sitemap XML")

    created_at = models.DateTimeField(auto_now_add=True, editable=False, help_text="When the data was fetched")
    updated_at = models.DateTimeField(auto_now=True, editable=False, help_text="When the data was last updated")

    class Meta(auto_prefetch.Model.Meta):
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


class SitemapManufacturer(auto_prefetch.Model):
    """Saves https://www.webhallen.com/sitemap.manufacturer.xml to the database."""

    sitemap = models.TextField(help_text="The sitemap XML")

    created_at = models.DateTimeField(auto_now_add=True, editable=False, help_text="When the data was fetched")
    updated_at = models.DateTimeField(auto_now=True, editable=False, help_text="When the data was last updated")

    class Meta(auto_prefetch.Model.Meta):
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


class SitemapArticle(auto_prefetch.Model):
    """Saves https://www.webhallen.com/sitemap.article.xml to the database."""

    sitemap = models.TextField(help_text="The sitemap XML")

    created_at = models.DateTimeField(auto_now_add=True, editable=False, help_text="When the data was fetched")
    updated_at = models.DateTimeField(auto_now=True, editable=False, help_text="When the data was last updated")

    class Meta(auto_prefetch.Model.Meta):
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
