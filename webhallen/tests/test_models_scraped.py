from __future__ import annotations

from unittest.mock import MagicMock, patch

import httpx
import pytest
from django.utils import timezone

from webhallen.models.scraped import WebhallenProductJSON


@pytest.fixture()
def webhallen_product() -> WebhallenProductJSON:
    """Fixture to create a WebhallenProductJSON instance.

    Returns:
        WebhallenProductJSON: A new WebhallenProductJSON instance.
    """
    return WebhallenProductJSON.objects.create(
        webhallen_id=123456,
        data={"name": "Sample Product", "price": 199.99},
    )


@pytest.mark.django_db
def test_create_webhallen_product() -> None:
    """Test creating a WebhallenProductJSON instance."""
    product: WebhallenProductJSON = WebhallenProductJSON.objects.create(webhallen_id=987654, data=None)
    assert product.webhallen_id == 987654
    assert product.data is None

    @pytest.mark.django_db
    def test_fetch_data(webhallen_product: WebhallenProductJSON) -> None:
        """Test fetch_data method."""
        with patch("webhallen.models.scraped.httpx.Client.get") as mock_get:
            # Mock the response from the Webhallen API
            mock_response: MagicMock = MagicMock()
            mock_response.json.return_value = {"name": "Updated Product", "price": 299.99}
            mock_response.status_code = 200
            mock_get.return_value = mock_response

            # Use a different httpx client to avoid caching with hishel
            with patch("webhallen.models.scraped.httpx.Client", new_callable=httpx.Client):
                # Test fetching data
                webhallen_product.fetch_data()
                webhallen_product.refresh_from_db()

                assert webhallen_product.data == {"name": "Updated Product", "price": 299.99}
                assert webhallen_product.updated_at > timezone.now() - timezone.timedelta(seconds=1)


@pytest.mark.django_db
def test_fetch_data_api_error(webhallen_product: WebhallenProductJSON) -> None:
    """Test fetch_data method handles API errors gracefully."""
    with patch("webhallen.models.scraped.httpx.Client.get") as mock_get:
        mock_response: MagicMock = MagicMock()
        mock_response.raise_for_status.side_effect = httpx.HTTPError("API Error")
        mock_get.return_value = mock_response

        # Attempt to fetch data
        webhallen_product.fetch_data()

        # Ensure that the data is not changed
        assert webhallen_product.data is not None  # Ensure previous data remains
        assert webhallen_product.updated_at < timezone.now()
