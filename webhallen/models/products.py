from __future__ import annotations

import logging
from typing import TYPE_CHECKING, TypeVar

import auto_prefetch
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.core.files.base import ContentFile
from django.db import models
from pictures.models import PictureField

from utils.field_updater import update_fields

if TYPE_CHECKING:
    import httpx

logger: logging.Logger = logging.getLogger(__name__)

T = TypeVar("T")

# TODO(TheLovinator): All docstrings are placeholders and need to be updated  # noqa: TD003


def create_and_import_component(data: dict, component_name: str) -> Component | None:
    """Create and import a component.

    Args:
        data (dict): The data to import.
        component_name (str): The name of the component.

    Returns:
        Component: The created component.
    """
    component_data: dict = data.get(component_name, {})
    if not component_data:
        logger.warning("No component data found for %s", component_name)
        return None

    component, created = Component.objects.get_or_create(attribute_id=component_data.get("attributeId"))
    if created:
        logger.info("Created new component: %s", component)

    component.import_json(component_data)

    return component


class CanonicalVariant(auto_prefetch.Model):
    """Canonical variant."""

    # Django fields
    id = models.PositiveBigIntegerField(primary_key=True, help_text="Canonical variant ID")
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the canonical variant was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the canonical variant was last updated")

    # Webhallen fields
    name = models.TextField(help_text="Variant name")

    def __str__(self) -> str:
        return f"Canonical variant - {self.name}"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        field_mapping: dict[str, str] = {"name": "name"}
        update_fields(instance=self, data=data, field_mapping=field_mapping)


class AverageRating(auto_prefetch.Model):
    """Average rating."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the average rating was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the average rating was last updated")

    # Webhallen fields
    rating = models.FloatField(help_text="Rating")
    rating_type = models.TextField(help_text="Rating type")

    def __str__(self) -> str:
        return f"Average rating - {self.rating} ({self.rating_type})"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        field_mapping: dict[str, str] = {
            "rating": "rating",
            "ratingType": "rating_type",
        }
        update_fields(instance=self, data=data, field_mapping=field_mapping)


class Categories(auto_prefetch.Model):
    """Categories."""

    # Django fields
    id = models.PositiveBigIntegerField(primary_key=True, help_text="Category ID")
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the category was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the category was last updated")

    # Webhallen fields
    active = models.BooleanField(help_text="Is active")
    fyndware_description = models.TextField(help_text="Fyndware description")
    icon = models.TextField(help_text="Icon")
    meta_title = models.TextField(help_text="Meta title")
    name = models.TextField(help_text="Name")
    order = models.PositiveBigIntegerField(help_text="Order")
    seo_name = models.TextField(help_text="SEO name")

    def __str__(self) -> str:
        return f"Category - {self.name}"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        field_mapping: dict[str, str] = {
            "active": "active",
            "fyndwareDescription": "fyndware_description",
            "icon": "icon",
            "metaTitle": "meta_title",
            "name": "name",
            "order": "order",
            "seoName": "seo_name",
        }
        update_fields(instance=self, data=data, field_mapping=field_mapping)


class VariantProperties(auto_prefetch.Model):
    """Properties of a variant.

    Example:
    {
        "product": {
            "variants": {
                "list": {
                    "variantProperties": {
                        "Färg": "Svart",
                        "Lagring": "64 GB",
                        "Anslutning": "Wi-Fi"
                    }
                }
            }
        }
    }
    """

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the variant properties were created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the variant properties were last updated")

    # Webhallen fields
    color = models.TextField(help_text="Variant color")
    connections = models.TextField(help_text="Variant connections")
    storage = models.TextField(help_text="Variant storage")

    def __str__(self) -> str:
        return f"Variant properties - {self.color}, {self.storage}, {self.connections}"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        field_mapping: dict[str, str] = {
            "Färg": "color",
            "Anslutning": "connections",
            "Lagring": "storage",
        }
        update_fields(instance=self, data=data, field_mapping=field_mapping)


class VariantGroups(auto_prefetch.Model):
    """Groups of variants."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the variant groups were created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the variant groups were last updated")

    # Webhallen fields
    name = models.TextField(help_text="Name")
    type = models.TextField(help_text="Type")
    values = ArrayField(models.TextField(), help_text="Values")

    def __str__(self) -> str:
        return f"Variant group - {self.name}"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        field_mapping: dict[str, str] = {
            "name": "name",
            "type": "type",
            "values": "values",
        }
        update_fields(instance=self, data=data, field_mapping=field_mapping)


class ListClass(auto_prefetch.Model):
    """List class."""

    # TODO(TheLovinator): Should this be a Product?  # noqa: TD003

    # Django fields
    id = models.PositiveBigIntegerField(primary_key=True, help_text="List ID")
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the list was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the list was last updated")

    # Webhallen fields
    discontinued = models.BooleanField(help_text="Is discontinued")
    is_fyndware = models.BooleanField(help_text="Is Fyndware")
    name = models.TextField(help_text="Name")
    variant_name = models.TextField(help_text="Variant name")

    # Relationships
    energy_marking = models.ForeignKey(
        "EnergyMarking",
        on_delete=models.CASCADE,
        help_text="Energy marking",
        related_name="list_classes",
    )
    lowest_price = models.ForeignKey(
        "Price",
        on_delete=models.CASCADE,
        help_text="Lowest price",
        related_name="list_classes_lowest_price",
    )
    price = models.ForeignKey(
        "Price",
        on_delete=models.CASCADE,
        help_text="Price",
        related_name="list_classes_price",
    )
    regular_price = models.ForeignKey(
        "Price",
        on_delete=models.CASCADE,
        help_text="Regular price",
        related_name="list_classes_regular_price",
    )
    release = models.ForeignKey(
        "Release",
        on_delete=models.CASCADE,
        help_text="Release",
        related_name="list_classes_release",
    )
    stock = models.ForeignKey(
        "Stock",
        on_delete=models.CASCADE,
        help_text="Stock",
        related_name="list_classes_stock",
    )
    variant_properties = models.ForeignKey(
        "VariantProperties",
        on_delete=models.CASCADE,
        help_text="Variant properties",
        related_name="list_classes_variant_properties",
    )

    def __str__(self) -> str:
        return f"List class - {self.name}"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        field_mapping: dict[str, str] = {
            "discontinued": "discontinued",
            "isFyndware": "is_fyndware",
            "name": "name",
            "variantName": "variant_name",
            # "energyMarking": "energy_marking",
            # "lowestPrice": "lowest_price",
            # "price": "price",
            # "regularPrice": "regular_price",
            # "release": "release",
            # "stock": "stock",
            # "variantProperties": "variant_properties",
        }
        update_fields(instance=self, data=data, field_mapping=field_mapping)

        # Handle relationships separately as they are nested.
        energy_marking_data = data.get("energyMarking", {})
        energy_marking, _ = EnergyMarking.objects.get_or_create(
            id=energy_marking_data.get("id"),
            defaults=energy_marking_data,
        )
        self.energy_marking = energy_marking

        self.import_lowest_price(data)
        self.import_price_data(data)
        self.import_regular_price(data)
        self.import_release_data(data)
        self.import_stock_data(data)
        self.import_variant_properties(data)

    def import_variant_properties(self, data: dict) -> None:
        """Import variant properties data."""
        variant_properties_data = data.get("variantProperties", {})
        variant_properties, created = VariantProperties.objects.get_or_create(
            color=variant_properties_data.get("Färg"),
            connections=variant_properties_data.get("Anslutning"),
            storage=variant_properties_data.get("Lagring"),
        )
        if created:
            logger.info("Created new variant properties: %s", variant_properties)

        variant_properties.import_json(variant_properties_data)
        self.variant_properties = variant_properties

    def import_stock_data(self, data: dict) -> None:
        """Import stock data."""
        stock_data: dict = data.get("stock", {})
        stock, created = Stock.objects.get_or_create(id=stock_data.get("id"))
        if created:
            logger.info("Created new stock: %s", stock)

        stock.import_json(stock_data)
        self.stock = stock

    def import_release_data(self, data: dict) -> None:
        """Import release data."""
        release_data: dict = data.get("release", {})
        release, created = Release.objects.get_or_create(id=release_data.get("id"))
        if created:
            logger.info("Created new release: %s", release)

        release.import_json(release_data)
        self.release = release

    def import_regular_price(self, data: dict) -> None:
        """Import regular price data."""
        regular_price_data: dict = data.get("regularPrice", {})
        regular_price, created = Price.objects.get_or_create(id=regular_price_data.get("id"))
        if created:
            logger.info("Created new regular price: %s", regular_price)

        regular_price.import_json(regular_price_data)
        self.regular_price = regular_price

    def import_price_data(self, data: dict) -> None:
        """Import price data."""
        price_data: dict = data.get("price", {})
        price, created = Price.objects.get_or_create(id=price_data.get("id"))
        if created:
            logger.info("Created new price: %s", price)

        price.import_json(price_data)
        self.price = price

    def import_lowest_price(self, data: dict) -> None:
        """Import lowest price data."""
        lowest_price_data: dict = data.get("lowestPrice", {})
        lowest_price, created = Price.objects.get_or_create(id=lowest_price_data.get("id"))
        if created:
            logger.info("Created new lowest price: %s", lowest_price)

        lowest_price.import_json(lowest_price_data)
        self.lowest_price = lowest_price


class Variants(auto_prefetch.Model):
    """Variants.

    Example:
        {
        "variants": {
            "canonicalVariant": {
                "id": 181686,
                "name": "Settlers från Catan 5-6 spelare Expansion (Sv)"
            },
            "list": {
                "id": 6332,
                "variantProperties": {
                    "Färg": "Svart",
                    "Lagring": "64 GB",
                    "Anslutning": "Wi-Fi"
                },
                "name": "Settlers från Catan - Sjöfarare Expansion (Sv)",
                "price": {
                    "price": "365.00",
                    "currency": "SEK",
                    "vat": 73,
                    "type": "campaign",
                    "endAt": "2025-01-04T20:06:52",
                    "startAt": "2023-05-26T09:28:45",
                    "soldAmount": null,
                    "maxAmountForPrice": null,
                    "amountLeft": 4906,
                    "nearlyOver": false,
                    "flashSale": false,
                    "maxQtyPerCustomer": 2
                },
                "stock": {
                    "web": 0,
                    "supplier": 0,
                    "displayCap": "50",
                    "1": 0,
                    "2": 0,
                    "5": 0,
                    "9": 0,
                    "11": 0,
                    "14": 0,
                    "15": 0,
                    "16": 0,
                    "19": 0,
                    "20": 0,
                    "27": 0,
                    "32": 0,
                    "isSentFromStore": 0,
                    "orders": {
                        "27": {
                            "amount": -10,
                            "days_since": "0"
                        },
                        "CL": {
                            "ordered": 51,
                            "status": 2,
                            "delivery_time": [
                                5
                            ],
                            "confirmed": true
                        },
                        "2": {
                            "amount": -10,
                            "days_since": "0"
                        },
                        "16": {
                            "amount": -10,
                            "days_since": "0"
                        }
                    }
                },
                "release": {
                    "timestamp": 997588800,
                    "format": "Y-m-d"
                },
                "isFyndware": false,
                "variantName": "Sjöfarare Expansion (Sv)",
                "discontinued": true,
                "regularPrice": {
                    "price": "365.00",
                    "currency": "SEK",
                    "vat": 73,
                    "type": null,
                    "endAt": "2025-01-04T19:23:15",
                    "startAt": "2023-05-26T09:28:45",
                    "soldAmount": null,
                    "maxAmountForPrice": null,
                    "amountLeft": null,
                    "nearlyOver": false,
                    "flashSale": false,
                    "maxQtyPerCustomer": null
                },
                "energyMarking": {
                    "rating": "G",
                    "scale": "A+",
                    "labelContent": null,
                    "productSheetContent": "-",
                    "labelImageUrl": "https://www.webhallen.com/images/669512-asus-rog-swift-pg27aqdm-265-oled-bildskarm-fo?raw",
                    "manufacturer": "Philips Lighting",
                    "itemCode": "915005630901"
                },
                "lowestPrice": {
                    "price": "199.00",
                    "currency": "SEK",
                    "vat": 39.8,
                    "type": "campaign",
                    "endAt": "2023-10-08T23:59:00",
                    "startAt": "2023-09-18T08:00:00",
                    "soldAmount": null,
                    "maxAmountForPrice": null,
                    "amountLeft": 0,
                    "nearlyOver": true,
                    "flashSale": false,
                    "maxQtyPerCustomer": 2
                }
            },
            "group": "1447",
            "variantGroups": {
                "name": "Färg",
                "type": "color",
                "values": [
                    "64gb",
                    "256gb"
                ]
            }
        }
    }
    """

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the variant was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the variant was last updated")

    # Webhallen fields
    canonical_variant = models.ForeignKey(CanonicalVariant, on_delete=models.CASCADE, help_text="Canonical variant")
    list = models.ForeignKey(ListClass, on_delete=models.CASCADE, help_text="List")
    group = models.PositiveBigIntegerField(help_text="Group")
    variant_groups = models.ForeignKey(VariantGroups, on_delete=models.CASCADE, help_text="Variant groups")

    def __str__(self) -> str:
        return f"Variant - {self.canonical_variant}"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        field_mapping: dict[str, str] = {
            # "canonicalVariant": "canonical_variant",
            # "list": "list",
            "group": "group",
            # "variantGroups": "variant_groups",
        }
        update_fields(instance=self, data=data, field_mapping=field_mapping)

        # canonicalVariant
        canonical_variant_data = data.get("canonicalVariant", {})
        canonical_variant, created = CanonicalVariant.objects.get_or_create(id=canonical_variant_data.get("id"))
        if created:
            logger.info("Created new canonical variant: %s", canonical_variant)
        canonical_variant.import_json(canonical_variant_data)
        self.canonical_variant = canonical_variant

        # variantGroups
        variant_groups = data.get("variantGroups", {})
        for variant_group_data in variant_groups:
            variant_group, created = VariantGroups.objects.get_or_create(id=variant_group_data.get("id"))
            if created:
                logger.info("Created new variant group: %s", variant_group)
            self.variant_groups = variant_group

        # ListClass
        list_data = data.get("list", {})
        list_class, created = ListClass.objects.get_or_create(id=list_data.get("id"))
        if created:
            logger.info("Created new list class: %s", list_class)
        list_class.import_json(list_data)
        self.list = list_class


class Order(auto_prefetch.Model):
    """Order details for each stock item.

    Example:
    {
        "product": {
            "stock": {
                "orders": {
                    "CL": {
                        "status": -1,
                        "ordered": 51,
                        "delivery_time": [
                            "2024-10-13"
                        ],
                        "confirmed": true
                    },
                    "27": {
                        "amount": -10,
                        "days_since": "0"
                    },
                    "16": {
                        "amount": -10,
                        "days_since": "0"
                    },
                    "5": {
                        "amount": -10,
                        "days_since": "0"
                    },
                    "2": {
                        "amount": -10,
                        "days_since": "0"
                    }
                }
            }
        }
    }
    """

    # Django fields
    stock = models.ForeignKey("Stock", on_delete=models.CASCADE, help_text="Stock", related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the order was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the order was last updated")

    # Webhallen fields
    # TODO(TheLovinator): Get store names from Webhallen API  # noqa: TD003
    # TODO(TheLovinator): Convert to choices  # noqa: TD003
    store = models.TextField(help_text="Store ID")  # CL, 27, 16, 5 or 2.
    amount = models.IntegerField(help_text="Amount of stock change (negative for reduction)")
    days_since = models.PositiveBigIntegerField(help_text="Days since the order was placed")
    status = models.IntegerField(null=True, blank=True, help_text="Order status (only for CL orders)")
    ordered = models.PositiveIntegerField(null=True, blank=True, help_text="Ordered quantity (only for CL orders)")
    confirmed = models.BooleanField(default=False, help_text="Order confirmation status (only for CL orders)")
    delivery_time = models.DateField(null=True, blank=True, help_text="Expected delivery date (only for CL orders)")

    def __str__(self) -> str:
        return f"Order - {self.store}, Amount: {self.amount}"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        field_mapping: dict[str, str] = {
            "store": "store",
            "amount": "amount",
            "days_since": "days_since",
            "status": "status",
            "ordered": "ordered",
            "confirmed": "confirmed",
            "delivery_time": "delivery_time",
        }
        update_fields(instance=self, data=data, field_mapping=field_mapping)


class Stock(auto_prefetch.Model):
    """How many products are in stock at each Webhallen store.

    Example:
    {
        "product": {
            "stock": {
                "web": 0,
                "supplier": 0,
                "displayCap": "50",
                "1": 0,
                "2": 0,
                "5": 0,
                "9": 0,
                "11": 0,
                "14": 0,
                "15": 0,
                "16": 0,
                "19": 0,
                "20": 0,
                "27": 0,
                "32": 0,
                "isSentFromStore": 0,
                "orders": {
                    "27": {
                        "amount": -10,
                        "days_since": "0"
                    },
                    "CL": {
                        "ordered": 51,
                        "status": 2,
                        "delivery_time": [
                            5
                        ],
                        "confirmed": true
                    },
                    "2": {
                        "amount": -10,
                        "days_since": "0"
                    },
                    "16": {
                        "amount": -10,
                        "days_since": "0"
                    }
                }
            }
        }
    }
    """

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the stock was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the stock was last updated")

    # Webhallen fields
    # TODO(TheLovinator): Get store names from Webhallen API  # noqa: TD003
    display_cap = models.PositiveBigIntegerField(help_text="Display cap")
    download = models.PositiveBigIntegerField(help_text="Download amount")
    is_sent_from_store = models.BooleanField(help_text="Is sent from store")
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
    supplier = models.PositiveBigIntegerField(help_text="Stock from supplier")
    web = models.PositiveBigIntegerField(help_text="Stock in web store")

    class Meta(auto_prefetch.Model.Meta):
        verbose_name: str = "Stock"
        verbose_name_plural: str = "Stock"

    def __str__(self) -> str:
        return f"Stock - {self.web} in web store"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        field_mapping: dict[str, str] = {
            "1": "store_1",
            "2": "store_2",
            "5": "store_5",
            "9": "store_9",
            "11": "store_11",
            "14": "store_14",
            "15": "store_15",
            "16": "store_16",
            "19": "store_19",
            "20": "store_20",
            "27": "store_27",
            "32": "store_32",
            "web": "web",
            "supplier": "supplier",
            "displayCap": "display_cap",
            "isSentFromStore": "is_sent_from_store",
            "download": "download",
            # "orders": "orders",
        }
        update_fields(instance=self, data=data, field_mapping=field_mapping)


class Price(auto_prefetch.Model):
    """The price at Webhallen."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the price was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the price was last updated")

    # Webhallen fields
    price = models.TextField(blank=True, help_text="Price of the product")
    currency = models.TextField(blank=True, help_text="The currency.")
    vat = models.FloatField(null=True, help_text="VAT")
    type = models.TextField(blank=True)
    end_at = models.DateTimeField(null=True, help_text="End date")
    start_at = models.DateTimeField(null=True, help_text="Start date")
    amount_left = models.PositiveBigIntegerField(null=True, help_text="Amount left")
    nearly_over = models.BooleanField(null=True, help_text="Is nearly over")
    flash_sale = models.BooleanField(null=True, help_text="Is a flash sale")
    max_qty_per_customer = models.PositiveBigIntegerField(null=True, help_text="Maximum quantity per customer")

    # TODO(TheLovinator): Is fields below correct?  # noqa: TD003
    max_amount_for_price = models.PositiveBigIntegerField(null=True, help_text="Maximum amount for price")
    sold_amount = models.PositiveBigIntegerField(null=True, help_text="Amount sold")

    def __str__(self) -> str:
        return f"{self.price} {self.currency}"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        field_mapping: dict[str, str] = {
            "price": "price",
            "currency": "currency",
            "vat": "vat",
            "type": "type",
            "endAt": "end_at",
            "startAt": "start_at",
            "amountLeft": "amount_left",
            "nearlyOver": "nearly_over",
            "flashSale": "flash_sale",
            "maxQtyPerCustomer": "max_qty_per_customer",
            "maxAmountForPrice": "max_amount_for_price",
            "soldAmount": "sold_amount",
        }
        update_fields(instance=self, data=data, field_mapping=field_mapping)


class Image(auto_prefetch.Model):
    """An image from Webhallen.

    Each product has zoom, large and thumb but it is the same URL but with different arguments.
    """

    # Django fields
    product_id = models.PositiveBigIntegerField(primary_key=True, help_text="Product ID")
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the image was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the image was last updated")

    # Webhallen fields
    url = models.URLField(blank=True, help_text="Image URL")
    image = PictureField(upload_to="images/webhallen/product/", help_text="Product image")

    def __str__(self) -> str:
        return f"Image - {self.image}"

    def download_image(self) -> None:
        """Download the image from the URL."""
        if not self.image:
            client: httpx.Client = settings.HISHEL_CLIENT
            response: httpx.Response = client.get(url=self.url, timeout=30)
            self.image.save(
                f"product_{self.product_id}.jpg",
                ContentFile(response.content),
            )

    def import_json(self, data: dict) -> None:
        """Import JSON data.

        Example:
        "images": {
            "zoom": "/images/product/6332?trim&w=1400",
            "large": "/images/product/6332?trim",
            "thumb": "/images/product/6332?trim&h=80"
        },
        """
        image_url: str = data.get("large", "")
        if image_url != self.url:
            self.url = f"https://www.webhallen.com{image_url}"
            self.save()


class Release(auto_prefetch.Model):
    """Release details."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the release was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the release was last updated")

    # Webhallen fields
    timestamp = models.DateTimeField(help_text="Timestamp")
    format = models.TextField(help_text="Format")

    def __str__(self) -> str:
        return f"Release - {self.timestamp}"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        field_mapping: dict[str, str] = {
            "timestamp": "timestamp",
            "format": "format",
        }
        update_fields(instance=self, data=data, field_mapping=field_mapping)


class Section(auto_prefetch.Model):
    """A section."""

    # Django fields
    # 7
    id = models.PositiveBigIntegerField(primary_key=True, help_text="Section ID")
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the section was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the section was last updated")

    # Webhallen fields

    # "Vi har LEGO, drönare, roligt merchandise och mycket mer"
    meta_title = models.TextField(help_text="Meta title")

    # true
    active = models.BooleanField(help_text="Is active")

    # "lek_gadgets"
    icon = models.TextField(help_text="Icon")

    # "Leksaker & Hobby"
    name = models.TextField(help_text="Name")

    def __str__(self) -> str:
        return f"Section - {self.name}"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        field_mapping: dict[str, str] = {
            "metaTitle": "meta_title",
            "active": "active",
            "icon": "icon",
            "name": "name",
        }
        update_fields(instance=self, data=data, field_mapping=field_mapping)


class MainCategoryPath(auto_prefetch.Model):
    """The main category path."""

    # Django fields
    # 3600
    id = models.PositiveBigIntegerField(primary_key=True, help_text="Main category path ID")
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the main category path was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the main category path was last updated")

    # Webhallen fields
    fyndware_description = models.TextField(help_text="Fyndware description")  # ""
    meta_title = models.TextField(help_text="Meta title")  # "Brädspel - Roliga spel för barn, vuxna & vänner!"
    seo_name = models.TextField(help_text="SEO name")  # "Sällskapsspel"
    active = models.BooleanField(help_text="Is active")  # true
    order = models.PositiveBigIntegerField(help_text="Order")  # 2
    icon = models.TextField(help_text="Icon")  # "bradspel"
    name = models.TextField(help_text="Name")  # "Brädspel"
    has_products = models.BooleanField(help_text="Has products")  # true
    index = models.PositiveBigIntegerField(help_text="Index")  # 0
    url_name = models.TextField(help_text="URL name")  # "pc"

    def __str__(self) -> str:
        return f"Main category path - {self.name}"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        field_mapping: dict[str, str] = {
            "fyndwareDescription": "fyndware_description",
            "metaTitle": "meta_title",
            "seoName": "seo_name",
            "active": "active",
            "order": "order",
            "icon": "icon",
            "name": "name",
            "hasProducts": "has_products",
            "index": "index",
            "url_name": "url_name",
        }
        update_fields(instance=self, data=data, field_mapping=field_mapping)


