"""
This module provides the command line interface (CLI) for The Cosmic Cafeteria.

Available commandes are:

- `tcc`: The main command for The Cosmic Cafeteria.
- `tcc --version`: Displays the version of The Cosmic Cafeteria.
- `tcc --help`: Displays help information.
- `tcc hero`: Manages heroes: `create`, `read`, `update`, and `delete`.
- `tcc meal`: Manages meals: `create`, `read`, `update`, and `delete`.
- `tcc order`: Manages orders: `create`, `read`, `update`, and `delete`.
"""
import click

from cli.__about__ import __version__


@click.group(context_settings={"help_option_names": ["-h", "--help"]}, invoke_without_command=True)
@click.version_option(version=__version__, prog_name="the-cosmic-cafeteria")
def main_cmd():
    click.echo("Hello world!")
