from __future__ import annotations

import logging
from typing import TYPE_CHECKING

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


# TODO(TheLovinator): All docstrings are placeholders and need to be updated  # noqa: TD003


def create_and_import_component(data: dict, component_name: str) -> Component:
    """Create and import a component.

    Args:
        data (dict): The data to import.
        component_name (str): The name of the component.

    Returns:
        Component: The created component.
    """
    component_data: dict = data.get(component_name, {})
    component, created = Component.objects.get_or_create(
        attribute_id=component_data.get("attributeId"),
    )
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
    variant_groups = models.ManyToManyField(VariantGroups, help_text="Variant groups")

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
            self.variant_groups.add(variant_group)

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

    # Relationships
    orders = models.ManyToManyField(Order, help_text="Orders for this stock", related_name="stock")

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

        # Handle orders separately as they are nested.
        orders = data.get("orders", {})
        for store, order_data in orders.items():
            order, _ = Order.objects.get_or_create(store=store, defaults=order_data)
            self.orders.add(order)


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
    packaged_quantity = models.ManyToManyField(
        Component,
        help_text="Packaged quantity",
        related_name="products_packaged_quantity",
    )
    brand = models.ManyToManyField(
        Component,
        help_text="Brand",
        related_name="products_brand",
    )
    product_line = models.ManyToManyField(
        Component,
        help_text="Product line",
        related_name="products_product_line",
    )
    manufacturer = models.ManyToManyField(
        Component,
        help_text="Manufacturer",
        related_name="products_manufacturer",
    )
    model = models.ManyToManyField(
        Component,
        help_text="Model",
        related_name="products_model",
    )
    compatibility = models.ManyToManyField(
        Component,
        help_text="Compatibility",
        related_name="products_compatibility",
    )
    country_specific_batches = models.ManyToManyField(
        Component,
        help_text="Country-specific batches",
        related_name="products_country_specific_batches",
    )
    localization = models.ManyToManyField(
        Component,
        help_text="Localization",
        related_name="products_localization",
    )
    game_publisher = models.ManyToManyField(
        Component,
        help_text="Game publisher",
        related_name="products_game_publisher",
    )
    game_developer = models.ManyToManyField(
        Component,
        help_text="Game developer",
        related_name="products_game_developer",
    )
    edition = models.ManyToManyField(
        Component,
        help_text="Edition",
        related_name="products_edition",
    )
    batch = models.ManyToManyField(
        Component,
        help_text="Batch",
        related_name="products_batch",
    )
    manufacturer_model_number = models.ManyToManyField(
        Component,
        help_text="Manufacturer's model number",
        related_name="products_manufacturer_model_number",
    )
    release_date = models.ManyToManyField(
        Component,
        help_text="Release date",
        related_name="products_release_date",
    )
    series = models.ManyToManyField(
        Component,
        help_text="Series",
        related_name="products_series",
    )

    def __str__(self) -> str:
        return "Header"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Förpackad kvantitet
        packaged_quantity: Component = create_and_import_component(data, "Förpackad kvantitet")
        self.packaged_quantity.add(packaged_quantity)

        # Märke
        brand: Component = create_and_import_component(data, "Märke")
        self.brand.add(brand)

        # Produktlinje
        product_line: Component = create_and_import_component(data, "Produktlinje")
        self.product_line.add(product_line)

        # Tillverkare
        manufacturer: Component = create_and_import_component(data, "Tillverkare")
        self.manufacturer.add(manufacturer)

        # Modell
        model: Component = create_and_import_component(data, "Modell")
        self.model.add(model)

        # Kompatibilitet
        compatibility: Component = create_and_import_component(data, "Kompatibilitet")
        self.compatibility.add(compatibility)

        # Landsspecifika satser
        country_specific_batches: Component = create_and_import_component(data, "Landsspecifika satser")
        self.country_specific_batches.add(country_specific_batches)

        # Lokalisering
        localization: Component = create_and_import_component(data, "Lokalisering")
        self.localization.add(localization)

        # Spelutgivare
        game_publisher: Component = create_and_import_component(data, "Spelutgivare")
        self.game_publisher.add(game_publisher)

        # Spelutvecklare
        game_developer: Component = create_and_import_component(data, "Spelutvecklare")
        self.game_developer.add(game_developer)

        # Utgåva
        edition: Component = create_and_import_component(data, "Utgåva")
        self.edition.add(edition)

        # Sats
        batch: Component = create_and_import_component(data, "Sats")
        self.batch.add(batch)

        # Tillverkarens modellnummer
        manufacturer_model_number: Component = create_and_import_component(data, "Tillverkarens modellnummer")
        self.manufacturer_model_number.add(manufacturer_model_number)

        # Utgivningsdatum
        release_date: Component = create_and_import_component(data, "Utgivningsdatum")
        self.release_date.add(release_date)

        # Serie
        series: Component = create_and_import_component(data, "Serie")
        self.series.add(series)


class DimensionsAndWeight(auto_prefetch.Model):
    """Mått och vikt.

    Note: All the field names are translated from Swedish to English.
    """

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the dimensions and weight were created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the dimensions and weight were last updated")

    # Webhallen fields
    weight = models.ManyToManyField(Component, help_text="Weight", related_name="dimensions_weight")
    length = models.ManyToManyField(Component, help_text="Length", related_name="dimensions_length")
    width = models.ManyToManyField(Component, help_text="Width", related_name="dimensions_width")
    height = models.ManyToManyField(Component, help_text="Height", related_name="dimensions_height")
    length_in_meters = models.ManyToManyField(
        Component,
        help_text="Length in meters",
        related_name="dimensions_length_in_meters",
    )
    diameter = models.ManyToManyField(Component, help_text="Diameter", related_name="dimensions_diameter")
    comments = models.ManyToManyField(Component, help_text="Comments", related_name="dimensions_comments")
    thickness = models.ManyToManyField(Component, help_text="Thickness", related_name="dimensions_thickness")
    volume = models.ManyToManyField(Component, help_text="Volume", related_name="dimensions_volume")
    comment = models.ManyToManyField(Component, help_text="Comment", related_name="dimensions_comment")
    min_height = models.ManyToManyField(Component, help_text="Minimum height", related_name="dimensions_min_height")
    backrest_height = models.ManyToManyField(
        Component,
        help_text="Backrest height",
        related_name="dimensions_backrest_height",
    )
    backrest_width = models.ManyToManyField(
        Component,
        help_text="Backrest width",
        related_name="dimensions_backrest_width",
    )
    max_length = models.ManyToManyField(Component, help_text="Maximum length", related_name="dimensions_max_length")

    def __str__(self) -> str:
        return "Dimensions and weight"

    def import_json(self, data: dict) -> None:
        """Import JSON data."""
        # Vikt
        weight: Component = create_and_import_component(data, "Vikt")
        self.weight.add(weight)

        # Längd
        length: Component = create_and_import_component(data, "Längd")
        self.length.add(length)

        # Bredd
        width: Component = create_and_import_component(data, "Bredd")
        self.width.add(width)

        # Höjd
        height: Component = create_and_import_component(data, "Höjd")
        self.height.add(height)

        # Längd i meter
        length_in_meters: Component = create_and_import_component(data, "Längd i meter")
        self.length_in_meters.add(length_in_meters)

        # Diameter
        diameter: Component = create_and_import_component(data, "Diameter")
        self.diameter.add(diameter)

        # Kommentarer
        comments: Component = create_and_import_component(data, "Kommentarer")
        self.comments.add(comments)

        # Grovlek
        thickness: Component = create_and_import_component(data, "Grovlek")
        self.thickness.add(thickness)

        # Volym
        volume: Component = create_and_import_component(data, "Volym")
        self.volume.add(volume)

        # Kommentar
        comment: Component = create_and_import_component(data, "Kommentar")
        self.comment.add(comment)

        # Min. höjd
        min_height: Component = create_and_import_component(data, "Min. höjd")
        self.min_height.add(min_height)

        # Ryggstödshöjd
        backrest_height: Component = create_and_import_component(data, "Ryggstödshöjd")
        self.backrest_height.add(backrest_height)

        # Ryggstödsbredd
        backrest_width: Component = create_and_import_component(data, "Ryggstödsbredd")
        self.backrest_width.add(backrest_width)

        # Max längd
        max_length: Component = create_and_import_component(data, "Max längd")
        self.max_length.add(max_length)