class Parts(auto_prefetch.Model):
    """Parts."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the part was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the part was last updated")

    # Webhallen fields
    comb = models.TextField(help_text="Value and unit")  # "Hona"

    # TODO(TheLovinator): What is this?  # noqa: TD003
    nnv = models.TextField(help_text="Numeric value. Int or float if value is number")  # null
    text_value = models.TextField(help_text="Text value. A string if value is number")  # "Hona"
    unit = models.TextField(help_text="Unit. Only if unit for value is given")  # ""
    value = models.TextField(help_text="Value")  # "Hona"

    def __str__(self) -> str:
        return f"Part - {self.value}"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        field_mapping: dict[str, str] = {
            "comb": "comb",
            "nnv": "nnv",
            "textValue": "text_value",
            "unit": "unit",
            "value": "value",
        }
        update_fields(instance=self, data=data, field_mapping=field_mapping)


class Component(auto_prefetch.Model):
    """Information under the Data field."""

    # Django fields
    # 246
    attribute_id = models.PositiveBigIntegerField(primary_key=True, help_text="Attribute ID")
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the component was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the component was last updated")

    # Webhallen fields
    name = models.TextField(help_text="Name")  # "Typ av I/O-kabel"
    value = models.TextField(help_text="Value")  # "Strömkabel"

    # Relationships
    part = models.ForeignKey(Parts, on_delete=models.CASCADE, help_text="Part", related_name="components")

    def __str__(self) -> str:
        return f"Component - {self.name}"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        field_mapping: dict[str, str] = {
            "name": "name",
            "value": "value",
        }
        update_fields(instance=self, data=data, field_mapping=field_mapping)

        parts = data.get("parts", {})
        part, created = Parts.objects.get_or_create(
            comb=parts.get("comb"),
            nnv=parts.get("nnv"),
            text_value=parts.get("text_value"),
            unit=parts.get("unit"),
            value=parts.get("value"),
        )
        if created:
            logger.info("Created new part: %s", part)
        self.part = part


class Header(auto_prefetch.Model):
    """Header.

    Note: All the field names are translated from Swedish to English.
    """

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the header was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the header was last updated")

    # Webhallen fields
    packaged_quantity = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Packaged quantity",
        related_name="products_packaged_quantity",
    )
    brand = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Brand",
        related_name="products_brand",
    )
    product_line = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        related_name="products_product_line",
    )
    manufacturer = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Manufacturer",
        related_name="products_manufacturer",
    )
    model = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Model",
        related_name="products_model",
    )
    compatibility = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Compatibility",
        related_name="products_compatibility",
    )
    country_specific_batches = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Country-specific batches",
        related_name="products_country_specific_batches",
    )
    localization = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Localization",
        related_name="products_localization",
    )
    game_publisher = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Game publisher",
        related_name="products_game_publisher",
    )
    game_developer = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Game developer",
        related_name="products_game_developer",
    )
    edition = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Edition",
        related_name="products_edition",
    )
    batch = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Batch",
        related_name="products_batch",
    )
    manufacturer_model_number = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Manufacturer's model number",
        related_name="products_manufacturer_model_number",
    )
    release_date = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Release date",
        related_name="products_release_date",
    )
    series = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Series",
        related_name="products_series",
    )

    def __str__(self) -> str:
        return "Header"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Förpackad kvantitet
        packaged_quantity: Component | None = create_and_import_component(data, "Förpackad kvantitet")
        self.packaged_quantity = packaged_quantity

        # Märke
        brand: Component | None = create_and_import_component(data, "Märke")
        self.brand = brand

        # Produktlinje
        product_line: Component | None = create_and_import_component(data, "Produktlinje")
        self.product_line = product_line

        # Tillverkare
        manufacturer: Component | None = create_and_import_component(data, "Tillverkare")
        self.manufacturer = manufacturer

        # Modell
        model: Component | None = create_and_import_component(data, "Modell")
        self.model = model

        # Kompatibilitet
        compatibility: Component | None = create_and_import_component(data, "Kompatibilitet")
        self.compatibility = compatibility

        # Landsspecifika satser
        country_specific_batches: Component | None = create_and_import_component(data, "Landsspecifika satser")
        self.country_specific_batches = country_specific_batches

        # Lokalisering
        localization: Component | None = create_and_import_component(data, "Lokalisering")
        self.localization = localization

        # Spelutgivare
        game_publisher: Component | None = create_and_import_component(data, "Spelutgivare")
        self.game_publisher = game_publisher

        # Spelutvecklare
        game_developer: Component | None = create_and_import_component(data, "Spelutvecklare")
        self.game_developer = game_developer

        # Utgåva
        edition: Component | None = create_and_import_component(data, "Utgåva")
        self.edition = edition

        # Sats
        batch: Component | None = create_and_import_component(data, "Sats")
        self.batch = batch

        # Tillverkarens modellnummer
        manufacturer_model_number: Component | None = create_and_import_component(data, "Tillverkarens modellnummer")
        self.manufacturer_model_number = manufacturer_model_number

        # Utgivningsdatum
        release_date: Component | None = create_and_import_component(data, "Utgivningsdatum")
        self.release_date = release_date

        # Serie
        series: Component | None = create_and_import_component(data, "Serie")
        self.series = series


class DimensionsAndWeight(auto_prefetch.Model):
    """Mått och vikt.

    Note: All the field names are translated from Swedish to English.
    """

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the dimensions and weight were created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the dimensions and weight were last updated")

    # Webhallen fields
    weight = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Weight",
        related_name="dimensions_weight",
    )
    length = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Length",
        related_name="dimensions_length",
    )
    width = models.ForeignKey(Component, on_delete=models.CASCADE, help_text="Width", related_name="dimensions_width")
    height = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Height",
        related_name="dimensions_height",
    )
    length_in_meters = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Length in meters",
        related_name="dimensions_length_in_meters",
    )
    diameter = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Diameter",
        related_name="dimensions_diameter",
    )
    comments = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Comments",
        related_name="dimensions_comments",
    )
    thickness = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Thickness",
        related_name="dimensions_thickness",
    )
    volume = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Volume",
        related_name="dimensions_volume",
    )
    comment = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Comment",
        related_name="dimensions_comment",
    )
    min_height = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Minimum height",
        related_name="dimensions_min_height",
    )
    backrest_height = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Backrest height",
        related_name="dimensions_backrest_height",
    )
    backrest_width = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Backrest width",
        related_name="dimensions_backrest_width",
    )
    max_length = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Maximum length",
        related_name="dimensions_max_length",
    )

    def __str__(self) -> str:
        return "Dimensions and weight"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Vikt
        weight: Component | None = create_and_import_component(data, "Vikt")
        self.weight = weight

        # Längd
        length: Component | None = create_and_import_component(data, "Längd")
        self.length = length

        # Bredd
        width: Component | None = create_and_import_component(data, "Bredd")
        self.width = width

        # Höjd
        height: Component | None = create_and_import_component(data, "Höjd")
        self.height = height

        # Längd i meter
        length_in_meters: Component | None = create_and_import_component(data, "Längd i meter")
        self.length_in_meters = length_in_meters

        # Diameter
        diameter: Component | None = create_and_import_component(data, "Diameter")
        self.diameter = diameter

        # Kommentarer
        comments: Component | None = create_and_import_component(data, "Kommentarer")
        self.comments = comments

        # Grovlek
        thickness: Component | None = create_and_import_component(data, "Grovlek")
        self.thickness = thickness

        # Volym
        volume: Component | None = create_and_import_component(data, "Volym")
        self.volume = volume

        # Kommentar
        comment: Component | None = create_and_import_component(data, "Kommentar")
        self.comment = comment

        # Min. höjd
        min_height: Component | None = create_and_import_component(data, "Min. höjd")
        self.min_height = min_height

        # Ryggstödshöjd
        backrest_height: Component | None = create_and_import_component(data, "Ryggstödshöjd")
        self.backrest_height = backrest_height

        # Ryggstödsbredd
        backrest_width: Component | None = create_and_import_component(data, "Ryggstödsbredd")
        self.backrest_width = backrest_width

        # Max längd
        max_length: Component | None = create_and_import_component(data, "Max längd")
        self.max_length = max_length


class General(auto_prefetch.Model):
    """Allmänt."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the general information was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the general information was last updated")

    # Webhallen fields
    product_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Product type",
        related_name="products_product_type",
    )
    accessory_category = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Accessory category",
        related_name="products_accessory_category",
    )
    consumable_subcategory = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Consumable subcategory",
        related_name="products_consumable_subcategory",
    )
    technology = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Technology",
        related_name="products_technology",
    )
    printer_consumables_class = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Printer consumables class",
        related_name="products_printer_consumables_class",
    )
    subcategory = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Subcategory",
        related_name="products_subcategory",
    )
    category = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Category",
        related_name="products_category",
    )
    installation_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Installation type",
        related_name="products_installation_type",
    )
    designed_for = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Designed for",
        related_name="products_designed_for",
    )
    environment = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Environment",
        related_name="products_environment",
    )
    number_of_set_parts = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Number of set parts",
        related_name="products_number_of_set_parts",
    )
    suitable_for = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Suitable for",
        related_name="products_suitable_for",
    )
    features = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Features",
        related_name="products_features",
    )
    learning = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Learning",
        related_name="products_learning",
    )
    min_age = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Minimum age",
        related_name="products_min_age",
    )
    max_age = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Maximum age",
        related_name="products_max_age",
    )
    one_board_computer_included = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="One board computer included",
        related_name="products_one_board_computer_included",
    )
    waterproof = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Waterproof",
        related_name="products_waterproof",
    )
    dimmer = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Dimmer",
        related_name="products_dimmer",
    )
    cable_length = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Cable length",
        related_name="products_cable_length",
    )
    supported_wattage_for_light_bulb = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Supported wattage for light bulb",
        related_name="products_supported_wattage_for_light_bulb",
    )
    number_of_installed_light_bulbs = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Number of installed light bulbs",
        related_name="products_number_of_installed_light_bulbs",
    )
    number_of_supported_light_bulbs = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Number of supported light bulbs",
        related_name="products_number_of_supported_light_bulbs",
    )
    battery_included = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Battery included",
        related_name="products_battery_included",
    )
    switch_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Switch type",
        related_name="products_switch_type",
    )
    switch_location = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Switch location",
        related_name="products_switch_location",
    )
    clamp_mount = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Clamp mount",
        related_name="products_clamp_mount",
    )
    tool_set_parts = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Tool set parts",
        related_name="products_tool_set_parts",
    )
    socket = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Socket",
        related_name="products_socket",
    )
    socket_size = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Socket size",
        related_name="products_socket_size",
    )
    tip = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Tip",
        related_name="products_tip",
    )
    tip_size = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Tip size",
        related_name="products_tip_size",
    )
    size = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Size",
        related_name="products_size",
    )
    shape = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Shape",
        related_name="products_shape",
    )
    tracking_data = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Tracking data",
        related_name="products_tracking_data",
    )
    solution = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Solution",
        related_name="products_solution",
    )
    character_theme = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Character theme",
        related_name="products_character_theme",
    )
    AC_adapter_included = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="AC adapter included",
        related_name="products_AC_adapter_included",
    )
    style = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Style",
        related_name="products_style",
    )
    recommended_for = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Recommended for",
        related_name="products_recommended_for",
    )
    recommended_use = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Recommended use",
        related_name="products_recommended_use",
    )
    connection = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Connection",
        related_name="products_connection",
    )
    type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Type",
        related_name="products_type",
    )
    total_length = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Total length",
        related_name="products_total_length",
    )
    payment_technology = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Payment technology",
        related_name="products_payment_technology",
    )
    mechanism = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Mechanism",
        related_name="products_mechanism",
    )
    tilt_lock = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Tilt lock",
        related_name="products_tilt_lock",
    )
    headrest = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Headrest",
        related_name="products_headrest",
    )
    armrest = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Armrest",
        related_name="products_armrest",
    )
    tilt = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Tilt",
        related_name="products_tilt",
    )
    ergonomic = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Ergonomic",
        related_name="products_ergonomic",
    )
    tilt_tension_adjustment = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Tilt tension adjustment",
        related_name="products_tilt_tension_adjustment",
    )
    _class = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Class",
        related_name="products_class",
    )
    kit_contents = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Kit contents",
        related_name="products_kit_contents",
    )
    media_subcategory = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Media subcategory",
        related_name="products_media_subcategory",
    )
    indoor_outdoor = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Indoor/outdoor",
        related_name="products_indoor_outdoor",
    )
    thermometer_scale = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Thermometer scale",
        related_name="products_thermometer_scale",
    )
    usage_modes = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Usage modes",
        related_name="products_usage_modes",
    )
    car_power_adapter_included = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Car power adapter included",
        related_name="products_car_power_adapter_included",
    )
    built_in_components = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Built-in components",
        related_name="products_built_in_components",
    )
    arm_construction = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Arm construction",
        related_name="products_arm_construction",
    )
    number_of_modules = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Number of modules",
        related_name="products_number_of_modules",
    )
    number_of_component_sets = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Number of component sets",
        related_name="products_number_of_component_sets",
    )
    number_of_sockets = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Number of sockets",
        related_name="products_number_of_sockets",
    )
    output_connection_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Output connection type",
        related_name="products_output_connection_type",
    )
    output_bar_configuration = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Output bar configuration",
        related_name="products_output_bar_configuration",
    )
    lock_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Lock type",
        related_name="products_lock_type",
    )
    power = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Power",
        related_name="products_power",
    )
    cordless = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Cordless",
        related_name="products_cordless",
    )
    diameter = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Diameter",
        related_name="products_diameter",
    )

    def __str__(self) -> str:
        return "General"

    def import_json(self, data: dict) -> None:  # noqa: PLR0914, PLR0915
        """Import JSON data."""
        # Produkttyp
        product_type: Component | None = create_and_import_component(data, "Produkttyp")
        self.product_type = product_type

        # Tillbehörskategori
        accessory_category: Component | None = create_and_import_component(data, "Tillbehörskategori")
        self.accessory_category = accessory_category

        # Underkategori förbrukningsartiklar
        consumable_subcategory: Component | None = create_and_import_component(
            data,
            "Underkategori förbrukningsartiklar",
        )
        self.consumable_subcategory = consumable_subcategory

        # Teknik
        technology: Component | None = create_and_import_component(data, "Teknik")
        self.technology = technology

        # Klass skrivarförbrukningsartiklar
        printer_consumables_class: Component | None = create_and_import_component(
            data,
            "Klass skrivarförbrukningsartiklar",
        )
        self.printer_consumables_class = printer_consumables_class

        # Underkategori
        subcategory: Component | None = create_and_import_component(data, "Underkategori")
        self.subcategory = subcategory

        # Kategori
        category: Component | None = create_and_import_component(data, "Kategori")
        self.category = category

        # Installationstyp
        installation_type: Component | None = create_and_import_component(data, "Installationstyp")
        self.installation_type = installation_type

        # Utformad för
        designed_for: Component | None = create_and_import_component(data, "Utformad för")
        self.designed_for = designed_for

        # Miljö
        environment: Component | None = create_and_import_component(data, "Miljö")
        self.environment = environment

        # Antal inställda delar
        number_of_set_parts: Component | None = create_and_import_component(data, "Antal inställda delar")
        self.number_of_set_parts = number_of_set_parts

        # Lämplig för
        suitable_for: Component | None = create_and_import_component(data, "Lämplig för")
        self.suitable_for = suitable_for

        # Funktioner
        features: Component | None = create_and_import_component(data, "Funktioner")
        self.features = features

        # Inlärning
        learning: Component | None = create_and_import_component(data, "Inlärning")
        self.learning = learning

        # Min. ålder
        min_age: Component | None = create_and_import_component(data, "Min. ålder")
        self.min_age = min_age

        # Max. ålder
        max_age: Component | None = create_and_import_component(data, "Max. ålder")
        self.max_age = max_age

        # En-kortsdator ingår
        one_board_computer_included: Component | None = create_and_import_component(data, "En-kortsdator ingår")
        self.one_board_computer_included = one_board_computer_included

        # Vattentät
        waterproof: Component | None = create_and_import_component(data, "Vattentät")
        self.waterproof = waterproof

        # Dimmer
        dimmer: Component | None = create_and_import_component(data, "Dimmer")
        self.dimmer = dimmer

        # Kabellängd
        cable_length: Component | None = create_and_import_component(data, "Kabellängd")
        self.cable_length = cable_length

        # Watt som stöds för glödlampa
        supported_wattage_for_light_bulb: Component | None = create_and_import_component(
            data,
            "Watt som stöds för glödlampa",
        )
        self.supported_wattage_for_light_bulb = supported_wattage_for_light_bulb

        # Antal installerade glödlampor
        number_of_installed_light_bulbs: Component | None = create_and_import_component(
            data,
            "Antal installerade glödlampor",
        )
        self.number_of_installed_light_bulbs = number_of_installed_light_bulbs

        # Antal glödlampor som stöds
        number_of_supported_light_bulbs: Component | None = create_and_import_component(
            data,
            "Antal glödlampor som stöds",
        )
        self.number_of_supported_light_bulbs = number_of_supported_light_bulbs

        # Batteri ingår
        battery_included: Component | None = create_and_import_component(data, "Batteri ingår")
        self.battery_included = battery_included

        # Omkopplingstyp
        switch_type: Component | None = create_and_import_component(data, "Omkopplingstyp")
        self.switch_type = switch_type

        # Omkopplingsplats
        switch_location: Component | None = create_and_import_component(data, "Omkopplingsplats")
        self.switch_location = switch_location

        # Klämmontering
        clamp_mount: Component | None = create_and_import_component(data, "Klämmontering")
        self.clamp_mount = clamp_mount

        # Verktygsuppsättning (delar)
        tool_set_parts: Component | None = create_and_import_component(data, "Verktygsuppsättning (delar)")
        self.tool_set_parts = tool_set_parts

        # Uttag
        socket: Component | None = create_and_import_component(data, "Uttag")
        self.socket = socket

        # Uttagsstorlek
        socket_size: Component | None = create_and_import_component(data, "Uttagsstorlek")
        self.socket_size = socket_size

        # Spets
        tip: Component | None = create_and_import_component(data, "Spets")
        self.tip = tip

        # Spetsstorlek
        tip_size: Component | None = create_and_import_component(data, "Spetsstorlek")
        self.tip_size = tip_size

        # Storlek
        size: Component | None = create_and_import_component(data, "Storlek")
        self.size = size

        # Form
        shape: Component | None = create_and_import_component(data, "Form")
        self.shape = shape

        # Spårningsdata
        tracking_data: Component | None = create_and_import_component(data, "Spårningsdata")
        self.tracking_data = tracking_data

        # Lösning
        solution: Component | None = create_and_import_component(data, "Lösning")
        self.solution = solution

        # Tecken/tema
        character_theme: Component | None = create_and_import_component(data, "Tecken/tema")
        self.character_theme = character_theme

        # Växelströmsadapter medföljer
        ac_adapter_included: Component | None = create_and_import_component(data, "Växelströmsadapter medföljer")
        self.AC_adapter_included = ac_adapter_included

        # Stil
        style: Component | None = create_and_import_component(data, "Stil")
        self.style = style

        # Rekommenderas för
        recommended_for: Component | None = create_and_import_component(data, "Rekommenderas för")
        self.recommended_for = recommended_for

        # Rekommenderad användning
        recommended_use: Component | None = create_and_import_component(data, "Rekommenderad användning")
        self.recommended_use = recommended_use

        # Anslutning
        connection: Component | None = create_and_import_component(data, "Anslutning")
        self.connection = connection

        # Typ
        _type: Component | None = create_and_import_component(data, "Typ")
        self.type = _type

        # Total längd
        total_length: Component | None = create_and_import_component(data, "Total längd")
        self.total_length = total_length

        # Betalningsteknik
        payment_technology: Component | None = create_and_import_component(data, "Betalningsteknik")
        self.payment_technology = payment_technology

        # Mekanism
        mechanism: Component | None = create_and_import_component(data, "Mekanism")
        self.mechanism = mechanism

        # Lutningslås
        tilt_lock: Component | None = create_and_import_component(data, "Lutningslås")
        self.tilt_lock = tilt_lock

        # Huvudstöd
        headrest: Component | None = create_and_import_component(data, "Huvudstöd")
        self.headrest = headrest

        # Armstöd
        armrest: Component | None = create_and_import_component(data, "Armstöd")
        self.armrest = armrest

        # Lutning
        tilt: Component | None = create_and_import_component(data, "Lutning")
        self.tilt = tilt

        # Ergonomisk
        ergonomic: Component | None = create_and_import_component(data, "Ergonomisk")
        self.ergonomic = ergonomic

        # Lutande spänningsjustering
        tilt_tension_adjustment: Component | None = create_and_import_component(data, "Lutande spänningsjustering")
        self.tilt_tension_adjustment = tilt_tension_adjustment

        # Klass
        _class: Component | None = create_and_import_component(data, "Klass")
        self._class = _class

        # Kitinnehåll
        kit_contents: Component | None = create_and_import_component(data, "Kitinnehåll")
        self.kit_contents = kit_contents

        # Underkategori medier
        media_subcategory: Component | None = create_and_import_component(data, "Underkategori medier")
        self.media_subcategory = media_subcategory

        # Inomhus/utomhus
        indoor_outdoor: Component | None = create_and_import_component(data, "Inomhus/utomhus")
        self.indoor_outdoor = indoor_outdoor

        # Termometerskala
        thermometer_scale: Component | None = create_and_import_component(data, "Termometerskala")
        self.thermometer_scale = thermometer_scale

        # Användningslägen
        usage_modes: Component | None = create_and_import_component(data, "Användningslägen")
        self.usage_modes = usage_modes

        # Bilströmsadapter medföljer
        car_power_adapter_included: Component | None = create_and_import_component(data, "Bilströmsadapter medföljer")
        self.car_power_adapter_included = car_power_adapter_included

        # Inbyggda komponenter
        built_in_components: Component | None = create_and_import_component(data, "Inbyggda komponenter")
        self.built_in_components = built_in_components

        # Armkonstruktion
        arm_construction: Component | None = create_and_import_component(data, "Armkonstruktion")
        self.arm_construction = arm_construction

        # Antal moduler
        number_of_modules: Component | None = create_and_import_component(data, "Antal moduler")
        self.number_of_modules = number_of_modules

        # Antal uppsättningar komponenter
        number_of_component_sets: Component | None = create_and_import_component(
            data,
            "Antal uppsättningar komponenter",
        )
        self.number_of_component_sets = number_of_component_sets

        # Antal uttag
        number_of_sockets: Component | None = create_and_import_component(data, "Antal uttag")
        self.number_of_sockets = number_of_sockets

        # Utgångsanslutningstyp
        output_connection_type: Component | None = create_and_import_component(data, "Utgångsanslutningstyp")
        self.output_connection_type = output_connection_type

        # Konfiguration av utgångsstänger
        output_bar_configuration: Component | None = create_and_import_component(
            data,
            "Konfiguration av utgångsstänger",
        )
        self.output_bar_configuration = output_bar_configuration

        # Låstyp
        lock_type: Component | None = create_and_import_component(data, "Låstyp")
        self.lock_type = lock_type

        # Ström
        power: Component | None = create_and_import_component(data, "Ström")
        self.power = power

        # Sladdlös
        cordless: Component | None = create_and_import_component(data, "Sladdlös")
        self.cordless = cordless

        # Diameter
        diameter: Component | None = create_and_import_component(data, "Diameter")
        self.diameter = diameter


class Miscellaneous(auto_prefetch.Model):
    """Miscellaneous information."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the miscellaneous information was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the miscellaneous information was last updated")

    # Webhallen fields
    color = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Color",
        related_name="miscellaneous_color",
    )
    color_category = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Color category",
        related_name="miscellaneous_color_category",
    )
    flat_screen_mounting_interface = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Flat screen mounting interface",
        related_name="miscellaneous_flat_screen_mounting_interface",
    )
    rack_mounting_kit = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Rack mounting kit",
        related_name="miscellaneous_rack_mounting_kit",
    )
    compatible_game_console = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Compatible game console",
        related_name="miscellaneous_compatible_game_console",
    )
    sound_pressure_level = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Sound pressure level",
        related_name="miscellaneous_sound_pressure_level",
    )
    external_color = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="External color",
        related_name="miscellaneous_external_color",
    )
    encryption_algorithm = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Encryption algorithm",
        related_name="miscellaneous_encryption_algorithm",
    )
    hard_drive_form_factor_compatibility = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="HDD form factor compatibility",
        related_name="miscellaneous_hard_drive_form_factor_compatibility",
    )
    hard_drive_compatible_form_factor_metric = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="HDD compatible form factor metric",
        related_name="miscellaneous_hard_drive_compatible_form_factor_metric",
    )
    material = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Material",
        related_name="miscellaneous_material",
    )
    product_material = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Product material",
        related_name="miscellaneous_product_material",
    )
    features = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Features",
        related_name="miscellaneous_features",
    )
    gaming = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Gaming",
        related_name="miscellaneous_gaming",
    )
    finish = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Finish",
        related_name="miscellaneous_finish",
    )
    works_with_chromebook = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Works with Chromebook",
        related_name="miscellaneous_works_with_chromebook",
    )
    recycled_product_content = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Recycled product content",
        related_name="miscellaneous_recycled_product_content",
    )
    included_accessories = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Included accessories",
        related_name="miscellaneous_included_accessories",
    )
    operating_time_without_power_connection = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Operating time without power connection",
        related_name="miscellaneous_operating_time_without_power_connection",
    )
    cordless_use = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Cordless use",
        related_name="miscellaneous_cordless_use",
    )
    max_load = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Max load",
        related_name="miscellaneous_max_load",
    )
    recycled_packaging_content = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Recycled packaging content",
        related_name="miscellaneous_recycled_packaging_content",
    )
    protection = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Protection",
        related_name="miscellaneous_protection",
    )
    packaging_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Packaging type",
        related_name="miscellaneous_packaging_type",
    )
    design_features = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Design features",
        related_name="miscellaneous_design_features",
    )
    package_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Package type",
        related_name="miscellaneous_package_type",
    )
    standards_followed = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Standards followed",
        related_name="miscellaneous_standards_followed",
    )
    coffee_maker_accessories = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Coffee maker accessories",
        related_name="miscellaneous_coffee_maker_accessories",
    )
    max_depth_for_water_resistance = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Max depth for water resistance",
        related_name="miscellaneous_max_depth_for_water_resistance",
    )
    for_underwater_use = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="For underwater use",
        related_name="miscellaneous_for_underwater_use",
    )
    pricing_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Pricing type",
        related_name="miscellaneous_pricing_type",
    )
    capacity = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Capacity",
        related_name="miscellaneous_capacity",
    )
    product_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Product type",
        related_name="miscellaneous_product_type",
    )
    processor_package = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Processor package",
        related_name="miscellaneous_processor_package",
    )
    waterproof = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Waterproof",
        related_name="miscellaneous_waterproof",
    )
    reparability_index = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Reparability index",
        related_name="miscellaneous_reparability_index",
    )
    sound_level = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Sound level",
        related_name="miscellaneous_sound_level",
    )
    noise_class = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Noise class",
        related_name="miscellaneous_noise_class",
    )
    rugged_design = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Rugged design",
        related_name="miscellaneous_rugged_design",
    )
    software_certification = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Software certification",
        related_name="miscellaneous_software_certification",
    )
    manufacturer_sales_program = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Manufacturer sales program",
        related_name="miscellaneous_manufacturer_sales_program",
    )
    recycled_product_content_comment = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Recycled product content comment",
        related_name="miscellaneous_recycled_product_content_comment",
    )
    recycled_packaging_content_comment = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Recycled packaging content comment",
        related_name="miscellaneous_recycled_packaging_content_comment",
    )
    product_condition = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Product condition",
        related_name="miscellaneous_product_condition",
    )
    ai_ready = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="AI ready",
        related_name="miscellaneous_ai_ready",
    )

    def __str__(self) -> str:
        return "Miscellaneous"

    def import_json(self, data: dict) -> None:  # noqa: PLR0914, PLR0915
        """Import JSON data."""
        # Färg
        color: Component | None = create_and_import_component(data, "Färg")
        self.color = color

        # Färgkategori
        color_category: Component | None = create_and_import_component(data, "Färgkategori")
        self.color_category = color_category

        # Monteringsgränssnitt för platt bildskärm
        flat_screen_mounting_interface: Component | None = create_and_import_component(
            data,
            "Monteringsgränssnitt för platt bildskärm",
        )
        self.flat_screen_mounting_interface = flat_screen_mounting_interface

        # Rackmonteringssats
        rack_mounting_kit: Component | None = create_and_import_component(data, "Rackmonteringssats")
        self.rack_mounting_kit = rack_mounting_kit

        # Kompatibla spelkonsol
        compatible_game_console: Component | None = create_and_import_component(data, "Kompatibla spelkonsol")
        self.compatible_game_console = compatible_game_console

        # Ljudtrycknivå
        sound_pressure_level: Component | None = create_and_import_component(data, "Ljudtrycknivå")
        self.sound_pressure_level = sound_pressure_level

        # Yttre färg
        external_color: Component | None = create_and_import_component(data, "Yttre färg")
        self.external_color = external_color

        # Krypteringsalgoritm
        encryption_algorithm: Component | None = create_and_import_component(data, "Krypteringsalgoritm")
        self.encryption_algorithm = encryption_algorithm

        # Formfaktorkomptibilitet för hårddisk
        hard_drive_form_factor_compatibility: Component | None = create_and_import_component(
            data,
            "Formfaktorkomptibilitet för hårddisk",
        )
        self.hard_drive_form_factor_compatibility = hard_drive_form_factor_compatibility

        # Hårddiskkompatibel formfaktor (metrisk)
        hard_drive_compatible_form_factor_metric: Component | None = create_and_import_component(
            data,
            "Hårddiskkompatibel formfaktor (metrisk)",
        )
        self.hard_drive_compatible_form_factor_metric = hard_drive_compatible_form_factor_metric

        # Material
        material: Component | None = create_and_import_component(data, "Material")
        self.material = material

        # Produktmaterial
        product_material: Component | None = create_and_import_component(data, "Produktmaterial")
        self.product_material = product_material

        # Egenskaper
        features: Component | None = create_and_import_component(data, "Egenskaper")
        self.features = features

        # Gaming
        gaming: Component | None = create_and_import_component(data, "Gaming")
        self.gaming = gaming

        # Finish
        finish: Component | None = create_and_import_component(data, "Finish")
        self.finish = finish

        # Fungerar med Chromebook
        works_with_chromebook: Component | None = create_and_import_component(data, "Fungerar med Chromebook")
        self.works_with_chromebook = works_with_chromebook

        # Återvunnet produktinnehåll
        recycled_product_content: Component | None = create_and_import_component(data, "Återvunnet produktinnehåll")
        self.recycled_product_content = recycled_product_content

        # Inkluderade tillbehör
        included_accessories: Component | None = create_and_import_component(data, "Inkluderade tillbehör")
        self.included_accessories = included_accessories

        # Driftstid utan nätanslutning
        operating_time_without_power_connection: Component | None = create_and_import_component(
            data,
            "Driftstid utan nätanslutning",
        )
        self.operating_time_without_power_connection = operating_time_without_power_connection

        # Sladdlös användning
        cordless_use: Component | None = create_and_import_component(data, "Sladdlös användning")
        self.cordless_use = cordless_use

        # Maxlast
        max_load: Component | None = create_and_import_component(data, "Maxlast")
        self.max_load = max_load

        # Återvunnet förpackningsinnehåll
        recycled_packaging_content: Component | None = create_and_import_component(
            data,
            "Återvunnet förpackningsinnehåll",
        )
        self.recycled_packaging_content = recycled_packaging_content

        # Skydd
        protection: Component | None = create_and_import_component(data, "Skydd")
        self.protection = protection

        # Förpackningstyp
        packaging_type: Component | None = create_and_import_component(data, "Förpackningstyp")
        self.packaging_type = packaging_type

        # Designfunktioner
        design_features: Component | None = create_and_import_component(data, "Designfunktioner")
        self.design_features = design_features

        # Pakettyp
        package_type: Component | None = create_and_import_component(data, "Pakettyp")
        self.package_type = package_type

        # Standarder som följs
        standards_followed: Component | None = create_and_import_component(data, "Standarder som följs")
        self.standards_followed = standards_followed

        # Kaffebryggartillbehör
        coffee_maker_accessories: Component | None = create_and_import_component(data, "Kaffebryggartillbehör")
        self.coffee_maker_accessories = coffee_maker_accessories

        # Maxdjup för vattentålighet
        max_depth_for_water_resistance: Component | None = create_and_import_component(
            data,
            "Maxdjup för vattentålighet",
        )
        self.max_depth_for_water_resistance = max_depth_for_water_resistance

        # För undervattensbruk
        for_underwater_use: Component | None = create_and_import_component(data, "För undervattensbruk")
        self.for_underwater_use = for_underwater_use

        # Typ av prissättning
        pricing_type: Component | None = create_and_import_component(data, "Typ av prissättning")
        self.pricing_type = pricing_type

        # Kapacitet
        capacity: Component | None = create_and_import_component(data, "Kapacitet")
        self.capacity = capacity

        # Produkttyp
        product_type: Component | None = create_and_import_component(data, "Produkttyp")
        self.product_type = product_type

        # Processorpaket
        processor_package: Component | None = create_and_import_component(data, "Processorpaket")
        self.processor_package = processor_package

        # Vattentät
        waterproof: Component | None = create_and_import_component(data, "Vattentät")
        self.waterproof = waterproof

        # Reparationsbarhetsindex
        reparability_index: Component | None = create_and_import_component(data, "Reparationsbarhetsindex")
        self.reparability_index = reparability_index

        # Ljudnivå
        sound_level: Component | None = create_and_import_component(data, "Ljudnivå")
        self.sound_level = sound_level

        # Bullerklass
        noise_class: Component | None = create_and_import_component(data, "Bullerklass")
        self.noise_class = noise_class

        # Robust design
        rugged_design: Component | None = create_and_import_component(data, "Robust design")
        self.rugged_design = rugged_design

        # Mjukvarucertifiering
        software_certification: Component | None = create_and_import_component(data, "Mjukvarucertifiering")
        self.software_certification = software_certification

        # Försäljningsprogram från tillverkaren
        manufacturer_sales_program: Component | None = create_and_import_component(
            data,
            "Försäljningsprogram från tillverkaren",
        )
        self.manufacturer_sales_program = manufacturer_sales_program

        # Återvunnet produktinnehåll (kommentar)
        recycled_product_content_comment: Component | None = create_and_import_component(
            data,
            "Återvunnet produktinnehåll (kommentar)",
        )
        self.recycled_product_content_comment = recycled_product_content_comment

        # Återvunnet förpackningsinnehåll (kommentar)
        recycled_packaging_content_comment: Component | None = create_and_import_component(
            data,
            "Återvunnet förpackningsinnehåll (kommentar)",
        )
        self.recycled_packaging_content_comment = recycled_packaging_content_comment

        # Produktens skick
        product_condition: Component | None = create_and_import_component(data, "Produktens skick")
        self.product_condition = product_condition

        # AI-klar
        ai_ready: Component | None = create_and_import_component(data, "AI-klar")
        self.ai_ready = ai_ready


class Cable(auto_prefetch.Model):
    """Cable."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the cable was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the cable was last updated")

    # Webhallen fields
    # Typ för vänster kontakt
    type_for_left_connector = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Type of left connector",
        related_name="cable_type_for_left_connector",
    )

    # Typ av högerkontakt
    type_of_right_connector = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Type of right connector",
        related_name="cable_type_of_right_connector",
    )

    # Höger kontakttyp
    right_connector_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Right connector type",
        related_name="cable_right_connector_type",
    )

    # Typ av I/O-kabel
    io_cable_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Type of I/O cable",
        related_name="cable_io_cable_type",
    )

    # Vänster kontakttyp
    left_connector_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Left connector type",
        related_name="cable_left_connector_type",
    )

    # Underkategori för kablar
    cable_subcategory = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Cable subcategory",
        related_name="cable_cable_subcategory",
    )

    # Teknik
    technology = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Technology",
        related_name="cable_technology",
    )

    # Typ av AV-kabel
    av_cable_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Type of AV cable",
        related_name="cable_av_cable_type",
    )

    # Typ av nätverkskabel
    network_cable_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Type of network cable",
        related_name="cable_network_cable_type",
    )

    # Kategori
    category = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Category",
        related_name="cable_category",
    )

    # Kablageschema
    cable_scheme = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Cable scheme",
        related_name="cable_cable_scheme",
    )

    # Typ av gränssnitt
    interface_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Interface type",
        related_name="cable_interface_type",
    )

    # Typ av kabel för lagringslösning
    storage_solution_cable_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Type of storage solution cable",
        related_name="cable_storage_solution_cable_type",
    )

    # Gränssnitt som stöds
    supported_interface = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Supported interface",
        related_name="cable_supported_interface",
    )

    # Standarder som följs
    standards_followed = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Standards followed",
        related_name="cable_standards_followed",
    )

    # Typ av fiberoptik
    fiber_optic_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Type of fiber optic",
        related_name="cable_fiber_optic_type",
    )

    def __str__(self) -> str:
        return "Cable"

    def import_json(self, data: dict) -> None:  # noqa: PLR0914
        """Import JSON data."""
        # Typ för vänster kontakt
        type_for_left_connector: Component | None = create_and_import_component(data, "Typ för vänster kontakt")
        self.type_for_left_connector = type_for_left_connector

        # Typ av högerkontakt
        type_of_right_connector: Component | None = create_and_import_component(data, "Typ av högerkontakt")
        self.type_of_right_connector = type_of_right_connector

        # Höger kontakttyp
        right_connector_type: Component | None = create_and_import_component(data, "Höger kontakttyp")
        self.right_connector_type = right_connector_type

        # Typ av I/O-kabel
        io_cable_type: Component | None = create_and_import_component(data, "Typ av I/O-kabel")
        self.io_cable_type = io_cable_type

        # Vänster kontakttyp
        left_connector_type: Component | None = create_and_import_component(data, "Vänster kontakttyp")
        self.left_connector_type = left_connector_type

        # Underkategori för kablar
        cable_subcategory: Component | None = create_and_import_component(data, "Underkategori för kablar")
        self.cable_subcategory = cable_subcategory

        # Teknik
        technology: Component | None = create_and_import_component(data, "Teknik")
        self.technology = technology

        # Typ av AV-kabel
        av_cable_type: Component | None = create_and_import_component(data, "Typ av AV-kabel")
        self.av_cable_type = av_cable_type

        # Typ av nätverkskabel
        network_cable_type: Component | None = create_and_import_component(data, "Typ av nätverkskabel")
        self.network_cable_type = network_cable_type

        # Kategori
        category: Component | None = create_and_import_component(data, "Kategori")
        self.category = category

        # Kablageschema
        cable_scheme: Component | None = create_and_import_component(data, "Kablageschema")
        self.cable_scheme = cable_scheme

        # Typ av gränssnitt
        interface_type: Component | None = create_and_import_component(data, "Typ av gränssnitt")
        self.interface_type = interface_type

        # Typ av kabel för lagringslösning
        storage_solution_cable_type: Component | None = create_and_import_component(
            data,
            "Typ av kabel för lagringslösning",
        )
        self.storage_solution_cable_type = storage_solution_cable_type

        # Gränssnitt som stöds
        supported_interface: Component | None = create_and_import_component(data, "Gränssnitt som stöds")
        self.supported_interface = supported_interface

        # Standarder som följs
        standards_followed: Component | None = create_and_import_component(data, "Standarder som följs")
        self.standards_followed = standards_followed

        # Typ av fiberoptik
        fiber_optic_type: Component | None = create_and_import_component(data, "Typ av fiberoptik")
        self.fiber_optic_type = fiber_optic_type


class InputDevice(auto_prefetch.Model):
    """Inmatningsenhet."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the input device was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the input device was last updated")

    # Webhallen fields
    connection_technology = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Connection technology",
        related_name="input_device_connection_technology",
    )
    interface = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Interface",
        related_name="input_device_interface",
    )
    product_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Product type",
        related_name="input_device_product_type",
    )
    backlit = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Backlit",
        related_name="input_device_backlit",
    )
    form_factor = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Form factor",
        related_name="input_device_form_factor",
    )
    interface_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Interface type",
        related_name="input_device_interface_type",
    )
    input_adapter_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Input adapter type",
        related_name="input_device_input_adapter_type",
    )
    keyboard_localization = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Keyboard localization",
        related_name="input_device_keyboard_localization",
    )
    motion_detection_technology = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Motion detection technology",
        related_name="input_device_motion_detection_technology",
    )
    orientation = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Orientation",
        related_name="input_device_orientation",
    )
    number_of_buttons = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Number of buttons",
        related_name="input_device_number_of_buttons",
    )
    motion_resolution = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Motion resolution",
        related_name="input_device_motion_resolution",
    )
    notebook_mouse = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Notebook mouse",
        related_name="input_device_notebook_mouse",
    )
    ergonomic_design = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Ergonomic design",
        related_name="input_device_ergonomic_design",
    )
    keyboard_layout = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Keyboard layout",
        related_name="input_device_keyboard_layout",
    )
    keyboard_technology = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Keyboard technology",
        related_name="input_device_keyboard_technology",
    )
    active_horizontal_area = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Active horizontal area",
        related_name="input_device_active_horizontal_area",
    )
    active_vertical_area = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Active vertical area",
        related_name="input_device_active_vertical_area",
    )
    anti_ghosting = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Anti-ghosting",
        related_name="input_device_anti_ghosting",
    )
    number_of_simultaneous_keypresses = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Number of simultaneous keypresses",
        related_name="input_device_number_of_simultaneous_keypresses",
    )
    type = models.ForeignKey(Component, on_delete=models.CASCADE, help_text="Type", related_name="input_device_type")
    key_lock_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Key lock type",
        related_name="input_device_key_lock_type",
    )
    backlight = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Backlight",
        related_name="input_device_backlight",
    )
    numeric_keypad = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Numeric keypad",
        related_name="input_device_numeric_keypad",
    )

    def __str__(self) -> str:
        return "Input device"

    def import_json(self, data: dict) -> None:  # noqa: PLR0914
        """Import JSON data."""
        # Anslutningsteknik
        connection_technology: Component | None = create_and_import_component(data, "Anslutningsteknik")
        self.connection_technology = connection_technology

        # Gränssnitt
        interface: Component | None = create_and_import_component(data, "Gränssnitt")
        self.interface = interface

        # Produkttyp
        product_type: Component | None = create_and_import_component(data, "Produkttyp")
        self.product_type = product_type

        # Bakgrundsbelyst
        backlit: Component | None = create_and_import_component(data, "Bakgrundsbelyst")
        self.backlit = backlit

        # Formfaktor
        form_factor: Component | None = create_and_import_component(data, "Formfaktor")
        self.form_factor = form_factor

        # Typ av gränssnitt
        interface_type: Component | None = create_and_import_component(data, "Typ av gränssnitt")
        self.interface_type = interface_type

        # Typ av ingångsadapter
        input_adapter_type: Component | None = create_and_import_component(data, "Typ av ingångsadapter")
        self.input_adapter_type = input_adapter_type

        # Tangentbordslokalisering
        keyboard_localization: Component | None = create_and_import_component(data, "Tangentbordslokalisering")
        self.keyboard_localization = keyboard_localization

        # Teknik för rörelsedetektering
        motion_detection_technology: Component | None = create_and_import_component(
            data,
            "Teknik för rörelsedetektering",
        )
        self.motion_detection_technology = motion_detection_technology

        # Inriktning
        orientation: Component | None = create_and_import_component(data, "Inriktning")
        self.orientation = orientation

        # Antal knappar
        number_of_buttons: Component | None = create_and_import_component(data, "Antal knappar")
        self.number_of_buttons = number_of_buttons

        # Rörelseupplösning
        motion_resolution: Component | None = create_and_import_component(data, "Rörelseupplösning")
        self.motion_resolution = motion_resolution

        # Notebook-mus
        notebook_mouse: Component | None = create_and_import_component(data, "Notebook-mus")
        self.notebook_mouse = notebook_mouse

        # Ergonomisk design
        ergonomic_design: Component | None = create_and_import_component(data, "Ergonomisk design")
        self.ergonomic_design = ergonomic_design

        # Tangentbordslayout
        keyboard_layout: Component | None = create_and_import_component(data, "Tangentbordslayout")
        self.keyboard_layout = keyboard_layout

        # Tangentbordsteknologi
        keyboard_technology: Component | None = create_and_import_component(data, "Tangentbordsteknologi")
        self.keyboard_technology = keyboard_technology

        # Aktivt horis. område
        active_horizontal_area: Component | None = create_and_import_component(data, "Aktivt horis. område")
        self.active_horizontal_area = active_horizontal_area

        # Aktivt vert. område
        active_vertical_area: Component | None = create_and_import_component(data, "Aktivt vert. område")
        self.active_vertical_area = active_vertical_area

        # Anti-ghosting
        anti_ghosting: Component | None = create_and_import_component(data, "Anti-ghosting")
        self.anti_ghosting = anti_ghosting

        # Antal samtidiga tangenttryck
        number_of_simultaneous_keypresses: Component | None = create_and_import_component(
            data,
            "Antal samtidiga tangenttryck",
        )
        self.number_of_simultaneous_keypresses = number_of_simultaneous_keypresses

        # Typ
        _type: Component | None = create_and_import_component(data, "Typ")
        self.type = _type

        # Nyckellåstyp
        key_lock_type: Component | None = create_and_import_component(data, "Nyckellåstyp")
        self.key_lock_type = key_lock_type

        # Bakgrundsbelysning
        backlight: Component | None = create_and_import_component(data, "Bakgrundsbelysning")
        self.backlight = backlight

        # Numeriskt tangentbord
        numeric_keypad: Component | None = create_and_import_component(data, "Numeriskt tangentbord")
        self.numeric_keypad = numeric_keypad


class ServiceAndSupport(auto_prefetch.Model):
    """Service and support."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the service and support was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the service and support was last updated")

    # Webhallen fields
    type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Type",
        related_name="service_and_support_type",
    )

    def __str__(self) -> str:
        return "Service and support"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Typ
        _type: Component | None = create_and_import_component(data, "Typ")
        self.type = _type


