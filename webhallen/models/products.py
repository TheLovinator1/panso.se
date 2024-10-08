from __future__ import annotations

import logging

import auto_prefetch
from django.contrib.postgres.fields import ArrayField
from django.db import models

logger: logging.Logger = logging.getLogger(__name__)

# TODO(TheLovinator): All docstrings are placeholders and need to be updated  # noqa: TD003


class CanonicalVariant(auto_prefetch.Model):
    """Canonical variant of a product."""

    id = models.PositiveBigIntegerField(primary_key=True, help_text="Canonical variant ID")
    name = models.TextField(help_text="Variant name")

    def __str__(self) -> str:
        return f"Canonical variant - {self.name}"


class AverageRating(auto_prefetch.Model):
    """Average rating of a product."""

    rating = models.FloatField(help_text="Rating")
    rating_type = models.TextField(help_text="Rating type")

    def __str__(self) -> str:
        return f"Average rating - {self.rating} ({self.rating_type})"


class Categories(auto_prefetch.Model):
    """Categories of a product."""

    id = models.PositiveBigIntegerField(primary_key=True, help_text="Category ID")
    fyndware_description = models.TextField(help_text="Fyndware description")
    meta_title = models.TextField(help_text="Meta title")
    seo_name = models.TextField(help_text="SEO name")
    active = models.BooleanField(help_text="Is active")
    order = models.PositiveBigIntegerField(help_text="Order")
    icon = models.TextField(help_text="Icon")
    name = models.TextField(help_text="Name")


class VariantProperties(auto_prefetch.Model):
    """Properties of a variant."""

    color = models.TextField(help_text="Color")  # Färg
    storage = models.TextField(help_text="Storage")  # lagring
    connections = models.TextField(help_text="Connections")  # anslutning


class VariantGroups(auto_prefetch.Model):
    """Groups of variants."""

    name = models.TextField(help_text="Name")
    type = models.TextField(help_text="Type")
    values = ArrayField(models.TextField(), help_text="Values")


class Variants(auto_prefetch.Model):
    """Variants of a product."""

    canonical_variant = models.ForeignKey(CanonicalVariant, on_delete=models.CASCADE, help_text="Canonical variant")
    list = models.ForeignKey("Product", on_delete=models.CASCADE, help_text="List")
    group = models.PositiveBigIntegerField(help_text="Group")
    variant_groups = models.ManyToManyField(VariantGroups, help_text="Variant groups")


class Order(auto_prefetch.Model):
    """Order details for each stock item."""

    store = models.TextField(help_text="Store ID")  # CL, 27, 16, 5 or 2.
    amount = models.IntegerField(help_text="Amount of stock change (negative for reduction)")
    days_since = models.PositiveIntegerField(help_text="Days since the order was placed")
    status = models.IntegerField(null=True, blank=True, help_text="Order status (only for CL orders)")
    ordered = models.PositiveIntegerField(null=True, blank=True, help_text="Ordered quantity (only for CL orders)")
    confirmed = models.BooleanField(default=False, help_text="Order confirmation status (only for CL orders)")
    delivery_time = models.DateField(null=True, blank=True, help_text="Expected delivery date (only for CL orders)")

    class Meta(auto_prefetch.Model.Meta):
        verbose_name: str = "Order"
        verbose_name_plural: str = "Orders"

    def __str__(self) -> str:
        return f"Order - {self.store}, Amount: {self.amount}"


class Stock(auto_prefetch.Model):
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
    web = models.PositiveBigIntegerField(help_text="Stock in web store")
    supplier = models.PositiveBigIntegerField(help_text="Stock from supplier")
    display_cap = models.PositiveBigIntegerField(help_text="Display cap")
    is_sent_from_store = models.BooleanField(help_text="Is sent from store")
    download = models.PositiveBigIntegerField(help_text="Download amount")

    orders = models.ManyToManyField(Order, help_text="Orders for this stock", related_name="stock")

    class Meta(auto_prefetch.Model.Meta):
        verbose_name: str = "Stock"
        verbose_name_plural: str = "Stock"

    def __str__(self) -> str:
        return f"Stock - {self.web} in web store"


class Price(auto_prefetch.Model):
    """The price of a product at Webhallen."""

    price = models.TextField(blank=True, help_text="Price of the product")
    currency = models.TextField(blank=True, help_text="The currency.")
    vat = models.FloatField(null=True, help_text="VAT")
    type = models.TextField(blank=True)
    end_at = models.DateTimeField(null=True, help_text="End date")
    start_at = models.DateTimeField(null=True, help_text="Start date")
    sold_amount = models.PositiveBigIntegerField(null=True, help_text="Amount sold")

    amount_left = models.PositiveBigIntegerField(null=True, help_text="Amount left")
    nearly_over = models.BooleanField(null=True, help_text="Is nearly over")
    flash_sale = models.BooleanField(null=True, help_text="Is a flash sale")
    max_qty_per_customer = models.PositiveBigIntegerField(null=True, help_text="Maximum quantity per customer")

    # TODO(TheLovinator): Is this correct field?  # noqa: TD003
    max_amount_for_price = models.PositiveBigIntegerField(null=True, help_text="Maximum amount for price")

    def __str__(self) -> str:
        return f"{self.price} {self.currency}"


