from __future__ import annotations

import logging

from django.db import models

logger: logging.Logger = logging.getLogger(__name__)


class Stock(models.Model):
    """How many products are in stock at each Webhallen store."""

    # TODO(TheLovinator): Get store names from Webhallen API  # noqa: TD003
    store_1 = models.PositiveBigIntegerField(help_text="Stock in store 1")
    store_2 = models.PositiveBigIntegerField(help_text="Stock in store 2")
    store_5 = models.PositiveBigIntegerField(help_text="Stock in store 5")
    store_9 = models.PositiveBigIntegerField(help_text="Stock in store 9")
    store_11 = models.PositiveBigIntegerField(help_text="Stock in store 11")
    store_14 = models.PositiveBigIntegerField(help_text="Stock in store 14")
    store_15 = models.PositiveBigIntegerField(help_text="Stock in store 15")
    store_16 = models.PositiveBigIntegerField(help_text="Stock in store 16")
    store_19 = models.PositiveBigIntegerField(help_text="Stock in store 19")
    store_20 = models.PositiveBigIntegerField(help_text="Stock in store 20")
    store_27 = models.PositiveBigIntegerField(help_text="Stock in store 27")
    store_32 = models.PositiveBigIntegerField(help_text="Stock in store 32")
    store_web = models.PositiveBigIntegerField(help_text="Stock in web store")
    supplier = models.PositiveBigIntegerField(help_text="Stock from supplier")
    display_cap = models.PositiveBigIntegerField(help_text="Display cap")
    is_sent_from_store = models.BooleanField(help_text="Is sent from store")

    class Meta:
        verbose_name: str = "Stock"
        verbose_name_plural: str = "Stock"

    def __str__(self) -> str:
        return f"Stock - {self.store_web} in web store"


class Price(models.Model):
    """The price of a product at Webhallen."""

    price = models.TextField(help_text="Price of the product")
    currency = models.TextField(help_text="The currency.")
    vat = models.PositiveBigIntegerField(help_text="Value-added tax")
    type = models.TextField()
    end_at = models.DateTimeField(help_text="End date")
    start_at = models.DateTimeField(help_text="Start date")
    sold_amount = models.PositiveBigIntegerField(help_text="Amount sold")
    nearly_over = models.BooleanField(help_text="Is nearly over")
    flash_sale = models.BooleanField(help_text="Is a flash sale")
    max_qty_per_customer = models.PositiveBigIntegerField(help_text="Maximum quantity per customer")

    def __str__(self) -> str:
        return f"{self.price} {self.currency}"


class Product(models.Model):
    """A product from Webhallen."""

    # 369004
    webhallen_id = models.PositiveBigIntegerField(primary_key=True, help_text="Webhallen product ID")

    # - variants

    # ASUS Dual GeForce RTX 4060 EVO 8GB OC
    name = models.TextField(help_text="Product name")

    # Current price? TODO: Check if this is the current price
    price = models.ForeignKey(
        Price,
        on_delete=models.CASCADE,
        help_text="The price of the product",
        related_name="current_price",
    )
    regular_price = models.ForeignKey(
        Price,
        on_delete=models.CASCADE,
        help_text="The regular price of the product",
        related_name="regular_price",
    )

    def __str__(self) -> str:
        return f"{self.name} ({self.webhallen_id})"
