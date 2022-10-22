import click
from spotlive import SpotLive
from .spot_cli import SpotCli, pass_spotcli
from .update.update import update

# Core CLI group
@click.group()
@click.option('--tm_path', envvar='tm_path'.upper(), help='path to json file with ticketmaster API credentials')
@click.option('--spotify_path', envvar='spotify_path'.upper(), help='path to json file with spotify API credentials')
@click.pass_context
def spotlive(ctx, tm_path, spotify_path):
    ctx.obj = SpotCli(tm_path, spotify_path)

spotlive.add_command(update)


# # @update.command()
# def update_from_json(tm_path, spotify_path, config_path):
#     spotify_app_creds = get_creds(spotify_path)
#     ticketmaster_app_creds = get_creds(tm_path)
#     sl = SpotLive(
#         spotify_app_creds=spotify_app_creds,
#         ticketmaster_app_creds=ticketmaster_app_creds
#         )
#     sl.update_from_config(config = config_path)
#     pass

# # auth.add_command(update_from_json)

# # @click.group()
# @click.command()
# @click.option('--tm_path', default=os.environ.get('tm_path'.upper(), ''), help='path to json file with ticketmaster API credentials')
# @click.option('--spotify_path', default=os.environ.get('spotify_path'.upper(), ''), help='path to json file with spotify API credentials')
# @click.option('--artists', default='', help='path to json file with SpotLive playlist configs')
# @click.option('--playlist_name', default='', help='path to json file with SpotLive playlist configs')
# def update_playlist(playlist_name, artists, tm_path, spotify_path):
#     spotify_app_creds = get_creds(spotify_path)
#     ticketmaster_app_creds = get_creds(tm_path)
#     sl = SpotLive(
#         spotify_app_creds=spotify_app_creds,
#         ticketmaster_app_creds=ticketmaster_app_creds
#         )
#     sl.spot.add_to_playlist(playlist_id = playlist_name, artists = artists)
#     pass




if __name__ == '__main__':
    print('hello')