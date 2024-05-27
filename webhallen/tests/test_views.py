import random
import string
from typing import TYPE_CHECKING

import pytest
from django.http.response import HttpResponse
from django.test import Client
from django.test.utils import override_settings
from django.urls import reverse

from webhallen.models import WebhallenJSON, WebhallenProduct

if TYPE_CHECKING:
    from django.http import HttpResponse


password: str = "".join(random.choices(string.ascii_letters + string.digits, k=12))
username: str = "".join(random.choices(string.ascii_lowercase, k=8))
email: str = (
    "".join(random.choices(string.ascii_lowercase, k=5))
    + "@"
    + "".join(random.choices(string.ascii_lowercase, k=3))
    + "."
    + "".join(random.choices(string.ascii_lowercase, k=2))
)


@pytest.mark.django_db()
@pytest.mark.parametrize("debug_mode", [True, False], ids=["debug_mode_true", "debug_mode_false"])
@pytest.mark.parametrize(
    "url",
    ["/webhallen/", "/webhallen", lambda: reverse("webhallen:webhallen_products")],
    ids=["url_webhallen", "url_webhallen_slash", "url_webhallen_reverse"],
)
def test_can_access_webhallen_products(client: Client, debug_mode: bool, url: str) -> None:
    """Test if a user can access the Webhallen products page."""
    with override_settings(DEBUG=debug_mode):
        # Resolve the URL for the lambda function
        if callable(url):
            url = url()

        # Create the products
        WebhallenProduct.objects.create(
            product_id=1,
            name="Test product",
            url="https://example.com",
        )
        WebhallenProduct.objects.create(
            product_id=2,
            name="Another test product",
            url="https://example.com",
        )

        # Access the products page
        response: HttpResponse = client.get(url, follow=True)

        # Check if the response is as expected
        assert response.status_code == 200, f"Response status code: {response.status_code}"

        # Check if the response content is as expected
        assert b"Webhallen products" in response.content, "Response content does not contain 'Webhallen products'"
        assert b"<p>2 products.</p>" in response.content, "Response content does not contain the number of products"
        assert b"<li>1 - " in response.content, "Response content does not contain the list of products"
        assert b"<li>2 - " in response.content, "Response content does not contain the list of products"

        # Check if the context is as expected
        assert response.context["canonical_url"] == "https://panso.se/webhallen/", "Canonical URL is not as expected"


@pytest.mark.django_db()
@pytest.mark.parametrize("debug_mode", [True, False], ids=["debug_mode_true", "debug_mode_false"])
@pytest.mark.parametrize(
    "url",
    ["/webhallen/", "/webhallen", lambda: reverse("webhallen:webhallen_products")],
    ids=["url_webhallen", "url_webhallen_slash", "url_webhallen_reverse"],
)
def test_can_access_webhallen_products_without_a_product(client: Client, debug_mode: bool, url: str) -> None:
    """Test if a user can access the Webhallen products page without a product."""
    with override_settings(DEBUG=debug_mode):
        # Resolve the URL for the lambda function
        if callable(url):
            url = url()

        # Access the product page
        response: HttpResponse = client.get(url, follow=True)

        # Check if the response is as expected
        assert response.status_code == 200, f"Response status code: {response.status_code}"

        # Check if the response content is as expected
        assert b"Webhallen products" in response.content, "Response content does not contain 'Webhallen products'"
        assert b"<p>0 products.</p>" in response.content, "Response content does not contain the number of products"
        assert (
            b"<li>No products yet.</li>" in response.content
        ), "Response content does not contain the list of products"

        # Check if the context is as expected
        assert response.context["canonical_url"] == "https://panso.se/webhallen/", "Canonical URL is not as expected"


