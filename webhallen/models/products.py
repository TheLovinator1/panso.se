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


class ListClass(auto_prefetch.Model):
    """List class of a product."""

    # TODO(TheLovinator): Should this be a Product?  # noqa: TD003

    id = models.PositiveBigIntegerField(primary_key=True, help_text="List ID")
    variant_properties = models.ManyToManyField(VariantProperties, help_text="Variant properties")
    name = models.TextField(help_text="Name")
    price = models.ForeignKey("Price", on_delete=models.CASCADE, help_text="Price")
    stock = models.ForeignKey("Stock", on_delete=models.CASCADE, help_text="Stock")
    release = models.ForeignKey("Release", on_delete=models.CASCADE, help_text="Release")
    is_fyndware = models.BooleanField(help_text="Is Fyndware")
    variant_name = models.TextField(help_text="Variant name")
    discontinued = models.BooleanField(help_text="Is discontinued")
    regular_price = models.ForeignKey("Price", on_delete=models.CASCADE, help_text="Regular price")
    energy_marking = models.ForeignKey("EnergyMarking", on_delete=models.CASCADE, help_text="Energy marking")
    lowest_price = models.ForeignKey("Price", on_delete=models.CASCADE, help_text="Lowest price")


class Variants(auto_prefetch.Model):
    """Variants of a product."""

    canonical_variant = models.ForeignKey(CanonicalVariant, on_delete=models.CASCADE, help_text="Canonical variant")
    list = models.ForeignKey(ListClass, on_delete=models.CASCADE, help_text="List")
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
    amount_left = models.PositiveBigIntegerField(null=True, help_text="Amount left")
    nearly_over = models.BooleanField(null=True, help_text="Is nearly over")
    flash_sale = models.BooleanField(null=True, help_text="Is a flash sale")
    max_qty_per_customer = models.PositiveBigIntegerField(null=True, help_text="Maximum quantity per customer")

    # TODO(TheLovinator): Is fields below correct?  # noqa: TD003
    max_amount_for_price = models.PositiveBigIntegerField(null=True, help_text="Maximum amount for price")
    sold_amount = models.PositiveBigIntegerField(null=True, help_text="Amount sold")

    def __str__(self) -> str:
        return f"{self.price} {self.currency}"


class Image(auto_prefetch.Model):
    """An image of a product from Webhallen.

    Each product has zoom, large and thumb but it is the same URL but with different arguments.
    """

    url = models.URLField(blank=True, help_text="Image URL")
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


class Parts(auto_prefetch.Model):
    """Parts of a product."""

    comb = models.TextField(help_text="Comb")
    nnv = models.FloatField(help_text="NNV")  # TODO(TheLovinator): What is this?  # noqa: TD003
    text_value = models.TextField(help_text="Text value")
    unit = models.TextField(help_text="Unit")
    value = models.TextField(help_text="Value")


class Component(auto_prefetch.Model):
    """Component of a product."""

    name = models.TextField(help_text="Name")
    value = models.TextField(help_text="Value")
    attribute_id = models.PositiveBigIntegerField(help_text="Attribute ID")
    parts = models.ManyToManyField(Parts, help_text="Parts")


class Header(auto_prefetch.Model):
    """Header of a product.

    Note: All the field names are translated from Swedish to English.
    """

    packaged_quantity = models.ManyToManyField(Component, help_text="Packaged quantity")
    brand = models.ManyToManyField(Component, help_text="Brand")
    product_line = models.ManyToManyField(Component, help_text="Product line")
    manufacturer = models.ManyToManyField(Component, help_text="Manufacturer")
    model = models.ManyToManyField(Component, help_text="Model")
    compatibility = models.ManyToManyField(Component, help_text="Compatibility")
    country_specific_batches = models.ManyToManyField(Component, help_text="Country-specific batches")
    localization = models.ManyToManyField(Component, help_text="Localization")
    game_publisher = models.ManyToManyField(Component, help_text="Game publisher")
    game_developer = models.ManyToManyField(Component, help_text="Game developer")
    edition = models.ManyToManyField(Component, help_text="Edition")
    batch = models.ManyToManyField(Component, help_text="Batch")
    manufacturer_model_number = models.ManyToManyField(Component, help_text="Manufacturer's model number")
    release_date = models.ManyToManyField(Component, help_text="Release date")
    series = models.ManyToManyField(Component, help_text="Series")


