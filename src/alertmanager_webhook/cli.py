import asyncio
from pathlib import Path

import click

from .app import app
from .config import Config


@click.group()
def main() -> None:
    pass


@main.command()
@click.argument(
    "config_file", type=click.Path(exists=True, dir_okay=False, path_type=Path)
)
def serve(config_file: Path) -> None:
    config = Config.load(config_file)
    asyncio.run(app(config))
