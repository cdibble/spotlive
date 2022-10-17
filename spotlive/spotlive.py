from spotlive.spotify import Spot
from spotlive.ticketmaster import Shows
import json
from datetime import datetime, timedelta
import pytz
from dateutil import parser

class SpotLive:
    def __init__(
        self,
        spotify_app_creds: dict,
        ticketmaster_app_creds: dict,
        start_date: str = None,
        days_forward: int = 30
        ):
        self.spot = Spot(spotify_app_creds)
        self.shows = Shows(ticketmaster_app_creds)
        self.start_date = start_date if start_date else datetime.utcnow().replace(
            # tzinfo= pytz.UTC,
            microsecond=0
            ).isoformat() # 
        self.end_date = (parser.parse(self.start_date) + timedelta(days=days_forward)).isoformat()
        self.playlists = self.spot.get_playlists(user = spotify_app_creds['user_id'])
    def get_events_by_venue(
        self,
        venues: list = None,
        city: str = None,
        latlong: str = None,
        radius_mi: int = None
        ):
        if not venues:
            venues = self.shows.venue_search(city=city, radius_mi=radius_mi, latlong=latlong)
        # venues = self.shows.venue_search(latlong='28,-120', radius_mi = 800)
        all_events=[]
        for venue in venues:
            try:
                all_events.extend(
                    self.shows.event_search(
                        start_date_time=self.start_date,
                        end_date_time=self.end_date,
                        venue_id=venue.id,
                    )
                )
            except:
                print(f"failed with: {venue.name}")
        return all_events
    def append_playlist(self, playlist_name: str, artists: list):
        playlist = [x for x in self.playlists if x.get('name','') == playlist_name]
        if len(playlist) == 0:
            playlist = self.spot.create_playlist(name = playlist_name, user_id = self.spot.user_id)
            # ISSUE: this above call does not seem to return a playlist object or id
        else:
            playlist = playlist[0]
        self.spot.add_to_playlist(
            playlist_id = playlist['id'],
            artists = artists
            )


def main():
    with open('secrets/ticketmaster_app_creds.json') as f:
        ticketmaster_app_creds = json.loads(f.read())
    with open('secrets/spotify_app_creds.json') as f:
        spotify_app_creds = json.loads(f.read())
    sl = SpotLive(spotify_app_creds=spotify_app_creds, ticketmaster_app_creds=ticketmaster_app_creds)
    venues = sl.shows.venue_search(city='San Diego', radius_mi = 20, limit = 200)
    venues = sl.shows.venue_search(keyword='Casbah', city = 'San Diego')
    venue_names = [x.name for x in venues]
    events = sl.get_events_by_venue(venues = venues)
    artists = [e.name for e in events]
    sl.append_playlist(playlist_name='tester_list', artists = artists)
    for artist in artists:
        arts = sl.spot.lookup_artist(artist, return_type='artist,track')
        tracks = [x['uri'] for x in arts['tracks']['items']]
        [x['uri'] for x in arts['tracks']['items']]