class DimensionsAndWeight(auto_prefetch.Model):
    """Dimensions and weight of a product."""

    weight = models.ManyToManyField(Component, help_text="Weight")
    length = models.ManyToManyField(Component, help_text="Length")
    width = models.ManyToManyField(Component, help_text="Width")
    height = models.ManyToManyField(Component, help_text="Height")
    length_in_meters = models.ManyToManyField(Component, help_text="Length in meters")
    diameter = models.ManyToManyField(Component, help_text="Diameter")
    comments = models.ManyToManyField(Component, help_text="Comments")
    thickness = models.ManyToManyField(Component, help_text="Thickness")
    volume = models.ManyToManyField(Component, help_text="Volume")
    comment = models.ManyToManyField(Component, help_text="Comment")
    min_height = models.ManyToManyField(Component, help_text="Minimum height")
    backrest_height = models.ManyToManyField(Component, help_text="Backrest height")
    backrest_width = models.ManyToManyField(Component, help_text="Backrest width")
    max_length = models.ManyToManyField(Component, help_text="Maximum length")


class General(auto_prefetch.Model):
    """General information of a product."""

    product_type = models.ManyToManyField(Component, help_text="Product type")
    accessory_category = models.ManyToManyField(Component, help_text="Accessory category")
    consumable_subcategory = models.ManyToManyField(Component, help_text="Consumable subcategory")
    technology = models.ManyToManyField(Component, help_text="Technology")
    printer_consumables_class = models.ManyToManyField(Component, help_text="Printer consumables class")
    subcategory = models.ManyToManyField(Component, help_text="Subcategory")
    category = models.ManyToManyField(Component, help_text="Category")
    installation_type = models.ManyToManyField(Component, help_text="Installation type")
    designed_for = models.ManyToManyField(Component, help_text="Designed for")
    environment = models.ManyToManyField(Component, help_text="Environment")
    number_of_set_parts = models.ManyToManyField(Component, help_text="Number of set parts")
    suitable_for = models.ManyToManyField(Component, help_text="Suitable for")
    features = models.ManyToManyField(Component, help_text="Features")
    learning = models.ManyToManyField(Component, help_text="Learning")
    min_age = models.ManyToManyField(Component, help_text="Minimum age")
    max_age = models.ManyToManyField(Component, help_text="Maximum age")
    one_board_computer_included = models.ManyToManyField(Component, help_text="One board computer included")
    waterproof = models.ManyToManyField(Component, help_text="Waterproof")
    dimmer = models.ManyToManyField(Component, help_text="Dimmer")
    cable_length = models.ManyToManyField(Component, help_text="Cable length")
    supported_wattage_for_light_bulb = models.ManyToManyField(Component, help_text="Supported wattage for light bulb")
    number_of_installed_light_bulbs = models.ManyToManyField(Component, help_text="Number of installed light bulbs")
    number_of_supported_light_bulbs = models.ManyToManyField(Component, help_text="Number of supported light bulbs")
    battery_included = models.ManyToManyField(Component, help_text="Battery included")
    switch_type = models.ManyToManyField(Component, help_text="Switch type")
    switch_location = models.ManyToManyField(Component, help_text="Switch location")
    clamp_mount = models.ManyToManyField(Component, help_text="Clamp mount")
    tool_set_parts = models.ManyToManyField(Component, help_text="Tool set parts")
    socket = models.ManyToManyField(Component, help_text="Socket")
    socket_size = models.ManyToManyField(Component, help_text="Socket size")
    tip = models.ManyToManyField(Component, help_text="Tip")
    tip_size = models.ManyToManyField(Component, help_text="Tip size")
    size = models.ManyToManyField(Component, help_text="Size")
    shape = models.ManyToManyField(Component, help_text="Shape")
    tracking_data = models.ManyToManyField(Component, help_text="Tracking data")
    solution = models.ManyToManyField(Component, help_text="Solution")
    character_theme = models.ManyToManyField(Component, help_text="Character theme")
    AC_adapter_included = models.ManyToManyField(Component, help_text="AC adapter included")
    style = models.ManyToManyField(Component, help_text="Style")
    recommended_for = models.ManyToManyField(Component, help_text="Recommended for")
    recommended_use = models.ManyToManyField(Component, help_text="Recommended use")
    connection = models.ManyToManyField(Component, help_text="Connection")
    type = models.ManyToManyField(Component, help_text="Type")
    total_length = models.ManyToManyField(Component, help_text="Total length")
    payment_technology = models.ManyToManyField(Component, help_text="Payment technology")
    mechanism = models.ManyToManyField(Component, help_text="Mechanism")
    tilt_lock = models.ManyToManyField(Component, help_text="Tilt lock")
    headrest = models.ManyToManyField(Component, help_text="Headrest")
    armrest = models.ManyToManyField(Component, help_text="Armrest")
    tilt = models.ManyToManyField(Component, help_text="Tilt")
    ergonomic = models.ManyToManyField(Component, help_text="Ergonomic")
    tilt_tension_adjustment = models.ManyToManyField(Component, help_text="Tilt tension adjustment")

    # TODO(TheLovinator): Rename in API to class when exporting  # noqa: TD003
    _class = models.ManyToManyField(Component, help_text="Class")
    kit_contents = models.ManyToManyField(Component, help_text="Kit contents")
    media_subcategory = models.ManyToManyField(Component, help_text="Media subcategory")
    indoor_outdoor = models.ManyToManyField(Component, help_text="Indoor/outdoor")
    thermometer_scale = models.ManyToManyField(Component, help_text="Thermometer scale")
    usage_modes = models.ManyToManyField(Component, help_text="Usage modes")
    car_power_adapter_included = models.ManyToManyField(Component, help_text="Car power adapter included")
    built_in_components = models.ManyToManyField(Component, help_text="Built-in components")
    arm_construction = models.ManyToManyField(Component, help_text="Arm construction")
    number_of_modules = models.ManyToManyField(Component, help_text="Number of modules")
    number_of_component_sets = models.ManyToManyField(Component, help_text="Number of component sets")
    number_of_sockets = models.ManyToManyField(Component, help_text="Number of sockets")
    output_connection_type = models.ManyToManyField(Component, help_text="Output connection type")
    output_bar_configuration = models.ManyToManyField(Component, help_text="Output bar configuration")
    lock_type = models.ManyToManyField(Component, help_text="Lock type")
    power = models.ManyToManyField(Component, help_text="Power")
    cordless = models.ManyToManyField(Component, help_text="Cordless")
    diameter = models.ManyToManyField(Component, help_text="Diameter")


