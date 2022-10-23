from spotify import Spot
from ticketmaster import Shows
import json
from datetime import datetime, timedelta
from dateutil import parser
import logging
module_logger = logging.getLogger(__name__)

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
        radius_mi: int = 10,
        classification: str = None
        ):
        if not venues:
            venues = self.shows.venue_search(city=city, radius_mi=radius_mi, latlong=latlong)
        # If venues are passed as strings, perform a lookup to get venue.id
        for i in range(len(venues)):
            if isinstance(venues[i], str):
                venue_i = self.shows.venue_search(
                    keyword = venues[i],
                    city=city,
                    radius_mi=radius_mi,
                    latlong=latlong
                    )
                # venue_i = list(set(venue_i))
                print([x.name for x in venue_i])
                if len(venue_i) > 1:
                    module_logger.warning(f"Venue lookup returned more than one possible result. Pass city or latlong/radius_mi to narrow down the results. {venue_i}")
                    venues[i] = venue_i[0]
                    venues.extend(venue_i[1:])
                else:
                    venues[i] = venue_i[0]
        # venues = self.shows.venue_search(latlong='28,-120', radius_mi = 800)
        all_events={}
        for venue in venues:
            try:
                all_events[venue] = self.shows.event_search(
                    start_date_time=self.start_date,
                    end_date_time=self.end_date,
                    venue_id=venue.id,
                    classification=classification
                )
            except:
                module_logger.info(f"failed with: {venue.name}")
                all_events[venue] = []
        return all_events
    def append_playlist(self, playlist_name: str, artists: list, tracks_per_artist: int, clear_playlist: bool = False, shuffle: bool = False):
        playlist = [x for x in self.playlists if x.get('name','') == playlist_name]
        if len(playlist) == 0:
            module_logger.info(f'creating playlist {playlist}')
            playlist = self.spot.create_playlist(
                name = playlist_name,
                user_id = self.spot.user_id,
                public=True
                )
        else:
            playlist = playlist[0]
        module_logger.info(f"Proceeding with playlist_id: {playlist['id']}")
        self.spot.add_to_playlist(
            playlist_id = playlist['id'],
            artists = artists,
            tracks_per_artist = tracks_per_artist,
            clear_playlist = clear_playlist,
            shuffle = shuffle
            )
    def update_from_config(self, config: dict = None):
        '''
        Params
        ------
        config: dict
            'include_city_venues': bool
                Whether to lookup venues in `cities`; if False, just use `cities` to narrow search for given `venues`.

        Example Config:
        {
            "playlist_name": "Casbah_1",
            "venues": ["Casbah"],
            "cities": ["San Diego"],
            "include_city_venues": false,
            "venue_exclude": [],
            "artist_exclude": [],
            "genre": null,
            "days_ahead": null,
            "clear_playlist": false,
            "tracks_per_artist": 5,
            "shuffle": false
        }
        '''
        if isinstance(config, str):
            # assume it's a path to json
            with open(config) as f:
                config = json.loads(f.read())
        module_logger.info(f"Updating playlist using config: {config}")
        for playlist_config in config:
            playlist_name = playlist_config.get('playlist_name')
            module_logger.warning(f"Updating playlist: {playlist_name}")
            if not playlist_name:
                raise ValueError("playlist_config must include key 'playlist_name' for the playlist to create or append")
            all_venues = playlist_config.get('venues', [])
            if playlist_config.get('cities'):
                if playlist_config.get('include_city_venues', False):
                    city_venues = []
                    for city in playlist_config.get('cities'):
                        city_venues.extend(
                            self.shows.venue_search(
                                city = city
                                )
                        )
                    all_venues.extend(city_venues)
            venues = [x for x in all_venues if x not in playlist_config.get('venue_exclude', [])]
            module_logger.info(f"Updating playlist using venues: {venues}")
            if playlist_config.get('days_ahead'):
                self.end_date = (parser.parse(self.start_date) + timedelta(days=int(playlist_config.get('days_ahead')))).isoformat()
            all_events = {}
            for city in playlist_config.get('cities', [None]):
                module_logger.warning(f"Getting events for {venues} in {city}")
                all_events = {**all_events,
                    **self.get_events_by_venue(
                        venues = venues,
                        city = city,
                        # classification = playlist_config.get('genre')
                    )
                }
            artists = []
            for venue, events in all_events.items():
                # print(venue.name)
                artists.extend(
                    [e.name for e in events if e.name not in playlist_config.get('artist_exclude', [])]
                )
            module_logger.debug(f"Updating playlist using artists: {artists}")
            self.append_playlist(
                playlist_name = playlist_name,
                artists = artists,
                clear_playlist = playlist_config.get('clear_playlist', False),
                shuffle = playlist_config.get('shuffle', False),
                tracks_per_artist = playlist_config.get('tracks_per_artist', 5)
                )
            module_logger.info(f"Ok. Updated {playlist_name}")



def main():
    from SpotLive.spotlive import SpotLive
    with open('secrets/ticketmaster_app_creds.json') as f:
        ticketmaster_app_creds = json.loads(f.read())
    with open('secrets/spotify_app_creds.json') as f:
        spotify_app_creds = json.loads(f.read())
    sl = SpotLive(spotify_app_creds=spotify_app_creds, ticketmaster_app_creds=ticketmaster_app_creds)
    sl.update_from_config(config = 'test/test_config.json')
    venues = sl.shows.venue_search(city='San Diego', radius_mi = 20, limit = 200)
    venues = sl.shows.venue_search(keyword='Casbah', city = 'San Diego')
    venue_names = [x.name for x in venues]
    all_events = sl.get_events_by_venue(venues = venues)
    all_events = sl.get_events_by_venue(venues = ['Casbah'], city = 'San Diego')
    artists = []
    for venue, events in all_events.items():
        artists.extend(
            [e.name for e in events if e.name not in {}.get('artist_exclude', [])]
        )
    artists = [e.name for e in events]
    artists = ['Minus The Bear']
    # for artist in artists:
    #     arts = sl.spot.lookup_artist(artist, return_type='artist,track')
    #     tracks = [x['uri'] for x in arts['tracks']['items']]
    #     [x['uri'] for x in arts['tracks']['items']]
    sl.append_playlist(playlist_name='tester_list2', artists = artists)

