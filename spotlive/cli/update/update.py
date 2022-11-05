import click
from ..spot_cli import SpotCli, pass_spotcli
import logging
module_logger = logging.getLogger(__name__)
import os

@click.command()
@click.argument('playlist_name')
@click.option('--venue', '-v', default=[], multiple = True, help='Venue for artist lookup. Can be passed multiple times')
@click.option('--city', default='', help='City for artist lookup')
@click.option('--tracks_per_artist', '-t', default = 5, help='Number of tracks per artist to add to playlist')
@click.option('--shuffle', default = False, is_flag = True, help='If True, Select random tracks per artist. If False, use top tracks.')
@click.option('--clear_playlist', '-c', default = False, is_flag = True, help='If True, clear playlist before adding to it.')
@click.option('--start_date', '-s', default = None, help='Start Date for events in YYYY-MM-DD or similar (readble by pandas.to_datetime)')
@click.option('--days_forward', '-d', default = 30, help='Number of days forward from start_date to search for events.')
@click.option('--tm_path', envvar='tm_path'.upper(), default = None, help='path to json file with ticketmaster API credentials')
@click.option('--spotify_path', envvar='spotify_path'.upper(), default = None, help='path to json file with spotify API credentials')
@pass_spotcli
def update(
    spotcli,
    playlist_name,
    venue,
    city,
    tracks_per_artist,
    shuffle,
    clear_playlist,
    start_date,
    days_forward,
    tm_path,
    spotify_path
    ):
    if (tm_path is not None) & (spotify_path is not None):
        spotcli = SpotCli(tm_path, spotify_path, start_date, days_forward)
        print(f"Got instance of SpotCli for: {spotcli.spotlive.start_date}")
    try:
        all_events = spotcli.spotlive.get_events_by_venue(
            venues = list(venue),
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
    # append. creating if necessary
    spotcli.spotlive.append_playlist(
        playlist_name = playlist_name,
        artists = artists,
        tracks_per_artist = tracks_per_artist,
        shuffle = shuffle,
        clear_playlist = clear_playlist,
        )