class Miscellaneous(auto_prefetch.Model):
    """Miscellaneous information of a product."""

    color = models.ManyToManyField(Component, help_text="Color")
    color_category = models.ManyToManyField(Component, help_text="Color category")
    flat_screen_mounting_interface = models.ManyToManyField(Component, help_text="Flat screen mounting interface")
    rack_mounting_kit = models.ManyToManyField(Component, help_text="Rack mounting kit")
    compatible_game_console = models.ManyToManyField(Component, help_text="Compatible game console")
    sound_pressure_level = models.ManyToManyField(Component, help_text="Sound pressure level")
    external_color = models.ManyToManyField(Component, help_text="External color")
    encryption_algorithm = models.ManyToManyField(Component, help_text="Encryption algorithm")
    hard_drive_form_factor_compatibility = models.ManyToManyField(Component, help_text="HDD form factor compatibility")
    hard_drive_compatible_form_factor_metric = models.ManyToManyField(
        Component,
        help_text="HDD compatible form factor metric",
    )
    material = models.ManyToManyField(Component, help_text="Material")
    product_material = models.ManyToManyField(Component, help_text="Product material")
    features = models.ManyToManyField(Component, help_text="Features")
    gaming = models.ManyToManyField(Component, help_text="Gaming")
    finish = models.ManyToManyField(Component, help_text="Finish")
    works_with_chromebook = models.ManyToManyField(Component, help_text="Works with Chromebook")
    recycled_product_content = models.ManyToManyField(Component, help_text="Recycled product content")
    included_accessories = models.ManyToManyField(Component, help_text="Included accessories")
    operating_time_without_power_connection = models.ManyToManyField(
        Component,
        help_text="Operating time without power connection",
    )
    cordless_use = models.ManyToManyField(Component, help_text="Cordless use")
    max_load = models.ManyToManyField(Component, help_text="Max load")
    recycled_packaging_content = models.ManyToManyField(Component, help_text="Recycled packaging content")
    protection = models.ManyToManyField(Component, help_text="Protection")
    packaging_type = models.ManyToManyField(Component, help_text="Packaging type")
    design_features = models.ManyToManyField(Component, help_text="Design features")
    package_type = models.ManyToManyField(Component, help_text="Package type")
    standards_followed = models.ManyToManyField(Component, help_text="Standards followed")
    coffee_maker_accessories = models.ManyToManyField(Component, help_text="Coffee maker accessories")
    max_depth_for_water_resistance = models.ManyToManyField(Component, help_text="Max depth for water resistance")
    for_underwater_use = models.ManyToManyField(Component, help_text="For underwater use")
    pricing_type = models.ManyToManyField(Component, help_text="Pricing type")
    capacity = models.ManyToManyField(Component, help_text="Capacity")
    product_type = models.ManyToManyField(Component, help_text="Product type")
    processor_package = models.ManyToManyField(Component, help_text="Processor package")
    waterproof = models.ManyToManyField(Component, help_text="Waterproof")
    reparability_index = models.ManyToManyField(Component, help_text="Reparability index")
    sound_level = models.ManyToManyField(Component, help_text="Sound level")
    noise_class = models.ManyToManyField(Component, help_text="Noise class")
    rugged_design = models.ManyToManyField(Component, help_text="Rugged design")
    software_certification = models.ManyToManyField(Component, help_text="Software certification")
    manufacturer_sales_program = models.ManyToManyField(Component, help_text="Manufacturer sales program")
    recycled_product_content_comment = models.ManyToManyField(Component, help_text="Recycled product content comment")
    recycled_packaging_content_comment = models.ManyToManyField(
        Component,
        help_text="Recycled packaging content comment",
    )
    product_condition = models.ManyToManyField(Component, help_text="Product condition")
    ai_ready = models.ManyToManyField(Component, help_text="AI ready")