@pytest.mark.django_db()
@pytest.mark.parametrize("debug_mode", [True, False], ids=["debug_mode_true", "debug_mode_false"])
@pytest.mark.parametrize(
    "url",
    ["/webhallen/1/", "/webhallen/1", lambda: reverse("webhallen:webhallen_product", kwargs={"product_id": 1})],
    ids=["url_webhallen_product", "url_webhallen_product_slash", "url_webhallen_product_reverse"],
)
def test_can_access_webhallen_product(client: Client, debug_mode: bool, url: str) -> None:
    """Test if a user can access a Webhallen product page."""
    with override_settings(DEBUG=debug_mode):
        # Resolve the URL for the lambda function
        if callable(url):
            url = url()

        # Create the product
        product: WebhallenProduct = WebhallenProduct.objects.create(
            product_id=1,
            name="Test product",
            url="https://example.com",
        )

        # Create the JSON
        WebhallenJSON.objects.create(
            product=product,
            scraped_url="https://example.com/json",
            json={
                "product": {
                    "name": "Test product",
                },
            },
        )

        # Access the admin page
        response: HttpResponse = client.get(url, follow=True)

        # Check if the response is as expected
        assert response.status_code == 200, f"Response status code: {response.status_code}"

        # Check if the response content is as expected
        assert b"Test product" in response.content, "Response content does not contain 'Test product'"

        assert (
            f"<h1>{product.name}</h1>".encode() in response.content
        ), "Response content does not contain the product name"

        # Check if the context is as expected
        assert response.context["canonical_url"] == "https://panso.se/webhallen/1/", "Canonical URL is not as expected"
        assert response.context["product"].product_id == 1, "Product ID is not as expected"
        assert response.context["product"].name == "Test product", "Product name is not as expected"

        # Check the JSON
        assert b"<code>{&#x27;product&#x27;:" in response.content, "Response content does not contain the JSON data"


@pytest.mark.django_db()
@pytest.mark.parametrize("debug_mode", [True, False], ids=["debug_mode_true", "debug_mode_false"])
@pytest.mark.parametrize(
    "url",
    ["/webhallen/1/", "/webhallen/1", lambda: reverse("webhallen:webhallen_product", kwargs={"product_id": 1})],
    ids=["url_webhallen_product", "url_webhallen_product_slash", "url_webhallen_product_reverse"],
)
def test_can_access_webhallen_product_404(client: Client, debug_mode: bool, url: str) -> None:
    """Test if a user can access a Webhallen product page that does not exist."""
    with override_settings(DEBUG=debug_mode):
        # Resolve the URL for the lambda function
        if callable(url):
            url = url()

        # Access the admin page
        response: HttpResponse = client.get(url, follow=True)

        # Check if the response is as expected
        assert response.status_code == 404, f"Response status code: {response.status_code}"


@pytest.mark.django_db()
@pytest.mark.parametrize("debug_mode", [True, False], ids=["debug_mode_true", "debug_mode_false"])
def test_webhallen_model_str(debug_mode: bool) -> None:
    """Test the __str__ method of the WebhallenJSON and WebhallenProduct models."""
    with override_settings(DEBUG=debug_mode):
        # Create the product
        product: WebhallenProduct = WebhallenProduct.objects.create(
            product_id=1,
            name="Test product",
            url="https://example.com",
        )

        # Create the JSON
        json: WebhallenJSON = WebhallenJSON.objects.create(
            product=product,
            scraped_url="https://example.com",
            json={},
        )

        # Check if the __str__ method is as expected
        assert (str(product)) == "1 - Test product", f"__str__ method: {product!s}"

        first = str(product.jsons.first())  # type: ignore  # noqa: PGH003
        assert first == "1 - Test product - https://example.com", f"__str__ method: {product.jsons.first()!s}"  # type: ignore  # noqa: PGH003
        assert (str(json)) == "1 - Test product - https://example.com", f"__str__ method: {json!s}"

        # Check if the __repr__ method is as expected
        assert (repr(product)) == "<WebhallenProduct: 1 - Test product>", f"__repr__ method: {product!r}"
        assert (
            (repr(product.jsons.first())) == "<WebhallenJSON: 1 - Test product - https://example.com>"  # type: ignore  # noqa: PGH003
        ), f"__repr__ method: {product.jsons.first()!r}"  # type: ignore  # noqa: PGH003
