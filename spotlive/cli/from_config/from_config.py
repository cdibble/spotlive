import click
from ..spot_cli import SpotCli, pass_spotcli
import logging
module_logger = logging.getLogger(__name__)

@click.command()
@click.argument('config_path')
@click.option('--tm_path', envvar='tm_path'.upper(), default = None, help='path to json file with ticketmaster API credentials')
@click.option('--spotify_path', envvar='spotify_path'.upper(), default = None, help='path to json file with spotify API credentials')
@pass_spotcli
def from_config(spotcli, config_path, tm_path, spotify_path):
    if (tm_path is not None) & (spotify_path is not None):
        spotcli = SpotCli(tm_path, spotify_path)
    try:
        spotcli.spotlive.update_from_config(
            config = config_path
            )
    except AttributeError:
        module_logger.error(f"Could not initiate SpotLive. Did you pass Spotify and Tickematser configs? See `spotlive update --help`.")