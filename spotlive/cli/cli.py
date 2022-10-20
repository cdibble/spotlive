import click
from spotlive import SpotLive
import json
import os

## Update Playlists from Config Json
@click.group()
def auth():
    pass

@click.group()
def update():
    pass

@update.command()
@click.option('--ticketmaster_json_path', default=os.environ.get('ticketmaster_json_path'.upper(), ''), help='path to json file with ticketmaster API credentials')
@click.option('--spotify_json_path', default=os.environ.get('spotify_json_path'.upper(), ''), help='path to json file with spotify API credentials')
@click.option('--config_path', default='', help='path to json file with SpotLive playlist configs')
def update_from_json(ticketmaster_json_path, spotify_json_path, config_path):
    spotify_app_creds = get_creds(spotify_json_path)
    ticketmaster_app_creds = get_creds(ticketmaster_json_path)
    sl = SpotLive(
        spotify_app_creds=spotify_app_creds,
        ticketmaster_app_creds=ticketmaster_app_creds
        )
    sl.update_from_config(config = config_path)
    pass


def get_creds(json_path):
    with open(json_path) as f:
        creds = json.loads(f.read())
    return creds

if __name__ == '__main__':
    print('hello')