from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

from django.core.management.base import BaseCommand

from webhallen.models.scraped import WebhallenProductJSON

if TYPE_CHECKING:
    from django.db.models.manager import BaseManager


class Command(BaseCommand):
    """Download all JSON data from the database and save to disk."""

    help = "Download all JSON data from the database and save to disk."

    def handle(self, *args: tuple, **kwargs: dict) -> None:  # noqa: ARG002
        """Handles the command."""
        output_path: Path = Path("output") / "products"
        output_path.mkdir(parents=True, exist_ok=True)

        products: BaseManager[WebhallenProductJSON] = WebhallenProductJSON.objects.all().filter(data__isnull=False)
        for product in products:
            json_file: Path = output_path / f"{product.webhallen_id}.json"
            with json_file.open("w", encoding="utf-8") as f:
                if not product.data:
                    self.stdout.write(self.style.WARNING(f"Product {product.webhallen_id} has no data."))
                    continue

                f.write(json.dumps(product.data, ensure_ascii=False, indent=2))

        self.stdout.write(self.style.SUCCESS(f"Downloaded {products.count()} products' JSON data to {output_path}."))