class Cable(auto_prefetch.Model):
    """Cable of a product."""

    something = models.TextField(help_text="Something")  # TODO(TheLovinator): What is this?  # noqa: TD003
    cable = models.ManyToManyField(Component, help_text="Cable")


class InputDevice(auto_prefetch.Model):
    """Input device of a product."""

    connection_technology = models.ManyToManyField(Component, help_text="Connection technology")
    interface = models.ManyToManyField(Component, help_text="Interface")
    product_type = models.ManyToManyField(Component, help_text="Product type")
    backlit = models.ManyToManyField(Component, help_text="Backlit")
    form_factor = models.ManyToManyField(Component, help_text="Form factor")
    interface_type = models.ManyToManyField(Component, help_text="Interface type")
    input_adapter_type = models.ManyToManyField(Component, help_text="Input adapter type")
    keyboard_localization = models.ManyToManyField(Component, help_text="Keyboard localization")
    motion_detection_technology = models.ManyToManyField(Component, help_text="Motion detection technology")
    orientation = models.ManyToManyField(Component, help_text="Orientation")
    number_of_buttons = models.ManyToManyField(Component, help_text="Number of buttons")
    motion_resolution = models.ManyToManyField(Component, help_text="Motion resolution")
    notebook_mouse = models.ManyToManyField(Component, help_text="Notebook mouse")
    ergonomic_design = models.ManyToManyField(Component, help_text="Ergonomic design")
    keyboard_layout = models.ManyToManyField(Component, help_text="Keyboard layout")
    keyboard_technology = models.ManyToManyField(Component, help_text="Keyboard technology")
    active_horizontal_area = models.ManyToManyField(Component, help_text="Active horizontal area")
    active_vertical_area = models.ManyToManyField(Component, help_text="Active vertical area")
    anti_ghosting = models.ManyToManyField(Component, help_text="Anti-ghosting")
    number_of_simultaneous_keypresses = models.ManyToManyField(Component, help_text="Number of simultaneous keypresses")
    type = models.ManyToManyField(Component, help_text="Type")
    key_lock_type = models.ManyToManyField(Component, help_text="Key lock type")
    backlight = models.ManyToManyField(Component, help_text="Backlight")
    numeric_keypad = models.ManyToManyField(Component, help_text="Numeric keypad")


