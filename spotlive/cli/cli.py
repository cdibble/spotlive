import click
from .spot_cli import SpotCli, pass_spotcli
from .from_config.from_config import from_config

# Core CLI group
@click.group()
@click.option('--tm_path', envvar='tm_path'.upper(), help='path to json file with ticketmaster API credentials')
@click.option('--spotify_path', envvar='spotify_path'.upper(), help='path to json file with spotify API credentials')
@click.pass_context
def spotlive(ctx, tm_path, spotify_path):
    ctx.obj = SpotCli(tm_path, spotify_path)

spotlive.add_command(from_config)