class General(auto_prefetch.Model):
    """Allmänt."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the general information was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the general information was last updated")

    # Webhallen fields
    product_type = models.ManyToManyField(
        Component,
        help_text="Product type",
        related_name="products_product_type",
    )
    accessory_category = models.ManyToManyField(
        Component,
        help_text="Accessory category",
        related_name="products_accessory_category",
    )
    consumable_subcategory = models.ManyToManyField(
        Component,
        help_text="Consumable subcategory",
        related_name="products_consumable_subcategory",
    )
    technology = models.ManyToManyField(
        Component,
        help_text="Technology",
        related_name="products_technology",
    )
    printer_consumables_class = models.ManyToManyField(
        Component,
        help_text="Printer consumables class",
        related_name="products_printer_consumables_class",
    )
    subcategory = models.ManyToManyField(
        Component,
        help_text="Subcategory",
        related_name="products_subcategory",
    )
    category = models.ManyToManyField(
        Component,
        help_text="Category",
        related_name="products_category",
    )
    installation_type = models.ManyToManyField(
        Component,
        help_text="Installation type",
        related_name="products_installation_type",
    )
    designed_for = models.ManyToManyField(
        Component,
        help_text="Designed for",
        related_name="products_designed_for",
    )
    environment = models.ManyToManyField(
        Component,
        help_text="Environment",
        related_name="products_environment",
    )
    number_of_set_parts = models.ManyToManyField(
        Component,
        help_text="Number of set parts",
        related_name="products_number_of_set_parts",
    )
    suitable_for = models.ManyToManyField(
        Component,
        help_text="Suitable for",
        related_name="products_suitable_for",
    )
    features = models.ManyToManyField(
        Component,
        help_text="Features",
        related_name="products_features",
    )
    learning = models.ManyToManyField(
        Component,
        help_text="Learning",
        related_name="products_learning",
    )
    min_age = models.ManyToManyField(
        Component,
        help_text="Minimum age",
        related_name="products_min_age",
    )
    max_age = models.ManyToManyField(
        Component,
        help_text="Maximum age",
        related_name="products_max_age",
    )
    one_board_computer_included = models.ManyToManyField(
        Component,
        help_text="One board computer included",
        related_name="products_one_board_computer_included",
    )
    waterproof = models.ManyToManyField(
        Component,
        help_text="Waterproof",
        related_name="products_waterproof",
    )
    dimmer = models.ManyToManyField(
        Component,
        help_text="Dimmer",
        related_name="products_dimmer",
    )
    cable_length = models.ManyToManyField(
        Component,
        help_text="Cable length",
        related_name="products_cable_length",
    )
    supported_wattage_for_light_bulb = models.ManyToManyField(
        Component,
        help_text="Supported wattage for light bulb",
        related_name="products_supported_wattage_for_light_bulb",
    )
    number_of_installed_light_bulbs = models.ManyToManyField(
        Component,
        help_text="Number of installed light bulbs",
        related_name="products_number_of_installed_light_bulbs",
    )
    number_of_supported_light_bulbs = models.ManyToManyField(
        Component,
        help_text="Number of supported light bulbs",
        related_name="products_number_of_supported_light_bulbs",
    )
    battery_included = models.ManyToManyField(
        Component,
        help_text="Battery included",
        related_name="products_battery_included",
    )
    switch_type = models.ManyToManyField(
        Component,
        help_text="Switch type",
        related_name="products_switch_type",
    )
    switch_location = models.ManyToManyField(
        Component,
        help_text="Switch location",
        related_name="products_switch_location",
    )
    clamp_mount = models.ManyToManyField(
        Component,
        help_text="Clamp mount",
        related_name="products_clamp_mount",
    )
    tool_set_parts = models.ManyToManyField(
        Component,
        help_text="Tool set parts",
        related_name="products_tool_set_parts",
    )
    socket = models.ManyToManyField(
        Component,
        help_text="Socket",
        related_name="products_socket",
    )
    socket_size = models.ManyToManyField(
        Component,
        help_text="Socket size",
        related_name="products_socket_size",
    )
    tip = models.ManyToManyField(
        Component,
        help_text="Tip",
        related_name="products_tip",
    )
    tip_size = models.ManyToManyField(
        Component,
        help_text="Tip size",
        related_name="products_tip_size",
    )
    size = models.ManyToManyField(
        Component,
        help_text="Size",
        related_name="products_size",
    )
    shape = models.ManyToManyField(
        Component,
        help_text="Shape",
        related_name="products_shape",
    )
    tracking_data = models.ManyToManyField(
        Component,
        help_text="Tracking data",
        related_name="products_tracking_data",
    )
    solution = models.ManyToManyField(
        Component,
        help_text="Solution",
        related_name="products_solution",
    )
    character_theme = models.ManyToManyField(
        Component,
        help_text="Character theme",
        related_name="products_character_theme",
    )
    AC_adapter_included = models.ManyToManyField(
        Component,
        help_text="AC adapter included",
        related_name="products_AC_adapter_included",
    )
    style = models.ManyToManyField(
        Component,
        help_text="Style",
        related_name="products_style",
    )
    recommended_for = models.ManyToManyField(
        Component,
        help_text="Recommended for",
        related_name="products_recommended_for",
    )
    recommended_use = models.ManyToManyField(
        Component,
        help_text="Recommended use",
        related_name="products_recommended_use",
    )
    connection = models.ManyToManyField(
        Component,
        help_text="Connection",
        related_name="products_connection",
    )
    type = models.ManyToManyField(
        Component,
        help_text="Type",
        related_name="products_type",
    )
    total_length = models.ManyToManyField(
        Component,
        help_text="Total length",
        related_name="products_total_length",
    )
    payment_technology = models.ManyToManyField(
        Component,
        help_text="Payment technology",
        related_name="products_payment_technology",
    )
    mechanism = models.ManyToManyField(
        Component,
        help_text="Mechanism",
        related_name="products_mechanism",
    )
    tilt_lock = models.ManyToManyField(
        Component,
        help_text="Tilt lock",
        related_name="products_tilt_lock",
    )
    headrest = models.ManyToManyField(
        Component,
        help_text="Headrest",
        related_name="products_headrest",
    )
    armrest = models.ManyToManyField(
        Component,
        help_text="Armrest",
        related_name="products_armrest",
    )
    tilt = models.ManyToManyField(
        Component,
        help_text="Tilt",
        related_name="products_tilt",
    )
    ergonomic = models.ManyToManyField(
        Component,
        help_text="Ergonomic",
        related_name="products_ergonomic",
    )
    tilt_tension_adjustment = models.ManyToManyField(
        Component,
        help_text="Tilt tension adjustment",
        related_name="products_tilt_tension_adjustment",
    )
    _class = models.ManyToManyField(
        Component,
        help_text="Class",
        related_name="products_class",
    )
    kit_contents = models.ManyToManyField(
        Component,
        help_text="Kit contents",
        related_name="products_kit_contents",
    )
    media_subcategory = models.ManyToManyField(
        Component,
        help_text="Media subcategory",
        related_name="products_media_subcategory",
    )
    indoor_outdoor = models.ManyToManyField(
        Component,
        help_text="Indoor/outdoor",
        related_name="products_indoor_outdoor",
    )
    thermometer_scale = models.ManyToManyField(
        Component,
        help_text="Thermometer scale",
        related_name="products_thermometer_scale",
    )
    usage_modes = models.ManyToManyField(
        Component,
        help_text="Usage modes",
        related_name="products_usage_modes",
    )
    car_power_adapter_included = models.ManyToManyField(
        Component,
        help_text="Car power adapter included",
        related_name="products_car_power_adapter_included",
    )
    built_in_components = models.ManyToManyField(
        Component,
        help_text="Built-in components",
        related_name="products_built_in_components",
    )
    arm_construction = models.ManyToManyField(
        Component,
        help_text="Arm construction",
        related_name="products_arm_construction",
    )
    number_of_modules = models.ManyToManyField(
        Component,
        help_text="Number of modules",
        related_name="products_number_of_modules",
    )
    number_of_component_sets = models.ManyToManyField(
        Component,
        help_text="Number of component sets",
        related_name="products_number_of_component_sets",
    )
    number_of_sockets = models.ManyToManyField(
        Component,
        help_text="Number of sockets",
        related_name="products_number_of_sockets",
    )
    output_connection_type = models.ManyToManyField(
        Component,
        help_text="Output connection type",
        related_name="products_output_connection_type",
    )
    output_bar_configuration = models.ManyToManyField(
        Component,
        help_text="Output bar configuration",
        related_name="products_output_bar_configuration",
    )
    lock_type = models.ManyToManyField(
        Component,
        help_text="Lock type",
        related_name="products_lock_type",
    )
    power = models.ManyToManyField(
        Component,
        help_text="Power",
        related_name="products_power",
    )
    cordless = models.ManyToManyField(
        Component,
        help_text="Cordless",
        related_name="products_cordless",
    )
    diameter = models.ManyToManyField(
        Component,
        help_text="Diameter",
        related_name="products_diameter",
    )

    def __str__(self) -> str:
        return "General"

    def import_json(self, data: dict) -> None:  # noqa: PLR0914, PLR0915
        """Import JSON data."""
        # Produkttyp
        product_type: Component = create_and_import_component(data, "Produkttyp")
        self.product_type.add(product_type)

        # Tillbehörskategori
        accessory_category: Component = create_and_import_component(data, "Tillbehörskategori")
        self.accessory_category.add(accessory_category)

        # Underkategori förbrukningsartiklar
        consumable_subcategory: Component = create_and_import_component(data, "Underkategori förbrukningsartiklar")
        self.consumable_subcategory.add(consumable_subcategory)

        # Teknik
        technology: Component = create_and_import_component(data, "Teknik")
        self.technology.add(technology)

        # Klass skrivarförbrukningsartiklar
        printer_consumables_class: Component = create_and_import_component(data, "Klass skrivarförbrukningsartiklar")
        self.printer_consumables_class.add(printer_consumables_class)

        # Underkategori
        subcategory: Component = create_and_import_component(data, "Underkategori")
        self.subcategory.add(subcategory)

        # Kategori
        category: Component = create_and_import_component(data, "Kategori")
        self.category.add(category)

        # Installationstyp
        installation_type: Component = create_and_import_component(data, "Installationstyp")
        self.installation_type.add(installation_type)

        # Utformad för
        designed_for: Component = create_and_import_component(data, "Utformad för")
        self.designed_for.add(designed_for)

        # Miljö
        environment: Component = create_and_import_component(data, "Miljö")
        self.environment.add(environment)

        # Antal inställda delar
        number_of_set_parts: Component = create_and_import_component(data, "Antal inställda delar")
        self.number_of_set_parts.add(number_of_set_parts)

        # Lämplig för
        suitable_for: Component = create_and_import_component(data, "Lämplig för")
        self.suitable_for.add(suitable_for)

        # Funktioner
        features: Component = create_and_import_component(data, "Funktioner")
        self.features.add(features)

        # Inlärning
        learning: Component = create_and_import_component(data, "Inlärning")
        self.learning.add(learning)

        # Min. ålder
        min_age: Component = create_and_import_component(data, "Min. ålder")
        self.min_age.add(min_age)

        # Max. ålder
        max_age: Component = create_and_import_component(data, "Max. ålder")
        self.max_age.add(max_age)

        # En-kortsdator ingår
        one_board_computer_included: Component = create_and_import_component(data, "En-kortsdator ingår")
        self.one_board_computer_included.add(one_board_computer_included)

        # Vattentät
        waterproof: Component = create_and_import_component(data, "Vattentät")
        self.waterproof.add(waterproof)

        # Dimmer
        dimmer: Component = create_and_import_component(data, "Dimmer")
        self.dimmer.add(dimmer)

        # Kabellängd
        cable_length: Component = create_and_import_component(data, "Kabellängd")
        self.cable_length.add(cable_length)

        # Watt som stöds för glödlampa
        supported_wattage_for_light_bulb: Component = create_and_import_component(data, "Watt som stöds för glödlampa")
        self.supported_wattage_for_light_bulb.add(supported_wattage_for_light_bulb)

        # Antal installerade glödlampor
        number_of_installed_light_bulbs: Component = create_and_import_component(data, "Antal installerade glödlampor")
        self.number_of_installed_light_bulbs.add(number_of_installed_light_bulbs)

        # Antal glödlampor som stöds
        number_of_supported_light_bulbs: Component = create_and_import_component(data, "Antal glödlampor som stöds")
        self.number_of_supported_light_bulbs.add(number_of_supported_light_bulbs)

        # Batteri ingår
        battery_included: Component = create_and_import_component(data, "Batteri ingår")
        self.battery_included.add(battery_included)

        # Omkopplingstyp
        switch_type: Component = create_and_import_component(data, "Omkopplingstyp")
        self.switch_type.add(switch_type)

        # Omkopplingsplats
        switch_location: Component = create_and_import_component(data, "Omkopplingsplats")
        self.switch_location.add(switch_location)

        # Klämmontering
        clamp_mount: Component = create_and_import_component(data, "Klämmontering")
        self.clamp_mount.add(clamp_mount)

        # Verktygsuppsättning (delar)
        tool_set_parts: Component = create_and_import_component(data, "Verktygsuppsättning (delar)")
        self.tool_set_parts.add(tool_set_parts)

        # Uttag
        socket: Component = create_and_import_component(data, "Uttag")
        self.socket.add(socket)

        # Uttagsstorlek
        socket_size: Component = create_and_import_component(data, "Uttagsstorlek")
        self.socket_size.add(socket_size)

        # Spets
        tip: Component = create_and_import_component(data, "Spets")
        self.tip.add(tip)

        # Spetsstorlek
        tip_size: Component = create_and_import_component(data, "Spetsstorlek")
        self.tip_size.add(tip_size)

        # Storlek
        size: Component = create_and_import_component(data, "Storlek")
        self.size.add(size)

        # Form
        shape: Component = create_and_import_component(data, "Form")
        self.shape.add(shape)

        # Spårningsdata
        tracking_data: Component = create_and_import_component(data, "Spårningsdata")
        self.tracking_data.add(tracking_data)

        # Lösning
        solution: Component = create_and_import_component(data, "Lösning")
        self.solution.add(solution)

        # Tecken/tema
        character_theme: Component = create_and_import_component(data, "Tecken/tema")
        self.character_theme.add(character_theme)

        # Växelströmsadapter medföljer
        ac_adapter_included: Component = create_and_import_component(data, "Växelströmsadapter medföljer")
        self.AC_adapter_included.add(ac_adapter_included)

        # Stil
        style: Component = create_and_import_component(data, "Stil")
        self.style.add(style)

        # Rekommenderas för
        recommended_for: Component = create_and_import_component(data, "Rekommenderas för")
        self.recommended_for.add(recommended_for)

        # Rekommenderad användning
        recommended_use: Component = create_and_import_component(data, "Rekommenderad användning")
        self.recommended_use.add(recommended_use)

        # Anslutning
        connection: Component = create_and_import_component(data, "Anslutning")
        self.connection.add(connection)

        # Typ
        _type: Component = create_and_import_component(data, "Typ")
        self.type.add(_type)

        # Total längd
        total_length: Component = create_and_import_component(data, "Total längd")
        self.total_length.add(total_length)

        # Betalningsteknik
        payment_technology: Component = create_and_import_component(data, "Betalningsteknik")
        self.payment_technology.add(payment_technology)

        # Mekanism
        mechanism: Component = create_and_import_component(data, "Mekanism")
        self.mechanism.add(mechanism)

        # Lutningslås
        tilt_lock: Component = create_and_import_component(data, "Lutningslås")
        self.tilt_lock.add(tilt_lock)

        # Huvudstöd
        headrest: Component = create_and_import_component(data, "Huvudstöd")
        self.headrest.add(headrest)

        # Armstöd
        armrest: Component = create_and_import_component(data, "Armstöd")
        self.armrest.add(armrest)

        # Lutning
        tilt: Component = create_and_import_component(data, "Lutning")
        self.tilt.add(tilt)

        # Ergonomisk
        ergonomic: Component = create_and_import_component(data, "Ergonomisk")
        self.ergonomic.add(ergonomic)

        # Lutande spänningsjustering
        tilt_tension_adjustment: Component = create_and_import_component(data, "Lutande spänningsjustering")
        self.tilt_tension_adjustment.add(tilt_tension_adjustment)

        # Klass
        _class: Component = create_and_import_component(data, "Klass")
        self._class.add(_class)

        # Kitinnehåll
        kit_contents: Component = create_and_import_component(data, "Kitinnehåll")
        self.kit_contents.add(kit_contents)

        # Underkategori medier
        media_subcategory: Component = create_and_import_component(data, "Underkategori medier")
        self.media_subcategory.add(media_subcategory)

        # Inomhus/utomhus
        indoor_outdoor: Component = create_and_import_component(data, "Inomhus/utomhus")
        self.indoor_outdoor.add(indoor_outdoor)

        # Termometerskala
        thermometer_scale: Component = create_and_import_component(data, "Termometerskala")
        self.thermometer_scale.add(thermometer_scale)

        # Användningslägen
        usage_modes: Component = create_and_import_component(data, "Användningslägen")
        self.usage_modes.add(usage_modes)

        # Bilströmsadapter medföljer
        car_power_adapter_included: Component = create_and_import_component(data, "Bilströmsadapter medföljer")
        self.car_power_adapter_included.add(car_power_adapter_included)

        # Inbyggda komponenter
        built_in_components: Component = create_and_import_component(data, "Inbyggda komponenter")
        self.built_in_components.add(built_in_components)

        # Armkonstruktion
        arm_construction: Component = create_and_import_component(data, "Armkonstruktion")
        self.arm_construction.add(arm_construction)

        # Antal moduler
        number_of_modules: Component = create_and_import_component(data, "Antal moduler")
        self.number_of_modules.add(number_of_modules)

        # Antal uppsättningar komponenter
        number_of_component_sets: Component = create_and_import_component(data, "Antal uppsättningar komponenter")
        self.number_of_component_sets.add(number_of_component_sets)

        # Antal uttag
        number_of_sockets: Component = create_and_import_component(data, "Antal uttag")
        self.number_of_sockets.add(number_of_sockets)

        # Utgångsanslutningstyp
        output_connection_type: Component = create_and_import_component(data, "Utgångsanslutningstyp")
        self.output_connection_type.add(output_connection_type)

        # Konfiguration av utgångsstänger
        output_bar_configuration: Component = create_and_import_component(data, "Konfiguration av utgångsstänger")
        self.output_bar_configuration.add(output_bar_configuration)

        # Låstyp
        lock_type: Component = create_and_import_component(data, "Låstyp")
        self.lock_type.add(lock_type)

        # Ström
        power: Component = create_and_import_component(data, "Ström")
        self.power.add(power)

        # Sladdlös
        cordless: Component = create_and_import_component(data, "Sladdlös")
        self.cordless.add(cordless)

        # Diameter
        diameter: Component = create_and_import_component(data, "Diameter")
        self.diameter.add(diameter)


class Miscellaneous(auto_prefetch.Model):
    """Miscellaneous information."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the miscellaneous information was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the miscellaneous information was last updated")

    # Webhallen fields
    color = models.ManyToManyField(Component, help_text="Color", related_name="miscellaneous_color")
    color_category = models.ManyToManyField(
        Component,
        help_text="Color category",
        related_name="miscellaneous_color_category",
    )
    flat_screen_mounting_interface = models.ManyToManyField(
        Component,
        help_text="Flat screen mounting interface",
        related_name="miscellaneous_flat_screen_mounting_interface",
    )
    rack_mounting_kit = models.ManyToManyField(
        Component,
        help_text="Rack mounting kit",
        related_name="miscellaneous_rack_mounting_kit",
    )
    compatible_game_console = models.ManyToManyField(
        Component,
        help_text="Compatible game console",
        related_name="miscellaneous_compatible_game_console",
    )
    sound_pressure_level = models.ManyToManyField(
        Component,
        help_text="Sound pressure level",
        related_name="miscellaneous_sound_pressure_level",
    )
    external_color = models.ManyToManyField(
        Component,
        help_text="External color",
        related_name="miscellaneous_external_color",
    )
    encryption_algorithm = models.ManyToManyField(
        Component,
        help_text="Encryption algorithm",
        related_name="miscellaneous_encryption_algorithm",
    )
    hard_drive_form_factor_compatibility = models.ManyToManyField(
        Component,
        help_text="HDD form factor compatibility",
        related_name="miscellaneous_hard_drive_form_factor_compatibility",
    )
    hard_drive_compatible_form_factor_metric = models.ManyToManyField(
        Component,
        help_text="HDD compatible form factor metric",
        related_name="miscellaneous_hard_drive_compatible_form_factor_metric",
    )
    material = models.ManyToManyField(Component, help_text="Material", related_name="miscellaneous_material")
    product_material = models.ManyToManyField(
        Component,
        help_text="Product material",
        related_name="miscellaneous_product_material",
    )
    features = models.ManyToManyField(Component, help_text="Features", related_name="miscellaneous_features")
    gaming = models.ManyToManyField(Component, help_text="Gaming", related_name="miscellaneous_gaming")
    finish = models.ManyToManyField(Component, help_text="Finish", related_name="miscellaneous_finish")
    works_with_chromebook = models.ManyToManyField(
        Component,
        help_text="Works with Chromebook",
        related_name="miscellaneous_works_with_chromebook",
    )
    recycled_product_content = models.ManyToManyField(
        Component,
        help_text="Recycled product content",
        related_name="miscellaneous_recycled_product_content",
    )
    included_accessories = models.ManyToManyField(
        Component,
        help_text="Included accessories",
        related_name="miscellaneous_included_accessories",
    )
    operating_time_without_power_connection = models.ManyToManyField(
        Component,
        help_text="Operating time without power connection",
        related_name="miscellaneous_operating_time_without_power_connection",
    )
    cordless_use = models.ManyToManyField(
        Component,
        help_text="Cordless use",
        related_name="miscellaneous_cordless_use",
    )
    max_load = models.ManyToManyField(Component, help_text="Max load", related_name="miscellaneous_max_load")
    recycled_packaging_content = models.ManyToManyField(
        Component,
        help_text="Recycled packaging content",
        related_name="miscellaneous_recycled_packaging_content",
    )
    protection = models.ManyToManyField(Component, help_text="Protection", related_name="miscellaneous_protection")
    packaging_type = models.ManyToManyField(
        Component,
        help_text="Packaging type",
        related_name="miscellaneous_packaging_type",
    )
    design_features = models.ManyToManyField(
        Component,
        help_text="Design features",
        related_name="miscellaneous_design_features",
    )
    package_type = models.ManyToManyField(
        Component,
        help_text="Package type",
        related_name="miscellaneous_package_type",
    )
    standards_followed = models.ManyToManyField(
        Component,
        help_text="Standards followed",
        related_name="miscellaneous_standards_followed",
    )
    coffee_maker_accessories = models.ManyToManyField(
        Component,
        help_text="Coffee maker accessories",
        related_name="miscellaneous_coffee_maker_accessories",
    )
    max_depth_for_water_resistance = models.ManyToManyField(
        Component,
        help_text="Max depth for water resistance",
        related_name="miscellaneous_max_depth_for_water_resistance",
    )
    for_underwater_use = models.ManyToManyField(
        Component,
        help_text="For underwater use",
        related_name="miscellaneous_for_underwater_use",
    )
    pricing_type = models.ManyToManyField(
        Component,
        help_text="Pricing type",
        related_name="miscellaneous_pricing_type",
    )
    capacity = models.ManyToManyField(Component, help_text="Capacity", related_name="miscellaneous_capacity")
    product_type = models.ManyToManyField(
        Component,
        help_text="Product type",
        related_name="miscellaneous_product_type",
    )
    processor_package = models.ManyToManyField(
        Component,
        help_text="Processor package",
        related_name="miscellaneous_processor_package",
    )
    waterproof = models.ManyToManyField(Component, help_text="Waterproof", related_name="miscellaneous_waterproof")
    reparability_index = models.ManyToManyField(
        Component,
        help_text="Reparability index",
        related_name="miscellaneous_reparability_index",
    )
    sound_level = models.ManyToManyField(Component, help_text="Sound level", related_name="miscellaneous_sound_level")
    noise_class = models.ManyToManyField(Component, help_text="Noise class", related_name="miscellaneous_noise_class")
    rugged_design = models.ManyToManyField(
        Component,
        help_text="Rugged design",
        related_name="miscellaneous_rugged_design",
    )
    software_certification = models.ManyToManyField(
        Component,
        help_text="Software certification",
        related_name="miscellaneous_software_certification",
    )
    manufacturer_sales_program = models.ManyToManyField(
        Component,
        help_text="Manufacturer sales program",
        related_name="miscellaneous_manufacturer_sales_program",
    )
    recycled_product_content_comment = models.ManyToManyField(
        Component,
        help_text="Recycled product content comment",
        related_name="miscellaneous_recycled_product_content_comment",
    )
    recycled_packaging_content_comment = models.ManyToManyField(
        Component,
        help_text="Recycled packaging content comment",
        related_name="miscellaneous_recycled_packaging_content_comment",
    )
    product_condition = models.ManyToManyField(
        Component,
        help_text="Product condition",
        related_name="miscellaneous_product_condition",
    )
    ai_ready = models.ManyToManyField(Component, help_text="AI ready", related_name="miscellaneous_ai_ready")

    def __str__(self) -> str:
        return "Miscellaneous"

    def import_json(self, data: dict) -> None:  # noqa: PLR0914, PLR0915
        """Import JSON data."""
        # Färg
        color: Component = create_and_import_component(data, "Färg")
        self.color.add(color)

        # Färgkategori
        color_category: Component = create_and_import_component(data, "Färgkategori")
        self.color_category.add(color_category)

        # Monteringsgränssnitt för platt bildskärm
        flat_screen_mounting_interface: Component = create_and_import_component(
            data,
            "Monteringsgränssnitt för platt bildskärm",
        )
        self.flat_screen_mounting_interface.add(flat_screen_mounting_interface)

        # Rackmonteringssats
        rack_mounting_kit: Component = create_and_import_component(data, "Rackmonteringssats")
        self.rack_mounting_kit.add(rack_mounting_kit)

        # Kompatibla spelkonsol
        compatible_game_console: Component = create_and_import_component(data, "Kompatibla spelkonsol")
        self.compatible_game_console.add(compatible_game_console)

        # Ljudtrycknivå
        sound_pressure_level: Component = create_and_import_component(data, "Ljudtrycknivå")
        self.sound_pressure_level.add(sound_pressure_level)

        # Yttre färg
        external_color: Component = create_and_import_component(data, "Yttre färg")
        self.external_color.add(external_color)

        # Krypteringsalgoritm
        encryption_algorithm: Component = create_and_import_component(data, "Krypteringsalgoritm")
        self.encryption_algorithm.add(encryption_algorithm)

        # Formfaktorkomptibilitet för hårddisk
        hard_drive_form_factor_compatibility: Component = create_and_import_component(
            data,
            "Formfaktorkomptibilitet för hårddisk",
        )
        self.hard_drive_form_factor_compatibility.add(hard_drive_form_factor_compatibility)

        # Hårddiskkompatibel formfaktor (metrisk)
        hard_drive_compatible_form_factor_metric: Component = create_and_import_component(
            data,
            "Hårddiskkompatibel formfaktor (metrisk)",
        )
        self.hard_drive_compatible_form_factor_metric.add(hard_drive_compatible_form_factor_metric)

        # Material
        material: Component = create_and_import_component(data, "Material")
        self.material.add(material)

        # Produktmaterial
        product_material: Component = create_and_import_component(data, "Produktmaterial")
        self.product_material.add(product_material)

        # Egenskaper
        features: Component = create_and_import_component(data, "Egenskaper")
        self.features.add(features)

        # Gaming
        gaming: Component = create_and_import_component(data, "Gaming")
        self.gaming.add(gaming)

        # Finish
        finish: Component = create_and_import_component(data, "Finish")
        self.finish.add(finish)

        # Fungerar med Chromebook
        works_with_chromebook: Component = create_and_import_component(data, "Fungerar med Chromebook")
        self.works_with_chromebook.add(works_with_chromebook)

        # Återvunnet produktinnehåll
        recycled_product_content: Component = create_and_import_component(data, "Återvunnet produktinnehåll")
        self.recycled_product_content.add(recycled_product_content)

        # Inkluderade tillbehör
        included_accessories: Component = create_and_import_component(data, "Inkluderade tillbehör")
        self.included_accessories.add(included_accessories)

        # Driftstid utan nätanslutning
        operating_time_without_power_connection: Component = create_and_import_component(
            data,
            "Driftstid utan nätanslutning",
        )
        self.operating_time_without_power_connection.add(operating_time_without_power_connection)

        # Sladdlös användning
        cordless_use: Component = create_and_import_component(data, "Sladdlös användning")
        self.cordless_use.add(cordless_use)

        # Maxlast
        max_load: Component = create_and_import_component(data, "Maxlast")
        self.max_load.add(max_load)

        # Återvunnet förpackningsinnehåll
        recycled_packaging_content: Component = create_and_import_component(data, "Återvunnet förpackningsinnehåll")
        self.recycled_packaging_content.add(recycled_packaging_content)

        # Skydd
        protection: Component = create_and_import_component(data, "Skydd")
        self.protection.add(protection)

        # Förpackningstyp
        packaging_type: Component = create_and_import_component(data, "Förpackningstyp")
        self.packaging_type.add(packaging_type)

        # Designfunktioner
        design_features: Component = create_and_import_component(data, "Designfunktioner")
        self.design_features.add(design_features)

        # Pakettyp
        package_type: Component = create_and_import_component(data, "Pakettyp")
        self.package_type.add(package_type)

        # Standarder som följs
        standards_followed: Component = create_and_import_component(data, "Standarder som följs")
        self.standards_followed.add(standards_followed)

        # Kaffebryggartillbehör
        coffee_maker_accessories: Component = create_and_import_component(data, "Kaffebryggartillbehör")
        self.coffee_maker_accessories.add(coffee_maker_accessories)

        # Maxdjup för vattentålighet
        max_depth_for_water_resistance: Component = create_and_import_component(data, "Maxdjup för vattentålighet")
        self.max_depth_for_water_resistance.add(max_depth_for_water_resistance)

        # För undervattensbruk
        for_underwater_use: Component = create_and_import_component(data, "För undervattensbruk")
        self.for_underwater_use.add(for_underwater_use)

        # Typ av prissättning
        pricing_type: Component = create_and_import_component(data, "Typ av prissättning")
        self.pricing_type.add(pricing_type)

        # Kapacitet
        capacity: Component = create_and_import_component(data, "Kapacitet")
        self.capacity.add(capacity)

        # Produkttyp
        product_type: Component = create_and_import_component(data, "Produkttyp")
        self.product_type.add(product_type)

        # Processorpaket
        processor_package: Component = create_and_import_component(data, "Processorpaket")
        self.processor_package.add(processor_package)

        # Vattentät
        waterproof: Component = create_and_import_component(data, "Vattentät")
        self.waterproof.add(waterproof)

        # Reparationsbarhetsindex
        reparability_index: Component = create_and_import_component(data, "Reparationsbarhetsindex")
        self.reparability_index.add(reparability_index)

        # Ljudnivå
        sound_level: Component = create_and_import_component(data, "Ljudnivå")
        self.sound_level.add(sound_level)

        # Bullerklass
        noise_class: Component = create_and_import_component(data, "Bullerklass")
        self.noise_class.add(noise_class)

        # Robust design
        rugged_design: Component = create_and_import_component(data, "Robust design")
        self.rugged_design.add(rugged_design)

        # Mjukvarucertifiering
        software_certification: Component = create_and_import_component(data, "Mjukvarucertifiering")
        self.software_certification.add(software_certification)

        # Försäljningsprogram från tillverkaren
        manufacturer_sales_program: Component = create_and_import_component(
            data,
            "Försäljningsprogram från tillverkaren",
        )
        self.manufacturer_sales_program.add(manufacturer_sales_program)

        # Återvunnet produktinnehåll (kommentar)
        recycled_product_content_comment: Component = create_and_import_component(
            data,
            "Återvunnet produktinnehåll (kommentar)",
        )
        self.recycled_product_content_comment.add(recycled_product_content_comment)

        # Återvunnet förpackningsinnehåll (kommentar)
        recycled_packaging_content_comment: Component = create_and_import_component(
            data,
            "Återvunnet förpackningsinnehåll (kommentar)",
        )
        self.recycled_packaging_content_comment.add(recycled_packaging_content_comment)

        # Produktens skick
        product_condition: Component = create_and_import_component(data, "Produktens skick")
        self.product_condition.add(product_condition)

        # AI-klar
        ai_ready: Component = create_and_import_component(data, "AI-klar")
        self.ai_ready.add(ai_ready)