class ServiceAndSupport(auto_prefetch.Model):
    """Service and support of a product."""

    service_and_support = models.ManyToManyField(Component, help_text="Service and support")


class GrossDimensionsAndWeight(auto_prefetch.Model):
    """Gross dimensions and weight of a product."""

    packing_weight = models.ManyToManyField(Component, help_text="Packing weight")
    packing_height = models.ManyToManyField(Component, help_text="Packing height")
    packing_depth = models.ManyToManyField(Component, help_text="Packing depth")
    packing_width = models.ManyToManyField(Component, help_text="Packing width")


class Consumables(auto_prefetch.Model):
    """Consumables of a product."""

    color = models.ManyToManyField(Component, help_text="Color")
    consumable_type = models.ManyToManyField(Component, help_text="Consumable type")
    number_of_pages_during_lifetime = models.ManyToManyField(Component, help_text="Number of pages during life cycle")
    coverage_for_lifetime = models.ManyToManyField(Component, help_text="Coverage for lifetime")


class Battery(auto_prefetch.Model):
    """Battery of a product."""

    included_quantity = models.ManyToManyField(Component, help_text="Included quantity")
    technology = models.ManyToManyField(Component, help_text="Technology")
    form_factor = models.ManyToManyField(Component, help_text="Form factor")
    capacity_ah = models.ManyToManyField(Component, help_text="Capacity (Ah)")
    supplied_voltage = models.ManyToManyField(Component, help_text="Supplied voltage")
    installed_count = models.ManyToManyField(Component, help_text="Installed count")
    charging_time = models.ManyToManyField(Component, help_text="Charging time")
    battery_time_up_to = models.ManyToManyField(Component, help_text="Battery time up to")
    capacity = models.ManyToManyField(Component, help_text="Capacity")
    talk_time = models.ManyToManyField(Component, help_text="Talk time")
    standby_time = models.ManyToManyField(Component, help_text="Standby time")
    run_time = models.ManyToManyField(Component, help_text="Run time")
    wireless_charging = models.ManyToManyField(Component, help_text="Wireless charging")
    fast_charging_technology = models.ManyToManyField(Component, help_text="Fast charging technology")
    capacity_wh = models.ManyToManyField(Component, help_text="Capacity (Wh)")
    battery_type = models.ManyToManyField(Component, help_text="Battery type")


class AVComponent(auto_prefetch.Model):
    """AV component of a product."""

    something = models.TextField(help_text="Something")  # TODO(TheLovinator): What is this?  # noqa: TD003
    av_component = models.ManyToManyField(Component, help_text="AV component")