class GrossDimensionsAndWeight(auto_prefetch.Model):
    """Mått och vikt (brutto)."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the gross dimensions and weight was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the gross dimensions and weight was last updated")

    # Webhallen fields
    packing_weight = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Packing weight",
        related_name="gross_dimensions_packing_weight",
    )
    packing_height = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Packing height",
        related_name="gross_dimensions_packing_height",
    )
    packing_depth = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Packing depth",
        related_name="gross_dimensions_packing_depth",
    )
    packing_width = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Packing width",
        related_name="gross_dimensions_packing_width",
    )

    def __str__(self) -> str:
        return "Gross dimensions and weight"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Emballagets vikt
        packing_weight: Component | None = create_and_import_component(data, "Emballagets vikt")
        self.packing_weight = packing_weight

        # Emballagets höjd
        packing_height: Component | None = create_and_import_component(data, "Emballagets höjd")
        self.packing_height = packing_height

        # Emballagets djup
        packing_depth: Component | None = create_and_import_component(data, "Emballagets djup")
        self.packing_depth = packing_depth

        # Emballagets bredd
        packing_width: Component | None = create_and_import_component(data, "Emballagets bredd")
        self.packing_width = packing_width


class Consumables(auto_prefetch.Model):
    """Förbrukningsartiklar."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the consumables was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the consumables was last updated")

    # Webhallen fields
    color = models.ForeignKey(Component, on_delete=models.CASCADE, help_text="Color", related_name="consumables_color")
    consumable_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Consumable type",
        related_name="consumables_consumable_type",
    )
    number_of_pages_during_lifetime = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Number of pages during life cycle",
        related_name="consumables_number_of_pages_during_lifetime",
    )
    coverage_for_lifetime = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Coverage for lifetime",
        related_name="consumables_coverage_for_lifetime",
    )
    original = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Original",
        related_name="consumables_original",
    )
    included_quantity = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Included quantity",
        related_name="consumables_included_quantity",
    )
    capacity = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Capacity",
        related_name="consumables_capacity",
    )
    toner_cartridge_features = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Toner cartridge features",
        related_name="consumables_toner_cartridge_features",
    )

    def __str__(self) -> str:
        return "Consumables"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Färg
        color: Component | None = create_and_import_component(data, "Färg")
        self.color = color

        # Typ av förbrukningsartikel
        consumable_type: Component | None = create_and_import_component(data, "Typ av förbrukningsartikel")
        self.consumable_type = consumable_type

        # Antal sidor under livslängd
        number_of_pages_during_lifetime: Component | None = create_and_import_component(
            data,
            "Antal sidor under livslängd",
        )
        self.number_of_pages_during_lifetime = number_of_pages_during_lifetime

        # Täckning för livslängd
        coverage_for_lifetime: Component | None = create_and_import_component(data, "Täckning för livslängd")
        self.coverage_for_lifetime = coverage_for_lifetime

        # Original
        original: Component | None = create_and_import_component(data, "Original")
        self.original = original

        # Inkluderat antal
        included_quantity: Component | None = create_and_import_component(data, "Inkluderat antal")
        self.included_quantity = included_quantity

        # Kapacitet
        capacity: Component | None = create_and_import_component(data, "Kapacitet")
        self.capacity = capacity

        # Egenskaper för tonerkassett
        toner_cartridge_features: Component | None = create_and_import_component(data, "Egenskaper för tonerkassett")
        self.toner_cartridge_features = toner_cartridge_features


class Battery(auto_prefetch.Model):
    """Batteri."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the battery was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the battery was last updated")

    # Webhallen fields
    included_quantity = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Included quantity",
        related_name="battery_included_quantity",
    )
    technology = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Technology",
        related_name="battery_technology",
    )
    form_factor = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Form factor",
        related_name="battery_form_factor",
    )
    capacity_ah = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Capacity (Ah)",
        related_name="battery_capacity_ah",
    )
    supplied_voltage = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Supplied voltage",
        related_name="battery_supplied_voltage",
    )
    installed_count = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Installed count",
        related_name="battery_installed_count",
    )
    charging_time = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Charging time",
        related_name="battery_charging_time",
    )
    battery_time_up_to = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Battery time up to",
        related_name="battery_time_up_to",
    )
    capacity = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Capacity",
        related_name="battery_capacity",
    )
    talk_time = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Talk time",
        related_name="battery_talk_time",
    )
    standby_time = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Standby time",
        related_name="battery_standby_time",
    )
    run_time = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Run time",
        related_name="battery_run_time",
    )
    wireless_charging = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Wireless charging",
        related_name="battery_wireless_charging",
    )
    fast_charging_technology = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Fast charging technology",
        related_name="battery_fast_charging_technology",
    )
    capacity_wh = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Capacity (Wh)",
        related_name="battery_capacity_wh",
    )
    battery_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Battery type",
        related_name="battery_type",
    )

    def __str__(self) -> str:
        return "Battery"

    def import_json(self, data: dict) -> None:  # noqa: PLR0914
        """Import JSON data."""
        # Inkluderad kvantitet
        included_quantity: Component | None = create_and_import_component(data, "Inkluderad kvantitet")
        self.included_quantity = included_quantity

        # Teknik
        technology: Component | None = create_and_import_component(data, "Teknik")
        self.technology = technology

        # Formfaktor
        form_factor: Component | None = create_and_import_component(data, "Formfaktor")
        self.form_factor = form_factor

        # Kapacitet (Ah)
        capacity_ah: Component | None = create_and_import_component(data, "Kapacitet (Ah)")
        self.capacity_ah = capacity_ah

        # Tillförd spänning
        supplied_voltage: Component | None = create_and_import_component(data, "Tillförd spänning")
        self.supplied_voltage = supplied_voltage

        # Installerat antal
        installed_count: Component | None = create_and_import_component(data, "Installerat antal")
        self.installed_count = installed_count

        # Laddningstid
        charging_time: Component | None = create_and_import_component(data, "Laddningstid")
        self.charging_time = charging_time

        # Batteritid (upp till)
        battery_time_up_to: Component | None = create_and_import_component(data, "Batteritid (upp till)")
        self.battery_time_up_to = battery_time_up_to

        # Kapacitet
        capacity: Component | None = create_and_import_component(data, "Kapacitet")
        self.capacity = capacity

        # Samtalstid
        talk_time: Component | None = create_and_import_component(data, "Samtalstid")
        self.talk_time = talk_time

        # Väntelägestid
        standby_time: Component | None = create_and_import_component(data, "Väntelägestid")
        self.standby_time = standby_time

        # Körtid
        run_time: Component | None = create_and_import_component(data, "Körtid")
        self.run_time = run_time

        # Trådlös laddning
        wireless_charging: Component | None = create_and_import_component(data, "Trådlös laddning")
        self.wireless_charging = wireless_charging

        # Snabbladdningsteknologi
        fast_charging_technology: Component | None = create_and_import_component(data, "Snabbladdningsteknologi")
        self.fast_charging_technology = fast_charging_technology

        # Kapacitet (Wh)
        capacity_wh: Component | None = create_and_import_component(data, "Kapacitet (Wh)")
        self.capacity_wh = capacity_wh

        # Batterityp
        battery_type: Component | None = create_and_import_component(data, "Batterityp")
        self.battery_type = battery_type


class AVComponent(auto_prefetch.Model):
    """AV-komponenter."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the AV component was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the AV component was last updated")

    # Webhallen fields
    mounting_components = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Mounting components",
        related_name="av_component_mounting_components",
    )
    type = models.ForeignKey(Component, on_delete=models.CASCADE, help_text="Type", related_name="av_component_type")
    recommended_use = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Recommended use",
        related_name="av_component_recommended_use",
    )
    color = models.ForeignKey(Component, on_delete=models.CASCADE, help_text="Color", related_name="av_component_color")
    material = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Material",
        related_name="av_component_material",
    )
    recommended_tv_size = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Recommended TV size",
        related_name="av_component_recommended_tv_size",
    )
    tilt = models.ForeignKey(Component, on_delete=models.CASCADE, help_text="Tilt", related_name="av_component_tilt")
    rotation = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Rotation",
        related_name="av_component_rotation",
    )
    panning = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Panning",
        related_name="av_component_panning",
    )
    leveling = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Leveling",
        related_name="av_component_leveling",
    )
    swivel_joint = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Swivel joint",
        related_name="av_component_swivel_joint",
    )
    design = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Design",
        related_name="av_component_design",
    )
    lifting_capacity = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Lifting capacity",
        related_name="av_component_lifting_capacity",
    )

    def __str__(self) -> str:
        return "AV component"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Monteringskomponenter
        mounting_components: Component | None = create_and_import_component(data, "Monteringskomponenter")
        self.mounting_components = mounting_components

        # Typ
        _type: Component | None = create_and_import_component(data, "Typ")
        self.type = _type

        # Rekommenderad användning
        recommended_use: Component | None = create_and_import_component(data, "Rekommenderad användning")
        self.recommended_use = recommended_use

        # Färg
        color: Component | None = create_and_import_component(data, "Färg")
        self.color = color

        # Material
        material: Component | None = create_and_import_component(data, "Material")
        self.material = material

        # Rekommenderad TV-storlek
        recommended_tv_size: Component | None = create_and_import_component(data, "Rekommenderad TV-storlek")
        self.recommended_tv_size = recommended_tv_size

        # Lutning
        tilt: Component | None = create_and_import_component(data, "Lutning")
        self.tilt = tilt

        # Rotation
        rotation: Component | None = create_and_import_component(data, "Rotation")
        self.rotation = rotation

        # Panorering
        panning: Component | None = create_and_import_component(data, "Panorering")
        self.panning = panning

        # Utjämning
        leveling: Component | None = create_and_import_component(data, "Utjämning")
        self.leveling = leveling

        # Svängtapp
        swivel_joint: Component | None = create_and_import_component(data, "Svängtapp")
        self.swivel_joint = swivel_joint

        # Design
        design: Component | None = create_and_import_component(data, "Design")
        self.design = design

        # Lyftkraft
        lifting_capacity: Component | None = create_and_import_component(data, "Lyftkraft")
        self.lifting_capacity = lifting_capacity


class RemoteControl(auto_prefetch.Model):
    """Fjärrkontroll."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the remote control was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the remote control was last updated")

    # Webhallen fields
    max_working_distance = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Max working distance",
        related_name="remote_control_max_working_distance",
    )
    remote_control_technology = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Remote control technology",
        related_name="remote_control_technology",
    )
    supported_devices = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Supported devices",
        related_name="remote_control_supported_devices",
    )
    type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Type",
        related_name="remote_control_type",
    )
    number_of_devices_supported = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Number of devices supported",
        related_name="remote_control_number_of_devices_supported",
    )

    def __str__(self) -> str:
        return "Remote control"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Max arbetsavstånd
        max_working_distance: Component | None = create_and_import_component(data, "Max arbetsavstånd")
        self.max_working_distance = max_working_distance

        # Fjärrkontrollteknik
        remote_control_technology: Component | None = create_and_import_component(data, "Fjärrkontrollteknik")
        self.remote_control_technology = remote_control_technology

        # Enheter som stöds
        supported_devices: Component | None = create_and_import_component(data, "Enheter som stöds")
        self.supported_devices = supported_devices

        # Typ
        _type: Component | None = create_and_import_component(data, "Typ")
        self.type = _type

        # Enhetsantal som stöds
        number_of_devices_supported: Component | None = create_and_import_component(data, "Enhetsantal som stöds")
        self.number_of_devices_supported = number_of_devices_supported


class VideoInput(auto_prefetch.Model):
    """Videoingång."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the video input was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the video input was last updated")

    # Webhallen fields
    support_for_audio_input = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Support for audio input",
        related_name="video_input_support_for_audio_input",
    )
    format_for_digital_video = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Format for digital video",
        related_name="video_input_format_for_digital_video",
    )
    format_for_analog_video = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Format for analog video",
        related_name="video_input_format_for_analog_video",
    )
    analog_video_signal = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Analog video signal",
        related_name="video_input_analog_video_signal",
    )
    resolution_for_digital_video_capture = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Resolution for digital video capture",
        related_name="video_input_resolution_for_digital_video_capture",
    )
    type_of_interface = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Type of interface",
        related_name="video_input_type_of_interface",
    )
    connection_technology = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Connection technology",
        related_name="video_input_connection_technology",
    )
    support_for_audio = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Support for audio",
        related_name="video_input_support_for_audio",
    )
    camera_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Camera type",
        related_name="video_input_camera_type",
    )
    computer_interface = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Computer interface",
        related_name="video_input_computer_interface",
    )
    maximum_digital_video_resolution = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Maximum digital video resolution",
        related_name="video_input_maximum_digital_video_resolution",
    )
    frame_rate_max = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Frame rate max",
        related_name="video_input_frame_rate_max",
    )
    day_and_night_function = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Day and night function",
        related_name="video_input_day_and_night_function",
    )
    camera_mounting_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Camera mounting type",
        related_name="video_input_camera_mounting_type",
    )
    mechanical_camera_design = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Mechanical camera design",
        related_name="video_input_mechanical_camera_design",
    )
    form_factor = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Form factor",
        related_name="video_input_form_factor",
    )
    resolution_for_still_shot = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Resolution for still shot",
        related_name="video_input_resolution_for_still_shot",
    )
    motion_detection = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Motion detection",
        related_name="video_input_motion_detection",
    )
    video_interface = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Video interface",
        related_name="video_input_video_interface",
    )
    type = models.ForeignKey(Component, on_delete=models.CASCADE, help_text="Type", related_name="video_input_type")
    image_capture_format = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Image capture format",
        related_name="video_input_image_capture_format",
    )
    properties = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Properties",
        related_name="video_input_properties",
    )
    digital_zoom = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Digital zoom",
        related_name="video_input_digital_zoom",
    )
    face_recognition = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Face recognition",
        related_name="video_input_face_recognition",
    )
    support_for_high_resolution_video = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Support for high resolution video",
        related_name="video_input_support_for_high_resolution_video",
    )
    continuous_shooting_rate = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Continuous shooting rate",
        related_name="video_input_continuous_shooting_rate",
    )
    image_stabilizer = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Image stabilizer",
        related_name="video_input_image_stabilizer",
    )
    max_video_resolution = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Max video resolution",
        related_name="video_input_max_video_resolution",
    )
    provided_interfaces = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Provided interfaces",
        related_name="video_input_provided_interfaces",
    )
    special_effects = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Special effects",
        related_name="video_input_special_effects",
    )
    digital_camera_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Digital camera type",
        related_name="video_input_digital_camera_type",
    )
    iso_max = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="ISO max",
        related_name="video_input_iso_max",
    )
    combined_with = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Combined with",
        related_name="video_input_combined_with",
    )
    light_sensitivity = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Light sensitivity",
        related_name="video_input_light_sensitivity",
    )

    def __str__(self) -> str:
        return "Video input"

    def import_json(self, data: dict) -> None:  # noqa: PLR0914, PLR0915
        """Import JSON data."""
        # Stöd för ljudingång
        support_for_audio_input: Component | None = create_and_import_component(data, "Stöd för ljudingång")
        self.support_for_audio_input = support_for_audio_input

        # Format för digital video
        format_for_digital_video: Component | None = create_and_import_component(data, "Format för digital video")
        self.format_for_digital_video = format_for_digital_video

        # Format för analog video
        format_for_analog_video: Component | None = create_and_import_component(data, "Format för analog video")
        self.format_for_analog_video = format_for_analog_video

        # Analog videosignal
        analog_video_signal: Component | None = create_and_import_component(data, "Analog videosignal")
        self.analog_video_signal = analog_video_signal

        # Upplösning vid digital videofångst
        resolution_for_digital_video_capture: Component | None = create_and_import_component(
            data,
            "Upplösning vid digital videofångst",
        )
        self.resolution_for_digital_video_capture = resolution_for_digital_video_capture

        # Typ av gränssnitt
        type_of_interface: Component | None = create_and_import_component(data, "Typ av gränssnitt")
        self.type_of_interface = type_of_interface

        # Anslutningsteknik
        connection_technology: Component | None = create_and_import_component(data, "Anslutningsteknik")
        self.connection_technology = connection_technology

        # Stöd för ljud
        support_for_audio: Component | None = create_and_import_component(data, "Stöd för ljud")
        self.support_for_audio = support_for_audio

        # Kameratyp
        camera_type: Component | None = create_and_import_component(data, "Kameratyp")
        self.camera_type = camera_type

        # Datorgränssnitt
        computer_interface: Component | None = create_and_import_component(data, "Datorgränssnitt")
        self.computer_interface = computer_interface

        # Maximal digital videoupplösning
        maximum_digital_video_resolution: Component | None = create_and_import_component(
            data,
            "Maximal digital videoupplösning",
        )
        self.maximum_digital_video_resolution = maximum_digital_video_resolution

        # Bildhastighet (max)
        frame_rate_max: Component | None = create_and_import_component(data, "Bildhastighet (max)")
        self.frame_rate_max = frame_rate_max

        # Dag- och nattfunktion
        day_and_night_function: Component | None = create_and_import_component(data, "Dag- och nattfunktion")
        self.day_and_night_function = day_and_night_function

        # Kameramonteringstyp
        camera_mounting_type: Component | None = create_and_import_component(data, "Kameramonteringstyp")
        self.camera_mounting_type = camera_mounting_type

        # Mekanisk kameradesign
        mechanical_camera_design: Component | None = create_and_import_component(data, "Mekanisk kameradesign")
        self.mechanical_camera_design = mechanical_camera_design

        # Formfaktor
        form_factor: Component | None = create_and_import_component(data, "Formfaktor")
        self.form_factor = form_factor

        # Upplösning för stillbildstagning
        resolution_for_still_shot: Component | None = create_and_import_component(
            data,
            "Upplösning för stillbildstagning",
        )
        self.resolution_for_still_shot = resolution_for_still_shot

        # Rörelsedetektion
        motion_detection: Component | None = create_and_import_component(data, "Rörelsedetektion")
        self.motion_detection = motion_detection

        # Videogränssnitt
        video_interface: Component | None = create_and_import_component(data, "Videogränssnitt")
        self.video_interface = video_interface

        # Typ
        _type: Component | None = create_and_import_component(data, "Typ")
        self.type = _type

        # Bildinspelningsformat
        image_capture_format: Component | None = create_and_import_component(data, "Bildinspelningsformat")
        self.image_capture_format = image_capture_format

        # Egenskaper
        properties: Component | None = create_and_import_component(data, "Egenskaper")
        self.properties = properties

        # Digital zoomning
        digital_zoom: Component | None = create_and_import_component(data, "Digital zoomning")
        self.digital_zoom = digital_zoom

        # Ansiktsigenkänning
        face_recognition: Component | None = create_and_import_component(data, "Ansiktsigenkänning")
        self.face_recognition = face_recognition

        # Stöd för högupplösningsvideo
        support_for_high_resolution_video: Component | None = create_and_import_component(
            data,
            "Stöd för högupplösningsvideo",
        )
        self.support_for_high_resolution_video = support_for_high_resolution_video

        # Kontinuerlig tagningshastighet
        continuous_shooting_rate: Component | None = create_and_import_component(data, "Kontinuerlig tagningshastighet")
        self.continuous_shooting_rate = continuous_shooting_rate

        # Bildstabiliserare
        image_stabilizer: Component | None = create_and_import_component(data, "Bildstabiliserare")
        self.image_stabilizer = image_stabilizer

        # Max. videoupplösning
        max_video_resolution: Component | None = create_and_import_component(data, "Max. videoupplösning")
        self.max_video_resolution = max_video_resolution

        # Tillhandahållna gränssnitt
        provided_interfaces: Component | None = create_and_import_component(data, "Tillhandahållna gränssnitt")
        self.provided_interfaces = provided_interfaces

        # Specialeffekter
        special_effects: Component | None = create_and_import_component(data, "Specialeffekter")
        self.special_effects = special_effects

        # Digitalkameratyp
        digital_camera_type: Component | None = create_and_import_component(data, "Digitalkameratyp")
        self.digital_camera_type = digital_camera_type

        # ISO (max)
        iso_max: Component | None = create_and_import_component(data, "ISO (max)")
        self.iso_max = iso_max

        # Kombinerad med
        combined_with: Component | None = create_and_import_component(data, "Kombinerad med")
        self.combined_with = combined_with

        # Ljuskänslighet
        light_sensitivity: Component | None = create_and_import_component(data, "Ljuskänslighet")
        self.light_sensitivity = light_sensitivity


class SystemRequirements(auto_prefetch.Model):
    """Systemkrav."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the system requirements was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the system requirements was last updated")

    # Webhallen fields
    required_operating_system = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Required operating system",
        related_name="system_requirements_required_operating_system",
    )
    os_family = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="OS family",
        related_name="system_requirements_os_family",
    )
    supported_host_platform = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Supported host platform",
        related_name="system_requirements_supported_host_platform",
    )

    def __str__(self) -> str:
        return "System requirements"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Operativsystem erfordras
        required_operating_system: Component | None = create_and_import_component(data, "Operativsystem erfordras")
        self.required_operating_system = required_operating_system

        # OS-familj
        os_family: Component | None = create_and_import_component(data, "OS-familj")
        self.os_family = os_family

        # Värdenhetsplattform som stöds
        supported_host_platform: Component | None = create_and_import_component(data, "Värdenhetsplattform som stöds")
        self.supported_host_platform = supported_host_platform


class Network(auto_prefetch.Model):
    """Network."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the network was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the network was last updated")

    # Webhallen fields
    type = models.ForeignKey(Component, on_delete=models.CASCADE, help_text="Type", related_name="network_type")
    number_of_ports = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Number of ports",
        related_name="network_number_of_ports",
    )
    subcategory = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Subcategory",
        related_name="network_subcategory",
    )
    form_factor = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Form factor",
        related_name="network_form_factor",
    )
    subtype = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Subtype",
        related_name="network_subtype",
    )
    managed = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Managed",
        related_name="network_managed",
    )
    jumbo_frame_support = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Jumbo frame support",
        related_name="network_jumbo_frame_support",
    )
    power_over_ethernet = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Power over Ethernet",
        related_name="network_power_over_ethernet",
    )
    connection_technology = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Connection technology",
        related_name="network_connection_technology",
    )
    data_link_protocol = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Data link protocol",
        related_name="network_data_link_protocol",
    )
    type_of_cabling = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Type of cabling",
        related_name="network_type_of_cabling",
    )
    interface_type_bus = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Interface type bus",
        related_name="network_interface_type_bus",
    )
    data_transfer_speed = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Data transfer speed",
        related_name="network_data_transfer_speed",
    )
    network_transport_protocol = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Network transport protocol",
        related_name="network_transport_protocol",
    )
    wireless_protocol = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Wireless protocol",
        related_name="network_wireless_protocol",
    )
    ac_standard = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="AC standard",
        related_name="network_ac_standard",
    )
    remote_administration_protocol = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Remote administration protocol",
        related_name="network_remote_administration_protocol",
    )
    number_of_wan_ports = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Number of WAN ports",
        related_name="network_number_of_wan_ports",
    )
    network_protocol = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Network protocol",
        related_name="network_network_protocol",
    )
    builtin_switch = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Built-in switch",
        related_name="network_builtin_switch",
    )
    important_functions = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Important functions",
        related_name="network_important_functions",
    )
    network_interface = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Network interface",
        related_name="network_network_interface",
    )
    advanced_switching = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Advanced switching",
        related_name="network_advanced_switching",
    )
    remote_management_interface = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Remote management interface",
        related_name="network_remote_management_interface",
    )
    max_area_indoor = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Max area indoor",
        related_name="network_max_area_indoor",
    )
    wireless_connection = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Wireless connection",
        related_name="network_wireless_connection",
    )
    lan_presentation_and_wireless_d_o = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="LAN presentation and wireless D/O",
        related_name="network_lan_presentation_and_wireless_d_o",
    )
    image_transfer_protocol_for_lan_and_wireless = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Image transfer protocol for LAN and wireless",
        related_name="network_image_transfer_protocol_for_lan_and_wireless",
    )
    support_for_wireless_lan = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Support for wireless LAN",
        related_name="network_support_for_wireless_lan",
    )
    cloud_managed = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Cloud managed",
        related_name="network_cloud_managed",
    )
    wire_protocol = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Wire protocol",
        related_name="network_wire_protocol",
    )

    def __str__(self) -> str:
        return "Network"

    def import_json(self, data: dict) -> None:  # noqa: PLR0914, PLR0915
        """Import JSON data."""
        # Typ
        _type: Component | None = create_and_import_component(data, "Typ")
        self.type = _type

        # Antal portar
        number_of_ports: Component | None = create_and_import_component(data, "Antal portar")
        self.number_of_ports = number_of_ports

        # Underkategori
        subcategory: Component | None = create_and_import_component(data, "Underkategori")
        self.subcategory = subcategory

        # Formfaktor
        form_factor: Component | None = create_and_import_component(data, "Formfaktor")
        self.form_factor = form_factor

        # Undertyp
        subtype: Component | None = create_and_import_component(data, "Undertyp")
        self.subtype = subtype

        # Managed
        managed: Component | None = create_and_import_component(data, "Managed")
        self.managed = managed

        # Jumbo Frame-support
        jumbo_frame_support: Component | None = create_and_import_component(data, "Jumbo Frame-support")
        self.jumbo_frame_support = jumbo_frame_support

        # PoE (Power Over Ethernet)
        power_over_ethernet: Component | None = create_and_import_component(data, "PoE (Power Over Ethernet)")
        self.power_over_ethernet = power_over_ethernet

        # Anslutningsteknik
        connection_technology: Component | None = create_and_import_component(data, "Anslutningsteknik")
        self.connection_technology = connection_technology

        # Datalänkprotokoll
        data_link_protocol: Component | None = create_and_import_component(data, "Datalänkprotokoll")
        self.data_link_protocol = data_link_protocol

        # Typ av kablage
        type_of_cabling: Component | None = create_and_import_component(data, "Typ av kablage")
        self.type_of_cabling = type_of_cabling

        # Gränssnittstyp (buss)
        interface_type_bus: Component | None = create_and_import_component(data, "Gränssnittstyp (buss)")
        self.interface_type_bus = interface_type_bus

        # Dataöverföringshastighet
        data_transfer_speed: Component | None = create_and_import_component(data, "Dataöverföringshastighet")
        self.data_transfer_speed = data_transfer_speed

        # Nätverks/transportprotokoll
        network_transport_protocol: Component | None = create_and_import_component(data, "Nätverks/transportprotokoll")
        self.network_transport_protocol = network_transport_protocol

        # Trådlöst protokoll
        wireless_protocol: Component | None = create_and_import_component(data, "Trådlöst protokoll")
        self.wireless_protocol = wireless_protocol

        # AC-Standard
        ac_standard: Component | None = create_and_import_component(data, "AC-Standard")
        self.ac_standard = ac_standard

        # Protokoll för administration på distans
        remote_administration_protocol: Component | None = create_and_import_component(
            data,
            "Protokoll för administration på distans",
        )
        self.remote_administration_protocol = remote_administration_protocol

        # Antal WAN-portar
        number_of_wan_ports: Component | None = create_and_import_component(data, "Antal WAN-portar")
        self.number_of_wan_ports = number_of_wan_ports

        # Nätverksprotokoll
        network_protocol: Component | None = create_and_import_component(data, "Nätverksprotokoll")
        self.network_protocol = network_protocol

        # Inbyggd Switch
        builtin_switch: Component | None = create_and_import_component(data, "Inbyggd Switch")
        self.builtin_switch = builtin_switch

        # Viktiga funktioner
        important_functions: Component | None = create_and_import_component(data, "Viktiga funktioner")
        self.important_functions = important_functions

        # Nätverksgränssnitt
        network_interface: Component | None = create_and_import_component(data, "Nätverksgränssnitt")
        self.network_interface = network_interface

        # Avancerad omkoppling
        advanced_switching: Component | None = create_and_import_component(data, "Avancerad omkoppling")
        self.advanced_switching = advanced_switching

        # Gränssnitt för fjärradministration
        remote_management_interface: Component | None = create_and_import_component(
            data,
            "Gränssnitt för fjärradministration",
        )
        self.remote_management_interface = remote_management_interface

        # Max område inomhus
        max_area_indoor: Component | None = create_and_import_component(data, "Max område inomhus")
        self.max_area_indoor = max_area_indoor

        # Trådlös anslutning
        wireless_connection: Component | None = create_and_import_component(data, "Trådlös anslutning")
        self.wireless_connection = wireless_connection

        # LAN-presentation och trådlös d:o
        lan_presentation_and_wireless_d_o: Component | None = create_and_import_component(
            data,
            "LAN-presentation och trådlös d:o",
        )
        self.lan_presentation_and_wireless_d_o = lan_presentation_and_wireless_d_o

        # Bildöverföringsprotokoll för LAN och trådlöst
        image_transfer_protocol_for_lan_and_wireless: Component | None = create_and_import_component(
            data,
            "Bildöverföringsprotokoll för LAN och trådlöst",
        )
        self.image_transfer_protocol_for_lan_and_wireless = image_transfer_protocol_for_lan_and_wireless

        # Stöd för Wireless LAN
        support_for_wireless_lan: Component | None = create_and_import_component(data, "Stöd för Wireless LAN")
        self.support_for_wireless_lan = support_for_wireless_lan

        # Molnhanterad
        cloud_managed: Component | None = create_and_import_component(data, "Molnhanterad")
        self.cloud_managed = cloud_managed

        # Trådprotokoll
        wire_protocol: Component | None = create_and_import_component(data, "Trådprotokoll")
        self.wire_protocol = wire_protocol


class SpeakerSystem(auto_prefetch.Model):
    """Högtalarsystem."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the speaker system was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the speaker system was last updated")

    # Webhallen fields
    connection_technology = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Connection technology",
        related_name="speaker_system_connection_technology",
    )
    amplification_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Amplification type",
        related_name="speaker_system_amplification_type",
    )
    speaker_configuration = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Speaker configuration",
        related_name="speaker_system_speaker_configuration",
    )
    continuous_current_for_sound_system_total = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Continuous current for sound system total",
        related_name="speaker_system_continuous_current_for_sound_system_total",
    )
    system_components = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="System components",
        related_name="speaker_system_system_components",
    )
    peak_current_for_sound_system_total = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Peak current for sound system total",
        related_name="speaker_system_peak_current_for_sound_system_total",
    )
    frequency_response = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Frequency response",
        related_name="speaker_system_frequency_response",
    )
    builtin_decoders = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Built-in decoders",
        related_name="speaker_system_builtin_decoders",
    )
    number_of_crossover_channels = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Number of crossover channels",
        related_name="speaker_system_number_of_crossover_channels",
    )
    continuous_current = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Continuous current",
        related_name="speaker_system_continuous_current",
    )
    handsfree_function = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Hands-free function",
        related_name="speaker_system_handsfree_function",
    )
    app_controlled = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="App controlled",
        related_name="speaker_system_app_controlled",
    )
    recommended_location = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Recommended location",
        related_name="speaker_system_recommended_location",
    )
    multiple_rooms = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Multiple rooms",
        related_name="speaker_system_multiple_rooms",
    )
    series = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Series",
        related_name="speaker_system_series",
    )
    speaker_element_diameter_metric = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Speaker element diameter metric",
        related_name="speaker_system_speaker_element_diameter_metric",
    )
    integrated_components = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Integrated components",
        related_name="speaker_system_integrated_components",
    )
    peak_current = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Peak current",
        related_name="speaker_system_peak_current",
    )

    def __str__(self) -> str:
        return "Speaker system"

    def import_json(self, data: dict) -> None:  # noqa: PLR0914
        """Import JSON data."""
        # Anslutningsteknik
        connection_technology: Component | None = create_and_import_component(data, "Anslutningsteknik")
        self.connection_technology = connection_technology

        # Förstärkningstyp
        amplification_type: Component | None = create_and_import_component(data, "Förstärkningstyp")
        self.amplification_type = amplification_type

        # Konfigurering av högtalarsystem
        speaker_configuration: Component | None = create_and_import_component(data, "Konfigurering av högtalarsystem")
        self.speaker_configuration = speaker_configuration

        # Kontinuerlig ström för ljudsystem (totalt)
        continuous_current_for_sound_system_total: Component | None = create_and_import_component(
            data,
            "Kontinuerlig ström för ljudsystem (totalt)",
        )
        self.continuous_current_for_sound_system_total = continuous_current_for_sound_system_total

        # Systemkomponenter
        system_components: Component | None = create_and_import_component(data, "Systemkomponenter")
        self.system_components = system_components

        # Toppström för ljudsystem (totalt)
        peak_current_for_sound_system_total: Component | None = create_and_import_component(
            data,
            "Toppström för ljudsystem (totalt)",
        )
        self.peak_current_for_sound_system_total = peak_current_for_sound_system_total

        # Frekvensrespons
        frequency_response: Component | None = create_and_import_component(data, "Frekvensrespons")
        self.frequency_response = frequency_response

        # Inbyggda avkodare
        builtin_decoders: Component | None = create_and_import_component(data, "Inbyggda avkodare")
        self.builtin_decoders = builtin_decoders

        # Antal övergångskanaler
        number_of_crossover_channels: Component | None = create_and_import_component(data, "Antal övergångskanaler")
        self.number_of_crossover_channels = number_of_crossover_channels

        # Kontinuerlig ström
        continuous_current: Component | None = create_and_import_component(data, "Kontinuerlig ström")
        self.continuous_current = continuous_current

        # Handsfree-funktion
        handsfree_function: Component | None = create_and_import_component(data, "Handsfree-funktion")
        self.handsfree_function = handsfree_function

        # App-kontrollerad
        app_controlled: Component | None = create_and_import_component(data, "App-kontrollerad")
        self.app_controlled = app_controlled

        # Rekommenderad placering
        recommended_location: Component | None = create_and_import_component(data, "Rekommenderad placering")
        self.recommended_location = recommended_location

        # Flera rum
        multiple_rooms: Component | None = create_and_import_component(data, "Flera rum")
        self.multiple_rooms = multiple_rooms

        # Serie
        series: Component | None = create_and_import_component(data, "Serie")
        self.series = series

        # Högtalarelementdiameter (metrisk)
        speaker_element_diameter_metric: Component | None = create_and_import_component(
            data,
            "Högtalarelementdiameter (metrisk)",
        )
        self.speaker_element_diameter_metric = speaker_element_diameter_metric

        # Integrerade komponenter
        integrated_components: Component | None = create_and_import_component(data, "Integrerade komponenter")
        self.integrated_components = integrated_components

        # Toppström
        peak_current: Component | None = create_and_import_component(data, "Toppström")
        self.peak_current = peak_current


class SoundSystem(auto_prefetch.Model):
    """Sound system."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the sound system was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the sound system was last updated")

    # Webhallen fields
    designed_for = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Designed for",
        related_name="sound_system_designed_for",
    )
    type = models.ForeignKey(Component, on_delete=models.CASCADE, help_text="Type", related_name="sound_system_type")
    recommended_use = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Recommended use",
        related_name="sound_system_recommended_use",
    )
    mode_for_audio_output = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Mode for audio output",
        related_name="sound_system_mode_for_audio_output",
    )
    functions = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Functions",
        related_name="sound_system_functions",
    )
    max_actuation_distance = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Max actuation distance",
        related_name="sound_system_max_actuation_distance",
    )
    sub_category = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Subcategory",
        related_name="sound_system_sub_category",
    )
    surround_sound_effects = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Surround sound effects",
        related_name="sound_system_surround_sound_effects",
    )
    builtin_decoders = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Built-in decoders",
        related_name="sound_system_builtin_decoders",
    )
    surround_system_class = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Surround system class",
        related_name="sound_system_surround_system_class",
    )
    speaker_system = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Speaker system",
        related_name="sound_system_speaker_system",
    )
    surround_mode = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Surround mode",
        related_name="sound_system_surround_mode",
    )
    digital_player_features = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Digital player features",
        related_name="sound_system_digital_player_features",
    )
    digital_audio_format = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Digital audio format",
        related_name="sound_system_digital_audio_format",
    )
    combined_with = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Combined with",
        related_name="sound_system_combined_with",
    )
    type_of_digital_player = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Type of digital player",
        related_name="sound_system_type_of_digital_player",
    )
    audio_format = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Audio format",
        related_name="sound_system_audio_format",
    )

    def __str__(self) -> str:
        return "Sound system"

    def import_json(self, data: dict) -> None:  # noqa: PLR0914
        """Import JSON data."""
        # Designad för
        designed_for: Component | None = create_and_import_component(data, "Designad för")
        self.designed_for = designed_for

        # Typ
        _type: Component | None = create_and_import_component(data, "Typ")
        self.type = _type

        # Rekommenderad användning
        recommended_use: Component | None = create_and_import_component(data, "Rekommenderad användning")
        self.recommended_use = recommended_use

        # Läge för ljudutgång
        mode_for_audio_output: Component | None = create_and_import_component(data, "Läge för ljudutgång")
        self.mode_for_audio_output = mode_for_audio_output

        # Funktioner
        functions: Component | None = create_and_import_component(data, "Funktioner")
        self.functions = functions

        # Max manöveravstånd
        max_actuation_distance: Component | None = create_and_import_component(data, "Max manöveravstånd")
        self.max_actuation_distance = max_actuation_distance

        # Underkategori
        sub_category: Component | None = create_and_import_component(data, "Underkategori")
        self.sub_category = sub_category

        # Surround-ljudeffekter
        surround_sound_effects: Component | None = create_and_import_component(data, "Surround-ljudeffekter")
        self.surround_sound_effects = surround_sound_effects

        # Inbyggda avkodare
        builtin_decoders: Component | None = create_and_import_component(data, "Inbyggda avkodare")
        self.builtin_decoders = builtin_decoders

        # Surroundsystem-klass
        surround_system_class: Component | None = create_and_import_component(data, "Surroundsystem-klass")
        self.surround_system_class = surround_system_class

        # Högtalarsystem
        speaker_system: Component | None = create_and_import_component(data, "Högtalarsystem")
        self.speaker_system = speaker_system

        # Surround-läge
        surround_mode: Component | None = create_and_import_component(data, "Surround-läge")
        self.surround_mode = surround_mode

        # Digitalspelarfunktioner
        digital_player_features: Component | None = create_and_import_component(data, "Digitalspelarfunktioner")
        self.digital_player_features = digital_player_features

        # Digialt ljudformat [sic]
        digital_audio_format: Component | None = create_and_import_component(data, "Digialt ljudformat")
        self.digital_audio_format = digital_audio_format

        # Kombinerad med
        combined_with: Component | None = create_and_import_component(data, "Kombinerad med")
        self.combined_with = combined_with

        # Typ av digitalspelare
        type_of_digital_player: Component | None = create_and_import_component(data, "Typ av digitalspelare")
        self.type_of_digital_player = type_of_digital_player

        # Ljudformat
        audio_format: Component | None = create_and_import_component(data, "Ljudformat")
        self.audio_format = audio_format


