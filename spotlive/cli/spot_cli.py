import click
from spotlive import SpotLive
import json
import os

class SpotCli(object):
    def __init__(self, tm_path, spotify_path):
        try:
            self.ticketmaster_app_creds = self.get_creds(tm_path)
        except TypeError:
            self.ticketmaster_app_creds = {}
        try:
            self.spotify_app_creds = self.get_creds(spotify_path)
        except TypeError:
            self.spotify_app_creds = {}
        try:
            self.spotlive = SpotLive(
                spotify_app_creds = self.spotify_app_creds,
                ticketmaster_app_creds = self.ticketmaster_app_creds
                )
        except:
            self.spotlive = None
    def get_creds(self, json_path):
        with open(json_path) as f:
            creds = json.loads(f.read())
        return creds

pass_spotcli = click.make_pass_decorator(SpotCli)
