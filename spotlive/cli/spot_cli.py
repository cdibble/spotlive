import click
from spotlive import SpotLive
import json

class SpotCli(object):
    def __init__(self, tm_path, spotify_path, start_date: str = None, days_forward: int = 30):
        try:
            self.ticketmaster_app_creds = self.get_creds(tm_path)
        except TypeError:
            self.ticketmaster_app_creds = {}
        try:
            self.spotify_app_creds = self.get_creds(spotify_path)
        except TypeError:
            self.spotify_app_creds = {}
        try:
            print(f"here start_date: {start_date}")
            print(f"days_forward: {days_forward}")
            self.spotlive = SpotLive(
                spotify_app_creds = self.spotify_app_creds,
                ticketmaster_app_creds = self.ticketmaster_app_creds,
                start_date = start_date,
                days_forward = days_forward
                )
        except:
            self.spotlive = None
    def get_creds(self, json_path):
        with open(json_path) as f:
            creds = json.loads(f.read())
        return creds

pass_spotcli = click.make_pass_decorator(SpotCli)