class PowerSupply(auto_prefetch.Model):
    """Nätdel."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the power supply was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the power supply was last updated")

    # Webhallen fields
    power_source = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Power source",
        related_name="power_supply_power_source",
    )
    power = models.ForeignKey(Component, on_delete=models.CASCADE, help_text="Power", related_name="power_supply_power")
    capacity_va = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Capacity (VA)",
        related_name="power_supply_capacity_va",
    )
    number_of_outlets = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Number of outlets",
        related_name="power_supply_number_of_outlets",
    )
    supplied_voltage = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Supplied voltage",
        related_name="power_supply_supplied_voltage",
    )
    mains_voltage = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Mains voltage",
        related_name="power_supply_mains_voltage",
    )
    ups_technology = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="UPS technology",
        related_name="power_supply_ups_technology",
    )
    form_factor = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Form factor",
        related_name="power_supply_form_factor",
    )
    voltage_dissipation = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Voltage dissipation",
        related_name="power_supply_voltage_dissipation",
    )
    demanded_frequency = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Required frequency",
        related_name="power_supply_demanded_frequency",
    )
    demanded_voltage = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Required voltage",
        related_name="power_supply_demanded_voltage",
    )
    max_electric_current = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Max electric current",
        related_name="power_supply_max_electric_current",
    )
    type = models.ForeignKey(Component, on_delete=models.CASCADE, help_text="Type", related_name="power_supply_type")
    required_frequency = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Required frequency",
        related_name="power_supply_required_frequency",
    )
    type_of_input_connector = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Type of input connector",
        related_name="power_supply_type_of_input_connector",
    )
    number_of_input_connectors = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Number of input connectors",
        related_name="power_supply_number_of_input_connectors",
    )
    type_of_output_contact = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Type of output contact",
        related_name="power_supply_type_of_output_contact",
    )
    modular_cable_management = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Modular cable management",
        related_name="power_supply_modular_cable_management",
    )
    power_supply_compatibility = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Power supply compatibility",
        related_name="power_supply_power_supply_compatibility",
    )
    cooling_system = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Cooling system",
        related_name="power_supply_cooling_system",
    )
    the_80_plus_certification = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="The 80 PLUS certification",
        related_name="power_supply_the_80_plus_certification",
    )
    alternative = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Alternative",
        related_name="power_supply_alternative",
    )
    cord_length = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Cord length",
        related_name="power_supply_cord_length",
    )
    energy_consumption_during_operation = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Energy consumption during operation",
        related_name="power_supply_energy_consumption_during_operation",
    )

    def __str__(self) -> str:
        return "Power supply"

    def import_json(self, data: dict) -> None:  # noqa: PLR0914
        """Import JSON data."""
        # Strömkälla
        power_source: Component | None = create_and_import_component(data, "Strömkälla")
        self.power_source = power_source

        # Effekt
        power: Component | None = create_and_import_component(data, "Effekt")
        self.power = power

        # Kapacitet (VA)
        capacity_va: Component | None = create_and_import_component(data, "Kapacitet (VA)")
        self.capacity_va = capacity_va

        # Antal utkontakter
        number_of_outlets: Component | None = create_and_import_component(data, "Antal utkontakter")
        self.number_of_outlets = number_of_outlets

        # Tillförd spänning
        supplied_voltage: Component | None = create_and_import_component(data, "Tillförd spänning")
        self.supplied_voltage = supplied_voltage

        # Nätspänning
        mains_voltage: Component | None = create_and_import_component(data, "Nätspänning")
        self.mains_voltage = mains_voltage

        # UPS-teknik
        ups_technology: Component | None = create_and_import_component(data, "UPS-teknik")
        self.ups_technology = ups_technology

        # Formfaktor
        form_factor: Component | None = create_and_import_component(data, "Formfaktor")
        self.form_factor = form_factor

        # Spänningsavledning
        voltage_dissipation: Component | None = create_and_import_component(data, "Spänningsavledning")
        self.voltage_dissipation = voltage_dissipation

        # Erfordrad frekvens
        demanded_frequency: Component | None = create_and_import_component(data, "Erfordrad frekvens")
        self.demanded_frequency = demanded_frequency

        # Erfordrad spänning
        demanded_voltage: Component | None = create_and_import_component(data, "Erfordrad spänning")
        self.demanded_voltage = demanded_voltage

        # Max elektrisk ström
        max_electric_current: Component | None = create_and_import_component(data, "Max elektrisk ström")
        self.max_electric_current = max_electric_current

        # Typ
        _type: Component | None = create_and_import_component(data, "Typ")
        self.type = _type

        # Erforderlig frekvens
        required_frequency: Component | None = create_and_import_component(data, "Erforderlig frekvens")
        self.required_frequency = required_frequency

        # Typ av ingångskontakt
        type_of_input_connector: Component | None = create_and_import_component(data, "Typ av ingångskontakt")
        self.type_of_input_connector = type_of_input_connector

        # Antal ingångskontakter
        number_of_input_connectors: Component | None = create_and_import_component(data, "Antal ingångskontakter")
        self.number_of_input_connectors = number_of_input_connectors

        # Typ av utkontakt
        type_of_output_contact: Component | None = create_and_import_component(data, "Typ av utkontakt")
        self.type_of_output_contact = type_of_output_contact

        # Modulär kabelhantering
        modular_cable_management: Component | None = create_and_import_component(data, "Modulär kabelhantering")
        self.modular_cable_management = modular_cable_management

        # Nätaggregatets kompatibilitet
        power_supply_compatibility: Component | None = create_and_import_component(
            data,
            "Nätaggregatets kompatibilitet",
        )
        self.power_supply_compatibility = power_supply_compatibility

        # Kylsystem
        cooling_system: Component | None = create_and_import_component(data, "Kylsystem")
        self.cooling_system = cooling_system

        # 80 PLUS-certifiering
        the_80_plus_certification: Component | None = create_and_import_component(data, "80 PLUS-certifiering")
        self.the_80_plus_certification = the_80_plus_certification

        # Alternativ
        alternative: Component | None = create_and_import_component(data, "Alternativ")
        self.alternative = alternative

        # Sladdlängd
        cord_length: Component | None = create_and_import_component(data, "Sladdlängd")
        self.cord_length = cord_length

        # Energiförbrukning vid drift
        energy_consumption_during_operation: Component | None = create_and_import_component(
            data,
            "Energiförbrukning vid drift",
        )
        self.energy_consumption_during_operation = energy_consumption_during_operation


class SettingsControlsAndIndicators(auto_prefetch.Model):
    """Inställningar, reglage och indikatorer."""

    # Django fields
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the settings, controls and indicators was created",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When the settings, controls and indicators was last updated",
    )

    # Webhallen fields
    number_of_fan_speed_settings = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Number of fan speed settings",
        related_name="settings_controls_and_indicators_number_of_fan_speed_settings",
    )
    remote_control = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Remote control",
        related_name="settings_controls_and_indicators_remote_control",
    )
    control_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Control type",
        related_name="settings_controls_and_indicators_control_type",
    )
    pulse_function = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Pulse function",
        related_name="settings_controls_and_indicators_pulse_function",
    )
    number_of_speed_settings = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Number of speed settings",
        related_name="settings_controls_and_indicators_number_of_speed_settings",
    )
    room_navigation = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Room navigation",
        related_name="settings_controls_and_indicators_room_navigation",
    )
    heating_time = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Heating time",
        related_name="settings_controls_and_indicators_heating_time",
    )
    programmable_cleaning_intervals = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Programmable cleaning intervals",
        related_name="settings_controls_and_indicators_programmable_cleaning_intervals",
    )
    controls_on_handle = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Controls on handle",
        related_name="settings_controls_and_indicators_controls_on_handle",
    )

    def __str__(self) -> str:
        return "Settings, controls and indicators"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Antal fläkthastighetsinställningar
        number_of_fan_speed_settings: Component | None = create_and_import_component(
            data,
            "Antal fläkthastighetsinställningar",
        )
        self.number_of_fan_speed_settings = number_of_fan_speed_settings

        # Fjärrkontroll
        remote_control: Component | None = create_and_import_component(data, "Fjärrkontroll")
        self.remote_control = remote_control

        # Reglagetyp
        control_type: Component | None = create_and_import_component(data, "Reglagetyp")
        self.control_type = control_type

        # Pulsfunktion
        pulse_function: Component | None = create_and_import_component(data, "Pulsfunktion")
        self.pulse_function = pulse_function

        # Antal hastighetsinställningar
        number_of_speed_settings: Component | None = create_and_import_component(data, "Antal hastighetsinställningar")
        self.number_of_speed_settings = number_of_speed_settings

        # Rumsnavigering
        room_navigation: Component | None = create_and_import_component(data, "Rumsnavigering")
        self.room_navigation = room_navigation

        # Uppvärmningstid
        heating_time: Component | None = create_and_import_component(data, "Uppvärmningstid")
        self.heating_time = heating_time

        # Programmerbara rengöringsintervall
        programmable_cleaning_intervals: Component | None = create_and_import_component(
            data,
            "Programmerbara rengöringsintervall",
        )
        self.programmable_cleaning_intervals = programmable_cleaning_intervals

        # Kontroller på handtaget
        controls_on_handle: Component | None = create_and_import_component(data, "Kontroller på handtaget")
        self.controls_on_handle = controls_on_handle


class Power(auto_prefetch.Model):
    """Ström."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the power was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the power was last updated")

    # Webhallen fields
    power_consumption = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Power consumption",
        related_name="power_power_consumption",
    )
    power_source = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Power source",
        related_name="power_power_source",
    )
    voltage = models.ForeignKey(Component, on_delete=models.CASCADE, help_text="Voltage", related_name="power_voltage")
    battery_charge = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Battery charge",
        related_name="power_battery_charge",
    )
    operation_time_without_mains = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Operation time without mains",
        related_name="power_operation_time_without_mains",
    )
    operation = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Operation",
        related_name="power_operation",
    )
    energy_consumption_per_year = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Energy consumption per year",
        related_name="power_energy_consumption_per_year",
    )
    power_consumption_operating_mode = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Power consumption operating mode",
        related_name="power_power_consumption_operating_mode",
    )
    energy_class = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Energy class",
        related_name="power_energy_class",
    )
    on_off_switch = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="On/off switch",
        related_name="power_on_off_switch",
    )
    power_consumption_hdr_on_mode = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Power consumption HDR on mode",
        related_name="power_power_consumption_hdr_on_mode",
    )
    energy_class_hdr = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Energy class HDR",
        related_name="power_energy_class_hdr",
    )
    energy_efficiency_ratio = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="EER (Energy Efficiency Ratio)",
        related_name="power_energy_efficiency_ratio",
    )
    ampere_capacity = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="https://en.wikipedia.org/wiki/Ampacity",
        related_name="power_ampere_capacity",
    )

    def __str__(self) -> str:
        return "Power"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Strömförbrukning
        power_consumption: Component | None = create_and_import_component(data, "Strömförbrukning")
        self.power_consumption = power_consumption

        # Strömkälla
        power_source: Component | None = create_and_import_component(data, "Strömkälla")
        self.power_source = power_source

        # Spänning
        voltage: Component | None = create_and_import_component(data, "Spänning")
        self.voltage = voltage

        # Batteriladdning
        battery_charge: Component | None = create_and_import_component(data, "Batteriladdning")
        self.battery_charge = battery_charge

        # Driftstid utan nätanslutning
        operation_time_without_mains: Component | None = create_and_import_component(
            data,
            "Driftstid utan nätanslutning",
        )
        self.operation_time_without_mains = operation_time_without_mains

        # Drift
        operation: Component | None = create_and_import_component(data, "Drift")
        self.operation = operation

        # Energikonsumtion per år
        energy_consumption_per_year: Component | None = create_and_import_component(
            data,
            "Energikonsumtion per år",
        )
        self.energy_consumption_per_year = energy_consumption_per_year

        # Strömkonsumtion (driftläge)
        power_consumption_operating_mode: Component | None = create_and_import_component(
            data,
            "Strömkonsumtion (driftläge)",
        )
        self.power_consumption_operating_mode = power_consumption_operating_mode

        # Energiklass
        energy_class: Component | None = create_and_import_component(data, "Energiklass")
        self.energy_class = energy_class

        # På/av-omkopplare
        on_off_switch: Component | None = create_and_import_component(data, "På/av-omkopplare")
        self.on_off_switch = on_off_switch

        # Strömförbrukning HDR (På-läge)
        power_consumption_hdr_on_mode: Component | None = create_and_import_component(
            data,
            "Strömförbrukning HDR (På-läge)",
        )
        self.power_consumption_hdr_on_mode = power_consumption_hdr_on_mode

        # Energiklass (HDR)
        energy_class_hdr: Component | None = create_and_import_component(data, "Energiklass (HDR)")
        self.energy_class_hdr = energy_class_hdr

        # (EER) Energy Efficiency Ratio
        energy_efficiency_ratio: Component | None = create_and_import_component(
            data,
            "(EER) Energy Efficiency Ratio",
        )
        self.energy_efficiency_ratio = energy_efficiency_ratio

        # Märkström
        ampere_capacity: Component | None = create_and_import_component(data, "Märkström")
        self.ampere_capacity = ampere_capacity


class HeatingAndCooling(auto_prefetch.Model):
    """Värme och kyla."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the heating and cooling was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the heating and cooling was last updated")

    # Webhallen fields
    product_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Product type",
        related_name="heating_and_cooling_product_type",
    )
    model = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Model",
        related_name="heating_and_cooling_model",
    )
    functions = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Functions",
        related_name="heating_and_cooling_functions",
    )
    air_flow = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Air flow",
        related_name="heating_and_cooling_air_flow",
    )
    container_capacity = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Container capacity",
        related_name="heating_and_cooling_container_capacity",
    )
    environment = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Environment",
        related_name="heating_and_cooling_environment",
    )
    air_flow_control = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Air flow control",
        related_name="heating_and_cooling_air_flow_control",
    )
    heating_capacity = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Heating capacity",
        related_name="heating_and_cooling_heating_capacity",
    )
    max_dehumidification_capacity = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Max dehumidification capacity",
        related_name="heating_and_cooling_max_dehumidification_capacity",
    )
    cooling_capacity = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Cooling capacity",
        related_name="heating_and_cooling_cooling_capacity",
    )
    cooling_capacity_btu_per_hour = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Cooling capacity (BTU per hour)",
        related_name="heating_and_cooling_cooling_capacity_btu_per_hour",
    )

    def __str__(self) -> str:
        return "Heating and cooling"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Produkttyp
        product_type: Component | None = create_and_import_component(data, "Produkttyp")
        self.product_type = product_type

        # Modell
        model: Component | None = create_and_import_component(data, "Modell")
        self.model = model

        # Funktioner
        functions: Component | None = create_and_import_component(data, "Funktioner")
        self.functions = functions

        # Luftflöde
        air_flow: Component | None = create_and_import_component(data, "Luftflöde")
        self.air_flow = air_flow

        # Behållarkapacitet
        container_capacity: Component | None = create_and_import_component(data, "Behållarkapacitet")
        self.container_capacity = container_capacity

        # Miljö
        environment: Component | None = create_and_import_component(data, "Miljö")
        self.environment = environment

        # Luftflödeskontroll
        air_flow_control: Component | None = create_and_import_component(data, "Luftflödeskontroll")
        self.air_flow_control = air_flow_control

        # Uppvärmningskapacitet (kW)
        heating_capacity: Component | None = create_and_import_component(data, "Uppvärmningskapacitet (kW)")
        self.heating_capacity = heating_capacity

        # Max avfuktningskapacitet
        max_dehumidification_capacity: Component | None = create_and_import_component(
            data,
            "Max avfuktningskapacitet",
        )
        self.max_dehumidification_capacity = max_dehumidification_capacity

        # Kylningskapacitet (kW)
        cooling_capacity: Component | None = create_and_import_component(data, "Kylningskapacitet (kW)")
        self.cooling_capacity = cooling_capacity

        # Kylningskapacitet (BTU/tim)
        cooling_capacity_btu_per_hour: Component | None = create_and_import_component(
            data,
            "Kylningskapacitet (BTU/tim)",
        )
        self.cooling_capacity_btu_per_hour = cooling_capacity_btu_per_hour


class RAM(auto_prefetch.Model):
    """Random access memory (RAM)."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the RAM was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the RAM was last updated")

    # Webhallen fields
    data_integrity_check = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Data integrity check",
        related_name="ram_data_integrity_check",
    )
    upgrade_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Upgrade type",
        related_name="ram_upgrade_type",
    )
    type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Type",
        related_name="ram_type",
    )
    memory_speed = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Memory speed",
        related_name="ram_memory_speed",
    )
    registered_or_buffered = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Registered or buffered",
        related_name="ram_registered_or_buffered",
    )
    ram_technology = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="RAM technology",
        related_name="ram_ram_technology",
    )
    cas_latency = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="CAS latency",
        related_name="ram_cas_latency",
    )
    adaptation_to_memory_specifications = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Adaptation to memory specifications",
        related_name="ram_adaptation_to_memory_specifications",
    )
    form_factor = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Form factor",
        related_name="ram_form_factor",
    )
    storage_capacity = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Storage capacity",
        related_name="ram_storage_capacity",
    )
    product_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Product type",
        related_name="ram_product_type",
    )
    memory_size = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Frame size",
        related_name="ram_memory_size",
    )
    empty_slots = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Empty slots",
        related_name="ram_empty_slots",
    )
    max_size_supported = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Max size supported",
        related_name="ram_max_size_supported",
    )
    internal_memory_ram = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Internal memory (RAM)",
        related_name="ram_internal_memory_ram",
    )
    number_of_slots = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Number of slots",
        related_name="ram_number_of_slots",
    )
    properties = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Properties",
        related_name="ram_properties",
    )
    low_profile = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Low profile",
        related_name="ram_low_profile",
    )

    def __str__(self) -> str:
        return "RAM"

    def import_json(self, data: dict) -> None:  # noqa: PLR0914
        """Import JSON data."""
        # Data Integrity Check
        data_integrity_check: Component | None = create_and_import_component(data, "Data Integrity Check")
        self.data_integrity_check = data_integrity_check

        # Uppgraderingstyp
        upgrade_type: Component | None = create_and_import_component(data, "Uppgraderingstyp")
        self.upgrade_type = upgrade_type

        # Typ
        _type: Component | None = create_and_import_component(data, "Typ")
        self.type = _type

        # Minneshastighet
        memory_speed: Component | None = create_and_import_component(data, "Minneshastighet")
        self.memory_speed = memory_speed

        # Registrerat eller buffrat
        registered_or_buffered: Component | None = create_and_import_component(data, "Registrerat eller buffrat")
        self.registered_or_buffered = registered_or_buffered

        # RAM Teknik
        ram_technology: Component | None = create_and_import_component(data, "RAM Teknik")
        self.ram_technology = ram_technology

        # CAS Latency
        cas_latency: Component | None = create_and_import_component(data, "CAS Latency")
        self.cas_latency = cas_latency

        # Anpassning till minnesspecifikationer
        adaptation_to_memory_specifications: Component | None = create_and_import_component(
            data,
            "Anpassning till minnesspecifikationer",
        )
        self.adaptation_to_memory_specifications = adaptation_to_memory_specifications

        # Formfaktor
        form_factor: Component | None = create_and_import_component(data, "Formfaktor")
        self.form_factor = form_factor

        # Lagringskapacitet
        storage_capacity: Component | None = create_and_import_component(data, "Lagringskapacitet")
        self.storage_capacity = storage_capacity

        # Produkttyp
        product_type: Component | None = create_and_import_component(data, "Produkttyp")
        self.product_type = product_type

        # RAM storlek
        memory_size: Component | None = create_and_import_component(data, "RAM storlek")
        self.memory_size = memory_size

        # Tomma kortplatser
        empty_slots: Component | None = create_and_import_component(data, "Tomma kortplatser")
        self.empty_slots = empty_slots

        # Maxstorlek som stöds
        max_size_supported: Component | None = create_and_import_component(data, "Maxstorlek som stöds")
        self.max_size_supported = max_size_supported

        # Internminne (RAM)
        internal_memory_ram: Component | None = create_and_import_component(data, "Internminne (RAM)")
        self.internal_memory_ram = internal_memory_ram

        # Antal kortplatser
        number_of_slots: Component | None = create_and_import_component(data, "Antal kortplatser")
        self.number_of_slots = number_of_slots

        # Egenskaper
        properties: Component | None = create_and_import_component(data, "Egenskaper")
        self.properties = properties

        # Lågt (RAM)
        low_profile: Component | None = create_and_import_component(data, "Lågt (RAM)")
        self.low_profile = low_profile


class AudioOutput(auto_prefetch.Model):
    """Ljudutgång."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the audio output was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the audio output was last updated")

    # Webhallen fields
    form_factor = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Form factor",
        related_name="audio_output_form_factor",
    )
    type = models.ForeignKey(Component, on_delete=models.CASCADE, help_text="Type", related_name="audio_output_type")
    interface_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Interface type",
        related_name="audio_output_interface_type",
    )
    audio_output_mode = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Audio output mode",
        related_name="audio_output_audio_output_mode",
    )
    connection_technology = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Connection technology",
        related_name="audio_output_connection_technology",
    )
    controls = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Controls",
        related_name="audio_output_controls",
    )
    headphone_ear_parts_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Headphone ear parts type",
        related_name="audio_output_headphone_ear_parts_type",
    )
    headphone_cup_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Headphone cup type",
        related_name="audio_output_headphone_cup_type",
    )
    available_microphone = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Available microphone",
        related_name="audio_output_available_microphone",
    )
    interface_connector = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Interface connector",
        related_name="audio_output_interface_connector",
    )
    frequency_response = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Frequency response",
        related_name="audio_output_frequency_response",
    )
    impedance = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Impedance",
        related_name="audio_output_impedance",
    )
    product_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Product type",
        related_name="audio_output_product_type",
    )
    wireless_technology = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Wireless technology",
        related_name="audio_output_wireless_technology",
    )
    anc = models.ForeignKey(Component, on_delete=models.CASCADE, help_text="ANC", related_name="audio_output_anc")
    dac_resolution = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="DAC resolution",
        related_name="audio_output_dac_resolution",
    )
    max_sampling_rate = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Max sampling rate",
        related_name="audio_output_max_sampling_rate",
    )
    signal_processor = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Signal processor",
        related_name="audio_output_signal_processor",
    )
    headphone_mount = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Headphone mount",
        related_name="audio_output_headphone_mount",
    )
    foldable = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Foldable",
        related_name="audio_output_foldable",
    )
    sound_isolating = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Sound isolating",
        related_name="audio_output_sound_isolating",
    )
    nfc_near_field_communication = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="NFC (Near Field Communication)",
        related_name="audio_output_nfc_near_field_communication",
    )
    style = models.ForeignKey(Component, on_delete=models.CASCADE, help_text="Style", related_name="audio_output_style")
    output_per_channel = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Output per channel",
        related_name="audio_output_output_per_channel",
    )

    def __str__(self) -> str:
        return "Audio output"

    def import_json(self, data: dict) -> None:  # noqa: PLR0914
        """Import JSON data."""
        # Formfaktor
        form_factor: Component | None = create_and_import_component(data, "Formfaktor")
        self.form_factor = form_factor

        # Typ
        _type: Component | None = create_and_import_component(data, "Typ")
        self.type = _type

        # Typ av gränssnitt
        interface_type: Component | None = create_and_import_component(data, "Typ av gränssnitt")
        self.interface_type = interface_type

        # Ljudutgångsläge
        audio_output_mode: Component | None = create_and_import_component(data, "Ljudutgångsläge")
        self.audio_output_mode = audio_output_mode

        # Anslutningsteknik
        connection_technology: Component | None = create_and_import_component(data, "Anslutningsteknik")
        self.connection_technology = connection_technology

        # Reglage
        controls: Component | None = create_and_import_component(data, "Reglage")
        self.controls = controls

        # Hörlurar, Ear-Parts-typ
        headphone_ear_parts_type: Component | None = create_and_import_component(data, "Hörlurar, Ear-Parts-typ")
        self.headphone_ear_parts_type = headphone_ear_parts_type

        # Hörlurar, kopptyp
        headphone_cup_type: Component | None = create_and_import_component(data, "Hörlurar, kopptyp")
        self.headphone_cup_type = headphone_cup_type

        # Tillgänglig mikrofon
        available_microphone: Component | None = create_and_import_component(data, "Tillgänglig mikrofon")
        self.available_microphone = available_microphone

        # Kopplingsgränssnitt
        interface_connector: Component | None = create_and_import_component(data, "Kopplingsgränssnitt")
        self.interface_connector = interface_connector

        # Frekvensrespons
        frequency_response: Component | None = create_and_import_component(data, "Frekvensrespons")
        self.frequency_response = frequency_response

        # Impedans
        impedance: Component | None = create_and_import_component(data, "Impedans")
        self.impedance = impedance

        # Produkttyp
        product_type: Component | None = create_and_import_component(data, "Produkttyp")
        self.product_type = product_type

        # Trådlös teknik
        wireless_technology: Component | None = create_and_import_component(data, "Trådlös teknik")
        self.wireless_technology = wireless_technology

        # ANC
        anc: Component | None = create_and_import_component(data, "ANC")
        self.anc = anc

        # DAC-upplösning
        dac_resolution: Component | None = create_and_import_component(data, "DAC-upplösning")
        self.dac_resolution = dac_resolution

        # Max. samplingsfrekvens
        max_sampling_rate: Component | None = create_and_import_component(data, "Max. samplingsfrekvens")
        self.max_sampling_rate = max_sampling_rate

        # Signalprocessor
        signal_processor: Component | None = create_and_import_component(data, "Signalprocessor")
        self.signal_processor = signal_processor

        # Hörlursmontering
        headphone_mount: Component | None = create_and_import_component(data, "Hörlursmontering")
        self.headphone_mount = headphone_mount

        # Fällbar
        foldable: Component | None = create_and_import_component(data, "Fällbar")
        self.foldable = foldable

        # Ljudisolerande
        sound_isolating: Component | None = create_and_import_component(data, "Ljudisolerande")
        self.sound_isolating = sound_isolating

        # NFC (Near Field Communication)
        nfc_near_field_communication: Component | None = create_and_import_component(
            data,
            "NFC (Near Field Communication)",
        )
        self.nfc_near_field_communication = nfc_near_field_communication

        # Stil
        style: Component | None = create_and_import_component(data, "Stil")
        self.style = style

        # Uteffekt / kanal
        output_per_channel: Component | None = create_and_import_component(data, "Uteffekt / kanal")
        self.output_per_channel = output_per_channel


class HeatsinkAndFan(auto_prefetch.Model):
    """Kylfläns och fläkt."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the heatsink and fan was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the heatsink and fan was last updated")

    # Webhallen fields
    fan_diameter = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Fan diameter",
        related_name="heatsink_and_fan_fan_diameter",
    )
    power_connector = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Power connector",
        related_name="heatsink_and_fan_power_connector",
    )
    compatible_with = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Compatible with",
        related_name="heatsink_and_fan_compatible_with",
    )
    cooler_material = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Cooler material",
        related_name="heatsink_and_fan_cooler_material",
    )
    radiator_size = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Radiator size",
        related_name="heatsink_and_fan_radiator_size",
    )

    def __str__(self) -> str:
        return "Heatsink and fan"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Fläktdiameter
        fan_diameter: Component | None = create_and_import_component(data, "Fläktdiameter")
        self.fan_diameter = fan_diameter

        # Starkströmskontakt
        power_connector: Component | None = create_and_import_component(data, "Starkströmskontakt")
        self.power_connector = power_connector

        # Kompatibel med
        compatible_with: Component | None = create_and_import_component(data, "Kompatibel med")
        self.compatible_with = compatible_with

        # Kylarmaterial
        cooler_material: Component | None = create_and_import_component(data, "Kylarmaterial")
        self.cooler_material = cooler_material

        # Storlek på radiator
        radiator_size: Component | None = create_and_import_component(data, "Storlek på radiator")
        self.radiator_size = radiator_size


class Storage(auto_prefetch.Model):
    """Lagring."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the storage was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the storage was last updated")

    # Webhallen fields
    model = models.ForeignKey(Component, on_delete=models.CASCADE, help_text="Model", related_name="storage_model")
    type = models.ForeignKey(Component, on_delete=models.CASCADE, help_text="Type", related_name="storage_type")
    interface = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Interface",
        related_name="storage_interface",
    )
    device_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Device type",
        related_name="storage_device_type",
    )
    product_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Product type",
        related_name="storage_product_type",
    )
    iscsi_support = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="iSCSI support",
        related_name="storage_iscsi_support",
    )
    network_storage_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Network storage type",
        related_name="storage_network_storage_type",
    )
    total_storage_capacity = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Total storage capacity",
        related_name="storage_total_storage_capacity",
    )
    total_array_capacity = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Total array capacity",
        related_name="storage_total_array_capacity",
    )
    external_interface_for_disk_array = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="External interface for disk array",
        related_name="storage_external_interface_for_disk_array",
    )
    external_interface_class_for_disk_array = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="External interface class for disk array",
        related_name="storage_external_interface_class_for_disk_array",
    )

    def __str__(self) -> str:
        return "Storage"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Modell
        model: Component | None = create_and_import_component(data, "Modell")
        self.model = model

        # Typ
        _type: Component | None = create_and_import_component(data, "Typ")
        self.type = _type

        # Gränssnitt
        interface: Component | None = create_and_import_component(data, "Gränssnitt")
        self.interface = interface

        # Typ av enhet
        device_type: Component | None = create_and_import_component(data, "Typ av enhet")
        self.device_type = device_type

        # Produkttyp
        product_type: Component | None = create_and_import_component(data, "Produkttyp")
        self.product_type = product_type

        # iSCSI-stöd
        iscsi_support: Component | None = create_and_import_component(data, "iSCSI-stöd")
        self.iscsi_support = iscsi_support

        # Typ av nätverkslagring
        network_storage_type: Component | None = create_and_import_component(data, "Typ av nätverkslagring")
        self.network_storage_type = network_storage_type

        # Total lagringskapacitet
        total_storage_capacity: Component | None = create_and_import_component(data, "Total lagringskapacitet")
        self.total_storage_capacity = total_storage_capacity

        # Total array-kapacitet
        total_array_capacity: Component | None = create_and_import_component(data, "Total array-kapacitet")
        self.total_array_capacity = total_array_capacity

        # Externt gränssnitt för hårddiskarray
        external_interface_for_disk_array: Component | None = create_and_import_component(
            data,
            "Externt gränssnitt för hårddiskarray",
        )
        self.external_interface_for_disk_array = external_interface_for_disk_array

        # Extern gränssnitt klass för hårddiskarray
        external_interface_class_for_disk_array: Component | None = create_and_import_component(
            data,
            "Extern gränssnitt klass för hårddiskarray",
        )
        self.external_interface_class_for_disk_array = external_interface_class_for_disk_array


class PortableStorageSolution(auto_prefetch.Model):
    """Flyttbar lagringslösning."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the portable storage solution was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the portable storage solution was last updated")

    # Webhallen fields
    type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Type",
        related_name="portable_storage_solution_type",
    )

    def __str__(self) -> str:
        return "Portable storage solution"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Typ
        _type: Component | None = create_and_import_component(data, "Typ")
        self.type = _type


class OpticalStorageSecondary(auto_prefetch.Model):
    """Optisk lagring (sekundär)."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the optical storage secondary was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the optical storage secondary was last updated")

    # Webhallen fields
    type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Type",
        related_name="optical_storage_secondary_type",
    )

    def __str__(self) -> str:
        return "Optical storage secondary"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Typ
        _type: Component | None = create_and_import_component(data, "Typ")
        self.type = _type


class OpticalStorage(auto_prefetch.Model):
    """Optisk lagring."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the optical storage was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the optical storage was last updated")

    # Webhallen fields
    write_speed = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Write speed",
        related_name="optical_storage_write_speed",
    )
    read_speed = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Read speed",
        related_name="optical_storage_read_speed",
    )
    rewrite_speed = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Rewrite speed",
        related_name="optical_storage_rewrite_speed",
    )
    type = models.ForeignKey(Component, on_delete=models.CASCADE, help_text="Type", related_name="optical_storage_type")
    buffer_size = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Buffer size",
        related_name="optical_storage_buffer_size",
    )
    device_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Device type",
        related_name="optical_storage_device_type",
    )

    def __str__(self) -> str:
        return "Optical storage"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Skrivhastighet
        write_speed: Component | None = create_and_import_component(data, "Skrivhastighet")
        self.write_speed = write_speed

        # Läshastighet
        read_speed: Component | None = create_and_import_component(data, "Läshastighet")
        self.read_speed = read_speed

        # Återskrivningshastighet
        rewrite_speed: Component | None = create_and_import_component(data, "Återskrivningshastighet")
        self.rewrite_speed = rewrite_speed

        # Typ
        _type: Component | None = create_and_import_component(data, "Typ")
        self.type = _type

        # Bufferstorlek
        buffer_size: Component | None = create_and_import_component(data, "Bufferstorlek")
        self.buffer_size = buffer_size

        # Enhetstyp
        device_type: Component | None = create_and_import_component(data, "Enhetstyp")
        self.device_type = device_type


