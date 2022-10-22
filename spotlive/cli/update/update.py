import click
from ..spot_cli import SpotCli, pass_spotcli
import logging
module_logger = logging.getLogger(__name__)
import os

@click.command()
@click.argument('playlist_name')
@click.option('--venue', '-v', default=[], multiple = True, help='Venue for artist lookup. Can be passed multiple times')
@click.option('--city', default='', help='City for artist lookup')
@click.option('--tm_path', envvar='tm_path'.upper(), default = None, help='path to json file with ticketmaster API credentials')
@click.option('--spotify_path', envvar='spotify_path'.upper(), default = None, help='path to json file with spotify API credentials')
@pass_spotcli
def update(spotcli, playlist_name, venue, city, tm_path, spotify_path):
    if (tm_path is not None) & (spotify_path is not None):
        spotcli = SpotCli(tm_path, spotify_path)
    try:
        all_events = spotcli.spotlive.get_events_by_venue(
            venues = venue,
            city = city
            )
    except AttributeError:
        module_logger.error(f"Could not initiate SpotLive. Did you pass Spotify and Ticketmaster configs? See `spotlive update_playlist --help`.")
    # pull artists from event objects
    artists = []
    for venue, events in all_events.items():
        artists.extend(
            [e.name for e in events]
        )
    spotcli.spotlive.spot.add_to_playlist(
        playlist_id = playlist_name,
        artists = artists
        )
