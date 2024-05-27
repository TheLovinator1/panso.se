import typing

import auto_prefetch
from django.db import models


class WebhallenProduct(auto_prefetch.Model):
    """A product from Webhallen."""

    created_at = models.DateTimeField(auto_now_add=True, help_text="The date and time the product was created.")
    modified_at = models.DateTimeField(auto_now=True, help_text="The date and time the product was last modified.")
    last_scraped_json_at = models.DateTimeField(
        help_text="The date and time the product was last scraped from the webhallen API.",
        blank=True,
        null=True,
    )

    product_id = models.IntegerField(help_text="Product id", unique=True, db_index=True)
    name = models.TextField(help_text="Product name.", null=True, blank=True)
    url = models.URLField(help_text="The URL of the product.")

    last_exception = models.TextField(
        help_text="The last exception that occurred when scraping the product.",
        blank=True,
        null=True,
    )

    class Meta(auto_prefetch.Model.Meta):
        verbose_name: str = "Webhallen Product"
        verbose_name_plural: str = "Webhallen Products"
        get_latest_by: str = "created_at"
        ordering: typing.ClassVar[list[str]] = ["-created_at"]
        indexes: typing.ClassVar[list[models.Index]] = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["modified_at"]),
            models.Index(fields=["name"]),
        ]

    def __str__(self) -> str:
        return f"{self.product_id} - {self.name}"  # pragma: no cover


class WebhallenJSON(auto_prefetch.Model):
    """JSON scraped from the webhallen API."""

    created_at = models.DateTimeField(auto_now_add=True, help_text="The date and time the JSON was first scraped.")
    modified_at = models.DateTimeField(auto_now=True, help_text="The date and time the JSON was last modified.")

    product = auto_prefetch.ForeignKey(
        WebhallenProduct,
        on_delete=models.CASCADE,
        help_text="The product associated with the JSON.",
        related_name="jsons",
    )
    scraped_url = models.URLField(help_text="The URL from which the JSON was scraped.", unique=True)
    json = models.JSONField(help_text="The JSON data scraped from the webhallen API.", blank=True, null=True)

    class Meta(auto_prefetch.Model.Meta):
        verbose_name: str = "Webhallen JSON"
        verbose_name_plural: str = "Webhallen JSONs"
        get_latest_by: str = "-created_at"
        ordering: typing.ClassVar[list] = ["-created_at"]
        indexes: typing.ClassVar[list[models.Index]] = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["modified_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.product} - {self.scraped_url}"  # pragma: no cover