class MemoryModule(auto_prefetch.Model):
    """Minnesmodul."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the memory module was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the memory module was last updated")

    # Webhallen fields
    quantity_in_kit = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Quantity in kit",
        related_name="memory_module_quantity_in_kit",
    )

    def __str__(self) -> str:
        return "Memory module"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Antal i kit
        quantity_in_kit: Component | None = create_and_import_component(data, "Antal i kit")
        self.quantity_in_kit = quantity_in_kit


class Antenna(auto_prefetch.Model):
    """Antenn."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the antenna was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the antenna was last updated")

    # Webhallen fields
    antenna_placement_mounting = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Antenna placement mounting",
        related_name="antenna_antenna_placement_mounting",
    )
    compatibility = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Compatibility",
        related_name="antenna_compatibility",
    )
    form_factor = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Form factor",
        related_name="antenna_form_factor",
    )
    frequency_range = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Frequency range",
        related_name="antenna_frequency_range",
    )
    type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Type",
        related_name="antenna_type",
    )

    def __str__(self) -> str:
        return "Antenna"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Antennplacering/-montering
        antenna_placement_mounting: Component | None = create_and_import_component(data, "Antennplacering/-montering")
        self.antenna_placement_mounting = antenna_placement_mounting

        # Kompatibilitet
        compatibility: Component | None = create_and_import_component(data, "Kompatibilitet")
        self.compatibility = compatibility

        # Formfaktor
        form_factor: Component | None = create_and_import_component(data, "Formfaktor")
        self.form_factor = form_factor

        # Frekvensintervall
        frequency_range: Component | None = create_and_import_component(data, "Frekvensintervall")
        self.frequency_range = frequency_range

        # Typ
        _type: Component | None = create_and_import_component(data, "Typ")
        self.type = _type


class System(auto_prefetch.Model):
    """System."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the system was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the system was last updated")

    # Webhallen fields
    device_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Device type",
        related_name="system_device_type",
    )
    docking_interface = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Docking interface",
        related_name="system_docking_interface",
    )
    video_interface = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Video interface",
        related_name="system_video_interface",
    )
    generation = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Generation",
        related_name="system_generation",
    )
    hard_drive_capacity = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Hard drive capacity",
        related_name="system_hard_drive_capacity",
    )
    fingerprint_reader = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Fingerprint reader",
        related_name="system_fingerprint_reader",
    )
    platform = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Platform",
        related_name="system_platform",
    )
    embedded_security = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Embedded security",
        related_name="system_embedded_security",
    )
    notebook_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Notebook type",
        related_name="system_notebook_type",
    )
    handheld_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Handheld type",
        related_name="system_handheld_type",
    )
    introduced = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Introduced",
        related_name="system_introduced",
    )
    type = models.ForeignKey(Component, on_delete=models.CASCADE, help_text="Type", related_name="system_type")
    dockable = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Dockable",
        related_name="system_dockable",
    )
    platform_technology = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Platform technology",
        related_name="system_platform_technology",
    )

    def __str__(self) -> str:
        return "System"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Enhetstyp
        device_type: Component | None = create_and_import_component(data, "Enhetstyp")
        self.device_type = device_type

        # Dockningsgränssnitt
        docking_interface: Component | None = create_and_import_component(data, "Dockningsgränssnitt")
        self.docking_interface = docking_interface

        # Videogränssnitt
        video_interface: Component | None = create_and_import_component(data, "Videogränssnitt")
        self.video_interface = video_interface

        # Generation
        generation: Component | None = create_and_import_component(data, "Generation")
        self.generation = generation

        # Hårddiskkapacitet
        hard_drive_capacity: Component | None = create_and_import_component(data, "Hårddiskkapacitet")
        self.hard_drive_capacity = hard_drive_capacity

        # Fingeravtrycksläsare
        fingerprint_reader: Component | None = create_and_import_component(data, "Fingeravtrycksläsare")
        self.fingerprint_reader = fingerprint_reader

        # Plattform
        platform: Component | None = create_and_import_component(data, "Plattform")
        self.platform = platform

        # Embedded Security
        embedded_security: Component | None = create_and_import_component(data, "Embedded Security")
        self.embedded_security = embedded_security

        # Notebook-typ
        notebook_type: Component | None = create_and_import_component(data, "Notebook-typ")
        self.notebook_type = notebook_type

        # Typ av handdator
        handheld_type: Component | None = create_and_import_component(data, "Typ av handdator")
        self.handheld_type = handheld_type

        # Introducerad
        introduced: Component | None = create_and_import_component(data, "Introducerad")
        self.introduced = introduced

        # Typ
        _type: Component | None = create_and_import_component(data, "Typ")
        self.type = _type

        # Dockningsbar
        dockable: Component | None = create_and_import_component(data, "Dockningsbar")
        self.dockable = dockable

        # Plattformsteknik
        platform_technology: Component | None = create_and_import_component(data, "Plattformsteknik")
        self.platform_technology = platform_technology


class ControllerCard(auto_prefetch.Model):
    """Kontrollerkort."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the controller card was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the controller card was last updated")

    # Webhallen fields
    type = models.ForeignKey(Component, on_delete=models.CASCADE, help_text="Type", related_name="controller_card_type")
    form_factor = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Form factor",
        related_name="controller_card_form_factor",
    )
    supported_devices = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Supported devices",
        related_name="controller_card_supported_devices",
    )
    max_number_of_devices = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Max number of devices",
        related_name="controller_card_max_number_of_devices",
    )
    power_source = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Power source",
        related_name="controller_card_power_source",
    )
    host_bus = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Host bus",
        related_name="controller_card_host_bus",
    )
    interface = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Interface",
        related_name="controller_card_interface",
    )
    number_of_channels = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Number of channels",
        related_name="controller_card_number_of_channels",
    )
    interface_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Interface type",
        related_name="controller_card_interface_type",
    )
    raid_level = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="RAID level",
        related_name="controller_card_raid_level",
    )

    def __str__(self) -> str:
        return "Controller card"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Typ
        _type: Component | None = create_and_import_component(data, "Typ")
        self.type = _type

        # Formfaktor
        form_factor: Component | None = create_and_import_component(data, "Formfaktor")
        self.form_factor = form_factor

        # Enheter som stöds
        supported_devices: Component | None = create_and_import_component(data, "Enheter som stöds")
        self.supported_devices = supported_devices

        # Max antal enheter
        max_number_of_devices: Component | None = create_and_import_component(data, "Max antal enheter")
        self.max_number_of_devices = max_number_of_devices

        # Strömkälla
        power_source: Component | None = create_and_import_component(data, "Strömkälla")
        self.power_source = power_source

        # Värdbuss
        host_bus: Component | None = create_and_import_component(data, "Värdbuss")
        self.host_bus = host_bus

        # Gränssnitt
        interface: Component | None = create_and_import_component(data, "Gränssnitt")
        self.interface = interface

        # Antal kanaler
        number_of_channels: Component | None = create_and_import_component(data, "Antal kanaler")
        self.number_of_channels = number_of_channels

        # Gränssnittstyp
        interface_type: Component | None = create_and_import_component(data, "Gränssnittstyp")
        self.interface_type = interface_type

        # RAID-nivå
        raid_level: Component | None = create_and_import_component(data, "RAID-nivå")
        self.raid_level = raid_level


class PersonalHygiene(auto_prefetch.Model):
    """Personlig hygien."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the personal hygiene was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the personal hygiene was last updated")

    # Webhallen fields
    category = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Category",
        related_name="personal_hygiene_category",
    )
    product_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Product type",
        related_name="personal_hygiene_product_type",
    )
    usage = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Usage",
        related_name="personal_hygiene_usage",
    )
    number_of_speed_settings = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Number of speed settings",
        related_name="personal_hygiene_number_of_speed_settings",
    )
    vibrations_per_minute = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Vibrations per minute",
        related_name="personal_hygiene_vibrations_per_minute",
    )

    def __str__(self) -> str:
        return "Personal hygiene"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Kategori
        category: Component | None = create_and_import_component(data, "Kategori")
        self.category = category

        # Produkttyp
        product_type: Component | None = create_and_import_component(data, "Produkttyp")
        self.product_type = product_type

        # Användning
        usage: Component | None = create_and_import_component(data, "Användning")
        self.usage = usage

        # Antal hastighetsinställningar
        number_of_speed_settings: Component | None = create_and_import_component(data, "Antal hastighetsinställningar")
        self.number_of_speed_settings = number_of_speed_settings

        # Svängningar per minut
        vibrations_per_minute: Component | None = create_and_import_component(data, "Svängningar per minut")
        self.vibrations_per_minute = vibrations_per_minute


class Warranty(auto_prefetch.Model):
    """Warranty."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the warranty was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the warranty was last updated")

    # Webhallen fields
    warranty = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Warranty",
        related_name="warranty_warranty",
    )

    def __str__(self) -> str:
        return "Warranty"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Garanti
        warranty: Component | None = create_and_import_component(data, "Garanti")
        self.warranty = warranty


class AccessoriesForDevices(auto_prefetch.Model):
    """Accessories for devices."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the accessories for devices was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the accessories for devices was last updated")

    # Webhallen fields
    type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Type",
        related_name="accessories_for_devices_type",
    )
    intended_for = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Intended for",
        related_name="accessories_for_devices_intended_for",
    )
    capacity = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Capacity",
        related_name="accessories_for_devices_capacity",
    )

    def __str__(self) -> str:
        return "Accessories for devices"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Typ
        _type: Component | None = create_and_import_component(data, "Typ")
        self.type = _type

        # Avsedd för
        intended_for: Component | None = create_and_import_component(data, "Avsedd för")
        self.intended_for = intended_for

        # Kapacitet
        capacity: Component | None = create_and_import_component(data, "Kapacitet")
        self.capacity = capacity


class VideoOutput(auto_prefetch.Model):
    """Video output."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the video output was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the video output was last updated")

    # Webhallen fields
    maximum_external_resolution = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Maximum external resolution",
        related_name="video_output_maximum_external_resolution",
    )
    type = models.ForeignKey(Component, on_delete=models.CASCADE, help_text="Type")
    supported_video_signals = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Supported video signals",
        related_name="video_output_supported_video_signals",
    )
    type_of_interface = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Type of interface",
        related_name="video_output_type_of_interface",
    )
    tv_connection = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="TV connection",
        related_name="video_output_tv_connection",
    )
    hdr_capacity = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="HDR capacity",
        related_name="video_output_hdr_capacity",
    )
    clock_speed = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Clock speed",
        related_name="video_output_clock_speed",
    )
    high_clock_speed = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="High clock speed",
        related_name="video_output_high_clock_speed",
    )
    low = models.ForeignKey(Component, on_delete=models.CASCADE, help_text="Low", related_name="video_output_low")
    chip_manufacturer = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Chip manufacturer",
        related_name="video_output_chip_manufacturer",
    )
    graphics_card = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Graphics card",
        related_name="video_output_graphics_card",
    )
    max_number_of_supported_displays = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Max number of supported displays",
        related_name="video_output_max_number_of_supported_displays",
    )
    dedicated_graphics_card = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Dedicated graphics card",
        related_name="video_output_dedicated_graphics_card",
    )
    graphics_processor_series = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Graphics processor series",
        related_name="video_output_graphics_processor_series",
    )
    vr_ready = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="VR ready",
        related_name="video_output_vr_ready",
    )
    hdcp_compatible = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="HDCP compatible",
        related_name="video_output_hdcp_compatible",
    )

    def __str__(self) -> str:
        return "Video output"

    def import_json(self, data: dict) -> None:  # noqa: PLR0914
        """Import JSON data."""
        # Maximal extern upplösning
        maximum_external_resolution: Component | None = create_and_import_component(data, "Maximal extern upplösning")
        self.maximum_external_resolution = maximum_external_resolution

        # Typ
        _type: Component | None = create_and_import_component(data, "Typ")
        self.type = _type

        # Videosignal som stöds
        supported_video_signals: Component | None = create_and_import_component(data, "Videosignal som stöds")
        self.supported_video_signals = supported_video_signals

        # Typ av gränssnitt
        type_of_interface: Component | None = create_and_import_component(data, "Typ av gränssnitt")
        self.type_of_interface = type_of_interface

        # TV-anslutning
        tv_connection: Component | None = create_and_import_component(data, "TV-anslutning")
        self.tv_connection = tv_connection

        # HDR-kapacitet
        hdr_capacity: Component | None = create_and_import_component(data, "HDR-kapacitet")
        self.hdr_capacity = hdr_capacity

        # Klockhastighet
        clock_speed: Component | None = create_and_import_component(data, "Klockhastighet")
        self.clock_speed = clock_speed

        # Snabb klockhastighet
        high_clock_speed: Component | None = create_and_import_component(data, "Snabb klockhastighet")
        self.high_clock_speed = high_clock_speed

        # Låg
        low: Component | None = create_and_import_component(data, "Låg")
        self.low = low

        # Chiptillverkare
        chip_manufacturer: Component | None = create_and_import_component(data, "Chiptillverkare")
        self.chip_manufacturer = chip_manufacturer

        # Grafikkort
        graphics_card: Component | None = create_and_import_component(data, "Grafikkort")
        self.graphics_card = graphics_card

        # Max antal bildskärmar som stöds
        max_number_of_supported_displays: Component | None = create_and_import_component(
            data,
            "Max antal bildskärmar som stöds",
        )
        self.max_number_of_supported_displays = max_number_of_supported_displays

        # Dedikerat grafikkort
        dedicated_graphics_card: Component | None = create_and_import_component(data, "Dedikerat grafikkort")
        self.dedicated_graphics_card = dedicated_graphics_card

        # Grafikprocessorserie
        graphics_processor_series: Component | None = create_and_import_component(data, "Grafikprocessorserie")
        self.graphics_processor_series = graphics_processor_series

        # VR-förberedd
        vr_ready: Component | None = create_and_import_component(data, "VR-förberedd")
        self.vr_ready = vr_ready

        # HDCP-kompatibel
        hdcp_compatible: Component | None = create_and_import_component(data, "HDCP-kompatibel")
        self.hdcp_compatible = hdcp_compatible


class SmallDevices(auto_prefetch.Model):
    """Small devices."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the small devices was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the small devices was last updated")

    # Webhallen fields
    product_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Product type",
        related_name="small_devices_product_type",
    )
    capacity = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Capacity",
        related_name="small_devices_capacity",
    )
    variable_temperature = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Variable temperature",
        related_name="small_devices_variable_temperature",
    )
    functions_and_settings = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Functions and settings",
        related_name="small_devices_functions_and_settings",
    )
    max_speed = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Max speed",
        related_name="small_devices_max_speed",
    )
    bowl_material = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Bowl material",
        related_name="small_devices_bowl_material",
    )
    included_blades_and_additives = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Included blades and additives",
        related_name="small_devices_included_blades_and_additives",
    )
    automatic_shutdown = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Automatic shutdown",
        related_name="small_devices_automatic_shutdown",
    )
    water_level_indicator = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Water level indicator",
        related_name="small_devices_water_level_indicator",
    )
    temperature_settings = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Temperature settings",
        related_name="small_devices_temperature_settings",
    )
    mass_container_capacity = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Mass container capacity",
        related_name="small_devices_mass_container_capacity",
    )
    multi_plate = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Multi-plate",
        related_name="small_devices_multi_plate",
    )
    food_capacity = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Food capacity",
        related_name="small_devices_food_capacity",
    )
    number_of_programs = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Number of programs",
        related_name="small_devices_number_of_programs",
    )
    number_of_people = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Number of people",
        related_name="small_devices_number_of_people",
    )

    def __str__(self) -> str:
        return "Small devices"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Produkttyp
        product_type: Component | None = create_and_import_component(data, "Produkttyp")
        self.product_type = product_type

        # Kapacitet
        capacity: Component | None = create_and_import_component(data, "Kapacitet")
        self.capacity = capacity

        # Variabel temperatur
        variable_temperature: Component | None = create_and_import_component(data, "Variabel temperatur")
        self.variable_temperature = variable_temperature

        # Funktion och inställningar
        functions_and_settings: Component | None = create_and_import_component(data, "Funktion och inställningar")
        self.functions_and_settings = functions_and_settings

        # Max. hastighet
        max_speed: Component | None = create_and_import_component(data, "Max. hastighet")
        self.max_speed = max_speed

        # Skålens material
        bowl_material: Component | None = create_and_import_component(data, "Skålens material")
        self.bowl_material = bowl_material

        # Inkluderade blad och tillsatser
        included_blades_and_additives: Component | None = create_and_import_component(
            data,
            "Inkluderade blad och tillsatser",
        )
        self.included_blades_and_additives = included_blades_and_additives

        # Automatisk avstängning
        automatic_shutdown: Component | None = create_and_import_component(data, "Automatisk avstängning")
        self.automatic_shutdown = automatic_shutdown

        # Vattennivåindikator
        water_level_indicator: Component | None = create_and_import_component(data, "Vattennivåindikator")
        self.water_level_indicator = water_level_indicator

        # Temperaturinställningar
        temperature_settings: Component | None = create_and_import_component(data, "Temperaturinställningar")
        self.temperature_settings = temperature_settings

        # Massbehållarkapacitet
        mass_container_capacity: Component | None = create_and_import_component(data, "Massbehållarkapacitet")
        self.mass_container_capacity = mass_container_capacity

        # Multiplatta
        multi_plate: Component | None = create_and_import_component(data, "Multiplatta")
        self.multi_plate = multi_plate

        # Livsmedelskapacitet
        food_capacity: Component | None = create_and_import_component(data, "Livsmedelskapacitet")
        self.food_capacity = food_capacity

        # Antal program
        number_of_programs: Component | None = create_and_import_component(data, "Antal program")
        self.number_of_programs = number_of_programs

        # Antal personer
        number_of_people: Component | None = create_and_import_component(data, "Antal personer")
        self.number_of_people = number_of_people


class Camera(auto_prefetch.Model):
    """Camera."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the camera was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the camera was last updated")

    # Webhallen fields
    image_sensor_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Image sensor type",
        related_name="camera_image_sensor_type",
    )
    optical_sensor_resolution = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Optical sensor resolution",
        related_name="camera_optical_sensor_resolution",
    )
    type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Type",
        related_name="camera_type",
    )
    shooting_methods = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Shooting methods",
        related_name="camera_shooting_methods",
    )

    def __str__(self) -> str:
        return "Camera"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Bildsensortyp
        image_sensor_type: Component | None = create_and_import_component(data, "Bildsensortyp")
        self.image_sensor_type = image_sensor_type

        # Optisk sensorupplösning
        optical_sensor_resolution: Component | None = create_and_import_component(data, "Optisk sensorupplösning")
        self.optical_sensor_resolution = optical_sensor_resolution

        # Typ
        _type: Component | None = create_and_import_component(data, "Typ")
        self.type = _type

        # Tagningsmetoder
        shooting_methods: Component | None = create_and_import_component(data, "Tagningsmetoder")
        self.shooting_methods = shooting_methods


class LightSource(auto_prefetch.Model):
    """Light source."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the light source was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the light source was last updated")

    # Webhallen fields
    type_of_light_source = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Type of light source",
        related_name="light_source_type_of_light_source",
    )
    luminous_flux = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Luminous flux",
        related_name="light_source_luminous_flux",
    )
    lifespan = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Lifespan",
        related_name="light_source_lifespan",
    )
    color_temperature = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Color temperature",
        related_name="light_source_color_temperature",
    )
    illumination_color = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Illumination color",
        related_name="light_source_illumination_color",
    )
    wattage = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Wattage",
        related_name="light_source_wattage",
    )
    energy_efficiency_class = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Energy efficiency class",
        related_name="light_source_energy_efficiency_class",
    )
    watt_equivalence = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Watt equivalence",
        related_name="light_source_watt_equivalence",
    )
    beam_angle = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Beam angle",
        related_name="light_source_beam_angle",
    )
    socket_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Socket type",
        related_name="light_source_socket_type",
    )
    color_rendering_index = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Color rendering index",
        related_name="light_source_color_rendering_index",
    )
    mercury_content = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Mercury content",
        related_name="light_source_mercury_content",
    )
    dimmable = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Dimmable",
        related_name="light_source_dimmable",
    )
    shape = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Shape",
        related_name="light_source_shape",
    )
    power_factor = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Power factor",
        related_name="light_source_power_factor",
    )
    lamp_current = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Lamp current",
        related_name="light_source_lamp_current",
    )
    start_time = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Start time",
        related_name="light_source_start_time",
    )
    warm_up_time = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Warm-up time",
        related_name="light_source_warm_up_time",
    )
    luminous_efficiency = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Luminous efficiency",
        related_name="light_source_luminous_efficiency",
    )

    def __str__(self) -> str:
        return "Light source"

    def import_json(self, data: dict) -> None:  # noqa: PLR0914
        """Import JSON data."""
        # Typ av ljuskälla
        type_of_light_source: Component | None = create_and_import_component(data, "Typ av ljuskälla")
        self.type_of_light_source = type_of_light_source

        # Ljusflöde
        luminous_flux: Component | None = create_and_import_component(data, "Ljusflöde")
        self.luminous_flux = luminous_flux

        # Livstid
        lifespan: Component | None = create_and_import_component(data, "Livstid")
        self.lifespan = lifespan

        # Färgtemperatur
        color_temperature: Component | None = create_and_import_component(data, "Färgtemperatur")
        self.color_temperature = color_temperature

        # Belysningsfärg
        illumination_color: Component | None = create_and_import_component(data, "Belysningsfärg")
        self.illumination_color = illumination_color

        # Watt-tal
        wattage: Component | None = create_and_import_component(data, "Watt-tal")
        self.wattage = wattage

        # Energieffektivitetsklass
        energy_efficiency_class: Component | None = create_and_import_component(data, "Energieffektivitetsklass")
        self.energy_efficiency_class = energy_efficiency_class

        # Wattmotsvarighet
        watt_equivalence: Component | None = create_and_import_component(data, "Wattmotsvarighet")
        self.watt_equivalence = watt_equivalence

        # Strålvinkel
        beam_angle: Component | None = create_and_import_component(data, "Strålvinkel")
        self.beam_angle = beam_angle

        # Uttagstyp
        socket_type: Component | None = create_and_import_component(data, "Uttagstyp")
        self.socket_type = socket_type

        # Färgåtergivningsindex
        color_rendering_index: Component | None = create_and_import_component(data, "Färgåtergivningsindex")
        self.color_rendering_index = color_rendering_index

        # Kvicksilverinnehåll
        mercury_content: Component | None = create_and_import_component(data, "Kvicksilverinnehåll")
        self.mercury_content = mercury_content

        # Dimningsbar
        dimmable: Component | None = create_and_import_component(data, "Dimningsbar")
        self.dimmable = dimmable

        # Form
        shape: Component | None = create_and_import_component(data, "Form")
        self.shape = shape

        # Strömfaktor
        power_factor: Component | None = create_and_import_component(data, "Strömfaktor")
        self.power_factor = power_factor

        # Lampström
        lamp_current: Component | None = create_and_import_component(data, "Lampström")
        self.lamp_current = lamp_current

        # Starttid
        start_time: Component | None = create_and_import_component(data, "Starttid")
        self.start_time = start_time

        # Uppvärmningstid
        warm_up_time: Component | None = create_and_import_component(data, "Uppvärmningstid")
        self.warm_up_time = warm_up_time

        # Upplysningseffektivitet
        luminous_efficiency: Component | None = create_and_import_component(data, "Upplysningseffektivitet")
        self.luminous_efficiency = luminous_efficiency


class Software(auto_prefetch.Model):
    """Programvara."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the software was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the software was last updated")

    # Webhallen fields
    number_of_licenses = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Number of licenses",
        related_name="software_number_of_licenses",
    )
    license_validity_period = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="License validity period",
        related_name="software_license_validity_period",
    )
    type_of_license = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Type of license",
        related_name="software_type_of_license",
    )
    license_category = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="License category",
        related_name="software_license_category",
    )
    version = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Version",
        related_name="software_version",
    )
    type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Type",
        related_name="software_type",
    )

    def __str__(self) -> str:
        return "Software"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Antal licenser
        number_of_licenses: Component | None = create_and_import_component(data, "Antal licenser")
        self.number_of_licenses = number_of_licenses

        # Giltighetsperiod för licens
        license_validity_period: Component | None = create_and_import_component(data, "Giltighetsperiod för licens")
        self.license_validity_period = license_validity_period

        # Typ av licens
        type_of_license: Component | None = create_and_import_component(data, "Typ av licens")
        self.type_of_license = type_of_license

        # Licenskategori
        license_category: Component | None = create_and_import_component(data, "Licenskategori")
        self.license_category = license_category

        # Version
        version: Component | None = create_and_import_component(data, "Version")
        self.version = version

        # Typ
        _type: Component | None = create_and_import_component(data, "Typ")
        self.type = _type


class CEAccessories(auto_prefetch.Model):
    """CE-tillbehör."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the CE marking was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the CE marking was last updated")

    # Webhallen fields
    product_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Product type",
        related_name="ce_accessories_product_type",
    )
    intended_for = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Intended for",
        related_name="ce_accessories_intended_for",
    )
    suitable_for_installation = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Suitable for installation",
        related_name="ce_accessories_suitable_for_installation",
    )

    def __str__(self) -> str:
        return "CE accessories"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Produkttyp
        product_type: Component | None = create_and_import_component(data, "Produkttyp")
        self.product_type = product_type

        # Avsedd för
        intended_for: Component | None = create_and_import_component(data, "Avsedd för")
        self.intended_for = intended_for

        # Lämplig för installation
        suitable_for_installation: Component | None = create_and_import_component(data, "Lämplig för installation")
        self.suitable_for_installation = suitable_for_installation


class Game(auto_prefetch.Model):
    """Spel."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the game was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the game was last updated")

    # Webhallen fields
    release_month = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Release month",
        related_name="game_release_month",
    )
    genre = models.ForeignKey(Component, on_delete=models.CASCADE, help_text="Genre", related_name="game_genre")
    esrb_rating = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="ESRB rating",
        related_name="game_esrb_rating",
    )
    pegi_content_description = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="PEGI content description",
        related_name="game_pegi_content_description",
    )
    usk_age_rating = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="USK age rating",
        related_name="game_usk_age_rating",
    )
    pegi_classification = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="PEGI classification",
        related_name="game_pegi_classification",
    )
    australian_state_evaluation = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Australian state evaluation",
        related_name="game_australian_state_evaluation",
    )
    platform = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Platform",
        related_name="game_platform",
    )
    release_year = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Release year",
        related_name="game_release_year",
    )
    release_day = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Release day",
        related_name="game_release_day",
    )
    multiplayer = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Multiplayer",
        related_name="game_multiplayer",
    )
    max_number_of_players = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Max number of players",
        related_name="game_max_number_of_players",
    )
    online_play = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Online play",
        related_name="game_online_play",
    )

    def __str__(self) -> str:
        return "Game"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Utgivningsmånad
        release_month: Component | None = create_and_import_component(data, "Utgivningsmånad")
        self.release_month = release_month

        # Genre
        genre: Component | None = create_and_import_component(data, "Genre")
        self.genre = genre

        # ESRB-märkning
        esrb_rating: Component | None = create_and_import_component(data, "ESRB-märkning")
        self.esrb_rating = esrb_rating

        # PEGI-innehållsbeskrivning
        pegi_content_description: Component | None = create_and_import_component(data, "PEGI-innehållsbeskrivning")
        self.pegi_content_description = pegi_content_description

        # USK-åldersgräns
        usk_age_rating: Component | None = create_and_import_component(data, "USK-åldersgräns")
        self.usk_age_rating = usk_age_rating

        # PEGI-klassificering
        pegi_classification: Component | None = create_and_import_component(data, "PEGI-klassificering")
        self.pegi_classification = pegi_classification

        # Utvärdering av australienska staten
        australian_state_evaluation: Component | None = create_and_import_component(
            data,
            "Utvärdering av australienska staten",
        )
        self.australian_state_evaluation = australian_state_evaluation

        # Plattform
        platform: Component | None = create_and_import_component(data, "Plattform")
        self.platform = platform

        # Utgivningsår
        release_year: Component | None = create_and_import_component(data, "Utgivningsår")
        self.release_year = release_year

        # Utgivningsdag
        release_day: Component | None = create_and_import_component(data, "Utgivningsdag")
        self.release_day = release_day

        # Multispelare
        multiplayer: Component | None = create_and_import_component(data, "Multispelare")
        self.multiplayer = multiplayer

        # Max antal spelare
        max_number_of_players: Component | None = create_and_import_component(data, "Max antal spelare")
        self.max_number_of_players = max_number_of_players

        # Onlinespel
        online_play: Component | None = create_and_import_component(data, "Onlinespel")
        self.online_play = online_play


class ToastersAndGrills(auto_prefetch.Model):
    """Brödrostar och grillar."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the toasters and grills was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the toasters and grills was last updated")

    # Webhallen fields
    product_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Product type",
        related_name="toasters_and_grills_product_type",
    )
    number_of_slices = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Number of slices",
        related_name="toasters_and_grills_number_of_slices",
    )
    number_of_outlets = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Number of outlets",
        related_name="toasters_and_grills_number_of_outlets",
    )

    def __str__(self) -> str:
        return "Toasters and grills"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Produkttyp
        product_type: Component | None = create_and_import_component(data, "Produkttyp")
        self.product_type = product_type

        # Antal skivor
        number_of_slices: Component | None = create_and_import_component(data, "Antal skivor")
        self.number_of_slices = number_of_slices

        # Antal uttag
        number_of_outlets: Component | None = create_and_import_component(data, "Antal uttag")
        self.number_of_outlets = number_of_outlets


class Scale(auto_prefetch.Model):
    """Våg."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the scale was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the scale was last updated")

    # Webhallen fields
    kitchen_scale_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Kitchen scale type",
        related_name="scale_kitchen_scale_type",
    )
    max_weight = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Max weight",
        related_name="scale_max_weight",
    )
    bathroom_scale_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Bathroom scale type",
        related_name="scale_bathroom_scale_type",
    )
    measurement_functions = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Measurement functions",
        related_name="scale_measurement_functions",
    )

    def __str__(self) -> str:
        return "Scale"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Köksvågstyp
        kitchen_scale_type: Component | None = create_and_import_component(data, "Köksvågstyp")
        self.kitchen_scale_type = kitchen_scale_type

        # Maxvikt
        max_weight: Component | None = create_and_import_component(data, "Maxvikt")
        self.max_weight = max_weight

        # Badrumsvågstyp
        bathroom_scale_type: Component | None = create_and_import_component(data, "Badrumsvågstyp")
        self.bathroom_scale_type = bathroom_scale_type

        # Mätfunktioner
        measurement_functions: Component | None = create_and_import_component(data, "Mätfunktioner")
        self.measurement_functions = measurement_functions


class HDD(auto_prefetch.Model):
    """Hard disk drive (HDD)."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the HDD was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the HDD was last updated")

    # Webhallen fields
    hard_disk_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Hard disk type",
        related_name="hdd_hard_disk_type",
    )
    interface = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Interface",
        related_name="hdd_interface",
    )
    external_device_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="External device type",
        related_name="hdd_external_device_type",
    )
    hard_disk_space = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Hard disk space",
        related_name="hdd_hard_disk_space",
    )
    spindle_speed = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Spindle speed",
        related_name="hdd_spindle_speed",
    )
    unrecoverable_error = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Unrecoverable error",
        related_name="hdd_unrecoverable_error",
    )
    data_transfer_rate = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Data transfer rate",
        related_name="hdd_data_transfer_rate",
    )
    internal_data_frequency = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Internal data frequency",
        related_name="hdd_internal_data_frequency",
    )
    average_seek_time = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Average seek time",
        related_name="hdd_average_seek_time",
    )
    form_factor = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Form factor",
        related_name="hdd_form_factor",
    )
    form_factor_short = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Form factor short",
        related_name="hdd_form_factor_short",
    )
    form_factor_metric = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Form factor metric",
        related_name="hdd_form_factor_metric",
    )
    form_factor_short_metric = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Form factor short metric",
        related_name="hdd_form_factor_short_metric",
    )
    buffer_size = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Buffer size",
        related_name="hdd_buffer_size",
    )
    internal_data_write_speed = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Internal data write speed",
        related_name="hdd_internal_data_write_speed",
    )
    nand_flash_memory_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="NAND flash memory type",
        related_name="hdd_nand_flash_memory_type",
    )
    _24_7_operation = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="24/7 operation",
        related_name="hdd_24_7_operation",
    )
    _4_kb_random_read = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="The 4 KB random read",
        related_name="hdd_4_kb_random_read",
    )
    type = models.ForeignKey(Component, on_delete=models.CASCADE, help_text="Type", related_name="hdd_type")
    ssd_form_factor = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="SSD form factor",
        related_name="hdd_ssd_form_factor",
    )
    hard_disk_features = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Hard disk features",
        related_name="hdd_hard_disk_features",
    )
    type_of_interface = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Type of interface",
        related_name="hdd_type_of_interface",
    )
    interface_class = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Interface class",
        related_name="hdd_interface_class",
    )
    ssd_capacity = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="SSD capacity",
        related_name="hdd_ssd_capacity",
    )

    def __str__(self) -> str:
        return "HDD"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Hårddisktyp
        hard_disk_type: Component | None = create_and_import_component(data, "Hårddisktyp")
        self.hard_disk_type = hard_disk_type

        # Gränssnitt
        interface: Component | None = create_and_import_component(data, "Gränssnitt")
        self.interface = interface

        # Extern enhetstyp
        external_device_type: Component | None = create_and_import_component(data, "Extern enhetstyp")
        self.external_device_type = external_device_type

        # Hårddiskutrymme
        hard_disk_space: Component | None = create_and_import_component(data, "Hårddiskutrymme")
        self.hard_disk_space = hard_disk_space

        # Spindelhastighet
        spindle_speed: Component | None = create_and_import_component(data, "Spindelhastighet")
        self.spindle_speed = spindle_speed

        # Icke återställningsbar fel
        unrecoverable_error: Component | None = create_and_import_component(data, "Icke återställningsbar fel")
        self.unrecoverable_error = unrecoverable_error

        # Dataöverföringshastighet
        data_transfer_rate: Component | None = create_and_import_component(data, "Dataöverföringshastighet")
        self.data_transfer_rate = data_transfer_rate

        # Intern datafrekvens
        internal_data_frequency: Component | None = create_and_import_component(data, "Intern datafrekvens")
        self.internal_data_frequency = internal_data_frequency

        # Genomsnittlig söktid
        average_seek_time: Component | None = create_and_import_component(data, "Genomsnittlig söktid")
        self.average_seek_time = average_seek_time

        # Formfaktor
        form_factor: Component | None = create_and_import_component(data, "Formfaktor")
        self.form_factor = form_factor

        # Formfaktor kort
        form_factor_short: Component | None = create_and_import_component(data, "Formfaktor kort")
        self.form_factor_short = form_factor_short

        # Formfaktor metrisk
        form_factor_metric: Component | None = create_and_import_component(data, "Formfaktor metrisk")
        self.form_factor_metric = form_factor_metric


class ExternalHardDrive(auto_prefetch.Model):
    """External hard drive."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the external hard drive was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the external hard drive was last updated")

    # Webhallen fields
    power_source = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Power source",
        related_name="external_hard_drive_power_source",
    )
    max_data_transfer_rate = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Max data transfer rate",
        related_name="external_hard_drive_max_data_transfer_rate",
    )
    usb_c_port = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="USB-C port",
        related_name="external_hard_drive_usb_c_port",
    )

    def __str__(self) -> str:
        return "External hard drive"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Strömkälla
        power_source: Component | None = create_and_import_component(data, "Strömkälla")
        self.power_source = power_source

        # Max dataöverföringshastighet
        max_data_transfer_rate: Component | None = create_and_import_component(data, "Max dataöverföringshastighet")
        self.max_data_transfer_rate = max_data_transfer_rate

        # USB-C-port
        usb_c_port: Component | None = create_and_import_component(data, "USB-C-port")
        self.usb_c_port = usb_c_port