class Image(auto_prefetch.Model):
    """An image of a product from Webhallen."""

    zoom = models.URLField(blank=True, help_text="Zoom image")
    large = models.URLField(blank=True, help_text="Large image")
    thumb = models.URLField(blank=True, help_text="Thumbnail image")

    image = models.ImageField(upload_to="images/webhallen/product/", help_text="Product image")

    def __str__(self) -> str:
        return f"Image - {self.image}"


class Release(auto_prefetch.Model):
    """Release details of a product."""

    timestamp = models.DateTimeField(help_text="Timestamp")
    format = models.TextField(help_text="Format")


class Section(auto_prefetch.Model):
    """A section of a product."""

    id = models.PositiveBigIntegerField(primary_key=True, help_text="Section ID")
    meta_title = models.TextField(help_text="Meta title")
    active = models.BooleanField(help_text="Is active")
    icon = models.TextField(help_text="Icon")
    name = models.TextField(help_text="Name")


class MainCategoryPath(auto_prefetch.Model):
    """The main category path of a product."""

    id = models.PositiveBigIntegerField(primary_key=True, help_text="Main category path ID")
    fyndware_description = models.TextField(help_text="Fyndware description")
    meta_title = models.TextField(help_text="Meta title")
    seo_name = models.TextField(help_text="SEO name")
    active = models.BooleanField(help_text="Is active")
    order = models.PositiveBigIntegerField(help_text="Order")
    icon = models.TextField(help_text="Icon")
    name = models.TextField(help_text="Name")
    has_products = models.BooleanField(help_text="Has products")
    index = models.PositiveBigIntegerField(help_text="Index")
    url_name = models.TextField(help_text="URL name")


class Data(auto_prefetch.Model):
    """Data of a product."""


class Manufacturer(auto_prefetch.Model):
    """Manufacturer of a product."""

    id = models.PositiveBigIntegerField(primary_key=True, help_text="Manufacturer ID")
    name = models.TextField(help_text="Manufacturer name")
    takeover_url = models.URLField(help_text="Takeover URL")
    website_url = models.URLField(help_text="Website URL")
    visible = models.BooleanField(help_text="Is visible")


class PartNumber(auto_prefetch.Model):
    """Part number of a product."""

    part_number = models.TextField(primary_key=True, help_text="Part number")

    def __str__(self) -> str:
        return f"Part number - {self.part_number}"


class EAN(auto_prefetch.Model):
    """EAN of a product."""

    ean = models.TextField(primary_key=True, help_text="EAN")

    def __str__(self) -> str:
        return f"EAN - {self.ean}"


class Prices(auto_prefetch.Model):
    """Shipping prices of a product."""

    price = models.PositiveBigIntegerField(help_text="Price")
    shipping_method_id = models.PositiveBigIntegerField(help_text="Shipping method ID")
    is_fixed_price = models.BooleanField(help_text="Is fixed price")
    maximum_package_size_id = models.PositiveBigIntegerField(help_text="Maximum package size ID")


class ShippingClass(auto_prefetch.Model):
    """Shipping class of a product."""

    id = models.PositiveBigIntegerField(primary_key=True, help_text="Shipping class ID")
    order = models.PositiveBigIntegerField(help_text="Order")
    prices = models.ManyToManyField(Prices, help_text="Prices")


class EnergyMarking(auto_prefetch.Model):
    """Energy marking of a product."""

    label_content = models.TextField(help_text="Label content")  # TODO(Thelovinator): Is this used?  # noqa: TD003
    rating = models.TextField(help_text="Rating")
    scale = models.TextField(help_text="Scale")
    product_sheet_content = models.TextField(help_text="Product sheet content")
    label_image_url = models.URLField(help_text="Label image URL")
    manufacturer = models.TextField(help_text="Manufacturer")
    item_code = models.TextField(help_text="Item code")


class StatusCode(auto_prefetch.Model):
    """Status code of a product."""

    status_code = models.TextField(primary_key=True, help_text="Status code")


class ReviewHighlightProduct(auto_prefetch.Model):
    """Review highlight product."""

    id = models.PositiveBigIntegerField(primary_key=True, help_text="Review highlight product ID")
    main_category_path = models.ForeignKey(MainCategoryPath, on_delete=models.CASCADE, help_text="Main category path")
    minimum_rank_level = models.PositiveBigIntegerField(help_text="Minimum rank level")
    status_codes = models.ManyToManyField(StatusCode, help_text="Status codes")
    meta_title = models.TextField(help_text="Meta title")
    section = models.ForeignKey(Section, on_delete=models.CASCADE, help_text="Section")
    name = models.TextField(help_text="Name")


