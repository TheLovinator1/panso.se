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
        output_path = Path("output")
        output_path.mkdir(parents=True, exist_ok=True)

        # Download all JSON data from the database
        json_data = WebhallenProductJSON.objects.all().filter(data__isnull=False)

        # Aggregate all keys and example values
        keys: dict[str, Any] = {}

        for product_data in json_data:
            if not product_data:
                continue

            data: dict | None = product_data.data
            webhallen_id: int = product_data.webhallen_id or 0

            if not data:
                self.stdout.write(self.style.WARNING(f"Product {webhallen_id} has no data."))
                continue

            # Recursive function to extract keys and values
            self.extract_keys(data, keys)

        # Create a JSON file with the aggregated keys
        output_path: Path = output_path / "keys.json"
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(keys, f, ensure_ascii=False, indent=2)

        self.stdout.write(self.style.SUCCESS(f"Successfully aggregated keys to {output_path}"))

    def extract_keys(self, data: dict[str, Any], keys: dict[str, Any]) -> None:  # noqa: C901, PLR0912
        """Recursively extracts keys and their structures from nested dictionaries and lists."""
        for key, value in data.items():
            # Check if the key already exists in the target keys
            if key not in keys:
                # Handle dict values (nested structure)
                if isinstance(value, dict):
                    keys[key] = {}
                    self.extract_keys(value, keys[key])
                # Handle list values
                elif isinstance(value, list):
                    keys[key] = {}
                    for item in value:
                        if isinstance(item, dict):
                            self.extract_keys(item, keys[key])
                        else:
                            # If it's a list of non-dicts, just store an example value
                            keys[key] = value
                else:
                    # Base case: for non-dict, non-list values, just store the value
                    keys[key] = value
            elif keys[key] is None:  # If the existing value is None, replace it
                keys[key] = value
            elif isinstance(value, dict):
                if isinstance(keys[key], dict):
                    self.extract_keys(value, keys[key])
            elif isinstance(value, list):
                # Recurse into lists containing dictionaries
                if isinstance(keys[key], dict):
                    for item in value:
                        if isinstance(item, dict):
                            self.extract_keys(item, keys[key])
                else:
                    # If it's a list of non-dicts, we just overwrite the example value
                    keys[key] = value
            else:
                # If the existing key has a non-None value, keep it
                continue