class Modem(auto_prefetch.Model):
    """Modem."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the modem was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the modem was last updated")

    # Webhallen fields
    connection_technology = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Connection technology",
        related_name="modem_connection_technology",
    )
    form_factor = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Form factor",
        related_name="modem_form_factor",
    )
    type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Type",
        related_name="modem_type",
    )
    max_transfer_rate = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Max transfer rate",
        related_name="modem_max_transfer_rate",
    )
    band = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Band",
        related_name="modem_band",
    )
    broadband_access_for_mobile_phone = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Broadband access for mobile phone",
        related_name="modem_broadband_access_for_mobile_phone",
    )

    def __str__(self) -> str:
        return "Modem"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Anslutningsteknik
        connection_technology: Component | None = create_and_import_component(data, "Anslutningsteknik")
        self.connection_technology = connection_technology

        # Formfaktor
        form_factor: Component | None = create_and_import_component(data, "Formfaktor")
        self.form_factor = form_factor

        # Typ
        _type: Component | None = create_and_import_component(data, "Typ")
        self.type = _type

        # Max överföringshastighet
        max_transfer_rate: Component | None = create_and_import_component(data, "Max överföringshastighet")
        self.max_transfer_rate = max_transfer_rate

        # Band
        band: Component | None = create_and_import_component(data, "Band")
        self.band = band

        # Bredbandsåtkomst för mobiltelefon
        broadband_access_for_mobile_phone: Component | None = create_and_import_component(
            data,
            "Bredbandsåtkomst för mobiltelefon",
        )
        self.broadband_access_for_mobile_phone = broadband_access_for_mobile_phone


class MobileBroadband(auto_prefetch.Model):
    """Mobilt bredband."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the mobile broadband was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the mobile broadband was last updated")

    # Webhallen fields
    cellular_protocol = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Cellular protocol",
        related_name="mobile_broadband_cellular_protocol",
    )
    generation = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Generation",
        related_name="mobile_broadband_generation",
    )

    def __str__(self) -> str:
        return "Mobile broadband"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Cellulärt protokoll
        cellular_protocol: Component | None = create_and_import_component(data, "Cellulärt protokoll")
        self.cellular_protocol = cellular_protocol

        # Generation
        generation: Component | None = create_and_import_component(data, "Generation")
        self.generation = generation


class AudioInput(auto_prefetch.Model):
    """Ljudingång."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the audio input was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the audio input was last updated")

    # Webhallen fields
    microphone_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Microphone type",
        related_name="audio_input_microphone_type",
    )
    sensitivity = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Sensitivity",
        related_name="audio_input_sensitivity",
    )
    type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Type",
        related_name="audio_input_type",
    )
    operational_mode_for_microphone = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Operational mode for microphone",
        related_name="audio_input_operational_mode_for_microphone",
    )
    connection_technology = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Connection technology",
        related_name="audio_input_connection_technology",
    )

    def __str__(self) -> str:
        return "Audio input"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Mikrofontyp
        microphone_type: Component | None = create_and_import_component(data, "Mikrofontyp")
        self.microphone_type = microphone_type

        # Känslighet
        sensitivity: Component | None = create_and_import_component(data, "Känslighet")
        self.sensitivity = sensitivity

        # Typ
        _type: Component | None = create_and_import_component(data, "Typ")
        self.type = _type

        # Operativt läge för mikrofon
        operational_mode_for_microphone: Component | None = create_and_import_component(
            data,
            "Operativt läge för mikrofon",
        )
        self.operational_mode_for_microphone = operational_mode_for_microphone

        # Anslutningsteknik
        connection_technology: Component | None = create_and_import_component(data, "Anslutningsteknik")
        self.connection_technology = connection_technology


class MemoryAdapter(auto_prefetch.Model):
    """Minnesadapter."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the memory adapter was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the memory adapter was last updated")

    # Webhallen fields
    model = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Model",
        related_name="memory_adapter_model",
    )
    interface = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Interface",
        related_name="memory_adapter_interface",
    )
    device_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Device type",
        related_name="memory_adapter_device_type",
    )
    support_for_memory_cards = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Support for memory cards",
        related_name="memory_adapter_support_for_memory_cards",
    )

    def __str__(self) -> str:
        return "Memory adapter"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Modell
        model: Component | None = create_and_import_component(data, "Modell")
        self.model = model

        # Gränssnitt
        interface: Component | None = create_and_import_component(data, "Gränssnitt")
        self.interface = interface

        # Enhetstyp
        device_type: Component | None = create_and_import_component(data, "Enhetstyp")
        self.device_type = device_type

        # Stöd för minneskort
        support_for_memory_cards: Component | None = create_and_import_component(data, "Stöd för minneskort")
        self.support_for_memory_cards = support_for_memory_cards


class InternetOfThings(auto_prefetch.Model):
    """Internet of Things (IoT)."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the internet of things was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the internet of things was last updated")

    # Webhallen fields
    communication_technology = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Communication technology",
        related_name="internet_of_things_communication_technology",
    )
    platform = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Platform",
        related_name="internet_of_things_platform",
    )
    compatible_with_internet_of_things = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Compatible with Internet of Things",
        related_name="internet_of_things_compatible_with_internet_of_things",
    )
    intelligent_assistant = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Intelligent assistant",
        related_name="internet_of_things_intelligent_assistant",
    )
    voice_controlled = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Voice controlled",
        related_name="internet_of_things_voice_controlled",
    )

    def __str__(self) -> str:
        return "Internet of Things"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Kommunikationsteknologi
        communication_technology: Component | None = create_and_import_component(data, "Kommunikationsteknologi")
        self.communication_technology = communication_technology

        # Plattform
        platform: Component | None = create_and_import_component(data, "Plattform")
        self.platform = platform

        # Kompatibel med Internet of Things (IoT)
        compatible_with_internet_of_things: Component | None = create_and_import_component(
            data,
            "Kompatibel med Internet of Things (IoT)",
        )
        self.compatible_with_internet_of_things = compatible_with_internet_of_things

        # Intelligent assistent
        intelligent_assistant: Component | None = create_and_import_component(data, "Intelligent assistent")
        self.intelligent_assistant = intelligent_assistant

        # Röstkontrollerad
        voice_controlled: Component | None = create_and_import_component(data, "Röstkontrollerad")
        self.voice_controlled = voice_controlled


class Cleaning(auto_prefetch.Model):
    """Rengöring."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the cleaning was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the cleaning was last updated")

    # Webhallen fields
    bag_capacity = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Bag capacity",
        related_name="cleaning_bag_capacity",
    )
    product_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Product type",
        related_name="cleaning_product_type",
    )
    container_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Container type",
        related_name="cleaning_container_type",
    )
    cleaning_agent_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Cleaning agent type",
        related_name="cleaning_cleaning_agent_type",
    )
    cleaning_method = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Cleaning method",
        related_name="cleaning_cleaning_method",
    )
    tank_capacity = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Tank capacity",
        related_name="cleaning_tank_capacity",
    )
    dust_emission_class = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Dust emission class",
        related_name="cleaning_dust_emission_class",
    )
    material_cleaning_performance_class = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Material cleaning performance class",
        related_name="cleaning_material_cleaning_performance_class",
    )
    cleaning_performance_class_for_hard_floor = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Cleaning performance class for hard floor",
        related_name="cleaning_cleaning_performance_class_for_hard_floor",
    )
    filter_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Filter type",
        related_name="cleaning_filter_type",
    )
    area_of_use = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Area of use",
        related_name="cleaning_area_of_use",
    )
    maximum_motor_power = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Maximum motor power",
        related_name="cleaning_maximum_motor_power",
    )
    max_suction_power_air_watts = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Max suction power (air watts)",
        related_name="cleaning_max_suction_power_air_watts",
    )

    def __str__(self) -> str:
        return "Cleaning"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Kapacitet hos påse
        bag_capacity: Component | None = create_and_import_component(data, "Kapacitet hos påse")
        self.bag_capacity = bag_capacity

        # Produkttyp
        product_type: Component | None = create_and_import_component(data, "Produkttyp")
        self.product_type = product_type

        # Typ av behållare
        container_type: Component | None = create_and_import_component(data, "Typ av behållare")
        self.container_type = container_type

        # Typ av rengöringsmedel
        cleaning_agent_type: Component | None = create_and_import_component(data, "Typ av rengöringsmedel")
        self.cleaning_agent_type = cleaning_agent_type

        # Rengöringsmetod
        cleaning_method: Component | None = create_and_import_component(data, "Rengöringsmetod")
        self.cleaning_method = cleaning_method

        # Tankkapacitet
        tank_capacity: Component | None = create_and_import_component(data, "Tankkapacitet")
        self.tank_capacity = tank_capacity

        # Dammåteremissionsklass
        dust_emission_class: Component | None = create_and_import_component(data, "Dammåteremissionsklass")
        self.dust_emission_class = dust_emission_class

        # Mattrengöringsprestandaklass
        material_cleaning_performance_class: Component | None = create_and_import_component(
            data,
            "Mattrengöringsprestandaklass",
        )
        self.material_cleaning_performance_class = material_cleaning_performance_class

        # Rengöringsprestandaklass för hårt golv
        cleaning_performance_class_for_hard_floor: Component | None = create_and_import_component(
            data,
            "Rengöringsprestandaklass för hårt golv",
        )
        self.cleaning_performance_class_for_hard_floor = cleaning_performance_class_for_hard_floor

        # Typ av filter
        filter_type: Component | None = create_and_import_component(data, "Typ av filter")
        self.filter_type = filter_type

        # Användningsområde
        area_of_use: Component | None = create_and_import_component(data, "Användningsområde")
        self.area_of_use = area_of_use

        # Maximal motoreffekt
        maximum_motor_power: Component | None = create_and_import_component(data, "Maximal motoreffekt")
        self.maximum_motor_power = maximum_motor_power

        # Max. sugkraft (luftwatt)
        max_suction_power_air_watts: Component | None = create_and_import_component(data, "Max. sugkraft (luftwatt)")
        self.max_suction_power_air_watts = max_suction_power_air_watts


class FlashMemory(auto_prefetch.Model):
    """Flash-minne."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the flash memory was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the flash memory was last updated")

    # Webhallen fields
    read_speed = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Read speed",
        related_name="flash_memory_read_speed",
    )
    form_factor = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Form factor",
        related_name="flash_memory_form_factor",
    )
    product_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Product type",
        related_name="flash_memory_product_type",
    )
    storage_capacity = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Storage capacity",
        related_name="flash_memory_storage_capacity",
    )
    storage_speed = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Storage speed",
        related_name="flash_memory_storage_speed",
    )
    installed_size = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Installed size",
        related_name="flash_memory_installed_size",
    )
    interface_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Interface type",
        related_name="flash_memory_interface_type",
    )
    internal_memory_capacity = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Internal memory capacity",
        related_name="flash_memory_internal_memory_capacity",
    )
    included_memory_adapter = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Included memory adapter",
        related_name="flash_memory_included_memory_adapter",
    )
    speed_class = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Speed class",
        related_name="flash_memory_speed_class",
    )
    supported_memory_cards = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Supported memory cards",
        related_name="flash_memory_supported_memory_cards",
    )
    technology = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Technology",
        related_name="flash_memory_technology",
    )
    user_memory = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="User memory",
        related_name="flash_memory_user_memory",
    )
    max_size_supported = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Max size supported",
        related_name="flash_memory_max_size_supported",
    )
    supported_flash_memory_cards = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Supported flash memory cards",
        related_name="flash_memory_supported_flash_memory_cards",
    )

    def __str__(self) -> str:
        return "Flash memory"

    def import_json(self, data: dict) -> None:  # noqa: PLR0914
        """Import JSON data."""
        # Läshastighet
        read_speed: Component | None = create_and_import_component(data, "Läshastighet")
        self.read_speed = read_speed

        # Formfaktor
        form_factor: Component | None = create_and_import_component(data, "Formfaktor")
        self.form_factor = form_factor

        # Produkttyp
        product_type: Component | None = create_and_import_component(data, "Produkttyp")
        self.product_type = product_type

        # Lagringskapacitet
        storage_capacity: Component | None = create_and_import_component(data, "Lagringskapacitet")
        self.storage_capacity = storage_capacity

        # Lagringshastighet
        storage_speed: Component | None = create_and_import_component(data, "Lagringshastighet")
        self.storage_speed = storage_speed

        # Installerad storlek
        installed_size: Component | None = create_and_import_component(data, "Installerad storlek")
        self.installed_size = installed_size

        # Gränssnittstyp
        interface_type: Component | None = create_and_import_component(data, "Gränssnittstyp")
        self.interface_type = interface_type

        # Internminneskapacitet
        internal_memory_capacity: Component | None = create_and_import_component(data, "Intern minneskapacitet")
        self.internal_memory_capacity = internal_memory_capacity

        # Medföljande minnesadapter
        included_memory_adapter: Component | None = create_and_import_component(data, "Minnesadapter som medföljer")
        self.included_memory_adapter = included_memory_adapter

        # Hastighetsklass
        speed_class: Component | None = create_and_import_component(data, "Hastighetsklass")
        self.speed_class = speed_class

        # Stödda minneskort
        supported_memory_cards: Component | None = create_and_import_component(data, "Minneskort som stöds")
        self.supported_memory_cards = supported_memory_cards

        # Teknologi
        technology: Component | None = create_and_import_component(data, "Teknik")
        self.technology = technology

        # Användarminne
        user_memory: Component | None = create_and_import_component(data, "Användarminne")
        self.user_memory = user_memory

        # Maximal storlek som stöds
        max_size_supported: Component | None = create_and_import_component(data, "Maxstorlek som stöds")
        self.max_size_supported = max_size_supported

        # Stödda flashminneskort
        supported_flash_memory_cards: Component | None = create_and_import_component(data, "Flash-minneskort som stöds")
        self.supported_flash_memory_cards = supported_flash_memory_cards

        # Warn if there are new fields in the JSON data
        available_fields: list[str] = [
            "Läshastighet",
            "Formfaktor",
            "Produkttyp",
            "Lagringskapacitet",
            "Lagringshastighet",
            "Installerad storlek",
            "Gränssnittstyp",
            "Intern minneskapacitet",
            "Minnesadapter som medföljer",
            "Hastighetsklass",
            "Minneskort som stöds",
            "Teknik",
            "Användarminne",
            "Maxstorlek som stöds",
            "Flash-minneskort som stöds",
        ]
        for key in data:
            if key not in available_fields:
                logger.warning("New field found in FlashMemory: %s", key)


class RadioSystem(auto_prefetch.Model):
    """Radiosystem."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the radio system was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the radio system was last updated")

    # Webhallen fields
    receiver_band = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Receiver band",
        related_name="radio_system_receiver_band",
    )
    receiver_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Receiver type",
        related_name="radio_system_receiver_type",
    )
    number_of_presets = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Number of presets",
        related_name="radio_system_number_of_presets",
    )

    def __str__(self) -> str:
        return "Radio system"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Mottagarband
        receiver_band: Component | None = create_and_import_component(data, "Mottagarband")
        self.receiver_band = receiver_band

        # Mottagartyp
        receiver_type: Component | None = create_and_import_component(data, "Mottagartyp")
        self.receiver_type = receiver_type

        # Antal förinställda stationer
        number_of_presets: Component | None = create_and_import_component(data, "Antal förinställda stationer")
        self.number_of_presets = number_of_presets

        # Warn if there are new fields in the JSON data
        available_fields: list[str] = ["Mottagarband", "Mottagartyp", "Antal förinställda stationer"]
        for key in data:
            if key not in available_fields:
                logger.warning("New field found in RadioSystem: %s", key)


class BuiltInDisplay(auto_prefetch.Model):
    """Inbyggd display."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the built-in display was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the built-in display was last updated")

    # Webhallen fields
    type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Type",
        related_name="built_in_display_type",
    )
    properties = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Properties",
        related_name="built_in_display_properties",
    )

    def __str__(self) -> str:
        return "Built-in display"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Typ
        _type: Component | None = create_and_import_component(data, "Typ")
        self.type = _type

        # Egenskaper
        properties: Component | None = create_and_import_component(data, "Egenskaper")
        self.properties = properties


class IPTelephony(auto_prefetch.Model):
    """IP-telefoni."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the IP telephony was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the IP telephony was last updated")

    # Webhallen fields
    voip = models.ForeignKey(Component, on_delete=models.CASCADE, help_text="VoIP", related_name="ip_telephony_voip")

    def __str__(self) -> str:
        return "IP telephony"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # VoIP
        voip: Component | None = create_and_import_component(data, "VoIP")
        self.voip = voip


class DVD(auto_prefetch.Model):
    """DVD."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the DVD was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the DVD was last updated")

    # Webhallen fields
    # Medietyp som laddas
    media_type_loaded = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Media type loaded",
        related_name="dvd_media_type_loaded",
    )
    # Formfaktor
    form_factor = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Form factor",
        related_name="dvd_form_factor",
    )

    # Typ
    _type = models.ForeignKey(Component, on_delete=models.CASCADE, help_text="Type", related_name="dvd_type")

    # Uppskalning
    upscaling = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Upscaling",
        related_name="dvd_upscaling",
    )

    # Inbyggda ljudavkodare
    built_in_audio_decoders = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Built-in audio decoders",
        related_name="dvd_built_in_audio_decoders",
    )

    # 3D-teknik
    _3d_technology = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="3D technology",
        related_name="dvd_3d_technology",
    )

    # Mediatyp
    media_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Media type",
        related_name="dvd_media_type",
    )

    def __str__(self) -> str:
        return "DVD"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Medietyp som laddas
        media_type_loaded: Component | None = create_and_import_component(data, "Medietyp som laddas")
        self.media_type_loaded = media_type_loaded

        # Formfaktor
        form_factor: Component | None = create_and_import_component(data, "Formfaktor")
        self.form_factor = form_factor

        # Typ
        _type: Component | None = create_and_import_component(data, "Typ")
        self._type = _type

        # Uppskalning
        upscaling: Component | None = create_and_import_component(data, "Uppskalning")
        self.upscaling = upscaling

        # Inbyggda ljudavkodare
        built_in_audio_decoders: Component | None = create_and_import_component(data, "Inbyggda ljudavkodare")
        self.built_in_audio_decoders = built_in_audio_decoders

        # 3D-teknik
        _3d_technology: Component | None = create_and_import_component(data, "3D-teknik")
        self._3d_technology = _3d_technology

        # Mediatyp
        media_type: Component | None = create_and_import_component(data, "Mediatyp")
        self.media_type = media_type


class CESystem(auto_prefetch.Model):
    """CE-system."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the CE system was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the CE system was last updated")

    # Webhallen fields
    # Moderlås
    child_lock = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Child lock",
        related_name="ce_system_child_lock",
    )

    def __str__(self) -> str:
        return "CE system"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Moderlås
        child_lock: Component | None = create_and_import_component(data, "Moderlås")
        self.child_lock = child_lock


class NetworkAndInternetMultimedia(auto_prefetch.Model):
    """Nätverks- och Internet-multimedia."""

    # Django fields
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the network and internet multimedia was created",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When the network and internet multimedia was last updated",
    )

    # Webhallen fields
    # ISS (Internet Streaming Services)
    internet_streaming_services = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Internet Streaming Services",
        related_name="network_and_internet_multimedia_internet_streaming_services",
    )
    # Anslutningsgränssnitt
    connection_interface = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Connection interface",
        related_name="network_and_internet_multimedia_connection_interface",
    )
    # DLNA
    dlna = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="DLNA",
        related_name="network_and_internet_multimedia_dlna",
    )

    # Anknytningsbarhet
    connectivity = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Connectivity",
        related_name="network_and_internet_multimedia_connectivity",
    )

    def __str__(self) -> str:
        return "Network and Internet multimedia"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # ISS (Internet Streaming Services)
        internet_streaming_services: Component | None = create_and_import_component(
            data,
            "ISS (Internet Streaming Services)",
        )
        self.internet_streaming_services = internet_streaming_services

        # Anslutningsgränssnitt
        connection_interface: Component | None = create_and_import_component(data, "Anslutningsgränssnitt")
        self.connection_interface = connection_interface

        # DLNA
        dlna: Component | None = create_and_import_component(data, "DLNA")
        self.dlna = dlna

        # Anknytningsbarhet
        connectivity: Component | None = create_and_import_component(data, "Anknytningsbarhet")
        self.connectivity = connectivity


class Display(auto_prefetch.Model):
    """Bildskärm."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the display was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the display was last updated")

    # Webhallen fields
    # Formfaktor
    form_factor = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Form factor",
        related_name="display_form_factor",
    )

    # Upplösning
    resolution = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Resolution",
        related_name="display_resolution",
    )

    # Responstid
    response_time = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Response time",
        related_name="display_response_time",
    )

    # Ljusstyrka för bild
    brightness = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Brightness",
        related_name="display_brightness",
    )

    # Skärmstorlek
    screen_size = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Screen size",
        related_name="display_screen_size",
    )

    # Bildkontrastförhållande
    image_contrast_ratio = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Image contrast ratio",
        related_name="display_image_contrast_ratio",
    )

    # Horisontell visningsvinkel
    horizontal_viewing_angle = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Horizontal viewing angle",
        related_name="display_horizontal_viewing_angle",
    )

    # Vertikal visningsvinkel
    vertical_viewing_angle = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Vertical viewing angle",
        related_name="display_vertical_viewing_angle",
    )

    # Gränssnitt
    interface = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Interface",
        related_name="display_interface",
    )

    # LCD-bakgrundsbelysningsteknik
    lcd_backlight_technology = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="LCD backlight technology",
        related_name="display_lcd_backlight_technology",
    )

    # Displaylägesjusteringar
    display_adjustments = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Display adjustments",
        related_name="display_display_adjustments",
    )

    # Färgstöd
    color_support = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Color support",
        related_name="display_color_support",
    )

    # Paneltyp
    panel_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Panel type",
        related_name="display_panel_type",
    )

    # Typ
    _type = models.ForeignKey(Component, on_delete=models.CASCADE, help_text="Type", related_name="display_type")

    # Böjd skärm
    curved_screen = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Curved screen",
        related_name="display_curved_screen",
    )

    # Videoformat
    video_format = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Video format",
        related_name="display_video_format",
    )

    # Bildens längd/breddförhållande
    aspect_ratio = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Aspect ratio",
        related_name="display_aspect_ratio",
    )

    # Diagonal storlek (metrisk)
    diagonal_size_metric = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Diagonal size (metric)",
        related_name="display_diagonal_size_metric",
    )

    # Uppdateringsfrekvens
    refresh_rate = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Refresh rate",
        related_name="display_refresh_rate",
    )

    # Normal svarstid
    normal_response_time = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Normal response time",
        related_name="display_normal_response_time",
    )

    # Diagonal storlek
    diagonal_size = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Diagonal size",
        related_name="display_diagonal_size",
    )

    # Dynamisk kontrastkvot
    dynamic_contrast_ratio = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Dynamic contrast ratio",
        related_name="display_dynamic_contrast_ratio",
    )

    # Pixelhöjd
    pixel_pitch = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Pixel pitch",
        related_name="display_pixel_pitch",
    )

    # Adaptive-Sync-teknologi
    adaptive_sync_technology = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Adaptive-Sync technology",
        related_name="display_adaptive_sync_technology",
    )

    # HDR-kapabel
    hdr_capable = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="HDR capable",
        related_name="display_hdr_capable",
    )

    # Kedjekoppling
    daisy_chain = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Daisy chain",
        related_name="display_daisy_chain",
    )

    # Pekskärm
    touchscreen = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Touchscreen",
        related_name="display_touchscreen",
    )

    # Bredbildsskärm
    widescreen = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Widescreen",
        related_name="display_widescreen",
    )

    # Bildskärmsupplösning
    display_resolution = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Display resolution",
        related_name="display_display_resolution",
    )

    # Multi-Touch-display
    multi_touch_display = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Multi-Touch display",
        related_name="display_multi_touch_display",
    )

    # Teknik
    technology = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Technology",
        related_name="display_technology",
    )

    # Visningsformat
    display_format = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Display format",
        related_name="display_display_format",
    )

    # Färgdjup
    color_depth = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Color depth",
        related_name="display_color_depth",
    )

    # Bildförhållande
    image_aspect_ratio = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Image aspect ratio",
        related_name="display_image_aspect_ratio",
    )

    # Vikbar
    foldable = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Foldable",
        related_name="display_foldable",
    )

    # LED-bakgrundsbelysningsteknik
    led_backlight_technology = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="LED backlight technology",
        related_name="display_led_backlight_technology",
    )

    # Smart bildskärm
    smart_display = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Smart display",
        related_name="display_smart_display",
    )

    def __str__(self) -> str:
        return "Display"

    def import_json(self, data: dict) -> None:  # noqa: PLR0914, PLR0915
        """Import JSON data."""
        # Formfaktor
        form_factor: Component | None = create_and_import_component(data, "Formfaktor")
        self.form_factor = form_factor

        # Upplösning
        resolution: Component | None = create_and_import_component(data, "Upplösning")
        self.resolution = resolution

        # Responstid
        response_time: Component | None = create_and_import_component(data, "Responstid")
        self.response_time = response_time

        # Ljusstyrka för bild
        brightness: Component | None = create_and_import_component(data, "Ljusstyrka för bild")
        self.brightness = brightness

        # Skärmstorlek
        screen_size: Component | None = create_and_import_component(data, "Skärmstorlek")
        self.screen_size = screen_size

        # Bildkontrastförhållande
        image_contrast_ratio: Component | None = create_and_import_component(data, "Bildkontrastförhållande")
        self.image_contrast_ratio = image_contrast_ratio

        # Horisontell visningsvinkel
        horizontal_viewing_angle: Component | None = create_and_import_component(data, "Horisontell visningsvinkel")
        self.horizontal_viewing_angle = horizontal_viewing_angle

        # Vertikal visningsvinkel
        vertical_viewing_angle: Component | None = create_and_import_component(data, "Vertikal visningsvinkel")
        self.vertical_viewing_angle = vertical_viewing_angle

        # Gränssnitt
        interface: Component | None = create_and_import_component(data, "Gränssnitt")
        self.interface = interface

        # LCD-bakgrundsbelysningsteknik
        lcd_backlight_technology: Component | None = create_and_import_component(data, "LCD-bakgrundsbelysningsteknik")
        self.lcd_backlight_technology = lcd_backlight_technology

        # Displaylägesjusteringar
        display_adjustments: Component | None = create_and_import_component(data, "Displaylägesjusteringar")
        self.display_adjustments = display_adjustments

        # Färgstöd
        color_support: Component | None = create_and_import_component(data, "Färgstöd")
        self.color_support = color_support

        # Paneltyp
        panel_type: Component | None = create_and_import_component(data, "Paneltyp")
        self.panel_type = panel_type

        # Typ
        _type: Component | None = create_and_import_component(data, "Typ")
        self._type = _type

        # Böjd skärm
        curved_screen: Component | None = create_and_import_component(data, "Böjd skärm")
        self.curved_screen = curved_screen

        # Videoformat
        video_format: Component | None = create_and_import_component(data, "Videoformat")
        self.video_format = video_format

        # Bildens längd/breddförhållande
        aspect_ratio: Component | None = create_and_import_component(data, "Bildens längd/breddförhållande")
        self.aspect_ratio = aspect_ratio

        # Diagonal storlek (metrisk)
        diagonal_size_metric: Component | None = create_and_import_component(data, "Diagonal storlek (metrisk)")
        self.diagonal_size_metric = diagonal_size_metric

        # Uppdateringsfrekvens
        refresh_rate: Component | None = create_and_import_component(data, "Uppdateringsfrekvens")
        self.refresh_rate = refresh_rate

        # Normal svarstid
        normal_response_time: Component | None = create_and_import_component(data, "Normal svarstid")
        self.normal_response_time = normal_response_time

        # Diagonal storlek
        diagonal_size: Component | None = create_and_import_component(data, "Diagonal storlek")
        self.diagonal_size = diagonal_size

        # Dynamisk kontrastkvot
        dynamic_contrast_ratio: Component | None = create_and_import_component(data, "Dynamisk kontrastkvot")
        self.dynamic_contrast_ratio = dynamic_contrast_ratio

        # Pixelhöjd
        pixel_pitch: Component | None = create_and_import_component(data, "Pixelhöjd")
        self.pixel_pitch = pixel_pitch

        # Adaptive-Sync-teknologi
        adaptive_sync_technology: Component | None = create_and_import_component(data, "Adaptive-Sync-teknologi")
        self.adaptive_sync_technology = adaptive_sync_technology

        # HDR-kapabel
        hdr_capable: Component | None = create_and_import_component(data, "HDR-kapabel")
        self.hdr_capable = hdr_capable

        # Kedjekoppling
        daisy_chain: Component | None = create_and_import_component(data, "Kedjekoppling")
        self.daisy_chain = daisy_chain

        # Pekskärm
        touchscreen: Component | None = create_and_import_component(data, "Pekskärm")
        self.touchscreen = touchscreen

        # Bredbildsskärm
        widescreen: Component | None = create_and_import_component(data, "Bredbildsskärm")
        self.widescreen = widescreen

        # Bildskärmsupplösning
        display_resolution: Component | None = create_and_import_component(data, "Bildskärmsupplösning")
        self.display_resolution = display_resolution

        # Multi-Touch-display
        multi_touch_display: Component | None = create_and_import_component(data, "Multi-Touch-display")
        self.multi_touch_display = multi_touch_display

        # Teknik
        technology: Component | None = create_and_import_component(data, "Teknik")
        self.technology = technology

        # Visningsformat
        display_format: Component | None = create_and_import_component(data, "Visningsformat")
        self.display_format = display_format

        # Färgdjup
        color_depth: Component | None = create_and_import_component(data, "Färgdjup")
        self.color_depth = color_depth

        # Bildförhållande
        image_aspect_ratio: Component | None = create_and_import_component(data, "Bildförhållande")
        self.image_aspect_ratio = image_aspect_ratio

        # Vikbar
        foldable: Component | None = create_and_import_component(data, "Vikbar")
        self.foldable = foldable

        # LED-bakgrundsbelysningsteknik
        led_backlight_technology: Component | None = create_and_import_component(data, "LED-bakgrundsbelysningsteknik")
        self.led_backlight_technology = led_backlight_technology

        # Smart bildskärm
        smart_display: Component | None = create_and_import_component(data, "Smart bildskärm")
        self.smart_display = smart_display


class TVTuner(auto_prefetch.Model):
    """TV-tuner."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the TV tuner was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the TV tuner was last updated")

    # Webhallen fields
    # TV-mottagaravkänning
    tv_receiver_detection = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="TV receiver detection",
        related_name="tv_tuner_tv_receiver_detection",
    )

    # Digital TV-mottagare
    digital_tv_receiver = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Digital TV receiver",
        related_name="tv_tuner_digital_tv_receiver",
    )

    # Konfigurering mottagare
    receiver_configuration = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Receiver configuration",
        related_name="tv_tuner_receiver_configuration",
    )

    # Villkorsstyrd åtkomst
    conditional_access = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Conditional access",
        related_name="tv_tuner_conditional_access",
    )

    # Text-TV
    teletext = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Teletext",
        related_name="tv_tuner_teletext",
    )

    # HDTV-mottagare
    hdtv_receiver = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="HDTV receiver",
        related_name="tv_tuner_hdtv_receiver",
    )

    # Digital-TV-service
    digital_tv_service = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Digital TV service",
        related_name="tv_tuner_digital_tv_service",
    )

    # Förhandsvisning för flera kanaler
    multi_channel_preview = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Multi-channel preview",
        related_name="tv_tuner_multi_channel_preview",
    )

    def __str__(self) -> str:
        return "TV tuner"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # TV-mottagaravkänning
        tv_receiver_detection: Component | None = create_and_import_component(data, "TV-mottagaravkänning")
        self.tv_receiver_detection = tv_receiver_detection

        # Digital TV-mottagare
        digital_tv_receiver: Component | None = create_and_import_component(data, "Digital TV-mottagare")
        self.digital_tv_receiver = digital_tv_receiver

        # Konfigurering mottagare
        receiver_configuration: Component | None = create_and_import_component(data, "Konfigurering mottagare")
        self.receiver_configuration = receiver_configuration

        # Villkorsstyrd åtkomst
        conditional_access: Component | None = create_and_import_component(data, "Villkorsstyrd åtkomst")
        self.conditional_access = conditional_access

        # Text-TV
        teletext: Component | None = create_and_import_component(data, "Text-TV")
        self.teletext = teletext

        # HDTV-mottagare
        hdtv_receiver: Component | None = create_and_import_component(data, "HDTV-mottagare")
        self.hdtv_receiver = hdtv_receiver

        # Digital-TV-service
        digital_tv_service: Component | None = create_and_import_component(data, "Digital-TV-service")
        self.digital_tv_service = digital_tv_service

        # Förhandsvisning för flera kanaler
        multi_channel_preview: Component | None = create_and_import_component(data, "Förhandsvisning för flera kanaler")
        self.multi_channel_preview = multi_channel_preview