class Cable(auto_prefetch.Model):
    """Cable."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the cable was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the cable was last updated")

    # Webhallen fields
    something = models.TextField(help_text="Something")  # TODO(TheLovinator): What is this?  # noqa: TD003
    cable = models.ManyToManyField(Component, help_text="Cable")


class InputDevice(auto_prefetch.Model):
    """Input device."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the input device was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the input device was last updated")
    # Webhallen fields
    connection_technology = models.ManyToManyField(
        Component,
        help_text="Connection technology",
        related_name="input_device_connection_technology",
    )
    interface = models.ManyToManyField(Component, help_text="Interface", related_name="input_device_interface")
    product_type = models.ManyToManyField(Component, help_text="Product type", related_name="input_device_product_type")
    backlit = models.ManyToManyField(Component, help_text="Backlit", related_name="input_device_backlit")
    form_factor = models.ManyToManyField(Component, help_text="Form factor", related_name="input_device_form_factor")
    interface_type = models.ManyToManyField(
        Component,
        help_text="Interface type",
        related_name="input_device_interface_type",
    )
    input_adapter_type = models.ManyToManyField(
        Component,
        help_text="Input adapter type",
        related_name="input_device_input_adapter_type",
    )
    keyboard_localization = models.ManyToManyField(
        Component,
        help_text="Keyboard localization",
        related_name="input_device_keyboard_localization",
    )
    motion_detection_technology = models.ManyToManyField(
        Component,
        help_text="Motion detection technology",
        related_name="input_device_motion_detection_technology",
    )
    orientation = models.ManyToManyField(Component, help_text="Orientation", related_name="input_device_orientation")
    number_of_buttons = models.ManyToManyField(
        Component,
        help_text="Number of buttons",
        related_name="input_device_number_of_buttons",
    )
    motion_resolution = models.ManyToManyField(
        Component,
        help_text="Motion resolution",
        related_name="input_device_motion_resolution",
    )
    notebook_mouse = models.ManyToManyField(
        Component,
        help_text="Notebook mouse",
        related_name="input_device_notebook_mouse",
    )
    ergonomic_design = models.ManyToManyField(
        Component,
        help_text="Ergonomic design",
        related_name="input_device_ergonomic_design",
    )
    keyboard_layout = models.ManyToManyField(
        Component,
        help_text="Keyboard layout",
        related_name="input_device_keyboard_layout",
    )
    keyboard_technology = models.ManyToManyField(
        Component,
        help_text="Keyboard technology",
        related_name="input_device_keyboard_technology",
    )
    active_horizontal_area = models.ManyToManyField(
        Component,
        help_text="Active horizontal area",
        related_name="input_device_active_horizontal_area",
    )
    active_vertical_area = models.ManyToManyField(
        Component,
        help_text="Active vertical area",
        related_name="input_device_active_vertical_area",
    )
    anti_ghosting = models.ManyToManyField(
        Component,
        help_text="Anti-ghosting",
        related_name="input_device_anti_ghosting",
    )
    number_of_simultaneous_keypresses = models.ManyToManyField(
        Component,
        help_text="Number of simultaneous keypresses",
        related_name="input_device_number_of_simultaneous_keypresses",
    )
    type = models.ManyToManyField(Component, help_text="Type", related_name="input_device_type")
    key_lock_type = models.ManyToManyField(
        Component,
        help_text="Key lock type",
        related_name="input_device_key_lock_type",
    )
    backlight = models.ManyToManyField(Component, help_text="Backlight", related_name="input_device_backlight")
    numeric_keypad = models.ManyToManyField(
        Component,
        help_text="Numeric keypad",
        related_name="input_device_numeric_keypad",
    )


