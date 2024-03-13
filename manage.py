from __future__ import annotations

import os
from datetime import datetime

import django
import typer
from django.core.management import call_command
from rich import print

# Set the Django settings module
os.environ.setdefault(key="DJANGO_SETTINGS_MODULE", value="panso.settings")
django.setup()

app = typer.Typer(
    name="panso",
    help="The panso.se management utility.",
    add_completion=False,
    no_args_is_help=True,
    pretty_exceptions_enable=True,
)


@app.command()
def migrate() -> None:
    """Apply database migrations."""
    # Take a backup of the database before migrating
    file_safe_datetime = datetime.now(tz=datetime.now().astimezone().tzinfo).strftime(
        "%Y-%m-%d_%H-%M-%S",
    )
    call_command(
        command_name="dumpdata",
        output=f"data/backup/{file_safe_datetime}.json.gz",
        format="json",
    )
    call_command(command_name="migrate")
    print("[green]Migrations applied.[/green]")


@app.command()
def runserver() -> None:
    """Run the development server."""
    migrate()

    call_command(command_name="runserver")


@app.command()
def serve() -> None:
    """Alias for runserver."""
    runserver()


@app.command()
def createsuperuser() -> None:
    """Create a superuser."""
    call_command(command_name="createsuperuser")
    print("[green]Superuser created.[/green]")


@app.command()
def collectstatic() -> None:
    """Collect static files."""
    call_command(command_name="collectstatic", interactive=False)


@app.command()
def test() -> None:
    """Run tests."""
    call_command(command_name="test")
    print("[green]Tests passed.[/green]")


@app.command()
def makemigrations() -> None:
    """Make migrations."""
    call_command(command_name="makemigrations")
    print("[green]Migrations created.[/green]")
    print("[yellow]Please run `migrate` to apply the migrations.[/yellow]")


if __name__ == "__main__":
    app()
