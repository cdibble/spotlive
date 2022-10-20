import click
from spotlive import SpotLive
import json
import os

## Update Playlists from Config Json
@click.group()
def auth():
    pass

# @click.group()
# def update():
#     pass


# @update.command()
@click.group()
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

@click.group()
@click.command()
@click.option('--ticketmaster_json_path', default=os.environ.get('ticketmaster_json_path'.upper(), ''), help='path to json file with ticketmaster API credentials')
@click.option('--spotify_json_path', default=os.environ.get('spotify_json_path'.upper(), ''), help='path to json file with spotify API credentials')
@click.option('--artists', default='', help='path to json file with SpotLive playlist configs')
@click.option('--playlist_name', default='', help='path to json file with SpotLive playlist configs')
def update_playlist(playlist_name, artists, ticketmaster_json_path, spotify_json_path):
    spotify_app_creds = get_creds(spotify_json_path)
    ticketmaster_app_creds = get_creds(ticketmaster_json_path)
    sl = SpotLive(
        spotify_app_creds=spotify_app_creds,
        ticketmaster_app_creds=ticketmaster_app_creds
        )
    sl.spot.add_to_playlist(playlist_id = playlist_name, artists = artists)
    pass


def get_creds(json_path):
    with open(json_path) as f:
        creds = json.loads(f.read())
    return creds



class Repo(object):
    def __init__(self, home=None, debug=False):
        self.home = os.path.abspath(home or '.')
        self.debug = debug


@click.group()
@click.option('--repo-home', envvar='REPO_HOME', default='.repo')
@click.option('--debug/--no-debug', default=False,
              envvar='REPO_DEBUG')
@click.pass_context
def cli(ctx, repo_home, debug):
    ctx.obj = Repo(repo_home, debug)



if __name__ == '__main__':
    print('hello')