class ServiceAndSupport(auto_prefetch.Model):
    """Service and support."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the service and support was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the service and support was last updated")

    # Webhallen fields
    service_and_support = models.ManyToManyField(Component, help_text="Service and support")


class GrossDimensionsAndWeight(auto_prefetch.Model):
    """Gross dimensions and weight."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the gross dimensions and weight was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the gross dimensions and weight was last updated")
    # Webhallen fields
    packing_weight = models.ManyToManyField(
        Component,
        help_text="Packing weight",
        related_name="gross_dimensions_packing_weight",
    )
    packing_height = models.ManyToManyField(
        Component,
        help_text="Packing height",
        related_name="gross_dimensions_packing_height",
    )
    packing_depth = models.ManyToManyField(
        Component,
        help_text="Packing depth",
        related_name="gross_dimensions_packing_depth",
    )
    packing_width = models.ManyToManyField(
        Component,
        help_text="Packing width",
        related_name="gross_dimensions_packing_width",
    )


class Consumables(auto_prefetch.Model):
    """Consumables."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the consumables was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the consumables was last updated")

    # Webhallen fields
    color = models.ManyToManyField(Component, help_text="Color", related_name="consumables_color")
    consumable_type = models.ManyToManyField(
        Component,
        help_text="Consumable type",
        related_name="consumables_consumable_type",
    )
    number_of_pages_during_lifetime = models.ManyToManyField(
        Component,
        help_text="Number of pages during life cycle",
        related_name="consumables_number_of_pages_during_lifetime",
    )
    coverage_for_lifetime = models.ManyToManyField(
        Component,
        help_text="Coverage for lifetime",
        related_name="consumables_coverage_for_lifetime",
    )


class Battery(auto_prefetch.Model):
    """Battery."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the battery was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the battery was last updated")
    # Webhallen fields
    included_quantity = models.ManyToManyField(
        Component,
        help_text="Included quantity",
        related_name="battery_included_quantity",
    )
    technology = models.ManyToManyField(Component, help_text="Technology", related_name="battery_technology")
    form_factor = models.ManyToManyField(Component, help_text="Form factor", related_name="battery_form_factor")
    capacity_ah = models.ManyToManyField(Component, help_text="Capacity (Ah)", related_name="battery_capacity_ah")
    supplied_voltage = models.ManyToManyField(
        Component,
        help_text="Supplied voltage",
        related_name="battery_supplied_voltage",
    )
    installed_count = models.ManyToManyField(
        Component,
        help_text="Installed count",
        related_name="battery_installed_count",
    )
    charging_time = models.ManyToManyField(Component, help_text="Charging time", related_name="battery_charging_time")
    battery_time_up_to = models.ManyToManyField(
        Component,
        help_text="Battery time up to",
        related_name="battery_time_up_to",
    )
    capacity = models.ManyToManyField(Component, help_text="Capacity", related_name="battery_capacity")
    talk_time = models.ManyToManyField(Component, help_text="Talk time", related_name="battery_talk_time")
    standby_time = models.ManyToManyField(Component, help_text="Standby time", related_name="battery_standby_time")
    run_time = models.ManyToManyField(Component, help_text="Run time", related_name="battery_run_time")
    wireless_charging = models.ManyToManyField(
        Component,
        help_text="Wireless charging",
        related_name="battery_wireless_charging",
    )
    fast_charging_technology = models.ManyToManyField(
        Component,
        help_text="Fast charging technology",
        related_name="battery_fast_charging_technology",
    )
    capacity_wh = models.ManyToManyField(Component, help_text="Capacity (Wh)", related_name="battery_capacity_wh")
    battery_type = models.ManyToManyField(Component, help_text="Battery type", related_name="battery_type")


class AVComponent(auto_prefetch.Model):
    """AV component."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the AV component was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the AV component was last updated")

    # Webhallen fields
    something = models.TextField(help_text="Something")  # TODO(TheLovinator): What is this?  # noqa: TD003
    av_component = models.ManyToManyField(Component, help_text="AV component")


class RemoteControl(auto_prefetch.Model):
    """Remote control."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the remote control was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the remote control was last updated")

    # Webhallen fields
    max_working_distance = models.ManyToManyField(
        Component,
        help_text="Max working distance",
        related_name="remote_control_max_working_distance",
    )
    remote_control_technology = models.ManyToManyField(
        Component,
        help_text="Remote control technology",
        related_name="remote_control_technology",
    )
    supported_devices = models.ManyToManyField(
        Component,
        help_text="Supported devices",
        related_name="remote_control_supported_devices",
    )
    type = models.ManyToManyField(
        Component,
        help_text="Type",
        related_name="remote_control_type",
    )
    number_of_devices_supported = models.ManyToManyField(
        Component,
        help_text="Number of devices supported",
        related_name="remote_control_number_of_devices_supported",
    )


class VideoInput(auto_prefetch.Model):
    """Video input."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the video input was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the video input was last updated")

    # Webhallen fields
    support_for_audio_input = models.ManyToManyField(
        Component,
        help_text="Support for audio input",
        related_name="video_input_support_for_audio_input",
    )
    format_for_digital_video = models.ManyToManyField(
        Component,
        help_text="Format for digital video",
        related_name="video_input_format_for_digital_video",
    )
    format_for_analog_video = models.ManyToManyField(
        Component,
        help_text="Format for analog video",
        related_name="video_input_format_for_analog_video",
    )
    analog_video_signal = models.ManyToManyField(
        Component,
        help_text="Analog video signal",
        related_name="video_input_analog_video_signal",
    )
    resolution_for_digital_video_capture = models.ManyToManyField(
        Component,
        help_text="Resolution for digital video capture",
        related_name="video_input_resolution_for_digital_video_capture",
    )
    type_of_interface = models.ManyToManyField(
        Component,
        help_text="Type of interface",
        related_name="video_input_type_of_interface",
    )
    connection_technology = models.ManyToManyField(
        Component,
        help_text="Connection technology",
        related_name="video_input_connection_technology",
    )
    support_for_audio = models.ManyToManyField(
        Component,
        help_text="Support for audio",
        related_name="video_input_support_for_audio",
    )
    camera_type = models.ManyToManyField(Component, help_text="Camera type", related_name="video_input_camera_type")
    computer_interface = models.ManyToManyField(
        Component,
        help_text="Computer interface",
        related_name="video_input_computer_interface",
    )
    maximum_digital_video_resolution = models.ManyToManyField(
        Component,
        help_text="Maximum digital video resolution",
        related_name="video_input_maximum_digital_video_resolution",
    )
    frame_rate_max = models.ManyToManyField(
        Component,
        help_text="Frame rate max",
        related_name="video_input_frame_rate_max",
    )
    day_and_night_function = models.ManyToManyField(
        Component,
        help_text="Day and night function",
        related_name="video_input_day_and_night_function",
    )
    camera_mounting_type = models.ManyToManyField(
        Component,
        help_text="Camera mounting type",
        related_name="video_input_camera_mounting_type",
    )
    mechanical_camera_design = models.ManyToManyField(
        Component,
        help_text="Mechanical camera design",
        related_name="video_input_mechanical_camera_design",
    )
    form_factor = models.ManyToManyField(Component, help_text="Form factor", related_name="video_input_form_factor")
    resolution_for_still_shot = models.ManyToManyField(
        Component,
        help_text="Resolution for still shot",
        related_name="video_input_resolution_for_still_shot",
    )
    motion_detection = models.ManyToManyField(
        Component,
        help_text="Motion detection",
        related_name="video_input_motion_detection",
    )
    video_interface = models.ManyToManyField(
        Component,
        help_text="Video interface",
        related_name="video_input_video_interface",
    )
    type = models.ManyToManyField(Component, help_text="Type", related_name="video_input_type")
    image_capture_format = models.ManyToManyField(
        Component,
        help_text="Image capture format",
        related_name="video_input_image_capture_format",
    )
    properties = models.ManyToManyField(Component, help_text="Properties", related_name="video_input_properties")
    digital_zoom = models.ManyToManyField(Component, help_text="Digital zoom", related_name="video_input_digital_zoom")
    face_recognition = models.ManyToManyField(
        Component,
        help_text="Face recognition",
        related_name="video_input_face_recognition",
    )
    support_for_high_resolution_video = models.ManyToManyField(
        Component,
        help_text="Support for high resolution video",
        related_name="video_input_support_for_high_resolution_video",
    )
    continuous_shooting_rate = models.ManyToManyField(
        Component,
        help_text="Continuous shooting rate",
        related_name="video_input_continuous_shooting_rate",
    )
    image_stabilizer = models.ManyToManyField(
        Component,
        help_text="Image stabilizer",
        related_name="video_input_image_stabilizer",
    )
    max_video_resolution = models.ManyToManyField(
        Component,
        help_text="Max video resolution",
        related_name="video_input_max_video_resolution",
    )
    provided_interfaces = models.ManyToManyField(
        Component,
        help_text="Provided interfaces",
        related_name="video_input_provided_interfaces",
    )
    special_effects = models.ManyToManyField(
        Component,
        help_text="Special effects",
        related_name="video_input_special_effects",
    )
    digital_camera_type = models.ManyToManyField(
        Component,
        help_text="Digital camera type",
        related_name="video_input_digital_camera_type",
    )
    iso_max = models.ManyToManyField(Component, help_text="ISO max", related_name="video_input_iso_max")
    combined_with = models.ManyToManyField(
        Component,
        help_text="Combined with",
        related_name="video_input_combined_with",
    )
    light_sensitivity = models.ManyToManyField(
        Component,
        help_text="Light sensitivity",
        related_name="video_input_light_sensitivity",
    )


class SystemRequirements(auto_prefetch.Model):
    """System requirements."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the system requirements was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the system requirements was last updated")

    # Webhallen fields
    required_operating_system = models.ManyToManyField(
        Component,
        help_text="Required operating system",
        related_name="system_requirements_required_operating_system",
    )
    os_family = models.ManyToManyField(Component, help_text="OS family", related_name="system_requirements_os_family")
    supported_host_platform = models.ManyToManyField(
        Component,
        help_text="Supported host platform",
        related_name="system_requirements_supported_host_platform",
    )


class Network(auto_prefetch.Model):
    """Network."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the network was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the network was last updated")

    # Webhallen fields
    type = models.ManyToManyField(Component, help_text="Type", related_name="network_type")
    number_of_ports = models.ManyToManyField(
        Component,
        help_text="Number of ports",
        related_name="network_number_of_ports",
    )
    subcategory = models.ManyToManyField(Component, help_text="Subcategory", related_name="network_subcategory")
    form_factor = models.ManyToManyField(Component, help_text="Form factor", related_name="network_form_factor")
    subtype = models.ManyToManyField(Component, help_text="Subtype", related_name="network_subtype")
    managed = models.ManyToManyField(Component, help_text="Managed", related_name="network_managed")
    jumbo_frame_support = models.ManyToManyField(
        Component,
        help_text="Jumbo frame support",
        related_name="network_jumbo_frame_support",
    )
    power_over_ethernet = models.ManyToManyField(
        Component,
        help_text="Power over Ethernet",
        related_name="network_power_over_ethernet",
    )
    connection_technology = models.ManyToManyField(
        Component,
        help_text="Connection technology",
        related_name="network_connection_technology",
    )
    data_link_protocol = models.ManyToManyField(
        Component,
        help_text="Data link protocol",
        related_name="network_data_link_protocol",
    )
    type_of_cabling = models.ManyToManyField(
        Component,
        help_text="Type of cabling",
        related_name="network_type_of_cabling",
    )
    interface_type_bus = models.ManyToManyField(
        Component,
        help_text="Interface type bus",
        related_name="network_interface_type_bus",
    )
    data_transfer_speed = models.ManyToManyField(
        Component,
        help_text="Data transfer speed",
        related_name="network_data_transfer_speed",
    )
    network_transport_protocol = models.ManyToManyField(
        Component,
        help_text="Network transport protocol",
        related_name="network_transport_protocol",
    )
    wireless_protocol = models.ManyToManyField(
        Component,
        help_text="Wireless protocol",
        related_name="network_wireless_protocol",
    )
    ac_standard = models.ManyToManyField(Component, help_text="AC standard", related_name="network_ac_standard")
    remote_administration_protocol = models.ManyToManyField(
        Component,
        help_text="Remote administration protocol",
        related_name="network_remote_administration_protocol",
    )
    number_of_wan_ports = models.ManyToManyField(
        Component,
        help_text="Number of WAN ports",
        related_name="network_number_of_wan_ports",
    )
    network_protocol = models.ManyToManyField(
        Component,
        help_text="Network protocol",
        related_name="network_network_protocol",
    )
    builtin_switch = models.ManyToManyField(
        Component,
        help_text="Built-in switch",
        related_name="network_builtin_switch",
    )
    important_functions = models.ManyToManyField(
        Component,
        help_text="Important functions",
        related_name="network_important_functions",
    )
    network_interface = models.ManyToManyField(
        Component,
        help_text="Network interface",
        related_name="network_network_interface",
    )
    advanced_switching = models.ManyToManyField(
        Component,
        help_text="Advanced switching",
        related_name="network_advanced_switching",
    )
    remote_management_interface = models.ManyToManyField(
        Component,
        help_text="Remote management interface",
        related_name="network_remote_management_interface",
    )
    max_area_indoor = models.ManyToManyField(
        Component,
        help_text="Max area indoor",
        related_name="network_max_area_indoor",
    )
    wireless_connection = models.ManyToManyField(
        Component,
        help_text="Wireless connection",
        related_name="network_wireless_connection",
    )
    lan_presentation_and_wireless_d_o = models.ManyToManyField(
        Component,
        help_text="LAN presentation and wireless D/O",
        related_name="network_lan_presentation_and_wireless_d_o",
    )
    image_transfer_protocol_for_lan_and_wireless = models.ManyToManyField(
        Component,
        help_text="Image transfer protocol for LAN and wireless",
        related_name="network_image_transfer_protocol_for_lan_and_wireless",
    )
    support_for_wireless_lan = models.ManyToManyField(
        Component,
        help_text="Support for wireless LAN",
        related_name="network_support_for_wireless_lan",
    )
    cloud_managed = models.ManyToManyField(Component, help_text="Cloud managed", related_name="network_cloud_managed")
    wire_protocol = models.ManyToManyField(Component, help_text="Wire protocol", related_name="network_wire_protocol")


class SpeakerSystem(auto_prefetch.Model):
    """Speaker system."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the speaker system was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the speaker system was last updated")
    # Webhallen fields
    connection_technology = models.ManyToManyField(
        Component,
        help_text="Connection technology",
        related_name="speaker_system_connection_technology",
    )
    amplification_type = models.ManyToManyField(
        Component,
        help_text="Amplification type",
        related_name="speaker_system_amplification_type",
    )
    speaker_configuration = models.ManyToManyField(
        Component,
        help_text="Speaker configuration",
        related_name="speaker_system_speaker_configuration",
    )
    continuous_current_for_sound_system_total = models.ManyToManyField(
        Component,
        help_text="Continuous current for sound system total",
        related_name="speaker_system_continuous_current_for_sound_system_total",
    )
    system_components = models.ManyToManyField(
        Component,
        help_text="System components",
        related_name="speaker_system_system_components",
    )
    peak_current_for_sound_system_total = models.ManyToManyField(
        Component,
        help_text="Peak current for sound system total",
        related_name="speaker_system_peak_current_for_sound_system_total",
    )
    frequency_response = models.ManyToManyField(
        Component,
        help_text="Frequency response",
        related_name="speaker_system_frequency_response",
    )
    builtin_decoders = models.ManyToManyField(
        Component,
        help_text="Built-in decoders",
        related_name="speaker_system_builtin_decoders",
    )
    number_of_crossover_channels = models.ManyToManyField(
        Component,
        help_text="Number of crossover channels",
        related_name="speaker_system_number_of_crossover_channels",
    )
    continuous_current = models.ManyToManyField(
        Component,
        help_text="Continuous current",
        related_name="speaker_system_continuous_current",
    )
    handsfree_function = models.ManyToManyField(
        Component,
        help_text="Hands-free function",
        related_name="speaker_system_handsfree_function",
    )
    app_controlled = models.ManyToManyField(
        Component,
        help_text="App controlled",
        related_name="speaker_system_app_controlled",
    )
    recommended_location = models.ManyToManyField(
        Component,
        help_text="Recommended location",
        related_name="speaker_system_recommended_location",
    )
    multiple_rooms = models.ManyToManyField(
        Component,
        help_text="Multiple rooms",
        related_name="speaker_system_multiple_rooms",
    )
    series = models.ManyToManyField(Component, help_text="Series", related_name="speaker_system_series")
    speaker_element_diameter_metric = models.ManyToManyField(
        Component,
        help_text="Speaker element diameter metric",
        related_name="speaker_system_speaker_element_diameter_metric",
    )
    integrated_components = models.ManyToManyField(
        Component,
        help_text="Integrated components",
        related_name="speaker_system_integrated_components",
    )
    peak_current = models.ManyToManyField(
        Component,
        help_text="Peak current",
        related_name="speaker_system_peak_current",
    )


