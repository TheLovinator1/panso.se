import re
from pathlib import Path

import pytest
from django.conf import settings


def get_env_variables_from_settings() -> list[str]:
    """Get environment variables from settings.py.

    Returns:
        list: List of environment variables used in settings.py.
    """
    env_vars: list[str] = [
        match.group(1)
        for attr in dir(settings)
        for value in [getattr(settings, attr)]
        if isinstance(value, str)
        for match in re.finditer(r'os\.getenv\(\s*(?:key\s*=\s*)?[\'"](.+?)[\'"]', value)
    ]
    return env_vars


def get_env_variables_from_file(file_path: str) -> list[str]:
    """Get environment variables from a file.

    Args:
        file_path: Path to the file.

    Returns:
        list: List of environment variables in the file.
    """
    env_vars: list[str] = []

    with Path(file_path).open(encoding="locale") as file:
        for line in file:
            match: re.Match[str] | None = re.match(r"\s*([A-Z_]+)\s*=", line)
            if match:
                env_vars.append(match.group(1))
    return env_vars


@pytest.mark.django_db()
def test_env_variables_in_env_example() -> None:
    """Test that all environment variables in settings.py are in .env.example."""
    # Get environment variables from settings.py
    env_vars_settings: list[str] = get_env_variables_from_settings()

    # Get environment variables from .env.example
    env_vars_example: list[str] = get_env_variables_from_file(".env.example")

    # Check that all environment variables from settings.py are in .env.example
    missing_vars: list[str] = [var for var in env_vars_settings if var not in env_vars_example]
    assert not missing_vars, f"Missing environment variables in .env.example: {missing_vars}"
