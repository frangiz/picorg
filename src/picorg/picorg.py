from pathlib import Path

import click

from picorg import __version__
from picorg.indexer import index_files
from picorg.rename import rename_files


@click.group()
@click.version_option(version=__version__, prog_name="picorg")
def cli():
    pass


@cli.command()
@click.option(
    "--root",
    default=".",
    help="The root folder to index",
    type=click.Path(exists=True),
)
def index(root: str) -> None:
    """Index all files in the given root folder"""
    index_files(Path(root))


@cli.command()
@click.option(
    "--folder",
    default=".",
    help="The folder to rename files in",
    type=click.Path(exists=True),
)
def rename(folder: str) -> None:
    """Rename all files in the current folder"""
    rename_files(folder)


@cli.command()
def hello() -> None:
    print("hello")


if __name__ == "__main__":
    cli()