class SoundSystem(auto_prefetch.Model):
    """Sound system."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the sound system was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the sound system was last updated")

    # Webhallen fields
    designed_for = models.ManyToManyField(Component, help_text="Designed for", related_name="sound_system_designed_for")
    type = models.ManyToManyField(Component, help_text="Type", related_name="sound_system_type")
    recommended_use = models.ManyToManyField(
        Component,
        help_text="Recommended use",
        related_name="sound_system_recommended_use",
    )
    mode_for_audio_output = models.ManyToManyField(
        Component,
        help_text="Mode for audio output",
        related_name="sound_system_mode_for_audio_output",
    )
    functions = models.ManyToManyField(Component, help_text="Functions", related_name="sound_system_functions")
    max_actuation_distance = models.ManyToManyField(
        Component,
        help_text="Max actuation distance",
        related_name="sound_system_max_actuation_distance",
    )
    sub_category = models.ManyToManyField(Component, help_text="Subcategory", related_name="sound_system_sub_category")
    surround_sound_effects = models.ManyToManyField(
        Component,
        help_text="Surround sound effects",
        related_name="sound_system_surround_sound_effects",
    )
    builtin_decoders = models.ManyToManyField(
        Component,
        help_text="Built-in decoders",
        related_name="sound_system_builtin_decoders",
    )
    surround_system_class = models.ManyToManyField(
        Component,
        help_text="Surround system class",
        related_name="sound_system_surround_system_class",
    )
    speaker_system = models.ManyToManyField(
        Component,
        help_text="Speaker system",
        related_name="sound_system_speaker_system",
    )
    surround_mode = models.ManyToManyField(
        Component,
        help_text="Surround mode",
        related_name="sound_system_surround_mode",
    )
    digital_player_features = models.ManyToManyField(
        Component,
        help_text="Digital player features",
        related_name="sound_system_digital_player_features",
    )
    digital_audio_format = models.ManyToManyField(
        Component,
        help_text="Digital audio format",
        related_name="sound_system_digital_audio_format",
    )
    combined_with = models.ManyToManyField(
        Component,
        help_text="Combined with",
        related_name="sound_system_combined_with",
    )
    type_of_digital_player = models.ManyToManyField(
        Component,
        help_text="Type of digital player",
        related_name="sound_system_type_of_digital_player",
    )
    audio_format = models.ManyToManyField(Component, help_text="Audio format", related_name="sound_system_audio_format")


class PowerSupply(auto_prefetch.Model):
    """Power supply."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the power supply was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the power supply was last updated")
    # Webhallen fields
    power_source = models.ManyToManyField(Component, help_text="Power source", related_name="power_supply_power_source")
    power = models.ManyToManyField(Component, help_text="Power", related_name="power_supply_power")
    capacity_va = models.ManyToManyField(Component, help_text="Capacity (VA)", related_name="power_supply_capacity_va")
    number_of_outlets = models.ManyToManyField(
        Component,
        help_text="Number of outlets",
        related_name="power_supply_number_of_outlets",
    )
    supplied_voltage = models.ManyToManyField(
        Component,
        help_text="Supplied voltage",
        related_name="power_supply_supplied_voltage",
    )
    mains_voltage = models.ManyToManyField(
        Component,
        help_text="Mains voltage",
        related_name="power_supply_mains_voltage",
    )
    ups_technology = models.ManyToManyField(
        Component,
        help_text="UPS technology",
        related_name="power_supply_ups_technology",
    )
    form_factor = models.ManyToManyField(Component, help_text="Form factor", related_name="power_supply_form_factor")
    voltage_dissipation = models.ManyToManyField(
        Component,
        help_text="Voltage dissipation",
        related_name="power_supply_voltage_dissipation",
    )
    demanded_frequency = models.ManyToManyField(
        Component,
        help_text="Required frequency",
        related_name="power_supply_demanded_frequency",
    )
    demanded_voltage = models.ManyToManyField(
        Component,
        help_text="Required voltage",
        related_name="power_supply_demanded_voltage",
    )
    max_electric_current = models.ManyToManyField(
        Component,
        help_text="Max electric current",
        related_name="power_supply_max_electric_current",
    )
    type = models.ManyToManyField(Component, help_text="Type", related_name="power_supply_type")
    required_frequency = models.ManyToManyField(
        Component,
        help_text="Required frequency",
        related_name="power_supply_required_frequency",
    )
    type_of_input_connector = models.ManyToManyField(
        Component,
        help_text="Type of input connector",
        related_name="power_supply_type_of_input_connector",
    )
    type_of_output_contact = models.ManyToManyField(
        Component,
        help_text="Type of output contact",
        related_name="power_supply_type_of_output_contact",
    )
    modular_cable_management = models.ManyToManyField(
        Component,
        help_text="Modular cable management",
        related_name="power_supply_modular_cable_management",
    )
    power_supply_compatibility = models.ManyToManyField(
        Component,
        help_text="Power supply compatibility",
        related_name="power_supply_power_supply_compatibility",
    )
    cooling_system = models.ManyToManyField(
        Component,
        help_text="Cooling system",
        related_name="power_supply_cooling_system",
    )
    the_80_plus_certification = models.ManyToManyField(
        Component,
        help_text="The 80 PLUS certification",
        related_name="power_supply_the_80_plus_certification",
    )
    alternative = models.ManyToManyField(Component, help_text="Alternative", related_name="power_supply_alternative")
    cord_length = models.ManyToManyField(Component, help_text="Cord length", related_name="power_supply_cord_length")
    energy_consumption_during_operation = models.ManyToManyField(
        Component,
        help_text="Energy consumption during operation",
        related_name="power_supply_energy_consumption_during_operation",
    )


class SettingsControlsAndIndicators(auto_prefetch.Model):
    """Settings, controls and indicators."""

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
    number_of_fan_speed_settings = models.ManyToManyField(
        Component,
        help_text="Number of fan speed settings",
        related_name="settings_controls_and_indicators_number_of_fan_speed_settings",
    )
    remote_control = models.ManyToManyField(
        Component,
        help_text="Remote control",
        related_name="settings_controls_and_indicators_remote_control",
    )
    control_type = models.ManyToManyField(
        Component,
        help_text="Control type",
        related_name="settings_controls_and_indicators_control_type",
    )
    pulse_function = models.ManyToManyField(
        Component,
        help_text="Pulse function",
        related_name="settings_controls_and_indicators_pulse_function",
    )
    number_of_speed_settings = models.ManyToManyField(
        Component,
        help_text="Number of speed settings",
        related_name="settings_controls_and_indicators_number_of_speed_settings",
    )
    room_navigation = models.ManyToManyField(
        Component,
        help_text="Room navigation",
        related_name="settings_controls_and_indicators_room_navigation",
    )
    heating_time = models.ManyToManyField(
        Component,
        help_text="Heating time",
        related_name="settings_controls_and_indicators_heating_time",
    )
    programmable_cleaning_intervals = models.ManyToManyField(
        Component,
        help_text="Programmable cleaning intervals",
        related_name="settings_controls_and_indicators_programmable_cleaning_intervals",
    )
    controls_on_handle = models.ManyToManyField(
        Component,
        help_text="Controls on handle",
        related_name="settings_controls_and_indicators_controls_on_handle",
    )


class Power(auto_prefetch.Model):
    """Power."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the power was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the power was last updated")

    # Webhallen fields
    power_consumption = models.ManyToManyField(
        Component,
        help_text="Power consumption",
        related_name="power_power_consumption",
    )
    power_source = models.ManyToManyField(Component, help_text="Power source", related_name="power_power_source")
    voltage = models.ManyToManyField(Component, help_text="Voltage", related_name="power_voltage")
    battery_charge = models.ManyToManyField(Component, help_text="Battery charge", related_name="power_battery_charge")
    operation_time_without_mains = models.ManyToManyField(
        Component,
        help_text="Operation time without mains",
        related_name="power_operation_time_without_mains",
    )
    operation = models.ManyToManyField(Component, help_text="Operation", related_name="power_operation")
    energy_consumption_per_year = models.ManyToManyField(
        Component,
        help_text="Energy consumption per year",
        related_name="power_energy_consumption_per_year",
    )
    power_consumption_operating_mode = models.ManyToManyField(
        Component,
        help_text="Power consumption operating mode",
        related_name="power_power_consumption_operating_mode",
    )
    energy_class = models.ManyToManyField(Component, help_text="Energy class", related_name="power_energy_class")
    on_off_switch = models.ManyToManyField(Component, help_text="On/off switch", related_name="power_on_off_switch")
    power_consumption_hdr_on_mode = models.ManyToManyField(
        Component,
        help_text="Power consumption HDR on mode",
        related_name="power_power_consumption_hdr_on_mode",
    )
    energy_class_hdr = models.ManyToManyField(
        Component,
        help_text="Energy class HDR",
        related_name="power_energy_class_hdr",
    )
    energy_efficiency_ratio = models.ManyToManyField(
        Component,
        help_text="EER (Energy Efficiency Ratio)",
        related_name="power_energy_efficiency_ratio",
    )
    ampere_capacity = models.ManyToManyField(
        Component,
        help_text="https://en.wikipedia.org/wiki/Ampacity",
        related_name="power_ampere_capacity",
    )


class HeatingAndCooling(auto_prefetch.Model):
    """Heating and cooling."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the heating and cooling was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the heating and cooling was last updated")

    # Webhallen fields
    product_type = models.ManyToManyField(
        Component,
        help_text="Product type",
        related_name="heating_and_cooling_product_type",
    )
    model = models.ManyToManyField(Component, help_text="Model", related_name="heating_and_cooling_model")
    functions = models.ManyToManyField(Component, help_text="Functions", related_name="heating_and_cooling_functions")
    air_flow = models.ManyToManyField(Component, help_text="Air flow", related_name="heating_and_cooling_air_flow")
    container_capacity = models.ManyToManyField(
        Component,
        help_text="Container capacity",
        related_name="heating_and_cooling_container_capacity",
    )
    environment = models.ManyToManyField(
        Component,
        help_text="Environment",
        related_name="heating_and_cooling_environment",
    )
    air_flow_control = models.ManyToManyField(
        Component,
        help_text="Air flow control",
        related_name="heating_and_cooling_air_flow_control",
    )
    heating_capacity = models.ManyToManyField(
        Component,
        help_text="Heating capacity",
        related_name="heating_and_cooling_heating_capacity",
    )
    max_dehumidification_capacity = models.ManyToManyField(
        Component,
        help_text="Max dehumidification capacity",
        related_name="heating_and_cooling_max_dehumidification_capacity",
    )
    cooling_capacity = models.ManyToManyField(
        Component,
        help_text="Cooling capacity",
        related_name="heating_and_cooling_cooling_capacity",
    )
    cooling_capacity_btu_per_hour = models.ManyToManyField(
        Component,
        help_text="Cooling capacity (BTU per hour)",
        related_name="heating_and_cooling_cooling_capacity_btu_per_hour",
    )