class Avatar(auto_prefetch.Model):
    """Avatar of a user."""

    id = models.PositiveBigIntegerField(primary_key=True, help_text="Avatar ID")
    title = models.TextField(help_text="Title")


class Knighthood(auto_prefetch.Model):
    """Webhallen knighthood."""


class User(auto_prefetch.Model):
    """A user of Webhallen."""

    id = models.PositiveBigIntegerField(primary_key=True, help_text="User ID")
    username = models.TextField(help_text="Username")
    is_public_profile = models.BooleanField(help_text="Is public profile")
    knighthood = models.ForeignKey(Knighthood, on_delete=models.CASCADE, help_text="Knighthood")
    rank_level = models.PositiveBigIntegerField(help_text="Rank level")
    avatar = models.ForeignKey(Avatar, on_delete=models.CASCADE, help_text="Avatar")


class ReviewHighlight(auto_prefetch.Model):
    """Review highlight of a product."""

    id = models.PositiveBigIntegerField(primary_key=True, help_text="Review highlight ID")
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


class Product(auto_prefetch.Model):
    """A product from Webhallen."""

    # 369004
    webhallen_id = models.PositiveBigIntegerField(primary_key=True, help_text="Webhallen product ID")

    variants = models.ManyToManyField(Variants, help_text="Variants")

    # ASUS Dual GeForce RTX 4060 EVO 8GB OC
    name = models.TextField(help_text="Product name")

    # Current price? TODO: Check if this is the current price
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
    lowest_price = auto_prefetch.ForeignKey(
        Price,
        on_delete=models.CASCADE,
        help_text="The lowest price of the product",
        related_name="lowest_price",
    )
    level_one_price = auto_prefetch.ForeignKey(
        Price,
        on_delete=models.CASCADE,
        help_text="The level one price of the product",
        related_name="level_one_price",
    )
    description = models.TextField(help_text="Product description")
    meta_title = models.TextField(help_text="Meta title")
    meta_description = models.TextField(help_text="Meta description")
    canonical_link = models.URLField(help_text="Canonical link")
    release = auto_prefetch.ForeignKey(Release, on_delete=models.CASCADE, help_text="Release")
    is_digital = models.BooleanField(help_text="Is digital")
    discontinued = models.BooleanField(help_text="Is discontinued")
    category_tree = models.TextField(help_text="Category tree")
    main_category_path = auto_prefetch.ForeignKey(
        MainCategoryPath,
        on_delete=models.CASCADE,
        help_text="Main category path",
    )
    # ifs_id = ????
    thumbnail = models.URLField(help_text="Thumbnail URL")
    package_size_id = models.PositiveBigIntegerField(help_text="Package size ID")
    long_delivery_notice = models.TextField(help_text="Long delivery notice")
    phone_subscription = models.BooleanField(help_text="Is a phone subscription")
    is_fyndware = models.BooleanField(help_text="Is Fyndware")
    main_title = models.TextField(help_text="Main title")
    sub_title = models.TextField(help_text="Sub title")
    is_shippable = models.BooleanField(help_text="Is shippable")
    is_collectable = models.BooleanField(help_text="Is collectable")
    description_provider = models.PositiveBigIntegerField(help_text="Description provider")
    minimum_rank_level = models.PositiveBigIntegerField(help_text="Minimum rank level")
    images = models.ManyToManyField(Image, help_text="Images")
    stock = auto_prefetch.ForeignKey(Stock, on_delete=models.CASCADE, help_text="Stock")
    section = auto_prefetch.ForeignKey(Section, on_delete=models.CASCADE, help_text="Section")
    # fyndware_of = ????
    data = auto_prefetch.ForeignKey(Data, on_delete=models.CASCADE, help_text="Data")
    manufacturer = auto_prefetch.ForeignKey(Manufacturer, on_delete=models.CASCADE, help_text="Manufacturer")
    part_numbers = models.ManyToManyField(PartNumber, help_text="Part numbers")
    eans = models.ManyToManyField(EAN, help_text="EANs")
    shipping_class = auto_prefetch.ForeignKey(ShippingClass, on_delete=models.CASCADE, help_text="Shipping class")
    average_rating = auto_prefetch.ForeignKey(AverageRating, on_delete=models.CASCADE, help_text="Average rating")
    energy_marking = auto_prefetch.ForeignKey(EnergyMarking, on_delete=models.CASCADE, help_text="Energy marking")
    status_codes = models.ManyToManyField(StatusCode, help_text="Status codes")
    categories = models.ManyToManyField(Categories, help_text="Categories")
    review_highlight = models.ManyToManyField(ReviewHighlight, help_text="Review highlights")

    def __str__(self) -> str:
        return f"{self.name} ({self.webhallen_id})"
