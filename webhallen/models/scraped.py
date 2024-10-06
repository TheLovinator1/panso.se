"""This module defines the WebhallenProductJSON model to store product data fetched from Webhallen's API.

The model provides methods to:
    - Fetch and store JSON data for a specific product from Webhallen's API.
    - Automatically retry fetching data if rate-limited (HTTP 429).
    - Fetch data for multiple products via a class method.

Classes:
    WebhallenProductJSON: Represents a single product's data, including methods for fetching API data.
"""

from __future__ import annotations

import logging
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

    webhallen_id = models.PositiveBigIntegerField(unique=True, help_text="Webhallen product ID")
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