class OpticalSensor(auto_prefetch.Model):
    """Optisk sensor."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the optical sensor was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the optical sensor was last updated")

    # Webhallen fields
    # Totalt antal pixlar
    total_pixels = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Total pixels",
        related_name="optical_sensor_total_pixels",
    )

    # Sensorstorlek
    sensor_size = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Sensor size",
        related_name="optical_sensor_sensor_size",
    )

    # Sensorstorlek (metrisk)
    sensor_size_metric = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Sensor size (metric)",
        related_name="optical_sensor_sensor_size_metric",
    )

    # Bildsensortyp
    image_sensor_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Image sensor type",
        related_name="optical_sensor_image_sensor_type",
    )

    # Antal sensorer
    number_of_sensors = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Number of sensors",
        related_name="optical_sensor_number_of_sensors",
    )

    # Sensorupplösning för videokamera
    video_camera_sensor_resolution = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Video camera sensor resolution",
        related_name="optical_sensor_video_camera_sensor_resolution",
    )

    # Effektiv upplösning för videobandspelare (fotoläge)
    video_recorder_effective_still_resolution = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Video recorder effective still resolution",
        related_name="optical_sensor_video_recorder_effective_still_resolution",
    )

    # Sensorupplösning
    sensor_resolution = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Sensor resolution",
        related_name="optical_sensor_sensor_resolution",
    )

    # Bildsensor storlek
    image_sensor_size = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Image sensor size",
        related_name="optical_sensor_image_sensor_size",
    )

    # Optisk sensorstorlek (metrisk)
    optical_sensor_size_metric = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Optical sensor size (metric)",
        related_name="optical_sensor_optical_sensor_size_metric",
    )

    def __str__(self) -> str:
        return "Optical sensor"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Totalt antal pixlar
        total_pixels: Component | None = create_and_import_component(data, "Totalt antal pixlar")
        self.total_pixels = total_pixels

        # Sensorstorlek
        sensor_size: Component | None = create_and_import_component(data, "Sensorstorlek")
        self.sensor_size = sensor_size

        # Sensorstorlek (metrisk)
        sensor_size_metric: Component | None = create_and_import_component(data, "Sensorstorlek (metrisk)")
        self.sensor_size_metric = sensor_size_metric

        # Bildsensortyp
        image_sensor_type: Component | None = create_and_import_component(data, "Bildsensortyp")
        self.image_sensor_type = image_sensor_type

        # Antal sensorer
        number_of_sensors: Component | None = create_and_import_component(data, "Antal sensorer")
        self.number_of_sensors = number_of_sensors

        # Sensorupplösning för videokamera
        video_camera_sensor_resolution: Component | None = create_and_import_component(
            data,
            "Sensorupplösning för videokamera",
        )
        self.video_camera_sensor_resolution = video_camera_sensor_resolution

        # Effektiv upplösning för videobandspelare (fotoläge
        video_recorder_effective_still_resolution: Component | None = create_and_import_component(
            data,
            "Effektiv upplösning för videobandspelare (fotoläge)",
        )
        self.video_recorder_effective_still_resolution = video_recorder_effective_still_resolution

        # Sensorupplösning
        sensor_resolution: Component | None = create_and_import_component(data, "Sensorupplösning")
        self.sensor_resolution = sensor_resolution

        # Bildsensor storlek
        image_sensor_size: Component | None = create_and_import_component(data, "Bildsensor storlek")
        self.image_sensor_size = image_sensor_size

        # Optisk sensorstorlek (metrisk)
        optical_sensor_size_metric: Component | None = create_and_import_component(
            data,
            "Optisk sensorstorlek (metrisk)",
        )
        self.optical_sensor_size_metric = optical_sensor_size_metric


class SurveillanceCamera(auto_prefetch.Model):
    """Övervakningskamera."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the surveillance camera was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the surveillance camera was last updated")

    # Webhallen fields
    # Inom-/utomhus
    indoor_outdoor = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Indoor/outdoor",
        related_name="surveillance_camera_indoor_outdoor",
    )

    # Inomhus/utomhus
    indoor_outdoor_ = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Indoor/outdoor",
        related_name="surveillance_camera_indoor_outdoor_",
    )

    def __str__(self) -> str:
        return "Surveillance camera"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Inom-/utomhus
        indoor_outdoor: Component | None = create_and_import_component(data, "Inom-/utomhus")
        self.indoor_outdoor = indoor_outdoor

        # Inomhus/utomhus
        indoor_outdoor_: Component | None = create_and_import_component(data, "Inomhus/utomhus")
        self.indoor_outdoor_ = indoor_outdoor_


class GameConsole(auto_prefetch.Model):
    """Spelkonsol."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the game console was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the game console was last updated")

    # Webhallen fields
    # Typ
    _type = models.ForeignKey(Component, on_delete=models.CASCADE, help_text="Type", related_name="game_console_type")

    # Namn
    name = models.ForeignKey(Component, on_delete=models.CASCADE, help_text="Name", related_name="game_console_name")

    # Lagringskapacitet
    storage_capacity = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Storage capacity",
        related_name="game_console_storage_capacity",
    )

    def __str__(self) -> str:
        return "Game console"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Typ
        _type: Component | None = create_and_import_component(data, "Typ")
        self._type = _type

        # Namn
        name: Component | None = create_and_import_component(data, "Namn")
        self.name = name

        # Lagringskapacitet
        storage_capacity: Component | None = create_and_import_component(data, "Lagringskapacitet")
        self.storage_capacity = storage_capacity


class QuickFilmDevelopment(auto_prefetch.Model):
    """Snabbframkallningsfilm."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the quick film development was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the quick film development was last updated")

    # Webhallen fields
    # Exponeringar per kassett
    exposures_per_cassette = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Exposures per cassette",
        related_name="quick_film_development_exposures_per_cassette",
    )

    # Bildområde
    image_area = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Image area",
        related_name="quick_film_development_image_area",
    )

    # Format
    _format = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Format",
        related_name="quick_film_development_format",
    )

    def __str__(self) -> str:
        return "Quick film development"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Exponeringar per kassett
        exposures_per_cassette: Component | None = create_and_import_component(data, "Exponeringar per kassett")
        self.exposures_per_cassette = exposures_per_cassette

        # Bildområde
        image_area: Component | None = create_and_import_component(data, "Bildområde")
        self.image_area = image_area

        # Format
        _format: Component | None = create_and_import_component(data, "Format")
        self._format = _format


class Film(auto_prefetch.Model):
    """Film."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the film was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the film was last updated")

    # Webhallen fields
    # Hastighet
    speed = models.ForeignKey(Component, on_delete=models.CASCADE, help_text="Speed", related_name="film_speed")

    # Typ
    _type = models.ForeignKey(Component, on_delete=models.CASCADE, help_text="Type", related_name="film_type")

    # Underkategori
    subcategory = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Subcategory",
        related_name="film_subcategory",
    )

    def __str__(self) -> str:
        return "Film"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Hastighet
        speed: Component | None = create_and_import_component(data, "Hastighet")
        self.speed = speed

        # Typ
        _type: Component | None = create_and_import_component(data, "Typ")
        self._type = _type

        # Underkategori
        subcategory: Component | None = create_and_import_component(data, "Underkategori")
        self.subcategory = subcategory


class CablesAndWires(auto_prefetch.Model):
    """Kablar och ledningar."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the cables and wires was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the cables and wires was last updated")

    # Webhallen fields
    # Teknik
    technology = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Technology",
        related_name="cables_and_wires_technology",
    )

    # Antal portar
    number_of_ports = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Number of ports",
        related_name="cables_and_wires_number_of_ports",
    )

    # Kategori
    category = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Category",
        related_name="cables_and_wires_category",
    )

    def __str__(self) -> str:
        return "Cables and wires"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Teknik
        technology: Component | None = create_and_import_component(data, "Teknik")
        self.technology = technology

        # Antal portar
        number_of_ports: Component | None = create_and_import_component(data, "Antal portar")
        self.number_of_ports = number_of_ports

        # Kategori
        category: Component | None = create_and_import_component(data, "Kategori")
        self.category = category


class NetworkTester(auto_prefetch.Model):
    """Nätverkstestare."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the network tester was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the network tester was last updated")

    # Webhallen fields
    # Enhetstyp
    device_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Device type",
        related_name="network_tester_device_type",
    )

    def __str__(self) -> str:
        return "Network tester"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Enhetstyp
        device_type: Component | None = create_and_import_component(data, "Enhetstyp")
        self.device_type = device_type


class Bag(auto_prefetch.Model):
    """Väska."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the bag was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the bag was last updated")

    # Webhallen fields
    # Färg
    color = models.ForeignKey(Component, on_delete=models.CASCADE, help_text="Color", related_name="bag_color")

    # Material
    material = models.ForeignKey(Component, on_delete=models.CASCADE, help_text="Material", related_name="bag_material")

    # Rekommenderad användning
    recommended_use = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Recommended use",
        related_name="bag_recommended_use",
    )

    # Typ
    _type = models.ForeignKey(Component, on_delete=models.CASCADE, help_text="Type", related_name="bag_type")

    # Bärrem
    shoulder_strap = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Shoulder strap",
        related_name="bag_shoulder_strap",
    )

    # Ytterligare utrymmen
    additional_compartments = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Additional compartments",
        related_name="bag_additional_compartments",
    )

    def __str__(self) -> str:
        return "Bag"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Färg
        color: Component | None = create_and_import_component(data, "Färg")
        self.color = color

        # Material
        material: Component | None = create_and_import_component(data, "Material")
        self.material = material

        # Rekommenderad användning
        recommended_use: Component | None = create_and_import_component(data, "Rekommenderad användning")
        self.recommended_use = recommended_use

        # Typ
        _type: Component | None = create_and_import_component(data, "Typ")
        self._type = _type

        # Bärrem
        shoulder_strap: Component | None = create_and_import_component(data, "Bärrem")
        self.shoulder_strap = shoulder_strap

        # Ytterligare utrymmen
        additional_compartments: Component | None = create_and_import_component(data, "Ytterligare utrymmen")
        self.additional_compartments = additional_compartments


class Motherboard(auto_prefetch.Model):
    """Moderkort."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the motherboard was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the motherboard was last updated")

    # Webhallen fields
    # Formfaktor
    form_factor = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Form factor",
        related_name="motherboard_form_factor",
    )

    # Kompatibla processorer
    compatible_processors = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Compatible processors",
        related_name="motherboard_compatible_processors",
    )

    # Processor-socket
    processor_socket = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Processor socket",
        related_name="motherboard_processor_socket",
    )

    # RAM-hastighet som stöds
    supported_ram_speed = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Supported RAM speed",
        related_name="motherboard_supported_ram_speed",
    )

    # RAM-teknik som stöds
    supported_ram_technology = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Supported RAM technology",
        related_name="motherboard_supported_ram_technology",
    )

    # RAM som stöds (registrerad eller buffrad)
    supported_ram_registered_or_buffered = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Supported RAM (registered or buffered)",
        related_name="motherboard_supported_ram_registered_or_buffered",
    )

    # Kretstyp
    chipset_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Chipset type",
        related_name="motherboard_chipset_type",
    )

    # Stöder Ram Integrity Check
    supports_ram_integrity_check = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Supports Ram Integrity Check",
        related_name="motherboard_supports_ram_integrity_check",
    )

    def __str__(self) -> str:
        return "Motherboard"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Formfaktor
        form_factor: Component | None = create_and_import_component(data, "Formfaktor")
        self.form_factor = form_factor

        # Kompatibla processorer
        compatible_processors: Component | None = create_and_import_component(data, "Kompatibla processorer")
        self.compatible_processors = compatible_processors

        # Processor-socket
        processor_socket: Component | None = create_and_import_component(data, "Processor-socket")
        self.processor_socket = processor_socket

        # RAM-hastighet som stöds
        supported_ram_speed: Component | None = create_and_import_component(data, "RAM-hastighet som stöds")
        self.supported_ram_speed = supported_ram_speed

        # RAM-teknik som stöds
        supported_ram_technology: Component | None = create_and_import_component(data, "RAM-teknik som stöds")
        self.supported_ram_technology = supported_ram_technology

        # RAM som stöds (registrerad eller buffrad)
        supported_ram_registered_or_buffered: Component | None = create_and_import_component(
            data,
            "RAM som stöds (registrerad eller buffrad)",
        )
        self.supported_ram_registered_or_buffered = supported_ram_registered_or_buffered

        # Kretstyp
        chipset_type: Component | None = create_and_import_component(data, "Kretstyp")
        self.chipset_type = chipset_type

        # Stöder Ram Integrity Check
        supports_ram_integrity_check: Component | None = create_and_import_component(data, "Stöder Ram Integrity Check")
        self.supports_ram_integrity_check = supports_ram_integrity_check


class Chassis(auto_prefetch.Model):
    """Chassi."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the chassis was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the chassis was last updated")

    # Webhallen fields
    # Formfaktor
    form_factor = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Form factor",
        related_name="chassis_form_factor",
    )

    # Antal interna fack
    number_of_internal_bays = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Number of internal bays",
        related_name="chassis_number_of_internal_bays",
    )

    # Tillverkarens format
    manufacturer_form_factor = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Manufacturer's format",
        related_name="chassis_manufacturer_form_factor",
    )

    # Max. höjd på CPU-kylare
    max_cpu_cooler_height = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Max. height of CPU cooler",
        related_name="chassis_max_cpu_cooler_height",
    )

    # Max. längd på videokort
    max_video_card_length = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Max. length of video card",
        related_name="chassis_max_video_card_length",
    )

    # Inbyggd USB-hubb
    built_in_usb_hub = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Built-in USB hub",
        related_name="chassis_built_in_usb_hub",
    )

    # Material på sidopanelens fönster
    side_panel_window_material = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Material of side panel window",
        related_name="chassis_side_panel_window_material",
    )

    # Sidopanel med fönster
    side_panel_window = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Side panel with window",
        related_name="chassis_side_panel_window",
    )

    # Maxlängd, strömförsörjning
    max_psu_length = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Max length, power supply",
        related_name="chassis_max_psu_length",
    )

    # Antal fack för hot-swap
    number_of_hot_swap_bays = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Number of hot-swap bays",
        related_name="chassis_number_of_hot_swap_bays",
    )

    # Antal fack på framsidan
    number_of_front_bays = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Number of front bays",
        related_name="chassis_number_of_front_bays",
    )

    # Inbyggd kamera
    built_in_camera = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Built-in camera",
        related_name="chassis_built_in_camera",
    )

    # Antal enheter/moduler som stöds
    number_of_supported_units_modules = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Number of supported units/modules",
        related_name="chassis_number_of_supported_units_modules",
    )

    # Antal installerade enheter / moduler
    number_of_installed_units_modules = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Number of installed units/modules",
        related_name="chassis_number_of_installed_units_modules",
    )

    # USB-strömförsörjning
    usb_power_supply = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="USB power supply",
        related_name="chassis_usb_power_supply",
    )

    # Inbyggt Ethernet
    built_in_ethernet = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Built-in Ethernet",
        related_name="chassis_built_in_ethernet",
    )

    def __str__(self) -> str:
        return "Chassis"

    def import_json(self, data: dict) -> None:  # noqa: PLR0914
        """Import JSON data."""
        # Formfaktor
        form_factor: Component | None = create_and_import_component(data, "Formfaktor")
        self.form_factor = form_factor

        # Antal interna fack
        number_of_internal_bays: Component | None = create_and_import_component(data, "Antal interna fack")
        self.number_of_internal_bays = number_of_internal_bays

        # Tillverkarens format
        manufacturer_form_factor: Component | None = create_and_import_component(data, "Tillverkarens format")
        self.manufacturer_form_factor = manufacturer_form_factor

        # Max. höjd på CPU-kylare
        max_cpu_cooler_height: Component | None = create_and_import_component(data, "Max. höjd på CPU-kylare")
        self.max_cpu_cooler_height = max_cpu_cooler_height

        # Max. längd på videokort
        max_video_card_length: Component | None = create_and_import_component(data, "Max. längd på videokort")
        self.max_video_card_length = max_video_card_length

        # Inbyggd USB-hubb
        built_in_usb_hub: Component | None = create_and_import_component(data, "Inbyggd USB-hubb")
        self.built_in_usb_hub = built_in_usb_hub

        # Material på sidopanelens fönster
        side_panel_window_material: Component | None = create_and_import_component(
            data,
            "Material på sidopanelens fönster",
        )
        self.side_panel_window_material = side_panel_window_material

        # Sidopanel med fönster
        side_panel_window: Component | None = create_and_import_component(data, "Sidopanel med fönster")
        self.side_panel_window = side_panel_window

        # Maxlängd, strömförsörjning
        max_psu_length: Component | None = create_and_import_component(data, "Maxlängd, strömförsörjning")
        self.max_psu_length = max_psu_length

        # Antal fack för hot-swap
        number_of_hot_swap_bays: Component | None = create_and_import_component(data, "Antal fack för hot-swap")
        self.number_of_hot_swap_bays = number_of_hot_swap_bays

        # Antal fack på framsidan
        number_of_front_bays: Component | None = create_and_import_component(data, "Antal fack på framsidan")
        self.number_of_front_bays = number_of_front_bays

        # Inbyggd kamera
        built_in_camera: Component | None = create_and_import_component(data, "Inbyggd kamera")
        self.built_in_camera = built_in_camera

        # Antal enheter/moduler som stöds
        number_of_supported_units_modules: Component | None = create_and_import_component(
            data,
            "Antal enheter/moduler som stöds",
        )
        self.number_of_supported_units_modules = number_of_supported_units_modules

        # Antal installerade enheter / moduler
        number_of_installed_units_modules: Component | None = create_and_import_component(
            data,
            "Antal installerade enheter / moduler",
        )
        self.number_of_installed_units_modules = number_of_installed_units_modules

        # USB-strömförsörjning
        usb_power_supply: Component | None = create_and_import_component(data, "USB-strömförsörjning")
        self.usb_power_supply = usb_power_supply

        # Inbyggt Ethernet
        built_in_ethernet: Component | None = create_and_import_component(data, "Inbyggt Ethernet")
        self.built_in_ethernet = built_in_ethernet


class Mobile(auto_prefetch.Model):
    """Mobil."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the mobile was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the mobile was last updated")

    # Webhallen fields
    # Teknik
    technology = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Technology",
        related_name="mobile_technology",
    )

    # Typ
    _type = models.ForeignKey(Component, on_delete=models.CASCADE, help_text="Type", related_name="mobile_type")

    # Telefon formfaktor
    phone_form_factor = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Phone form factor",
        related_name="mobile_phone_form_factor",
    )

    # Serviceleverantör
    service_provider = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Service provider",
        related_name="mobile_service_provider",
    )

    # SIM-korttyp
    sim_card_type = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="SIM card type",
        related_name="mobile_sim_card_type",
    )

    # Antal SIM-kortplatser
    number_of_sim_card_slots = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Number of SIM card slots",
        related_name="mobile_number_of_sim_card_slots",
    )

    # Operativsystem
    operating_system = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Operating system",
        related_name="mobile_operating_system",
    )

    # Kontakter
    contacts = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Contacts",
        related_name="mobile_contacts",
    )

    # Generationen mobilt bredband
    mobile_broadband_generation = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Generation of mobile broadband",
        related_name="mobile_mobile_broadband_generation",
    )

    # Operativsystemfamilj
    operating_system_family = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Operating system family",
        related_name="mobile_operating_system_family",
    )

    # Användargränssnitt
    user_interface = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="User interface",
        related_name="mobile_user_interface",
    )

    # Inbyggda komponenter
    built_in_components = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Built-in components",
        related_name="mobile_built_in_components",
    )

    def __str__(self) -> str:
        return "Mobile"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Teknik
        technology: Component | None = create_and_import_component(data, "Teknik")
        self.technology = technology

        # Typ
        _type: Component | None = create_and_import_component(data, "Typ")
        self._type = _type

        # Telefon formfaktor
        phone_form_factor: Component | None = create_and_import_component(data, "Telefon formfaktor")
        self.phone_form_factor = phone_form_factor

        # Serviceleverantör
        service_provider: Component | None = create_and_import_component(data, "Serviceleverantör")
        self.service_provider = service_provider

        # SIM-korttyp
        sim_card_type: Component | None = create_and_import_component(data, "SIM-korttyp")
        self.sim_card_type = sim_card_type

        # Antal SIM-kortplatser
        number_of_sim_card_slots: Component | None = create_and_import_component(data, "Antal SIM-kortplatser")
        self.number_of_sim_card_slots = number_of_sim_card_slots

        # Operativsystem
        operating_system: Component | None = create_and_import_component(data, "Operativsystem")
        self.operating_system = operating_system

        # Kontakter
        contacts: Component | None = create_and_import_component(data, "Kontakter")
        self.contacts = contacts

        # Generationen mobilt bredband
        mobile_broadband_generation: Component | None = create_and_import_component(
            data,
            "Generationen mobilt bredband",
        )
        self.mobile_broadband_generation = mobile_broadband_generation

        # Operativsystemfamilj
        operating_system_family: Component | None = create_and_import_component(data, "Operativsystemfamilj")
        self.operating_system_family = operating_system_family

        # Användargränssnitt
        user_interface: Component | None = create_and_import_component(data, "Användargränssnitt")
        self.user_interface = user_interface

        # Inbyggda komponenter
        built_in_components: Component | None = create_and_import_component(data, "Inbyggda komponenter")
        self.built_in_components = built_in_components


class Communications(auto_prefetch.Model):
    """Kommunikationer."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the communications was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the communications was last updated")

    # Webhallen fields
    # Trådlöst gränssnitt
    wireless_interface = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Wireless interface",
        related_name="communications_wireless_interface",
    )

    # Dataöverföring
    data_transfer = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Data transfer",
        related_name="communications_data_transfer",
    )

    def __str__(self) -> str:
        return "Communications"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Trådlöst gränssnitt
        wireless_interface: Component | None = create_and_import_component(data, "Trådlöst gränssnitt")
        self.wireless_interface = wireless_interface

        # Dataöverföring
        data_transfer: Component | None = create_and_import_component(data, "Dataöverföring")
        self.data_transfer = data_transfer


class Processor(auto_prefetch.Model):
    """Processor."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the processor was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the processor was last updated")

    # Webhallen fields
    # Tillverkare
    manufacturer = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Manufacturer",
        related_name="processor_manufacturer",
    )

    # Processor
    processor = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Processor",
        related_name="processor_processor",
    )

    # Klockfrekvens
    clock_frequency = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Clock frequency",
        related_name="processor_clock_frequency",
    )

    # Generation
    generation = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Generation",
        related_name="processor_generation",
    )

    # Antal processorkärnor
    number_of_processor_cores = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Number of processor cores",
        related_name="processor_number_of_processor_cores",
    )

    # Processorfamilj
    processor_family = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Processor family",
        related_name="processor_processor_family",
    )

    # Funktioner
    features = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Features",
        related_name="processor_features",
    )

    # Installerat antal
    installed_number = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Installed number",
        related_name="processor_installed_number",
    )

    # Sockel
    socket = models.ForeignKey(Component, on_delete=models.CASCADE, help_text="Socket", related_name="processor_socket")

    # Cache
    cache = models.ForeignKey(Component, on_delete=models.CASCADE, help_text="Cache", related_name="processor_cache")

    # Max antal som stöds
    max_supported_number = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Max supported number",
        related_name="processor_max_supported_number",
    )

    # Busshastighet
    bus_speed = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Bus speed",
        related_name="processor_bus_speed",
    )

    # Möjligheter till uppgradering
    upgrade_options = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Upgrade options",
        related_name="processor_upgrade_options",
    )

    def __str__(self) -> str:
        return "Processor"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Tillverkare
        manufacturer: Component | None = create_and_import_component(data, "Tillverkare")
        self.manufacturer = manufacturer

        # Processor
        processor: Component | None = create_and_import_component(data, "Processor")
        self.processor = processor

        # Klockfrekvens
        clock_frequency: Component | None = create_and_import_component(data, "Klockfrekvens")
        self.clock_frequency = clock_frequency

        # Generation
        generation: Component | None = create_and_import_component(data, "Generation")
        self.generation = generation

        # Antal processorkärnor
        number_of_processor_cores: Component | None = create_and_import_component(data, "Antal processorkärnor")
        self.number_of_processor_cores = number_of_processor_cores

        # Processorfamilj
        processor_family: Component | None = create_and_import_component(data, "Processorfamilj")
        self.processor_family = processor_family

        # Funktioner
        features: Component | None = create_and_import_component(data, "Funktioner")
        self.features = features

        # Installerat antal
        installed_number: Component | None = create_and_import_component(data, "Installerat antal")
        self.installed_number = installed_number

        # Sockel
        socket: Component | None = create_and_import_component(data, "Sockel")
        self.socket = socket

        # Cache
        cache: Component | None = create_and_import_component(data, "Cache")
        self.cache = cache

        # Max antal som stöds
        max_supported_number: Component | None = create_and_import_component(data, "Max antal som stöds")
        self.max_supported_number = max_supported_number

        # Busshastighet
        bus_speed: Component | None = create_and_import_component(data, "Busshastighet")
        self.bus_speed = bus_speed

        # Möjligheter till uppgradering
        upgrade_options: Component | None = create_and_import_component(data, "Möjligheter till uppgradering")
        self.upgrade_options = upgrade_options


class Toasters(auto_prefetch.Model):
    """Brödrostar."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the toasters was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the toasters was last updated")

    # Webhallen fields
    # Antal rostningsnivåer
    number_of_toasting_levels = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Number of toasting levels",
        related_name="toasters_number_of_toasting_levels",
    )

    def __str__(self) -> str:
        return "Toasters"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Antal rostningsnivåer
        number_of_toasting_levels: Component | None = create_and_import_component(data, "Antal rostningsnivåer")
        self.number_of_toasting_levels = number_of_toasting_levels


