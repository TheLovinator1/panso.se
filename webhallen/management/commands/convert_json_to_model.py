from __future__ import annotations

from pathlib import Path
from typing import Any

from django.core.management.base import BaseCommand

from webhallen.models.products import Product
from webhallen.models.scraped import WebhallenProductJSON


class Command(BaseCommand):
    """Create a single JSON file with all unique keys and an example value from JSON objects."""

    help = "Aggregate all keys from JSON data in the database into a single file with one example value per key."

    def handle(self, *args: tuple, **kwargs: dict) -> None:  # noqa: ARG002
        """Handles the command."""
        output_path = Path("output")
        output_path.mkdir(parents=True, exist_ok=True)

        # Download all JSON data from the database
        json_data = WebhallenProductJSON.objects.all().filter(data__isnull=False)

        for product_data in json_data:
            if not product_data:
                continue

            data: dict | None = product_data.data
            webhallen_id: int = product_data.webhallen_id or 0

            if not data:
                self.stdout.write(self.style.WARNING(f"Product {webhallen_id} has no data."))
                continue

            # Recursive function to extract keys and values
            self.handle_json(data, webhallen_id)

        self.stdout.write(self.style.SUCCESS(f"Successfully aggregated keys to {output_path}"))

    def handle_json(self, data: dict[str, Any], webhallen_id: int) -> None:
        """Convert JSON data to models."""
        # Get or create the product
        product, created = Product.objects.get_or_create(webhallen_id=webhallen_id)
        if created:
            self.stdout.write(self.style.SUCCESS(f"Product {webhallen_id} created."))

        # Update the product with the JSON data
        product.import_json(data)