class RemoteControl(auto_prefetch.Model):
    """Remote control of a product."""

    max_working_distance = models.ManyToManyField(Component, help_text="Max working distance")
    remote_control_technology = models.ManyToManyField(Component, help_text="Remote control technology")
    supported_devices = models.ManyToManyField(Component, help_text="Supported devices")
    type = models.ManyToManyField(Component, help_text="Type")
    number_of_devices_supported = models.ManyToManyField(Component, help_text="Number of devices supported")


class VideoInput(auto_prefetch.Model):
    """Video input of a product."""

    support_for_audio_input = models.ManyToManyField(Component, help_text="Support for audio input")
    format_for_digital_video = models.ManyToManyField(Component, help_text="Format for digital video")
    format_for_analog_video = models.ManyToManyField(Component, help_text="Format for analog video")
    analog_video_signal = models.ManyToManyField(Component, help_text="Analog video signal")
    resolution_for_digital_video_capture = models.ManyToManyField(
        Component,
        help_text="Resolution for digital video capture",
    )
    type_of_interface = models.ManyToManyField(Component, help_text="Type of interface")
    connection_technology = models.ManyToManyField(Component, help_text="Connection technology")
    support_for_audio = models.ManyToManyField(Component, help_text="Support for audio")
    camera_type = models.ManyToManyField(Component, help_text="Camera type")
    computer_interface = models.ManyToManyField(Component, help_text="Computer interface")
    maximum_digital_video_resolution = models.ManyToManyField(Component, help_text="Maximum digital video resolution")
    frame_rate_max = models.ManyToManyField(Component, help_text="Frame rate max")
    day_and_night_function = models.ManyToManyField(Component, help_text="Day and night function")
    camera_mounting_type = models.ManyToManyField(Component, help_text="Camera mounting type")
    mechanical_camera_design = models.ManyToManyField(Component, help_text="Mechanical camera design")
    form_factor = models.ManyToManyField(Component, help_text="Form factor")
    resolution_for_still_shot = models.ManyToManyField(Component, help_text="Resolution for still shot")
    motion_detection = models.ManyToManyField(Component, help_text="Motion detection")
    video_interface = models.ManyToManyField(Component, help_text="Video interface")
    type = models.ManyToManyField(Component, help_text="Type")
    image_capture_format = models.ManyToManyField(Component, help_text="Image capture format")
    properties = models.ManyToManyField(Component, help_text="Properties")
    digital_zoom = models.ManyToManyField(Component, help_text="Digital zoom")
    face_recognition = models.ManyToManyField(Component, help_text="Face recognition")
    support_for_high_resolution_video = models.ManyToManyField(Component, help_text="Support for high resolution video")
    continuous_shooting_rate = models.ManyToManyField(Component, help_text="Continuous shooting rate")
    image_stabilizer = models.ManyToManyField(Component, help_text="Image stabilizer")
    max_video_resolution = models.ManyToManyField(Component, help_text="Max video resolution")
    provided_interfaces = models.ManyToManyField(Component, help_text="Provided interfaces")
    special_effects = models.ManyToManyField(Component, help_text="Special effects")
    digital_camera_type = models.ManyToManyField(Component, help_text="Digital camera type")
    iso_max = models.ManyToManyField(Component, help_text="ISO max")
    combined_with = models.ManyToManyField(Component, help_text="Combined with")
    light_sensitivity = models.ManyToManyField(Component, help_text="Light sensitivity")