class EnvironmentalStandards(auto_prefetch.Model):
    """Miljöstandarder."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the environmental standards was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the environmental standards was last updated")

    # Webhallen fields
    # ENERGY STAR-certifierad
    energy_star_certified = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="ENERGY STAR-certified",
        related_name="environmental_standards_energy_star_certified",
    )

    # ENERGY STAR
    energy_star = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="ENERGY STAR",
        related_name="environmental_standards_energy_star",
    )

    # Blue Angel-kompatibel
    blue_angel_compatible = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Blue Angel-compatible",
        related_name="environmental_standards_blue_angel_compatible",
    )

    # Ekomärkning Nordic Swan
    ecolabel_nordic_swan = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Ecolabel Nordic Swan",
        related_name="environmental_standards_ecolabel_nordic_swan",
    )

    # TCO-certifiering
    tco_certification = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="TCO certification",
        related_name="environmental_standards_tco_certification",
    )

    # TCO-certifierad
    tco_certified = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="TCO certified",
        related_name="environmental_standards_tco_certified",
    )

    # EPEAT-nivå
    epeat_level = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="EPEAT level",
        related_name="environmental_standards_epeat_level",
    )

    # EPEAT-kompatibel
    epeat_compatible = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="EPEAT-compatible",
        related_name="environmental_standards_epeat_compatible",
    )

    # Blå ängel
    blue_angel = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        help_text="Blue Angel",
        related_name="environmental_standards_blue_angel",
    )

    def __str__(self) -> str:
        return "Environmental standards"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # ENERGY STAR-certifierad
        energy_star_certified: Component | None = create_and_import_component(data, "ENERGY STAR-certifierad")
        self.energy_star_certified = energy_star_certified

        # ENERGY STAR
        energy_star: Component | None = create_and_import_component(data, "ENERGY STAR")
        self.energy_star = energy_star

        # Blue Angel-kompatibel
        blue_angel_compatible: Component | None = create_and_import_component(data, "Blue Angel-kompatibel")
        self.blue_angel_compatible = blue_angel_compatible

        # Ekomärkning Nordic Swan
        ecolabel_nordic_swan: Component | None = create_and_import_component(data, "Ekomärkning Nordic Swan")
        self.ecolabel_nordic_swan = ecolabel_nordic_swan

        # TCO-certifiering
        tco_certification: Component | None = create_and_import_component(data, "TCO-certifiering")
        self.tco_certification = tco_certification

        # TCO-certifierad
        tco_certified: Component | None = create_and_import_component(data, "TCO-certifierad")
        self.tco_certified = tco_certified

        # EPEAT-nivå
        epeat_level: Component | None = create_and_import_component(data, "EPEAT-nivå")
        self.epeat_level = epeat_level

        # EPEAT-kompatibel
        epeat_compatible: Component | None = create_and_import_component(data, "EPEAT-kompatibel")
        self.epeat_compatible = epeat_compatible

        # Blå ängel
        blue_angel: Component | None = create_and_import_component(data, "Blå ängel")
        self.blue_angel = blue_angel


class Data(auto_prefetch.Model):
    """Data."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the data was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the data was last updated")

    # Webhallen fields
    cable = models.ForeignKey(Cable, on_delete=models.CASCADE, help_text="Cable", related_name="data_cable")
    header = models.ForeignKey(Header, on_delete=models.CASCADE, help_text="Header", related_name="data_header")
    dimensions_and_weight = models.ForeignKey(
        DimensionsAndWeight,
        on_delete=models.CASCADE,
        help_text="Dimensions and weight",
        related_name="data_dimensions_and_weight",
    )
    general = models.ForeignKey(General, on_delete=models.CASCADE, help_text="General", related_name="data_general")
    miscellaneous = models.ForeignKey(
        Miscellaneous,
        on_delete=models.CASCADE,
        help_text="Miscellaneous",
        related_name="data_miscellaneous",
    )
    input_device = models.ForeignKey(
        InputDevice,
        on_delete=models.CASCADE,
        help_text="Input device",
        related_name="data_input_device",
    )
    service_and_support = models.ForeignKey(
        ServiceAndSupport,
        on_delete=models.CASCADE,
        help_text="Service and support",
        related_name="data_service_and_support",
    )
    gross_dimensions_and_weight = models.ForeignKey(
        GrossDimensionsAndWeight,
        on_delete=models.CASCADE,
        help_text="Gross dimensions and weight",
        related_name="data_gross_dimensions_and_weight",
    )
    consumables = models.ForeignKey(
        Consumables,
        on_delete=models.CASCADE,
        help_text="Consumables",
        related_name="data_consumables",
    )
    battery = models.ForeignKey(Battery, on_delete=models.CASCADE, help_text="Battery", related_name="data_battery")
    av_components = models.ForeignKey(
        AVComponent,
        on_delete=models.CASCADE,
        help_text="AV components",
        related_name="data_av_components",
    )
    remote_control = models.ForeignKey(
        RemoteControl,
        on_delete=models.CASCADE,
        help_text="Remote control",
        related_name="data_remote_control",
    )
    video_input = models.ForeignKey(
        VideoInput,
        on_delete=models.CASCADE,
        help_text="Video input",
        related_name="data_video_input",
    )
    system_requirements = models.ForeignKey(
        SystemRequirements,
        on_delete=models.CASCADE,
        help_text="System requirements",
        related_name="data_system_requirements",
    )
    network = models.ForeignKey(Network, on_delete=models.CASCADE, help_text="Network", related_name="data_network")
    speaker_system = models.ForeignKey(
        SpeakerSystem,
        on_delete=models.CASCADE,
        help_text="Speaker system",
        related_name="data_speaker_system",
    )
    sound_system = models.ForeignKey(
        SoundSystem,
        on_delete=models.CASCADE,
        help_text="Sound system",
        related_name="data_sound_system",
    )
    power_supply = models.ForeignKey(
        PowerSupply,
        on_delete=models.CASCADE,
        help_text="Power supply",
        related_name="data_power_supply",
    )
    settings_controls_and_indicators = models.ForeignKey(
        SettingsControlsAndIndicators,
        on_delete=models.CASCADE,
        help_text="Settings, controls and indicators",
        related_name="data_settings_controls_and_indicators",
    )
    power = models.ForeignKey(Power, on_delete=models.CASCADE, help_text="Power", related_name="data_power")
    heating_and_cooling = models.ForeignKey(
        HeatingAndCooling,
        on_delete=models.CASCADE,
        help_text="Heating and cooling",
        related_name="data_heating_and_cooling",
    )
    ram = models.ForeignKey(RAM, on_delete=models.CASCADE, help_text="RAM", related_name="data_ram")
    audio_output = models.ForeignKey(
        AudioOutput,
        on_delete=models.CASCADE,
        help_text="Audio output",
        related_name="data_audio_output",
    )
    heatsink_and_fan = models.ForeignKey(
        HeatsinkAndFan,
        on_delete=models.CASCADE,
        help_text="Heatsink and fan",
        related_name="data_heatsink_and_fan",
    )
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, help_text="Storage", related_name="data_storage")
    optical_storage_secondary = models.ForeignKey(
        OpticalStorageSecondary,
        on_delete=models.CASCADE,
        help_text="Optical storage secondary",
        related_name="data_optical_storage_secondary",
    )
    portable_storage_solution = models.ForeignKey(
        PortableStorageSolution,
        on_delete=models.CASCADE,
        help_text="Portable storage solution",
        related_name="data_portable_storage_solution",
    )
    optical_storage = models.ForeignKey(
        OpticalStorage,
        on_delete=models.CASCADE,
        help_text="Optical storage",
        related_name="data_optical_storage",
    )
    memory_module = models.ForeignKey(
        MemoryModule,
        on_delete=models.CASCADE,
        help_text="Memory module",
        related_name="data_memory_module",
    )
    antenna = models.ForeignKey(Antenna, on_delete=models.CASCADE, help_text="Antenna", related_name="data_antenna")
    system = models.ForeignKey(System, on_delete=models.CASCADE, help_text="System", related_name="data_system")
    controller_card = models.ForeignKey(
        ControllerCard,
        on_delete=models.CASCADE,
        help_text="Controller card",
        related_name="data_controller_card",
    )
    personal_hygiene = models.ForeignKey(
        PersonalHygiene,
        on_delete=models.CASCADE,
        help_text="Personal hygiene",
        related_name="data_personal_hygiene",
    )
    warranty = models.ForeignKey(Warranty, on_delete=models.CASCADE, help_text="Warranty", related_name="data_warranty")
    accessories_for_devices = models.ForeignKey(
        AccessoriesForDevices,
        on_delete=models.CASCADE,
        help_text="Accessories for devices",
        related_name="data_accessories_for_devices",
    )
    video_output = models.ForeignKey(
        VideoOutput,
        on_delete=models.CASCADE,
        help_text="Video output",
        related_name="data_video_output",
    )
    small_devices = models.ForeignKey(
        SmallDevices,
        on_delete=models.CASCADE,
        help_text="Small devices",
        related_name="data_small_devices",
    )
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, help_text="Camera", related_name="data_camera")
    light_source = models.ForeignKey(
        LightSource,
        on_delete=models.CASCADE,
        help_text="Light sources",
        related_name="data_light_source",
    )
    software = models.ForeignKey(Software, on_delete=models.CASCADE, help_text="Software", related_name="data_software")
    ce_accessories = models.ForeignKey(
        CEAccessories,
        on_delete=models.CASCADE,
        help_text="CE accessories",
        related_name="data_ce_accessories",
    )
    game = models.ForeignKey(Game, on_delete=models.CASCADE, help_text="Game", related_name="data_game")
    toasters_and_grills = models.ForeignKey(
        ToastersAndGrills,
        on_delete=models.CASCADE,
        help_text="Toasters and grills",
        related_name="data_toasters_and_grills",
    )
    scale = models.ForeignKey(Scale, on_delete=models.CASCADE, help_text="Scale", related_name="data_scale")
    hard_drive = models.ForeignKey(HDD, on_delete=models.CASCADE, help_text="Harddisk", related_name="data_hard_drive")
    external_hard_drive = models.ForeignKey(
        ExternalHardDrive,
        on_delete=models.CASCADE,
        help_text="External hard drive",
        related_name="data_external_hard_drive",
    )
    modem = models.ForeignKey(Modem, on_delete=models.CASCADE, help_text="Modem", related_name="data_modem")
    mobile_broadband = models.ForeignKey(
        MobileBroadband,
        on_delete=models.CASCADE,
        help_text="Mobile broadband",
        related_name="data_mobile_broadband",
    )
    audio_input = models.ForeignKey(
        AudioInput,
        on_delete=models.CASCADE,
        help_text="Audio input",
        related_name="data_audio_input",
    )
    memory_adapter = models.ForeignKey(
        MemoryAdapter,
        on_delete=models.CASCADE,
        help_text="Memory adapter",
        related_name="data_memory_adapter",
    )
    internet_of_things = models.ForeignKey(
        InternetOfThings,
        on_delete=models.CASCADE,
        help_text="Internet of things",
        related_name="data_internet_of_things",
    )
    cleaning = models.ForeignKey(Cleaning, on_delete=models.CASCADE, help_text="Cleaning", related_name="data_cleaning")
    flash_memory = models.ForeignKey(
        FlashMemory,
        on_delete=models.CASCADE,
        help_text="Flash memory",
        related_name="data_flash_memory",
    )
    radio_system = models.ForeignKey(
        RadioSystem,
        on_delete=models.CASCADE,
        help_text="Radio system",
        related_name="data_radio_system",
    )

    built_in_display = models.ForeignKey(
        BuiltInDisplay,
        on_delete=models.CASCADE,
        help_text="Built-in display",
        related_name="data_built_in_display",
    )
    ip_telephony = models.ForeignKey(
        IPTelephony,
        on_delete=models.CASCADE,
        help_text="IP telephony",
        related_name="data_ip_telephony",
    )
    dvd = models.ForeignKey(DVD, on_delete=models.CASCADE, help_text="DVD", related_name="data_dvd")
    ce_system = models.ForeignKey(
        CESystem,
        on_delete=models.CASCADE,
        help_text="CE system",
        related_name="data_ce_system",
    )
    network_and_internet_multimedia = models.ForeignKey(
        NetworkAndInternetMultimedia,
        on_delete=models.CASCADE,
        help_text="Network and Internet multimedia",
        related_name="data_network_and_internet_multimedia",
    )
    display = models.ForeignKey(Display, on_delete=models.CASCADE, help_text="Display", related_name="data_display")
    tv_tuner = models.ForeignKey(TVTuner, on_delete=models.CASCADE, help_text="TV tuner", related_name="data_tv_tuner")
    optical_sensor = models.ForeignKey(
        OpticalSensor,
        on_delete=models.CASCADE,
        help_text="Optical sensor",
        related_name="data_optical_sensor",
    )
    surveillance_camera = models.ForeignKey(
        SurveillanceCamera,
        on_delete=models.CASCADE,
        help_text="Surveillance camera",
        related_name="data_surveillance_camera",
    )
    game_console = models.ForeignKey(
        GameConsole,
        on_delete=models.CASCADE,
        help_text="Game console",
        related_name="data_game_console",
    )
    quick_film_development = models.ForeignKey(
        QuickFilmDevelopment,
        on_delete=models.CASCADE,
        help_text="Quick film development",
        related_name="data_quick_film_development",
    )
    film = models.ForeignKey(Film, on_delete=models.CASCADE, help_text="Film", related_name="data_film")
    cables_and_wires = models.ForeignKey(
        CablesAndWires,
        on_delete=models.CASCADE,
        help_text="Cables and wires",
        related_name="data_cables_and_wires",
    )
    network_tester = models.ForeignKey(
        NetworkTester,
        on_delete=models.CASCADE,
        help_text="Network tester",
        related_name="data_network_tester",
    )
    bag = models.ForeignKey(Bag, on_delete=models.CASCADE, help_text="Bag", related_name="data_bag")
    motherboard = models.ForeignKey(
        Motherboard,
        on_delete=models.CASCADE,
        help_text="Motherboard",
        related_name="data_motherboard",
    )
    chassis = models.ForeignKey(Chassis, on_delete=models.CASCADE, help_text="Chassis", related_name="data_chassis")
    mobile = models.ForeignKey(Mobile, on_delete=models.CASCADE, help_text="Mobile", related_name="data_mobile")
    communications = models.ForeignKey(
        Communications,
        on_delete=models.CASCADE,
        help_text="Communications",
        related_name="data_communications",
    )
    processor = models.ForeignKey(
        Processor,
        on_delete=models.CASCADE,
        help_text="Processor",
        related_name="data_processor",
    )
    toasters = models.ForeignKey(Toasters, on_delete=models.CASCADE, help_text="Toasters", related_name="data_toasters")
    environmental_standards = models.ForeignKey(
        EnvironmentalStandards,
        on_delete=models.CASCADE,
        help_text="Environmental standards",
        related_name="data_environmental_standards",
    )

    # TODO(TheLovinator): Also add the following fields:  # noqa: TD003

    # Kablar och ledningar
    # Nätverkstestare
    # Väska
    # Moderkort
    # Chassi
    # Mobil
    # Kommunikationer
    # Processor
    # Brödrostar
    # Miljöstandarder
    # Videominne
    # Kylskåp
    # Timer
    # Stativ
    # Tillbehör
    # Objektivsystem
    # Notebook-kompatibla dimensioner
    # Kaffemaskiner
    # Rakapparater, trimmers och epilatorer
    # Förstärkare
    # Hållare
    # Skärm
    # Kontorsapparat
    # Anslutningsmöjlighet
    # Utskrift
    # Dokument- och mediehantering
    # Kopiering
    # Skanning
    # Huvud
    # Belysningssystem
    # Medföljande OS
    # Vridbar
    # Licensiering
    # Innermått
    # Fläktinformation
    # Kortläsare
    # GPS-system
    # Gränssnittssammanfattning
    # Cacheminne
    # Band
    # Fodral
    # Inmatningsenhet (CE)
    # Främre kamera
    # Bakre kamera
    # Funktioner
    # Övervakningssats
    # Bakgrund
    # Faxapparat
    # Vattenkokare
    # Övriga attribut
    # Videosystem
    # Skrivare
    # 3D-skrivare
    # 3D-skrivarförbrukningsartiklar
    # Digitalkamera
    # Gränssnitt
    # Klocka och larm
    # Projektor
    # Linser
    # Armstöd
    # Huvudstöd
    # Bas
    # Ryggstöd
    # Sittplats
    # Kamerablixt
    # Sökare
    # Projektorlampa
    # Miljöparametrar
    # Tangentbord
    # Kylskåpsfunktioner
    # Vinkylare
    # Energi- och vattenkonsumtion
    # Skanner
    # Etikettskrivare
    # Medier
    # Utskriftssystem
    # Glassmaskin
    # Strykjärn
    # Matberedare
    # Mixers
    # Television
    # Mediespelare
    # Hårddisk (andra)
    # Videokameraegenskaper
    # Lameradisplay
    # Kameraminne
    # Kamerafunktioner
    # Linssystem i projektor
    # Sidor och fodral
    # Arkivering
    # Fotoalbum
    # Funktioner hos 360 kamera
    # Digitalspelare
    # Digital lagring
    # Studio- och produktionsutrustning
    # Grafiksystem
    # Elektriska krydd- och kaffekvarnar
    # Ställ och hållare
    # Programvarufamilj
    # Filter
    # Eltandborstar
    # Hårborttagningssystem
    # Digitala multimediaenheter
    # Hårvård
    # Digitalt ljud
    # Slutare
    # Spelfilm
    # Stillbilder
    # Linssystem (2:a)
    # GPS-kompatibilitet
    # Kontrollerkort (2:a)
    # Switch och dimmer
    # Varmluftsfritöser
    # Hållbarhet

    def __str__(self) -> str:
        return "Data"

    @staticmethod
    def create_and_import_data(
        model: type[T],
        data: dict,
        key: str,
    ) -> auto_prefetch.Model | None:
        """Generalized method to create and import data.

        Returns:
            auto_prefetch.Model | None: The created or imported model instance.
        """
        if key not in data:
            return None

        product_instance, _ = model.objects.get_or_create(name=key)  # type: ignore  # noqa: PGH003
        product_instance.import_json(data[key])
        return product_instance

    def import_json(self, data: dict) -> None:  # noqa: PLR0914, PLR0915
        """Import JSON data."""
        # cable
        cable: auto_prefetch.Model | None = self.create_and_import_data(Cable, data, "Kabel")
        self.cable = cable

        # header
        header: auto_prefetch.Model | None = self.create_and_import_data(Header, data, "Header")
        self.header = header

        # dimensions_and_weight
        dimensions_and_weight: auto_prefetch.Model | None = self.create_and_import_data(
            DimensionsAndWeight,
            data,
            "Mått och vikt",
        )
        self.dimensions_and_weight = dimensions_and_weight

        # general
        general: auto_prefetch.Model | None = self.create_and_import_data(General, data, "Allmänt")
        self.general = general

        # miscellaneous
        miscellaneous: auto_prefetch.Model | None = self.create_and_import_data(Miscellaneous, data, "Diverse")
        self.miscellaneous = miscellaneous

        # input_device
        input_device: auto_prefetch.Model | None = self.create_and_import_data(InputDevice, data, "Inmatningsenhet")
        self.input_device = input_device

        # service_and_support
        service_and_support: auto_prefetch.Model | None = self.create_and_import_data(
            ServiceAndSupport,
            data,
            "Service och support",
        )
        self.service_and_support = service_and_support

        # gross_dimensions_and_weight
        gross_dimensions_and_weight: auto_prefetch.Model | None = self.create_and_import_data(
            GrossDimensionsAndWeight,
            data,
            "Mått och vikt (brutto)",
        )
        self.gross_dimensions_and_weight = gross_dimensions_and_weight

        # consumables
        consumables: auto_prefetch.Model | None = self.create_and_import_data(Consumables, data, "Förbrukningsartiklar")
        self.consumables = consumables

        # battery
        battery: auto_prefetch.Model | None = self.create_and_import_data(Battery, data, "Batteri")
        self.battery = battery

        # av_components
        av_components: auto_prefetch.Model | None = self.create_and_import_data(AVComponent, data, "AV-komponenter")
        self.av_components = av_components

        # remote_control
        remote_control: auto_prefetch.Model | None = self.create_and_import_data(RemoteControl, data, "Fjärrkontroll")
        self.remote_control = remote_control

        # video_input
        video_input: auto_prefetch.Model | None = self.create_and_import_data(VideoInput, data, "Videoingång")
        self.video_input = video_input

        # system_requirements
        system_requirements: auto_prefetch.Model | None = self.create_and_import_data(
            SystemRequirements,
            data,
            "Systemkrav",
        )
        self.system_requirements = system_requirements

        # network
        network: auto_prefetch.Model | None = self.create_and_import_data(Network, data, "Nätverk")
        self.network = network

        # speaker_system
        speaker_system: auto_prefetch.Model | None = self.create_and_import_data(SpeakerSystem, data, "Högtalarsystem")
        self.speaker_system = speaker_system

        # sound_system
        sound_system: auto_prefetch.Model | None = self.create_and_import_data(SoundSystem, data, "Ljudsystem")
        self.sound_system = sound_system

        # power_supply
        power_supply: auto_prefetch.Model | None = self.create_and_import_data(PowerSupply, data, "Nätdel")
        self.power_supply = power_supply

        # settings_controls_and_indicators
        settings_controls_and_indicators: auto_prefetch.Model | None = self.create_and_import_data(
            SettingsControlsAndIndicators,
            data,
            "Inställningar, reglage och indikatorer",
        )
        self.settings_controls_and_indicators = settings_controls_and_indicators

        # power
        power: auto_prefetch.Model | None = self.create_and_import_data(Power, data, "Ström")
        self.power = power

        # heating_and_cooling
        heating_and_cooling: auto_prefetch.Model | None = self.create_and_import_data(
            HeatingAndCooling,
            data,
            "Värme och kyla",
        )
        self.heating_and_cooling = heating_and_cooling

        # ram
        ram: auto_prefetch.Model | None = self.create_and_import_data(RAM, data, "RAM")
        self.ram = ram

        # audio_output
        audio_output: auto_prefetch.Model | None = self.create_and_import_data(AudioOutput, data, "Ljudutgång")
        self.audio_output = audio_output

        # heatsink_and_fan
        heatsink_and_fan: auto_prefetch.Model | None = self.create_and_import_data(
            HeatsinkAndFan,
            data,
            "Kylfläns och fläkt",
        )
        self.heatsink_and_fan = heatsink_and_fan

        # storage
        storage: auto_prefetch.Model | None = self.create_and_import_data(Storage, data, "Lagring")
        self.storage = storage

        # optical_storage_secondary
        optical_storage_secondary: auto_prefetch.Model | None = self.create_and_import_data(
            OpticalStorageSecondary,
            data,
            "Optisk lagring (sekundär)",
        )
        self.optical_storage_secondary = optical_storage_secondary

        # portable_storage_solution
        portable_storage_solution: auto_prefetch.Model | None = self.create_and_import_data(
            PortableStorageSolution,
            data,
            "Flyttbar lagringslösning",
        )
        self.portable_storage_solution = portable_storage_solution

        # optical_storage
        optical_storage: auto_prefetch.Model | None = self.create_and_import_data(
            OpticalStorage,
            data,
            "Optisk lagring",
        )
        self.optical_storage = optical_storage

        # memory_module
        memory_module: auto_prefetch.Model | None = self.create_and_import_data(MemoryModule, data, "Minnesmodul")
        self.memory_module = memory_module

        # antenna
        antenna: auto_prefetch.Model | None = self.create_and_import_data(Antenna, data, "Antenn")
        self.antenna = antenna

        # system
        system: auto_prefetch.Model | None = self.create_and_import_data(System, data, "System")
        self.system = system

        # controller_card
        controller_card: auto_prefetch.Model | None = self.create_and_import_data(
            ControllerCard,
            data,
            "Kontrollerkort",
        )
        self.controller_card = controller_card

        # personal_hygiene
        personal_hygiene: auto_prefetch.Model | None = self.create_and_import_data(
            PersonalHygiene,
            data,
            "Personlig hygien",
        )
        self.personal_hygiene = personal_hygiene

        # warranty
        warranty: auto_prefetch.Model | None = self.create_and_import_data(Warranty, data, "Garanti")
        self.warranty = warranty

        # accessories_for_devices
        accessories_for_devices: auto_prefetch.Model | None = self.create_and_import_data(
            AccessoriesForDevices,
            data,
            "Tillbehör till apparater",
        )
        self.accessories_for_devices = accessories_for_devices

        # video_output
        video_output: auto_prefetch.Model | None = self.create_and_import_data(VideoOutput, data, "Videoutgång")
        self.video_output = video_output

        # small_devices
        small_devices: auto_prefetch.Model | None = self.create_and_import_data(SmallDevices, data, "Små apparater")
        self.small_devices = small_devices

        # camera
        camera: auto_prefetch.Model | None = self.create_and_import_data(Camera, data, "Kamera")
        self.camera = camera

        # light_source
        light_source: auto_prefetch.Model | None = self.create_and_import_data(LightSource, data, "Ljuskälla")
        self.light_source = light_source

        # software
        software: auto_prefetch.Model | None = self.create_and_import_data(Software, data, "Programvara")
        self.software = software

        # ce_accessories
        ce_accessories: auto_prefetch.Model | None = self.create_and_import_data(CEAccessories, data, "CE-tillbehör")
        self.ce_accessories = ce_accessories

        # game
        game: auto_prefetch.Model | None = self.create_and_import_data(Game, data, "Spel")
        self.game = game

        # toasters_and_grills
        toasters_and_grills: auto_prefetch.Model | None = self.create_and_import_data(
            ToastersAndGrills,
            data,
            "Brödrostar och grillar",
        )
        self.toasters_and_grills = toasters_and_grills

        # scale
        scale: auto_prefetch.Model | None = self.create_and_import_data(Scale, data, "Våg")
        self.scale = scale

        # hard_drive
        hard_drive: auto_prefetch.Model | None = self.create_and_import_data(HDD, data, "Hårddisk")
        self.hard_drive = hard_drive

        # external_hard_drive
        external_hard_drive: auto_prefetch.Model | None = self.create_and_import_data(
            ExternalHardDrive,
            data,
            "Extern hårddisk",
        )
        self.external_hard_drive = external_hard_drive

        # modem
        modem: auto_prefetch.Model | None = self.create_and_import_data(Modem, data, "Modem")
        self.modem = modem

        # mobile_broadband
        mobile_broadband: auto_prefetch.Model | None = self.create_and_import_data(
            MobileBroadband,
            data,
            "Mobilt bredband",
        )
        self.mobile_broadband = mobile_broadband

        # audio_input
        audio_input: auto_prefetch.Model | None = self.create_and_import_data(AudioInput, data, "Ljudingång")
        self.audio_input = audio_input

        # memory_adapter
        memory_adapter: auto_prefetch.Model | None = self.create_and_import_data(MemoryAdapter, data, "Minnesadapter")
        self.memory_adapter = memory_adapter

        # internet_of_things
        internet_of_things: auto_prefetch.Model | None = self.create_and_import_data(
            InternetOfThings,
            data,
            "Internet of Things (IoT)",
        )
        self.internet_of_things = internet_of_things

        # cleaning
        cleaning: auto_prefetch.Model | None = self.create_and_import_data(Cleaning, data, "Rengöring")
        self.cleaning = cleaning

        # flash_memory
        flash_memory: auto_prefetch.Model | None = self.create_and_import_data(FlashMemory, data, "Flash-minne")
        self.flash_memory = flash_memory

        # radio_system
        radio_system: auto_prefetch.Model | None = self.create_and_import_data(RadioSystem, data, "Radiosystem")
        self.radio_system = radio_system

        # Warn if there are new fields in the JSON data
        available_fields: list[str] = [
            "Kabel",
            "Rubrik",
            "Mått och vikt",
            "Allmänt",
            "Övrigt",
            "Inmatningsenhet",
            "Service och support",
            "Brutmått och vikt",
            "Förbrukningsmaterial",
            "Batteri",
            "AV-komponenter",
            "Fjärrkontroll",
            "Videoingång",
            "Systemkrav",
            "Nätverk",
            "Högtalarsystem",
            "Ljudsystem",
            "Strömförsörjning",
            "Inställningar, reglage och indikatorer",
            "Effekt",
            "Uppvärmning och kylning",
            "RAM",
            "Ljudutgång",
            "Kylfläns och fläkt",
            "Lagring",
            "Optisk lagring sekundär",
            "Bärbar lagringslösning",
            "Optisk lagring",
            "Minnesmodul",
            "Antenn",
            "System",
            "Kontrollerkort",
            "Personlig hygien",
            "Garanti",
            "Tillbehör för enheter",
            "Video utgång",
            "Små enheter",
            "Kamera",
            "Ljuskällor",
            "Programvara",
            "CE-tillbehör",
            "Spel",
            "Brödrostar och grillar",
            "Våg",
            "Hårddisk",
            "Extern hårddisk",
            "Modem",
            "Mobilt bredband",
            "Ljudingång",
            "Minnesadapter",
            "Internet of things",
            "Rengöring",
            "Flash-minne",
            "Radiosystem",
        ]
        for key in data:
            if key not in available_fields:
                logger.warning("New field found in Data: %s", key)


class Manufacturer(auto_prefetch.Model):
    """Manufacturer."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the manufacturer was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the manufacturer was last updated")

    # Webhallen fields
    id = models.PositiveBigIntegerField(primary_key=True, help_text="Manufacturer ID")
    name = models.TextField(help_text="Manufacturer name")
    takeover_url = models.URLField(help_text="Takeover URL")
    website_url = models.URLField(help_text="Website URL")
    visible = models.BooleanField(help_text="Is visible")


class PartNumber(auto_prefetch.Model):
    """Part number."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the part number was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the part number was last updated")

    # Webhallen fields
    part_number = models.TextField(primary_key=True, help_text="Part number")

    def __str__(self) -> str:
        return f"Part number - {self.part_number}"


class EAN(auto_prefetch.Model):
    """EAN."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the EAN was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the EAN was last updated")

    # Webhallen fields
    ean = models.TextField(primary_key=True, help_text="EAN")

    def __str__(self) -> str:
        return f"EAN - {self.ean}"


class Prices(auto_prefetch.Model):
    """Shipping prices."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the shipping prices was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the shipping prices was last updated")

    # Webhallen fields
    price = models.PositiveBigIntegerField(help_text="Price")
    shipping_method_id = models.PositiveBigIntegerField(help_text="Shipping method ID")
    is_fixed_price = models.BooleanField(help_text="Is fixed price")
    maximum_package_size_id = models.PositiveBigIntegerField(help_text="Maximum package size ID")


class ShippingClass(auto_prefetch.Model):
    """Shipping class."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the shipping class was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the shipping class was last updated")

    # Webhallen fields
    id = models.PositiveBigIntegerField(primary_key=True, help_text="Shipping class ID")
    order = models.PositiveBigIntegerField(help_text="Order")
    prices = models.ForeignKey(Prices, on_delete=models.CASCADE, help_text="Prices")


class EnergyMarking(auto_prefetch.Model):
    """Energy marking.

    Example:
    {
        "product": {
            "energyMarking": {
                "rating": "G",
                "scale": "A+",
                "labelContent": null,
                "productSheetContent": "-",
                "labelImageUrl": "https://www.webhallen.com/images/669512-asus-rog-swift-pg27aqdm-265-oled-bildskarm-fo?raw",
                "manufacturer": "Philips Lighting",
                "itemCode": "915005630901"
            }
        }
    }
    """

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="Created at")
    updated_at = models.DateTimeField(auto_now=True, help_text="Updated at")

    # Webhallen fields
    item_code = models.TextField(help_text="Item code")
    label_content = models.TextField(help_text="Label content")  # TODO(Thelovinator): Is this used?  # noqa: TD003
    label_image_url = models.URLField(help_text="Label image URL")  # TODO(Thelovinator): Download image  # noqa: TD003
    manufacturer = models.TextField(help_text="Manufacturer")
    product_sheet_content = models.TextField(help_text="Product sheet content")
    rating = models.TextField(help_text="Rating")
    scale = models.TextField(help_text="Scale")

    def __str__(self) -> str:
        return f"Energy marking - {self.item_code}"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        field_mapping: dict[str, str] = {
            "itemCode": "item_code",
            "labelContent": "label_content",
            "labelImageUrl": "label_image_url",
            "manufacturer": "manufacturer",
            "productSheetContent": "product_sheet_content",
            "rating": "rating",
            "scale": "scale",
        }

        update_fields(instance=self, data=data, field_mapping=field_mapping)

        # Warn if labelContent is not None
        if self.label_content is not None:
            # TODO(Thelovinator): Send Discord message  # noqa: TD003
            logger.warning("Label content is not None - %s", self.label_content)


class StatusCode(auto_prefetch.Model):
    """Status code."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the status code was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the status code was last updated")

    # Webhallen fields
    status_code = models.TextField(primary_key=True, help_text="Status code")


class ReviewHighlightProduct(auto_prefetch.Model):
    """Review highlight product."""

    # Django fields
    id = models.PositiveBigIntegerField(primary_key=True, help_text="Review highlight product ID")
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the review highlight product was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the review highlight product was last updated")

    # Webhallen fields
    main_category_path = models.ForeignKey(MainCategoryPath, on_delete=models.CASCADE, help_text="Main category path")
    minimum_rank_level = models.PositiveBigIntegerField(help_text="Minimum rank level")
    status_codes = models.ForeignKey(StatusCode, on_delete=models.CASCADE, help_text="Status codes")
    meta_title = models.TextField(help_text="Meta title")
    section = models.ForeignKey(Section, on_delete=models.CASCADE, help_text="Section")
    name = models.TextField(help_text="Name")


class Avatar(auto_prefetch.Model):
    """Avatar of a user."""

    # Django fields
    id = models.PositiveBigIntegerField(primary_key=True, help_text="Avatar ID")
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the avatar was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the avatar was last updated")

    # Webhallen fields
    title = models.TextField(help_text="Title")


class Knighthood(auto_prefetch.Model):
    """Webhallen knighthood."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the knighthood was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the knighthood was last updated")

    # Webhallen fields
    # TODO(TheLovinator): Warn if we find fields for this  # noqa: TD003


class User(auto_prefetch.Model):
    """A user of Webhallen."""

    # Django fields
    id = models.PositiveBigIntegerField(primary_key=True, help_text="User ID")
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the user was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the user was last updated")

    # Webhallen fields
    username = models.TextField(help_text="Username")
    is_public_profile = models.BooleanField(help_text="Is public profile")
    knighthood = models.ForeignKey(Knighthood, on_delete=models.CASCADE, help_text="Knighthood")
    rank_level = models.PositiveBigIntegerField(help_text="Rank level")
    avatar = models.ForeignKey(Avatar, on_delete=models.CASCADE, help_text="Avatar")


class PossibleDeliveryMethod(auto_prefetch.Model):
    """Possible delivery method."""

    # Django fields
    id = models.PositiveBigIntegerField(primary_key=True, help_text="Possible delivery method ID")
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the possible delivery method was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the possible delivery method was last updated")


class ReviewHighlight(auto_prefetch.Model):
    """Review highlight."""

    # Django fields
    id = models.PositiveBigIntegerField(primary_key=True, help_text="Review highlight ID")

    # This is created instead of created_at because created_at is from the Webhallen API
    created = models.DateTimeField(auto_now_add=True, help_text="When the review highlight was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the review highlight was last updated")

    # Webhallen fields
    text = models.TextField(help_text="Review highlight text")
    rating = models.PositiveBigIntegerField(help_text="Rating")
    upvotes = models.PositiveBigIntegerField(help_text="Upvotes")
    downvotes = models.PositiveBigIntegerField(help_text="Downvotes")
    verified_purchase = models.BooleanField(help_text="Verified purchase")
    created_at = models.DateTimeField(help_text="Created at")
    is_anonymous = models.BooleanField(help_text="Is anonymous")
    is_employee = models.BooleanField(help_text="Is employee")
    product = models.ForeignKey(ReviewHighlightProduct, on_delete=models.CASCADE, help_text="Product")
    is_hype = models.BooleanField(help_text="Is hype")
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="User")


class ResursPartPaymentPrice(auto_prefetch.Model):
    """https://www.webhallen.com/se/info/48-Betala-senare-med-Resurs."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the Resurs part payment price was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the Resurs part payment price was last updated")

    # Webhallen fields
    monthly_cost = models.TextField(help_text="Monthly cost")
    duration_months = models.PositiveBigIntegerField(help_text="Duration in months")


class Insurance(auto_prefetch.Model):
    """Insurance."""

    # Django fields
    id = models.PositiveBigIntegerField(primary_key=True, help_text="Insurance ID")
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the insurance was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the insurance was last updated")

    # Webhallen fields
    name = models.TextField(help_text="Insurance name")
    price = models.PositiveBigIntegerField(help_text="Insurance price")
    provider = models.PositiveBigIntegerField(help_text="Insurance provider")
    length = models.PositiveBigIntegerField(help_text="Insurance length")

    def __str__(self) -> str:
        return f"Insurance - {self.name}"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        field_mapping: dict[str, str] = {
            "name": "name",
            "price": "price",
            "provider": "provider",
            "length": "length",
        }

        update_fields(instance=self, data=data, field_mapping=field_mapping)


class ExcludeShippingMethod(auto_prefetch.Model):
    """Excluded shipping method."""

    # Django fields
    id = models.PositiveBigIntegerField(primary_key=True, help_text="Exclude shipping method ID")
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the exclude shipping method was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the exclude shipping method was last updated")

    def __str__(self) -> str:
        return f"Exclude shipping method - {self.id}"


class Meta(auto_prefetch.Model):
    """Meta.

    Example:
        "product": {
            "meta": {
            "highlight_member_offer": true,
            "excluded_shipping_methods": [
                "28"
            ],
            "is_hygiene_article": true,
            "requires_prepayment": "TRUE"
            },
        }

    """

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the meta was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the meta was last updated")

    # Webhallen fields
    highlight_member_offer = models.BooleanField(help_text="Highlight member offer")
    excluded_shipping_methods = models.ForeignKey(
        ExcludeShippingMethod,
        on_delete=models.CASCADE,
        help_text="Excluded shipping methods",
    )
    is_hygiene_article = models.BooleanField(help_text="Is hygiene article")
    requires_prepayment = models.TextField(help_text="Requires prepayment")

    def __str__(self) -> str:
        return f"Meta - {self.pk}"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        field_mapping: dict[str, str] = {
            "highlight_member_offer": "highlight_member_offer",
            "excluded_shipping_methods": "excluded_shipping_methods",
            "is_hygiene_article": "is_hygiene_article",
            "requires_prepayment": "requires_prepayment",
        }

        update_fields(instance=self, data=data, field_mapping=field_mapping)


class FyndwareClass(auto_prefetch.Model):
    """Fyndware class."""

    # Django fields
    webhallen_id = models.PositiveBigIntegerField(primary_key=True, help_text="Fyndware class ID")
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the Fyndware class was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the Fyndware class was last updated.")

    # Webhallen fields
    condition = models.TextField(help_text="Condition")
    description = models.TextField(help_text="Description")
    name = models.TextField(help_text="Name")
    short_name = models.TextField(help_text="Short name")  # TODO(TheLovinator): Is this correct?  # noqa: TD003

    def __str__(self) -> str:
        return f"{self.name} ({self.webhallen_id})"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        field_mapping: dict[str, str] = {
            "condition": "condition",
            "description": "description",
            "name": "name",
            "shortName": "short_name",
        }

        update_fields(instance=self, data=data, field_mapping=field_mapping)


class Product(auto_prefetch.Model):
    """A product from Webhallen."""

    # Django fields
    webhallen_id = models.PositiveBigIntegerField(primary_key=True, help_text="Webhallen product ID")
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the product was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the product was last updated")

    # Webhallen fields
    # fyndware_of = ???? # TODO(TheLovinator): What is this?  # noqa: TD003
    # ifs_id = ???? # TODO(TheLovinator): What is this?  # noqa: TD003
    canonical_link = models.URLField(help_text="Canonical link")
    category_tree = models.TextField(help_text="Category tree")
    description = models.TextField(help_text="Product description")
    description_provider = models.PositiveBigIntegerField(help_text="Description provider")
    discontinued = models.BooleanField(help_text="Is discontinued")
    is_collectable = models.BooleanField(help_text="Is collectable")
    is_digital = models.BooleanField(help_text="Is digital")
    is_fyndware = models.BooleanField(help_text="Is Fyndware")
    is_shippable = models.BooleanField(help_text="Is shippable")
    long_delivery_notice = models.TextField(help_text="Long delivery notice")
    main_title = models.TextField(help_text="Main title")
    meta_description = models.TextField(help_text="Meta description")
    meta_title = models.TextField(help_text="Meta title")
    minimum_rank_level = models.PositiveBigIntegerField(help_text="Minimum rank level")
    name = models.TextField(help_text="Product name")
    package_size_id = models.PositiveBigIntegerField(help_text="Package size ID")
    phone_subscription = models.BooleanField(help_text="Is a phone subscription")
    sub_title = models.TextField(help_text="Sub title")
    thumbnail = models.URLField(help_text="Thumbnail URL")
    ticket = models.TextField(help_text="Ticket")

    # ForeignKey fields
    average_rating = auto_prefetch.ForeignKey(AverageRating, on_delete=models.CASCADE, help_text="Average rating")
    data = auto_prefetch.ForeignKey(Data, on_delete=models.CASCADE, help_text="Data")
    energy_marking = auto_prefetch.ForeignKey(EnergyMarking, on_delete=models.CASCADE, help_text="Energy marking")
    fyndware_class = auto_prefetch.ForeignKey(FyndwareClass, on_delete=models.CASCADE, help_text="Fyndware class")
    level_one_price = auto_prefetch.ForeignKey(
        Price,
        on_delete=models.CASCADE,
        help_text="The level one price of the product",
        related_name="level_one_price",
    )
    lowest_price = auto_prefetch.ForeignKey(
        Price,
        on_delete=models.CASCADE,
        help_text="The lowest price of the product",
        related_name="lowest_price",
    )
    main_category_path = auto_prefetch.ForeignKey(
        MainCategoryPath,
        on_delete=models.CASCADE,
        help_text="Main category path",
    )
    manufacturer = auto_prefetch.ForeignKey(Manufacturer, on_delete=models.CASCADE, help_text="Manufacturer")
    meta = auto_prefetch.ForeignKey(Meta, on_delete=models.CASCADE, help_text="Meta")
    price = auto_prefetch.ForeignKey(
        Price,
        on_delete=models.CASCADE,
        help_text="The price of the product",
        related_name="current_price",
    )
    regular_price = auto_prefetch.ForeignKey(
        Price,
        on_delete=models.CASCADE,
        help_text="The regular price of the product",
        related_name="regular_price",
    )
    release = auto_prefetch.ForeignKey(Release, on_delete=models.CASCADE, help_text="Release")
    section = auto_prefetch.ForeignKey(Section, on_delete=models.CASCADE, help_text="Section")
    shipping_class = auto_prefetch.ForeignKey(ShippingClass, on_delete=models.CASCADE, help_text="Shipping class")
    stock = auto_prefetch.ForeignKey(Stock, on_delete=models.CASCADE, help_text="Stock")

    categories = models.ForeignKey(
        Categories,
        on_delete=models.CASCADE,
        help_text="Categories",
        related_name="product_categories",
    )
    eans = models.ForeignKey(EAN, on_delete=models.CASCADE, help_text="EANs", related_name="product_eans")
    images = models.ForeignKey(Image, on_delete=models.CASCADE, help_text="Images", related_name="product_images")
    insurance = models.ForeignKey(
        Insurance,
        on_delete=models.CASCADE,
        help_text="Insurance",
        related_name="product_insurance",
    )
    part_numbers = models.ForeignKey(
        PartNumber,
        on_delete=models.CASCADE,
        help_text="Part numbers",
        related_name="product_part_numbers",
    )
    possible_delivery_methods = models.ForeignKey(
        PossibleDeliveryMethod,
        on_delete=models.CASCADE,
        help_text="Possible delivery methods",
        related_name="product_possible_delivery_methods",
    )
    resurs_part_payment_price = models.ForeignKey(
        ResursPartPaymentPrice,
        on_delete=models.CASCADE,
        help_text="Resurs part payment price",
        related_name="product_resurs_part_payment_price",
    )
    review_highlight = models.ForeignKey(
        ReviewHighlight,
        on_delete=models.CASCADE,
        help_text="Review highlights",
        related_name="product_review_highlight",
    )
    status_codes = models.ForeignKey(
        StatusCode,
        on_delete=models.CASCADE,
        help_text="Status codes",
        related_name="product_status_codes",
    )
    variants = models.ForeignKey(
        Variants,
        on_delete=models.CASCADE,
        help_text="Variants",
        related_name="product_variants",
    )

    def __str__(self) -> str:
        return f"{self.name} ({self.webhallen_id})"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        field_mapping: dict[str, str] = {
            "canonicalLink": "canonical_link",
            "categoryTree": "category_tree",
            "description": "description",
            "descriptionProvider": "description_provider",
            "discontinued": "discontinued",
            "isCollectable": "is_collectable",
            "isDigital": "is_digital",
            "isFyndware": "is_fyndware",
            "isShippable": "is_shippable",
            "longDeliveryNotice": "long_delivery_notice",
            "mainTitle": "main_title",
            "metaDescription": "meta_description",
            "metaTitle": "meta_title",
            "minimumRankLevel": "minimum_rank_level",
            "name": "name",
            "packageSizeId": "package_size_id",
            "phoneSubscription": "phone_subscription",
            "subTitle": "sub_title",
            "thumbnail": "thumbnail",
            "ticket": "ticket",
        }
        update_fields(instance=self, data=data, field_mapping=field_mapping)

        # FyndwareClass
        self.handle_fyndware_class(data)

    def handle_fyndware_class(self, data: dict) -> None:
        """Handle fyndwareClass."""
        fyndware_class_data = data.get("fyndwareClass")
        if fyndware_class_data:
            fyndware_class, _ = FyndwareClass.objects.get_or_create(webhallen_id=fyndware_class_data["id"])
            fyndware_class.import_json(fyndware_class_data)

            self.fyndware_class = fyndware_class
            self.save()
