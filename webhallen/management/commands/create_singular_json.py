from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from django.core.management.base import BaseCommand

from webhallen.models import WebhallenProductJSON


class Command(BaseCommand):
    """Create a single JSON file with all unique keys and an example value from JSON objects."""

    help = "Aggregate all keys from JSON data in the database into a single file with one example value per key."

    def handle(self, *args: tuple, **kwargs: dict) -> None:  # noqa: ARG002
        """Handles the command."""
        # Download all JSON data from the database
        json_data = WebhallenProductJSON.objects.values_list("data", flat=True)

        # Aggregate all keys and example values
        keys: dict[str, Any] = {}

        for product_data in json_data:
            if not product_data:
                continue

            data = product_data["product"]

            # Recursive function to extract keys and values
            self.extract_keys(data, keys)

        # Create a JSON file with the aggregated keys
        output_path = Path("aggregated_keys.json")
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(keys, f, ensure_ascii=False, indent=2)

        self.stdout.write(self.style.SUCCESS(f"Successfully aggregated keys to {output_path}"))

    def extract_keys(self, data: dict[str, Any], keys: dict[str, Any]) -> None:
        """Recursively extracts keys and their first example value from the provided data."""
        for key, value in data.items():
            # Only add if the key is not already in keys
            if key not in keys:
                keys[key] = value  # Store the first encountered value

            # If the value is a dictionary, recurse into it
            if isinstance(value, dict):
                self.extract_keys(value, keys)

            # If the value is a list, check its contents
            elif isinstance(value, list) and value:  # If the list is not empty
                self.extract_keys(value[0] if isinstance(value[0], dict) else {key: value[0]}, keys)