class RAM(auto_prefetch.Model):
    """Random access memory (RAM)."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the RAM was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the RAM was last updated")

    # Webhallen fields
    data_integrity_check = models.ManyToManyField(
        Component,
        help_text="Data integrity check",
        related_name="ram_data_integrity_check",
    )
    upgrade_type = models.ManyToManyField(
        Component,
        help_text="Upgrade type",
        related_name="ram_upgrade_type",
    )
    type = models.ManyToManyField(
        Component,
        help_text="Type",
        related_name="ram_type",
    )
    memory_speed = models.ManyToManyField(
        Component,
        help_text="Memory speed",
        related_name="ram_memory_speed",
    )
    registered_or_buffered = models.ManyToManyField(
        Component,
        help_text="Registered or buffered",
        related_name="ram_registered_or_buffered",
    )
    ram_technology = models.ManyToManyField(
        Component,
        help_text="RAM technology",
        related_name="ram_ram_technology",
    )
    cas_latency = models.ManyToManyField(
        Component,
        help_text="CAS latency",
        related_name="ram_cas_latency",
    )
    adaptation_to_memory_specifications = models.ManyToManyField(
        Component,
        help_text="Adaptation to memory specifications",
        related_name="ram_adaptation_to_memory_specifications",
    )
    form_factor = models.ManyToManyField(
        Component,
        help_text="Form factor",
        related_name="ram_form_factor",
    )
    storage_capacity = models.ManyToManyField(
        Component,
        help_text="Storage capacity",
        related_name="ram_storage_capacity",
    )
    product_type = models.ManyToManyField(
        Component,
        help_text="Product type",
        related_name="ram_product_type",
    )
    memory_size = models.ManyToManyField(
        Component,
        help_text="Frame size",
        related_name="ram_memory_size",
    )
    empty_slots = models.ManyToManyField(
        Component,
        help_text="Empty slots",
        related_name="ram_empty_slots",
    )
    max_size_supported = models.ManyToManyField(
        Component,
        help_text="Max size supported",
        related_name="ram_max_size_supported",
    )
    internal_memory_ram = models.ManyToManyField(
        Component,
        help_text="Internal memory (RAM)",
        related_name="ram_internal_memory_ram",
    )
    number_of_slots = models.ManyToManyField(
        Component,
        help_text="Number of slots",
        related_name="ram_number_of_slots",
    )
    properties = models.ManyToManyField(
        Component,
        help_text="Properties",
        related_name="ram_properties",
    )
    low_profile = models.ManyToManyField(
        Component,
        help_text="Low profile",
        related_name="ram_low_profile",
    )


class AudioOutput(auto_prefetch.Model):
    """Audio output."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the audio output was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the audio output was last updated")

    # Webhallen fields
    form_factor = models.ManyToManyField(Component, help_text="Form factor", related_name="audio_output_form_factor")
    type = models.ManyToManyField(Component, help_text="Type", related_name="audio_output_type")
    interface_type = models.ManyToManyField(
        Component,
        help_text="Interface type",
        related_name="audio_output_interface_type",
    )
    audio_output_mode = models.ManyToManyField(
        Component,
        help_text="Audio output mode",
        related_name="audio_output_audio_output_mode",
    )
    connection_technology = models.ManyToManyField(
        Component,
        help_text="Connection technology",
        related_name="audio_output_connection_technology",
    )
    controls = models.ManyToManyField(Component, help_text="Controls", related_name="audio_output_controls")
    headphone_ear_parts_type = models.ManyToManyField(
        Component,
        help_text="Headphone ear parts type",
        related_name="audio_output_headphone_ear_parts_type",
    )
    headphone_cup_type = models.ManyToManyField(
        Component,
        help_text="Headphone cup type",
        related_name="audio_output_headphone_cup_type",
    )
    available_microphone = models.ManyToManyField(
        Component,
        help_text="Available microphone",
        related_name="audio_output_available_microphone",
    )
    interface_connector = models.ManyToManyField(
        Component,
        help_text="Interface connector",
        related_name="audio_output_interface_connector",
    )
    frequency_response = models.ManyToManyField(
        Component,
        help_text="Frequency response",
        related_name="audio_output_frequency_response",
    )
    impedance = models.ManyToManyField(Component, help_text="Impedance", related_name="audio_output_impedance")
    product_type = models.ManyToManyField(Component, help_text="Product type", related_name="audio_output_product_type")
    wireless_technology = models.ManyToManyField(
        Component,
        help_text="Wireless technology",
        related_name="audio_output_wireless_technology",
    )
    anc = models.ManyToManyField(Component, help_text="ANC", related_name="audio_output_anc")
    dac_resolution = models.ManyToManyField(
        Component,
        help_text="DAC resolution",
        related_name="audio_output_dac_resolution",
    )
    max_sampling_rate = models.ManyToManyField(
        Component,
        help_text="Max sampling rate",
        related_name="audio_output_max_sampling_rate",
    )
    signal_processor = models.ManyToManyField(
        Component,
        help_text="Signal processor",
        related_name="audio_output_signal_processor",
    )
    headphone_mount = models.ManyToManyField(
        Component,
        help_text="Headphone mount",
        related_name="audio_output_headphone_mount",
    )
    foldable = models.ManyToManyField(Component, help_text="Foldable", related_name="audio_output_foldable")
    sound_isolating = models.ManyToManyField(
        Component,
        help_text="Sound isolating",
        related_name="audio_output_sound_isolating",
    )
    nfc_near_field_communication = models.ManyToManyField(
        Component,
        help_text="NFC (Near Field Communication)",
        related_name="audio_output_nfc_near_field_communication",
    )
    style = models.ManyToManyField(Component, help_text="Style", related_name="audio_output_style")
    output_per_channel = models.ManyToManyField(
        Component,
        help_text="Output per channel",
        related_name="audio_output_output_per_channel",
    )


class HeatsinkAndFan(auto_prefetch.Model):
    """Heatsink and fan."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the heatsink and fan was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the heatsink and fan was last updated")

    # Webhallen fields
    fan_diameter = models.ManyToManyField(
        Component,
        help_text="Fan diameter",
        related_name="heatsink_and_fan_fan_diameter",
    )
    power_connector = models.ManyToManyField(
        Component,
        help_text="Power connector",
        related_name="heatsink_and_fan_power_connector",
    )
    compatible_with = models.ManyToManyField(
        Component,
        help_text="Compatible with",
        related_name="heatsink_and_fan_compatible_with",
    )
    cooler_material = models.ManyToManyField(
        Component,
        help_text="Cooler material",
        related_name="heatsink_and_fan_cooler_material",
    )
    radiator_size = models.ManyToManyField(
        Component,
        help_text="Radiator size",
        related_name="heatsink_and_fan_radiator_size",
    )


class Storage(auto_prefetch.Model):
    """Storage."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the storage was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the storage was last updated")

    # Webhallen fields
    model = models.ManyToManyField(Component, help_text="Model", related_name="storage_model")
    type = models.ManyToManyField(Component, help_text="Type", related_name="storage_type")
    interface = models.ManyToManyField(Component, help_text="Interface", related_name="storage_interface")
    device_type = models.ManyToManyField(Component, help_text="Device type", related_name="storage_device_type")
    product_type = models.ManyToManyField(Component, help_text="Product type", related_name="storage_product_type")
    iscsi_support = models.ManyToManyField(Component, help_text="iSCSI support", related_name="storage_iscsi_support")
    network_storage_type = models.ManyToManyField(
        Component,
        help_text="Network storage type",
        related_name="storage_network_storage_type",
    )
    total_storage_capacity = models.ManyToManyField(
        Component,
        help_text="Total storage capacity",
        related_name="storage_total_storage_capacity",
    )
    total_array_capacity = models.ManyToManyField(
        Component,
        help_text="Total array capacity",
        related_name="storage_total_array_capacity",
    )
    external_interface_for_disk_array = models.ManyToManyField(
        Component,
        help_text="External interface for disk array",
        related_name="storage_external_interface_for_disk_array",
    )
    external_interface_class_for_disk_array = models.ManyToManyField(
        Component,
        help_text="External interface class for disk array",
        related_name="storage_external_interface_class_for_disk_array",
    )


class PortableStorageSolution(auto_prefetch.Model):
    """Portable storage solution."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the portable storage solution was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the portable storage solution was last updated")

    # Webhallen fields
    type = models.ManyToManyField(Component, help_text="Type", related_name="portable_storage_solution_type")


class OpticalStorageSecondary(auto_prefetch.Model):
    """Optical storage secondary."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the optical storage secondary was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the optical storage secondary was last updated")

    # Webhallen fields
    type = models.ManyToManyField(Component, help_text="Type", related_name="optical_storage_secondary_type")


class OpticalStorage(auto_prefetch.Model):
    """Optical storage."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the optical storage was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the optical storage was last updated")

    # Webhallen fields
    write_speed = models.ManyToManyField(Component, help_text="Write speed", related_name="optical_storage_write_speed")
    read_speed = models.ManyToManyField(Component, help_text="Read speed", related_name="optical_storage_read_speed")
    rewrite_speed = models.ManyToManyField(
        Component,
        help_text="Rewrite speed",
        related_name="optical_storage_rewrite_speed",
    )
    type = models.ManyToManyField(Component, help_text="Type", related_name="optical_storage_type")
    buffer_size = models.ManyToManyField(Component, help_text="Buffer size", related_name="optical_storage_buffer_size")
    device_type = models.ManyToManyField(Component, help_text="Device type", related_name="optical_storage_device_type")


class MemoryModule(auto_prefetch.Model):
    """Memory module."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the memory module was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the memory module was last updated")

    # Webhallen fields
    quantity_in_kit = models.ManyToManyField(
        Component,
        help_text="Quantity in kit",
        related_name="memory_module_quantity_in_kit",
    )


class Antenna(auto_prefetch.Model):
    """Antenna."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the antenna was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the antenna was last updated")

    # Webhallen fields
    antenna_placement_mounting = models.ManyToManyField(
        Component,
        help_text="Antenna placement mounting",
        related_name="antenna_antenna_placement_mounting",
    )
    compatibility = models.ManyToManyField(
        Component,
        help_text="Compatibility",
        related_name="antenna_compatibility",
    )
    form_factor = models.ManyToManyField(
        Component,
        help_text="Form factor",
        related_name="antenna_form_factor",
    )
    frequency_range = models.ManyToManyField(
        Component,
        help_text="Frequency range",
        related_name="antenna_frequency_range",
    )
    type = models.ManyToManyField(
        Component,
        help_text="Type",
        related_name="antenna_type",
    )


class System(auto_prefetch.Model):
    """System."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the system was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the system was last updated")

    # Webhallen fields
    device_type = models.ManyToManyField(Component, help_text="Device type", related_name="system_device_type")
    docking_interface = models.ManyToManyField(
        Component,
        help_text="Docking interface",
        related_name="system_docking_interface",
    )
    video_interface = models.ManyToManyField(
        Component,
        help_text="Video interface",
        related_name="system_video_interface",
    )
    generation = models.ManyToManyField(Component, help_text="Generation", related_name="system_generation")
    hard_drive_capacity = models.ManyToManyField(
        Component,
        help_text="Hard drive capacity",
        related_name="system_hard_drive_capacity",
    )
    fingerprint_reader = models.ManyToManyField(
        Component,
        help_text="Fingerprint reader",
        related_name="system_fingerprint_reader",
    )
    platform = models.ManyToManyField(Component, help_text="Platform", related_name="system_platform")
    embedded_security = models.ManyToManyField(
        Component,
        help_text="Embedded security",
        related_name="system_embedded_security",
    )
    notebook_type = models.ManyToManyField(Component, help_text="Notebook type", related_name="system_notebook_type")
    handheld_type = models.ManyToManyField(Component, help_text="Handheld type", related_name="system_handheld_type")
    introduced = models.ManyToManyField(Component, help_text="Introduced", related_name="system_introduced")
    type = models.ManyToManyField(Component, help_text="Type", related_name="system_type")
    dockable = models.ManyToManyField(Component, help_text="Dockable", related_name="system_dockable")
    platform_technology = models.ManyToManyField(
        Component,
        help_text="Platform technology",
        related_name="system_platform_technology",
    )


class ControllerCard(auto_prefetch.Model):
    """Controller card."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the controller card was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the controller card was last updated")

    # Webhallen fields
    type = models.ManyToManyField(Component, help_text="Type", related_name="controller_card_type")
    form_factor = models.ManyToManyField(Component, help_text="Form factor", related_name="controller_card_form_factor")
    supported_devices = models.ManyToManyField(
        Component,
        help_text="Supported devices",
        related_name="controller_card_supported_devices",
    )
    max_number_of_devices = models.ManyToManyField(
        Component,
        help_text="Max number of devices",
        related_name="controller_card_max_number_of_devices",
    )
    power_source = models.ManyToManyField(
        Component,
        help_text="Power source",
        related_name="controller_card_power_source",
    )
    host_bus = models.ManyToManyField(Component, help_text="Host bus", related_name="controller_card_host_bus")
    interface = models.ManyToManyField(Component, help_text="Interface", related_name="controller_card_interface")
    number_of_channels = models.ManyToManyField(
        Component,
        help_text="Number of channels",
        related_name="controller_card_number_of_channels",
    )
    interface_type = models.ManyToManyField(
        Component,
        help_text="Interface type",
        related_name="controller_card_interface_type",
    )
    raid_level = models.ManyToManyField(Component, help_text="RAID level", related_name="controller_card_raid_level")


class PersonalHygiene(auto_prefetch.Model):
    """Personal hygiene."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the personal hygiene was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the personal hygiene was last updated")

    # Webhallen fields
    category = models.ManyToManyField(Component, help_text="Category", related_name="personal_hygiene_category")
    product_type = models.ManyToManyField(
        Component,
        help_text="Product type",
        related_name="personal_hygiene_product_type",
    )
    usage = models.ManyToManyField(Component, help_text="Usage", related_name="personal_hygiene_usage")
    number_of_speed_settings = models.ManyToManyField(
        Component,
        help_text="Number of speed settings",
        related_name="personal_hygiene_number_of_speed_settings",
    )
    vibrations_per_minute = models.ManyToManyField(
        Component,
        help_text="Vibrations per minute",
        related_name="personal_hygiene_vibrations_per_minute",
    )


class Warranty(auto_prefetch.Model):
    """Warranty."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the warranty was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the warranty was last updated")

    # Webhallen fields
    warranty = models.ManyToManyField(Component, help_text="Warranty", related_name="warranty_warranty")


class AccessoriesForDevices(auto_prefetch.Model):
    """Accessories for devices."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the accessories for devices was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the accessories for devices was last updated")

    # Webhallen fields
    type = models.ManyToManyField(Component, help_text="Type", related_name="accessories_for_devices_type")
    intended_for = models.ManyToManyField(
        Component,
        help_text="Intended for",
        related_name="accessories_for_devices_intended_for",
    )
    capacity = models.ManyToManyField(Component, help_text="Capacity", related_name="accessories_for_devices_capacity")


