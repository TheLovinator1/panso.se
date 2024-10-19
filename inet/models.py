from __future__ import annotations

import logging
from typing import Literal

from django.db import models

from utils.field_updater import update_fields

logger: logging.Logger = logging.getLogger(__name__)


class KeySpecification(models.Model):
    """Key specification model."""

    # Django fields
    id = models.PositiveBigIntegerField(primary_key=True, help_text="Key specification ID")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Created at")
    updated_at = models.DateTimeField(auto_now=True, help_text="Updated at")

    # Inet fields
    name = models.TextField(blank=False)
    value = models.TextField(blank=False)
    description = models.TextField(blank=True)
    is_key_text = models.BooleanField(null=False, help_text="Is key text")

    def __str__(self) -> str:
        return self.name

    def import_json(self, data: dict) -> models.Model:
        """Import JSON data.

        Args:
            data (dict): Data from the API to import.

        Returns:
            models.Model: The updated instance.
        """
        field_mapping: dict[str, str] = {
            "name": "name",
            "value": "value",
            "description": "description",
            "isKeyText": "is_key_text",
        }

        return update_fields(instance=self, data=data, field_mapping=field_mapping)


class Price(models.Model):
    """Price model."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="Created at")
    updated_at = models.DateTimeField(auto_now=True, help_text="Updated at")

    # Inet fields
    list_price_ex_vat = models.DecimalField(
        null=True,
        help_text="List price excluding VAT",
        decimal_places=2,
        max_digits=10,
    )
    list_price = models.PositiveBigIntegerField(null=True, help_text="List price")
    price_ex_vat = models.DecimalField(null=True, help_text="Price excluding VAT", decimal_places=2, max_digits=10)
    price = models.PositiveBigIntegerField(null=True, help_text="Price")

    def __str__(self) -> str:
        return str(self.price)

    def import_json(self, data: dict) -> models.Model:
        """Import JSON data.

        Args:
            data (dict): Data from the API to import.

        Returns:
            models.Model: The updated instance.
        """
        field_mapping: dict[str, str] = {
            "listPriceExVat": "list_price_ex_vat",
            "listPrice": "list_price",
            "priceExVat": "price_ex_vat",
            "price": "price",
        }

        return update_fields(instance=self, data=data, field_mapping=field_mapping)


class Qty(models.Model):
    """Qty model."""

    # Django fields
    store_id = models.PositiveBigIntegerField(primary_key=True, help_text="Store ID")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Created at")
    updated_at = models.DateTimeField(auto_now=True, help_text="Updated at")

    # Inet fields
    qty = models.PositiveBigIntegerField(null=True, help_text="Qty")
    blocked = models.BooleanField(null=True, help_text="Blocked")
    restock_days = models.PositiveBigIntegerField(null=True, help_text="Restock days")
    is_delayed = models.BooleanField(null=True, help_text="Is delayed")

    def __str__(self) -> int | Literal["0"]:
        return self.qty or "0"

    def import_json(self, data: dict) -> models.Model:
        """Import JSON data.

        Args:
            data (dict): Data from the API to import.

        Returns:
            models.Model: The updated instance.
        """
        field_mapping: dict[str, str] = {
            "qty": "qty",
            "blocked": "blocked",
            "restockDays": "restock_days",
            "isDelayed": "is_delayed",
        }

        return update_fields(instance=self, data=data, field_mapping=field_mapping)


class KeyText(models.Model):
    """Key text model."""

    # Django fields
    key_text = models.TextField(primary_key=True, help_text="Key text")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Created at")
    updated_at = models.DateTimeField(auto_now=True, help_text="Updated at")

    def __str__(self) -> str:
        return self.key_text


class Product(models.Model):
    """Product model."""

    # Django fields
    id = models.PositiveBigIntegerField(primary_key=True, help_text="Product ID")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Created at")
    updated_at = models.DateTimeField(auto_now=True, help_text="Updated at")

    # Inet fields
    active = models.BooleanField(null=False, help_text="Active")
    bargain_parent_id = models.PositiveBigIntegerField(null=True, help_text="Bargain parent ID")
    category_id = models.PositiveBigIntegerField(null=True, help_text="Category ID")
    freight_cost = models.DecimalField(null=True, help_text="Freight cost", decimal_places=2, max_digits=10)
    hidden = models.BooleanField(null=False, help_text="Hidden")
    hype_count = models.PositiveBigIntegerField(null=True, help_text="Hype count")
    hype_score = models.PositiveBigIntegerField(null=True, help_text="Hype score")
    image = models.TextField(blank=True, help_text="Image")
    is_assembly = models.BooleanField(null=False, help_text="Is assembly")
    is_bargain = models.BooleanField(null=False, help_text="Is bargain")
    is_consignment_product = models.BooleanField(null=False, help_text="Is consignment product")
    is_easy_build = models.BooleanField(null=False, help_text="Is easy build")
    is_monthly_subscription = models.BooleanField(null=False, help_text="Is monthly subscription")
    is_virtual = models.BooleanField(null=False, help_text="Is virtual")
    manufacturer_id = models.PositiveBigIntegerField(null=True, help_text="Manufacturer ID")
    name = models.TextField(blank=False)
    purchase_status = models.TextField(blank=True, help_text="Purchase status")
    qty_limit = models.PositiveBigIntegerField(null=True, help_text="Qty limit")
    release_date = models.DateField(null=True, help_text="Release date")
    review_count = models.PositiveBigIntegerField(null=True, help_text="Review count")
    review_score = models.DecimalField(null=True, help_text="Review score", decimal_places=2, max_digits=10)
    selling_point = models.TextField(blank=True, help_text="Selling point")
    template_id = models.PositiveBigIntegerField(null=True, help_text="Template ID")
    url_name = models.TextField(blank=True, help_text="URL name")
    vat = models.DecimalField(null=True, help_text="VAT", decimal_places=2, max_digits=10)

    # Relationships
    key_specifications = models.ManyToManyField(KeySpecification, help_text="Key specifications")
    key_text = models.ManyToManyField(KeyText, help_text="Key text")
    price = models.ForeignKey(Price, on_delete=models.CASCADE, help_text="Price")
    qty = models.ForeignKey(Qty, on_delete=models.CASCADE, help_text="Qty")

    def __str__(self) -> str:
        return self.name

    def import_json(self, data: dict) -> models.Model:
        """Import JSON data.

        Args:
            data (dict): Data from the API to import.

        Returns:
            models.Model: The updated instance.
        """
        field_mapping: dict[str, str] = {
            "active": "active",
            "bargainParentId": "bargain_parent_id",
            "categoryId": "category_id",
            "freightCost": "freight_cost",
            "hidden": "hidden",
            "hypeCount": "hype_count",
            "hypeScore": "hype_score",
            "image": "image",
            "isAssembly": "is_assembly",
            "isBargain": "is_bargain",
            "isConsignmentProduct": "is_consignment_product",
            "isEasyBuild": "is_easy_build",
            "isMonthlySubscription": "is_monthly_subscription",
            "isVirtual": "is_virtual",
            "manufacturerId": "manufacturer_id",
            "name": "name",
            "purchaseStatus": "purchase_status",
            "qtyLimit": "qty_limit",
            "releaseDate": "release_date",
            "reviewCount": "review_count",
            "reviewScore": "review_score",
            "sellingPoint": "selling_point",
            "templateId": "template_id",
            "urlName": "url_name",
            "vat": "vat",
            # "keySpecifications": "key_specifications",
            # "keyText": "key_text",
            # "price": "price",
            # "qty": "qty",
        }

        self.handle_key_specifications(data)
        self.handle_key_texts(data)
        self.handle_price(data)
        self.handle_qty(data)

        return update_fields(instance=self, data=data, field_mapping=field_mapping)

    def handle_key_specifications(self, data: dict) -> None:
        """Handle keySpecifications.

        Args:
            data (dict): Data from the API to import.
        """
        key_specifications_data = data.get("keySpecifications")
        if key_specifications_data:
            for key_specification in key_specifications_data:
                key_specification_instance, created = KeySpecification.objects.get_or_create(id=key_specification["id"])
                if created:
                    logger.info("Created new key specification %s for product %s", key_specification_instance, self)

                key_specification_instance.import_json(key_specification)
                self.key_specifications.add(key_specification_instance)

    def handle_qty(self, data: dict) -> None:
        """Handle qty.

        Args:
            data (dict): Data from the API to import.
        """
        qty_data = data.get("qty")
        if qty_data:
            qty_instance, created = Qty.objects.get_or_create(store_id=qty_data["id"])
            if created:
                logger.info("Created new qty %s for product %s", qty_instance, self)

            qty_instance.import_json(qty_data)
            self.qty = qty_instance

    def handle_price(self, data: dict) -> None:
        """Handle price.

        Args:
            data (dict): Data from the API to import.
        """
        price_data = data.get("price")
        if price_data:
            price_instance, created = Price.objects.get_or_create(id=price_data["id"])
            if created:
                logger.info("Created new price %s for product %s", price_instance, self)

            price_instance.import_json(price_data)
            self.price = price_instance

    def handle_key_texts(self, data: dict) -> None:
        """Handle keyText.

        Args:
            data (dict): Data from the API to import.
        """
        key_text_data = data.get("keyText")
        if key_text_data:
            for key_text in key_text_data:
                key_text_instance, created = KeyText.objects.get_or_create(key_text=key_text)
                if created:
                    logger.info("Created new key text %s for product %s", key_text_instance, self)

                self.key_text.add(key_text_instance)
