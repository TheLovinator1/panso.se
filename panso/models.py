import typing

from django.db import models


class WebhallenJSON(models.Model):
    """JSON scraped from the webhallen API."""

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, help_text="Flag to indicate if the JSON is still available for use.")

    product_id = models.IntegerField(help_text="The product id of the product.", unique=True, db_index=True)
    scraped_url = models.URLField(help_text="The URL from which the JSON was scraped.", unique=True)
    json = models.JSONField(help_text="The JSON data scraped from the webhallen API.", blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=[("success", "Success"), ("error", "Error")],
        default="success",
        help_text="Status of the scraping process",
    )
    error_message = models.TextField(
        blank=True,
        help_text="Error message if the scraping process encountered an issue",
        default="",
    )

    class Meta:
        verbose_name: str = "Webhallen JSON"
        verbose_name_plural: str = "Webhallen JSONs"
        get_latest_by: str = "created_at"
        ordering: typing.ClassVar[list] = ["-created_at"]
        constraints: typing.ClassVar[list] = [
            models.CheckConstraint(check=models.Q(product_id__gte=0), name="product_id_not_negative"),
            models.CheckConstraint(
                check=models.Q(scraped_url__startswith="https://www.webhallen.com/api/product/"),
                name="scraped_url_starts_with_https_www_webhallen_com_api_product_",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.product_id} - {self.scraped_url} - {self.created_at}"

    def delete(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003, ARG002
        self.is_active = False
        self.save()
