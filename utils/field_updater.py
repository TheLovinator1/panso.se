from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from django.db import models
    from django.db.models.base import Model

logger: logging.Logger = logging.getLogger(__name__)


def get_value(data: dict, key: str) -> datetime | str | None:
    """Get a value from a dictionary.

    We have this function so we can handle values that we need to convert to a different type. For example, we might
    need to convert a string to a datetime object.

    Args:
        data (dict): The dictionary to get the value from.
        key (str): The key to get the value for.

    Returns:
        datetime | str | None: The value from the dictionary
    """
    data_key: Any | None = data.get(key)
    if not data_key:
        return None

    # Dates are in the format "2025-01-04T19:23:15"
    dates: list[str] = ["endAt", "startAt", "createdAt", "earnableUntil"]
    if key in dates:
        date_str: str = data_key
        if date_str.endswith("Z"):
            date_str = date_str.replace("Z", "+00:00")
        return datetime.fromisoformat(date_str)

    # Timestamps are in the format 997588800
    if key == "timestamp":
        return datetime.fromtimestamp(data_key, tz=UTC)

    return data_key


def update_field(instance: models.Model, django_field_name: str, new_value: str | datetime | None) -> int:
    """Update a field on an instance if the new value is different from the current value.

    Args:
        instance (models.Model): The Django model instance.
        django_field_name (str): The name of the field to update.
        new_value (str | datetime | None): The new value to update the field with.

    Returns:
        int: 1 if the field was updated, 0 if it was not.
    """
    # Get the current value of the field.
    try:
        current_value = getattr(instance, django_field_name)
    except AttributeError:
        logger.exception("Field %s does not exist on %s", django_field_name, instance)
        return 0

    # Check for differences between current and new values.
    if isinstance(current_value, list) and isinstance(new_value, list):
        if sorted(current_value) != sorted(new_value):
            setattr(instance, django_field_name, new_value)
            return 1
    elif new_value and new_value != current_value:
        setattr(instance, django_field_name, new_value)
        return 1

    # 0 fields updated.
    return 0


def update_fields(instance: models.Model, data: dict, field_mapping: dict[str, str]) -> Model:
    """Update multiple fields on an instance using a mapping from external field names to model field names.

    Args:
        instance (models.Model): The Django model instance.
        data (dict): The new data to update the fields with.
        field_mapping (dict[str, str]): A dictionary mapping external field names to model field names. Left side is
            the json key and the right side is the model field name.

    Returns:
        models.Model: The updated instance.
    """
    updated_field_count = 0
    for json_field, django_field_name in field_mapping.items():
        try:
            data_key: datetime | str | None = get_value(data, json_field)
            updated_field_count += update_field(
                instance=instance,
                django_field_name=django_field_name,
                new_value=data_key,
            )
        except KeyError as e:
            logger.warning("Field %s not found in data. Error: %s", json_field, e)
        except Exception:
            logger.exception("Error updating field %s on instance %s", django_field_name, instance)

    if updated_field_count > 0:
        try:
            instance.save()
            logger.info("Updated %s fields for %s", updated_field_count, instance)
        except Exception:
            logger.exception("Error saving instance %s", instance)

    return instance
