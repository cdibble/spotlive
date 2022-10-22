import click
from ..spot_cli import SpotCli, pass_spotcli
import logging
module_logger = logging.getLogger(__name__)

@click.command()
@click.argument('config_path')
@click.option('--tracks_per_artist', '-t', default = 5, help='Number of tracks per artist to add to playlist')
@click.option('--shuffle', default = False, is_flag = True, help='If True, Select random tracks per artist. If False, use top tracks.')
@click.option('--clear_playlist', '-c', default = False, is_flag = True, help='If True, clear playlist before adding to it.')
@click.option('--tm_path', envvar='tm_path'.upper(), default = None, help='path to json file with ticketmaster API credentials')
@click.option('--spotify_path', envvar='spotify_path'.upper(), default = None, help='path to json file with spotify API credentials')
@pass_spotcli
def from_config(spotcli, config_path, tracks_per_artist, shuffle, clear_playlist, tm_path, spotify_path):
    if (tm_path is not None) & (spotify_path is not None):
        spotcli = SpotCli(tm_path, spotify_path)
    try:
        spotcli.spotlive.update_from_config(
            config = config_path,
            tracks_per_artist = tracks_per_artist,
            shuffle = shuffle,
            clear_playlist = clear_playlist,
            )
    except AttributeError:
        module_logger.error(f"Could not initiate SpotLive. Did you pass Spotify and Tickematser configs? See `spotlive update --help`.")