class Data(auto_prefetch.Model):
    """Data of a product."""

    cable = models.ForeignKey(Cable, on_delete=models.CASCADE, help_text="Cable")
    header = models.ForeignKey(Header, on_delete=models.CASCADE, help_text="Header")
    dimensions_and_weight = models.ForeignKey(
        DimensionsAndWeight,
        on_delete=models.CASCADE,
        help_text="Dimensions and weight",
    )
    general = models.ForeignKey(General, on_delete=models.CASCADE, help_text="General")
    miscellaneous = models.ForeignKey(Miscellaneous, on_delete=models.CASCADE, help_text="Miscellaneous")
    input_device = models.ForeignKey(InputDevice, on_delete=models.CASCADE, help_text="Input device")
    service_and_support = models.ForeignKey(
        ServiceAndSupport,
        on_delete=models.CASCADE,
        help_text="Service and support",
    )
    gross_dimensions_and_weight = models.ForeignKey(
        GrossDimensionsAndWeight,
        on_delete=models.CASCADE,
        help_text="Gross dimensions and weight",
    )
    consumables = models.ManyToManyField(Consumables, help_text="Consumables")
    battery = models.ManyToManyField(Battery, help_text="Battery")
    av_components = models.ManyToManyField(AVComponent, help_text="AV components")
    remote_control = models.ManyToManyField(RemoteControl, help_text="Remote control")
    video_input = models.ManyToManyField(VideoInput, help_text="Video input")


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


class PossibleDeliveryMethod(auto_prefetch.Model):
    """Possible delivery method of a product."""

    id = models.PositiveBigIntegerField(primary_key=True, help_text="Possible delivery method ID")


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


class ResursPartPaymentPrice(auto_prefetch.Model):
    """https://www.webhallen.com/se/info/48-Betala-senare-med-Resurs."""

    monthly_cost = models.TextField(help_text="Monthly cost")
    duration_months = models.PositiveBigIntegerField(help_text="Duration in months")


class Insurance(auto_prefetch.Model):
    """Insurance of a product."""

    id = models.PositiveBigIntegerField(primary_key=True, help_text="Insurance ID")
    name = models.TextField(help_text="Insurance name")
    price = models.PositiveBigIntegerField(help_text="Insurance price")
    provider = models.PositiveBigIntegerField(help_text="Insurance provider")
    length = models.PositiveBigIntegerField(help_text="Insurance length")


class ExcludeShippingMethod(auto_prefetch.Model):
    """Excluded shipping method."""

    id = models.PositiveBigIntegerField(primary_key=True, help_text="Exclude shipping method ID")


class Meta(auto_prefetch.Model):
    """Meta of a product."""

    highlight_member_offer = models.BooleanField(help_text="Highlight member offer")
    excluded_shipping_methods = models.ManyToManyField(ExcludeShippingMethod, help_text="Excluded shipping methods")
    is_hygiene_article = models.BooleanField(help_text="Is hygiene article")
    requires_prepayment = models.TextField(help_text="Requires prepayment")


class FyndwareClass(auto_prefetch.Model):
    """Fyndware class of a product."""

    id = models.PositiveBigIntegerField(primary_key=True, help_text="Fyndware class ID")
    condition = models.TextField(help_text="Condition")
    description = models.TextField(help_text="Description")
    name = models.TextField(help_text="Name")
    short_name = models.TextField(help_text="Short name")  # TODO(TheLovinator): Is this correct?  # noqa: TD003


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
    # ifs_id = ???? # TODO(TheLovinator): What is this?  # noqa: TD003
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
    meta = auto_prefetch.ForeignKey(Meta, on_delete=models.CASCADE, help_text="Meta")
    insurance = models.ManyToManyField(Insurance, help_text="Insurance")
    possible_delivery_methods = models.ManyToManyField(PossibleDeliveryMethod, help_text="Possible delivery methods")
    resurs_part_payment_price = models.ManyToManyField(ResursPartPaymentPrice, help_text="Resurs part payment price")
    ticket = models.TextField(help_text="Ticket")
    fyndware_class = auto_prefetch.ForeignKey(FyndwareClass, on_delete=models.CASCADE, help_text="Fyndware class")

    def __str__(self) -> str:
        return f"{self.name} ({self.webhallen_id})"