class VideoOutput(auto_prefetch.Model):
    """Video output."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the video output was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the video output was last updated")

    # Webhallen fields
    maximum_external_resolution = models.ManyToManyField(
        Component,
        help_text="Maximum external resolution",
        related_name="video_output_maximum_external_resolution",
    )
    type = models.ManyToManyField(Component, help_text="Type")
    supported_video_signals = models.ManyToManyField(
        Component,
        help_text="Supported video signals",
        related_name="video_output_supported_video_signals",
    )
    type_of_interface = models.ManyToManyField(
        Component,
        help_text="Type of interface",
        related_name="video_output_type_of_interface",
    )
    tv_connection = models.ManyToManyField(
        Component,
        help_text="TV connection",
        related_name="video_output_tv_connection",
    )
    hdr_capacity = models.ManyToManyField(
        Component,
        help_text="HDR capacity",
        related_name="video_output_hdr_capacity",
    )
    clock_speed = models.ManyToManyField(
        Component,
        help_text="Clock speed",
        related_name="video_output_clock_speed",
    )
    high_clock_speed = models.ManyToManyField(
        Component,
        help_text="High clock speed",
        related_name="video_output_high_clock_speed",
    )
    low = models.ManyToManyField(Component, help_text="Low", related_name="video_output_low")
    chip_manufacturer = models.ManyToManyField(
        Component,
        help_text="Chip manufacturer",
        related_name="video_output_chip_manufacturer",
    )
    graphics_card = models.ManyToManyField(
        Component,
        help_text="Graphics card",
        related_name="video_output_graphics_card",
    )
    max_number_of_supported_displays = models.ManyToManyField(
        Component,
        help_text="Max number of supported displays",
        related_name="video_output_max_number_of_supported_displays",
    )
    dedicated_graphics_card = models.ManyToManyField(
        Component,
        help_text="Dedicated graphics card",
        related_name="video_output_dedicated_graphics_card",
    )
    graphics_processor_series = models.ManyToManyField(
        Component,
        help_text="Graphics processor series",
        related_name="video_output_graphics_processor_series",
    )
    vr_ready = models.ManyToManyField(Component, help_text="VR ready", related_name="video_output_vr_ready")
    hdcp_compatible = models.ManyToManyField(
        Component,
        help_text="HDCP compatible",
        related_name="video_output_hdcp_compatible",
    )


class SmallDevices(auto_prefetch.Model):
    """Small devices."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the small devices was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the small devices was last updated")

    # Webhallen fields
    product_type = models.ManyToManyField(
        Component,
        help_text="Product type",
        related_name="small_devices_product_type",
    )
    capacity = models.ManyToManyField(Component, help_text="Capacity", related_name="small_devices_capacity")
    variable_temperature = models.ManyToManyField(
        Component,
        help_text="Variable temperature",
        related_name="small_devices_variable_temperature",
    )
    functions_and_settings = models.ManyToManyField(
        Component,
        help_text="Functions and settings",
        related_name="small_devices_functions_and_settings",
    )
    max_speed = models.ManyToManyField(Component, help_text="Max speed", related_name="small_devices_max_speed")
    bowl_material = models.ManyToManyField(
        Component,
        help_text="Bowl material",
        related_name="small_devices_bowl_material",
    )
    included_blades_and_additives = models.ManyToManyField(
        Component,
        help_text="Included blades and additives",
        related_name="small_devices_included_blades_and_additives",
    )
    automatic_shutdown = models.ManyToManyField(
        Component,
        help_text="Automatic shutdown",
        related_name="small_devices_automatic_shutdown",
    )
    water_level_indicator = models.ManyToManyField(
        Component,
        help_text="Water level indicator",
        related_name="small_devices_water_level_indicator",
    )
    temperature_settings = models.ManyToManyField(
        Component,
        help_text="Temperature settings",
        related_name="small_devices_temperature_settings",
    )
    mass_container_capacity = models.ManyToManyField(
        Component,
        help_text="Mass container capacity",
        related_name="small_devices_mass_container_capacity",
    )
    multi_plate = models.ManyToManyField(Component, help_text="Multi-plate", related_name="small_devices_multi_plate")
    food_capacity = models.ManyToManyField(
        Component,
        help_text="Food capacity",
        related_name="small_devices_food_capacity",
    )
    number_of_programs = models.ManyToManyField(
        Component,
        help_text="Number of programs",
        related_name="small_devices_number_of_programs",
    )
    number_of_people = models.ManyToManyField(
        Component,
        help_text="Number of people",
        related_name="small_devices_number_of_people",
    )


class Camera(auto_prefetch.Model):
    """Camera."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the camera was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the camera was last updated")

    # Webhallen fields
    image_sensor_type = models.ManyToManyField(
        Component,
        help_text="Image sensor type",
        related_name="camera_image_sensor_type",
    )
    optical_sensor_resolution = models.ManyToManyField(
        Component,
        help_text="Optical sensor resolution",
        related_name="camera_optical_sensor_resolution",
    )
    type = models.ManyToManyField(
        Component,
        help_text="Type",
        related_name="camera_type",
    )
    shooting_methods = models.ManyToManyField(
        Component,
        help_text="Shooting methods",
        related_name="camera_shooting_methods",
    )


class LightSource(auto_prefetch.Model):
    """Light source."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the light source was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the light source was last updated")

    # Webhallen fields
    type_of_light_source = models.ManyToManyField(
        Component,
        help_text="Type of light source",
        related_name="light_source_type_of_light_source",
    )
    luminous_flux = models.ManyToManyField(
        Component,
        help_text="Luminous flux",
        related_name="light_source_luminous_flux",
    )
    lifespan = models.ManyToManyField(
        Component,
        help_text="Lifespan",
        related_name="light_source_lifespan",
    )
    color_temperature = models.ManyToManyField(
        Component,
        help_text="Color temperature",
        related_name="light_source_color_temperature",
    )
    illumination_color = models.ManyToManyField(
        Component,
        help_text="Illumination color",
        related_name="light_source_illumination_color",
    )
    wattage = models.ManyToManyField(
        Component,
        help_text="Wattage",
        related_name="light_source_wattage",
    )
    energy_efficiency_class = models.ManyToManyField(
        Component,
        help_text="Energy efficiency class",
        related_name="light_source_energy_efficiency_class",
    )
    watt_equivalence = models.ManyToManyField(
        Component,
        help_text="Watt equivalence",
        related_name="light_source_watt_equivalence",
    )
    beam_angle = models.ManyToManyField(
        Component,
        help_text="Beam angle",
        related_name="light_source_beam_angle",
    )
    socket_type = models.ManyToManyField(
        Component,
        help_text="Socket type",
        related_name="light_source_socket_type",
    )
    color_rendering_index = models.ManyToManyField(
        Component,
        help_text="Color rendering index",
        related_name="light_source_color_rendering_index",
    )
    mercury_content = models.ManyToManyField(
        Component,
        help_text="Mercury content",
        related_name="light_source_mercury_content",
    )
    dimmable = models.ManyToManyField(
        Component,
        help_text="Dimmable",
        related_name="light_source_dimmable",
    )
    shape = models.ManyToManyField(
        Component,
        help_text="Shape",
        related_name="light_source_shape",
    )
    power_factor = models.ManyToManyField(
        Component,
        help_text="Power factor",
        related_name="light_source_power_factor",
    )
    lamp_current = models.ManyToManyField(
        Component,
        help_text="Lamp current",
        related_name="light_source_lamp_current",
    )
    start_time = models.ManyToManyField(
        Component,
        help_text="Start time",
        related_name="light_source_start_time",
    )
    warm_up_time = models.ManyToManyField(
        Component,
        help_text="Warm-up time",
        related_name="light_source_warm_up_time",
    )
    luminous_efficiency = models.ManyToManyField(
        Component,
        help_text="Luminous efficiency",
        related_name="light_source_luminous_efficiency",
    )


class Software(auto_prefetch.Model):
    """Software."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the software was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the software was last updated")

    # Webhallen fields
    number_of_licenses = models.ManyToManyField(
        Component,
        help_text="Number of licenses",
        related_name="software_number_of_licenses",
    )
    license_validity_period = models.ManyToManyField(
        Component,
        help_text="License validity period",
        related_name="software_license_validity_period",
    )
    type_of_license = models.ManyToManyField(
        Component,
        help_text="Type of license",
        related_name="software_type_of_license",
    )
    license_category = models.ManyToManyField(
        Component,
        help_text="License category",
        related_name="software_license_category",
    )
    version = models.ManyToManyField(
        Component,
        help_text="Version",
        related_name="software_version",
    )
    type = models.ManyToManyField(
        Component,
        help_text="Type",
        related_name="software_type",
    )


class CEAccessories(auto_prefetch.Model):
    """CE marking."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the CE marking was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the CE marking was last updated")

    # Webhallen fields
    product_type = models.ManyToManyField(
        Component,
        help_text="Product type",
        related_name="ce_accessories_product_type",
    )
    intended_for = models.ManyToManyField(
        Component,
        help_text="Intended for",
        related_name="ce_accessories_intended_for",
    )
    suitable_for_installation = models.ManyToManyField(
        Component,
        help_text="Suitable for installation",
        related_name="ce_accessories_suitable_for_installation",
    )


class Game(auto_prefetch.Model):
    """Game."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the game was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the game was last updated")

    # Webhallen fields
    release_month = models.ManyToManyField(Component, help_text="Release month", related_name="game_release_month")
    genre = models.ManyToManyField(Component, help_text="Genre", related_name="game_genre")
    esrb_rating = models.ManyToManyField(Component, help_text="ESRB rating", related_name="game_esrb_rating")
    pegi_content_description = models.ManyToManyField(
        Component,
        help_text="PEGI content description",
        related_name="game_pegi_content_description",
    )
    usk_age_rating = models.ManyToManyField(Component, help_text="USK age rating", related_name="game_usk_age_rating")
    pegi_classification = models.ManyToManyField(
        Component,
        help_text="PEGI classification",
        related_name="game_pegi_classification",
    )
    australian_state_evaluation = models.ManyToManyField(
        Component,
        help_text="Australian state evaluation",
        related_name="game_australian_state_evaluation",
    )
    platform = models.ManyToManyField(Component, help_text="Platform", related_name="game_platform")
    release_year = models.ManyToManyField(Component, help_text="Release year", related_name="game_release_year")
    release_day = models.ManyToManyField(Component, help_text="Release day", related_name="game_release_day")
    multiplayer = models.ManyToManyField(Component, help_text="Multiplayer", related_name="game_multiplayer")
    max_number_of_players = models.ManyToManyField(
        Component,
        help_text="Max number of players",
        related_name="game_max_number_of_players",
    )
    online_play = models.ManyToManyField(Component, help_text="Online play", related_name="game_online_play")


class ToastersAndGrills(auto_prefetch.Model):
    """Toasters and grills."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the toasters and grills was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the toasters and grills was last updated")

    # Webhallen fields
    product_type = models.ManyToManyField(
        Component,
        help_text="Product type",
        related_name="toasters_and_grills_product_type",
    )
    number_of_slices = models.ManyToManyField(
        Component,
        help_text="Number of slices",
        related_name="toasters_and_grills_number_of_slices",
    )
    number_of_outlets = models.ManyToManyField(
        Component,
        help_text="Number of outlets",
        related_name="toasters_and_grills_number_of_outlets",
    )


class Scale(auto_prefetch.Model):
    """Scale."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the scale was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the scale was last updated")

    # Webhallen fields
    kitchen_scale_type = models.ManyToManyField(
        Component,
        help_text="Kitchen scale type",
        related_name="scale_kitchen_scale_type",
    )
    max_weight = models.ManyToManyField(Component, help_text="Max weight", related_name="scale_max_weight")
    bathroom_scale_type = models.ManyToManyField(
        Component,
        help_text="Bathroom scale type",
        related_name="scale_bathroom_scale_type",
    )
    measurement_functions = models.ManyToManyField(
        Component,
        help_text="Measurement functions",
        related_name="scale_measurement_functions",
    )


class HDD(auto_prefetch.Model):
    """Hard disk drive (HDD)."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the HDD was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the HDD was last updated")

    # Webhallen fields
    hard_disk_type = models.ManyToManyField(Component, help_text="Hard disk type", related_name="hdd_hard_disk_type")
    interface = models.ManyToManyField(Component, help_text="Interface", related_name="hdd_interface")
    external_device_type = models.ManyToManyField(
        Component,
        help_text="External device type",
        related_name="hdd_external_device_type",
    )
    hard_disk_space = models.ManyToManyField(Component, help_text="Hard disk space", related_name="hdd_hard_disk_space")
    spindle_speed = models.ManyToManyField(Component, help_text="Spindle speed", related_name="hdd_spindle_speed")
    unrecoverable_error = models.ManyToManyField(
        Component,
        help_text="Unrecoverable error",
        related_name="hdd_unrecoverable_error",
    )
    data_transfer_rate = models.ManyToManyField(
        Component,
        help_text="Data transfer rate",
        related_name="hdd_data_transfer_rate",
    )
    internal_data_frequency = models.ManyToManyField(
        Component,
        help_text="Internal data frequency",
        related_name="hdd_internal_data_frequency",
    )
    average_seek_time = models.ManyToManyField(
        Component,
        help_text="Average seek time",
        related_name="hdd_average_seek_time",
    )
    form_factor = models.ManyToManyField(Component, help_text="Form factor", related_name="hdd_form_factor")
    form_factor_short = models.ManyToManyField(
        Component,
        help_text="Form factor short",
        related_name="hdd_form_factor_short",
    )
    form_factor_metric = models.ManyToManyField(
        Component,
        help_text="Form factor metric",
        related_name="hdd_form_factor_metric",
    )
    form_factor_short_metric = models.ManyToManyField(
        Component,
        help_text="Form factor short metric",
        related_name="hdd_form_factor_short_metric",
    )
    buffer_size = models.ManyToManyField(Component, help_text="Buffer size", related_name="hdd_buffer_size")
    internal_data_write_speed = models.ManyToManyField(
        Component,
        help_text="Internal data write speed",
        related_name="hdd_internal_data_write_speed",
    )
    nand_flash_memory_type = models.ManyToManyField(
        Component,
        help_text="NAND flash memory type",
        related_name="hdd_nand_flash_memory_type",
    )
    _24_7_operation = models.ManyToManyField(Component, help_text="24/7 operation", related_name="hdd_24_7_operation")
    _4_kb_random_read = models.ManyToManyField(
        Component,
        help_text="The 4 KB random read",
        related_name="hdd_4_kb_random_read",
    )
    type = models.ManyToManyField(Component, help_text="Type", related_name="hdd_type")
    ssd_form_factor = models.ManyToManyField(Component, help_text="SSD form factor", related_name="hdd_ssd_form_factor")
    hard_disk_features = models.ManyToManyField(
        Component,
        help_text="Hard disk features",
        related_name="hdd_hard_disk_features",
    )
    type_of_interface = models.ManyToManyField(
        Component,
        help_text="Type of interface",
        related_name="hdd_type_of_interface",
    )
    interface_class = models.ManyToManyField(Component, help_text="Interface class", related_name="hdd_interface_class")
    ssd_capacity = models.ManyToManyField(Component, help_text="SSD capacity", related_name="hdd_ssd_capacity")


class ExternalHardDrive(auto_prefetch.Model):
    """External hard drive."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the external hard drive was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the external hard drive was last updated")

    # Webhallen fields
    power_source = models.ManyToManyField(
        Component,
        help_text="Power source",
        related_name="external_hard_drive_power_source",
    )
    max_data_transfer_rate = models.ManyToManyField(
        Component,
        help_text="Max data transfer rate",
        related_name="external_hard_drive_max_data_transfer_rate",
    )
    usb_c_port = models.ManyToManyField(
        Component,
        help_text="USB-C port",
        related_name="external_hard_drive_usb_c_port",
    )


class Modem(auto_prefetch.Model):
    """Modem."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the modem was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the modem was last updated")

    # Webhallen fields
    connection_technology = models.ManyToManyField(
        Component,
        help_text="Connection technology",
        related_name="modem_connection_technology",
    )
    form_factor = models.ManyToManyField(
        Component,
        help_text="Form factor",
        related_name="modem_form_factor",
    )
    type = models.ManyToManyField(
        Component,
        help_text="Type",
        related_name="modem_type",
    )
    max_transfer_rate = models.ManyToManyField(
        Component,
        help_text="Max transfer rate",
        related_name="modem_max_transfer_rate",
    )
    band = models.ManyToManyField(
        Component,
        help_text="Band",
        related_name="modem_band",
    )
    broadband_access_for_mobile_phone = models.ManyToManyField(
        Component,
        help_text="Broadband access for mobile phone",
        related_name="modem_broadband_access_for_mobile_phone",
    )


class MobileBroadband(auto_prefetch.Model):
    """Mobile broadband."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the mobile broadband was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the mobile broadband was last updated")

    # Webhallen fields
    cellular_protocol = models.ManyToManyField(
        Component,
        help_text="Cellular protocol",
        related_name="mobile_broadband_cellular_protocol",
    )
    generation = models.ManyToManyField(
        Component,
        help_text="Generation",
        related_name="mobile_broadband_generation",
    )


class AudioInput(auto_prefetch.Model):
    """Audio input."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the audio input was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the audio input was last updated")

    # Webhallen fields
    microphone_type = models.ManyToManyField(
        Component,
        help_text="Microphone type",
        related_name="audio_input_microphone_type",
    )
    sensitivity = models.ManyToManyField(
        Component,
        help_text="Sensitivity",
        related_name="audio_input_sensitivity",
    )
    type = models.ManyToManyField(
        Component,
        help_text="Type",
        related_name="audio_input_type",
    )
    operational_mode_for_microphone = models.ManyToManyField(
        Component,
        help_text="Operational mode for microphone",
        related_name="audio_input_operational_mode_for_microphone",
    )
    connection_technology = models.ManyToManyField(
        Component,
        help_text="Connection technology",
        related_name="audio_input_connection_technology",
    )


class MemoryAdapter(auto_prefetch.Model):
    """Memory adapter."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the memory adapter was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the memory adapter was last updated")

    # Webhallen fields
    model = models.ManyToManyField(Component, help_text="Model", related_name="memory_adapter_model")
    interface = models.ManyToManyField(Component, help_text="Interface", related_name="memory_adapter_interface")
    device_type = models.ManyToManyField(Component, help_text="Device type", related_name="memory_adapter_device_type")
    support_for_memory_cards = models.ManyToManyField(
        Component,
        help_text="Support for memory cards",
        related_name="memory_adapter_support_for_memory_cards",
    )


class InternetOfThings(auto_prefetch.Model):
    """Internet of things."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the internet of things was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the internet of things was last updated")

    # Webhallen fields
    communication_technology = models.ManyToManyField(
        Component,
        help_text="Communication technology",
        related_name="internet_of_things_communication_technology",
    )
    platform = models.ManyToManyField(
        Component,
        help_text="Platform",
        related_name="internet_of_things_platform",
    )
    compatible_with_internet_of_things = models.ManyToManyField(
        Component,
        help_text="Compatible with Internet of Things",
        related_name="internet_of_things_compatible_with_internet_of_things",
    )
    intelligent_assistant = models.ManyToManyField(
        Component,
        help_text="Intelligent assistant",
        related_name="internet_of_things_intelligent_assistant",
    )
    voice_controlled = models.ManyToManyField(
        Component,
        help_text="Voice controlled",
        related_name="internet_of_things_voice_controlled",
    )


class Cleaning(auto_prefetch.Model):
    """Cleaning."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the cleaning was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the cleaning was last updated")

    # Webhallen fields
    bag_capacity = models.ManyToManyField(Component, help_text="Bag capacity", related_name="cleaning_bag_capacity")
    product_type = models.ManyToManyField(Component, help_text="Product type", related_name="cleaning_product_type")
    container_type = models.ManyToManyField(
        Component,
        help_text="Container type",
        related_name="cleaning_container_type",
    )
    cleaning_agent_type = models.ManyToManyField(
        Component,
        help_text="Cleaning agent type",
        related_name="cleaning_cleaning_agent_type",
    )
    cleaning_method = models.ManyToManyField(
        Component,
        help_text="Cleaning method",
        related_name="cleaning_cleaning_method",
    )
    tank_capacity = models.ManyToManyField(Component, help_text="Tank capacity", related_name="cleaning_tank_capacity")
    dust_emission_class = models.ManyToManyField(
        Component,
        help_text="Dust emission class",
        related_name="cleaning_dust_emission_class",
    )
    material_cleaning_performance_class = models.ManyToManyField(
        Component,
        help_text="Material cleaning performance class",
        related_name="cleaning_material_cleaning_performance_class",
    )
    cleaning_performance_class_for_hard_floor = models.ManyToManyField(
        Component,
        help_text="Cleaning performance class for hard floor",
        related_name="cleaning_cleaning_performance_class_for_hard_floor",
    )
    filter_type = models.ManyToManyField(Component, help_text="Filter type", related_name="cleaning_filter_type")
    area_of_use = models.ManyToManyField(Component, help_text="Area of use", related_name="cleaning_area_of_use")
    maximum_motor_power = models.ManyToManyField(
        Component,
        help_text="Maximum motor power",
        related_name="cleaning_maximum_motor_power",
    )
    max_suction_power_air_watts = models.ManyToManyField(
        Component,
        help_text="Max suction power (air watts)",
        related_name="cleaning_max_suction_power_air_watts",
    )


class FlashMemory(auto_prefetch.Model):
    """Flash memory."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the flash memory was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the flash memory was last updated")

    # Webhallen fields
    read_speed = models.ManyToManyField(Component, help_text="Read speed", related_name="flash_memory_read_speed")
    form_factor = models.ManyToManyField(Component, help_text="Form factor", related_name="flash_memory_form_factor")
    product_type = models.ManyToManyField(Component, help_text="Product type", related_name="flash_memory_product_type")
    storage_capacity = models.ManyToManyField(
        Component,
        help_text="Storage capacity",
        related_name="flash_memory_storage_capacity",
    )
    storage_speed = models.ManyToManyField(
        Component,
        help_text="Storage speed",
        related_name="flash_memory_storage_speed",
    )
    installed_size = models.ManyToManyField(
        Component,
        help_text="Installed size",
        related_name="flash_memory_installed_size",
    )
    interface_type = models.ManyToManyField(
        Component,
        help_text="Interface type",
        related_name="flash_memory_interface_type",
    )
    internal_memory_capacity = models.ManyToManyField(
        Component,
        help_text="Internal memory capacity",
        related_name="flash_memory_internal_memory_capacity",
    )
    included_memory_adapter = models.ManyToManyField(
        Component,
        help_text="Included memory adapter",
        related_name="flash_memory_included_memory_adapter",
    )
    speed_class = models.ManyToManyField(Component, help_text="Speed class", related_name="flash_memory_speed_class")
    supported_memory_cards = models.ManyToManyField(
        Component,
        help_text="Supported memory cards",
        related_name="flash_memory_supported_memory_cards",
    )
    technology = models.ManyToManyField(Component, help_text="Technology", related_name="flash_memory_technology")
    user_memory = models.ManyToManyField(Component, help_text="User memory", related_name="flash_memory_user_memory")
    max_size_supported = models.ManyToManyField(
        Component,
        help_text="Max size supported",
        related_name="flash_memory_max_size_supported",
    )
    supported_flash_memory_cards = models.ManyToManyField(
        Component,
        help_text="Supported flash memory cards",
        related_name="flash_memory_supported_flash_memory_cards",
    )


class RadioSystem(auto_prefetch.Model):
    """Radio system."""

    # Django fields
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the radio system was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the radio system was last updated")

    # Webhallen fields
    receiver_band = models.ManyToManyField(
        Component,
        help_text="Receiver band",
        related_name="radio_system_receiver_band",
    )
    receiver_type = models.ManyToManyField(
        Component,
        help_text="Receiver type",
        related_name="radio_system_receiver_type",
    )
    number_of_presets = models.ManyToManyField(
        Component,
        help_text="Number of presets",
        related_name="radio_system_number_of_presets",
    )


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
    consumables = models.ManyToManyField(Consumables, help_text="Consumables", related_name="data_consumables")
    battery = models.ManyToManyField(Battery, help_text="Battery", related_name="data_battery")
    av_components = models.ManyToManyField(AVComponent, help_text="AV components", related_name="data_av_components")
    remote_control = models.ManyToManyField(
        RemoteControl,
        help_text="Remote control",
        related_name="data_remote_control",
    )
    video_input = models.ManyToManyField(VideoInput, help_text="Video input", related_name="data_video_input")
    system_requirements = models.ManyToManyField(
        SystemRequirements,
        help_text="System requirements",
        related_name="data_system_requirements",
    )
    network = models.ManyToManyField(Network, help_text="Network", related_name="data_network")
    speaker_system = models.ManyToManyField(
        SpeakerSystem,
        help_text="Speaker system",
        related_name="data_speaker_system",
    )
    sound_system = models.ManyToManyField(SoundSystem, help_text="Sound system", related_name="data_sound_system")
    power_supply = models.ManyToManyField(PowerSupply, help_text="Power supply", related_name="data_power_supply")
    settings_controls_and_indicators = models.ManyToManyField(
        SettingsControlsAndIndicators,
        help_text="Settings, controls and indicators",
        related_name="data_settings_controls_and_indicators",
    )
    power = models.ManyToManyField(Power, help_text="Power", related_name="data_power")
    heating_and_cooling = models.ManyToManyField(
        HeatingAndCooling,
        help_text="Heating and cooling",
        related_name="data_heating_and_cooling",
    )
    ram = models.ManyToManyField(RAM, help_text="RAM", related_name="data_ram")
    audio_output = models.ManyToManyField(AudioOutput, help_text="Audio output", related_name="data_audio_output")
    heatsink_and_fan = models.ManyToManyField(
        HeatsinkAndFan,
        help_text="Heatsink and fan",
        related_name="data_heatsink_and_fan",
    )
    storage = models.ManyToManyField(Storage, help_text="Storage", related_name="data_storage")
    optical_storage_secondary = models.ManyToManyField(
        OpticalStorageSecondary,
        help_text="Optical storage secondary",
        related_name="data_optical_storage_secondary",
    )
    portable_storage_solution = models.ManyToManyField(
        PortableStorageSolution,
        help_text="Portable storage solution",
        related_name="data_portable_storage_solution",
    )
    optical_storage = models.ManyToManyField(
        OpticalStorage,
        help_text="Optical storage",
        related_name="data_optical_storage",
    )
    memory_module = models.ManyToManyField(MemoryModule, help_text="Memory module", related_name="data_memory_module")
    antenna = models.ManyToManyField(Antenna, help_text="Antenna", related_name="data_antenna")
    system = models.ManyToManyField(System, help_text="System", related_name="data_system")
    controller_card = models.ManyToManyField(
        ControllerCard,
        help_text="Controller card",
        related_name="data_controller_card",
    )
    personal_hygiene = models.ManyToManyField(
        PersonalHygiene,
        help_text="Personal hygiene",
        related_name="data_personal_hygiene",
    )
    warranty = models.ManyToManyField(Warranty, help_text="Warranty", related_name="data_warranty")
    accessories_for_devices = models.ManyToManyField(
        AccessoriesForDevices,
        help_text="Accessories for devices",
        related_name="data_accessories_for_devices",
    )
    video_output = models.ManyToManyField(VideoOutput, help_text="Video output", related_name="data_video_output")
    small_devices = models.ManyToManyField(SmallDevices, help_text="Small devices", related_name="data_small_devices")
    camera = models.ManyToManyField(Camera, help_text="Camera", related_name="data_camera")
    light_source = models.ManyToManyField(LightSource, help_text="Light sources", related_name="data_light_source")
    software = models.ManyToManyField(Software, help_text="Software", related_name="data_software")
    ce_accessories = models.ManyToManyField(
        CEAccessories,
        help_text="CE accessories",
        related_name="data_ce_accessories",
    )
    game = models.ManyToManyField(Game, help_text="Game", related_name="data_game")
    toasters_and_grills = models.ManyToManyField(
        ToastersAndGrills,
        help_text="Toasters and grills",
        related_name="data_toasters_and_grills",
    )
    scale = models.ManyToManyField(Scale, help_text="Scale", related_name="data_scale")
    hard_drive = models.ManyToManyField(HDD, help_text="Harddisk", related_name="data_hard_drive")
    external_hard_drive = models.ManyToManyField(
        ExternalHardDrive,
        help_text="External hard drive",
        related_name="data_external_hard_drive",
    )
    modem = models.ManyToManyField(Modem, help_text="Modem", related_name="data_modem")
    mobile_broadband = models.ManyToManyField(
        MobileBroadband,
        help_text="Mobile broadband",
        related_name="data_mobile_broadband",
    )
    audio_input = models.ManyToManyField(AudioInput, help_text="Audio input", related_name="data_audio_input")
    memory_adapter = models.ManyToManyField(
        MemoryAdapter,
        help_text="Memory adapter",
        related_name="data_memory_adapter",
    )
    internet_of_things = models.ManyToManyField(
        InternetOfThings,
        help_text="Internet of things",
        related_name="data_internet_of_things",
    )
    cleaning = models.ManyToManyField(Cleaning, help_text="Cleaning", related_name="data_cleaning")
    flash_memory = models.ManyToManyField(FlashMemory, help_text="Flash memory", related_name="data_flash_memory")
    radio_system = models.ManyToManyField(RadioSystem, help_text="Radio system", related_name="data_radio_system")


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
    prices = models.ManyToManyField(Prices, help_text="Prices")


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
    status_codes = models.ManyToManyField(StatusCode, help_text="Status codes")
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
    excluded_shipping_methods = models.ManyToManyField(ExcludeShippingMethod, help_text="Excluded shipping methods")
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

    # ManyToMany fields
    categories = models.ManyToManyField(Categories, help_text="Categories", related_name="product_categories")
    eans = models.ManyToManyField(EAN, help_text="EANs", related_name="product_eans")
    images = models.ManyToManyField(Image, help_text="Images", related_name="product_images")
    insurance = models.ManyToManyField(Insurance, help_text="Insurance", related_name="product_insurance")
    part_numbers = models.ManyToManyField(PartNumber, help_text="Part numbers", related_name="product_part_numbers")
    possible_delivery_methods = models.ManyToManyField(
        PossibleDeliveryMethod,
        help_text="Possible delivery methods",
        related_name="product_possible_delivery_methods",
    )
    resurs_part_payment_price = models.ManyToManyField(
        ResursPartPaymentPrice,
        help_text="Resurs part payment price",
        related_name="product_resurs_part_payment_price",
    )
    review_highlight = models.ManyToManyField(
        ReviewHighlight,
        help_text="Review highlights",
        related_name="product_review_highlight",
    )
    status_codes = models.ManyToManyField(StatusCode, help_text="Status codes", related_name="product_status_codes")
    variants = models.ManyToManyField(Variants, help_text="Variants", related_name="product_variants")

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
