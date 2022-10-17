import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

class Spot:
    def __init__(self, spotify_app_creds: dict, user_id: str = None):
        '''
        Auth with Spotify App

        params
        --------
        spotify_app_creds: dict
            client_id, client_secret, redirect_uri for a Spotify App
        '''
        self.spot = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=spotify_app_creds.get('client_id'),
                client_secret=spotify_app_creds.get('client_secret'),
                redirect_uri=spotify_app_creds.get('redirect_uri'),
                scope="user-library-read")
            )
        self.user_id = user_id
    def get_playlists(self, user: str = 'spotify'):
        playlists = self.spot.user_playlists('spotify')
        # playlists = self.spot.current_user_playlists()
        while playlists:
            for i, playlist in enumerate(playlists['items']):
                print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
            if playlists['next']:
                playlists = self.spot.next(playlists)
            else:
                playlists = None
        return playlists
    def set_user_playlists(self, user_id: str = None):
        if not user_id:
            user_id = self.user_id
        self.playlists = self.get_playlists(user = user_id)
    def create_playlist(self, name: str, user_id: str = None, public: bool = False, collaborative: bool = False, description: str = ''):
        if not user_id:
            user_id = self.user_id
        self.spot.user_playlist_create(
            user = user_id,
            name = name,
            public = public, 
            collaborative= collaborative,
            description = description
        )
    def add_to_playlist(self, playlist_id: str = None, items: list = []):
        self.spot.playlist_add_items(
            playlist_id=playlist_id,
            items = items
        )
    def get_saved_tracks(self):
        results = self.spot.current_user_saved_tracks()
        for idx, item in enumerate(results['items']):
            track = item['track']
            print(idx, track['artists'][0]['name'], " – ", track['name'])
    def lookup_artist(self, name: str):
        name = 'Radiohead'
        results = self.spot.search(q='artist:' + name, type='artist')
        items = results['artists']['items']
        if len(items) > 0:
            artist = items[0]
            print(artist['name'], artist['images'][0]['url'])


def main():
    with open('secrets/spotify_app_creds.json') as f:
        spotify_app_creds = json.loads(f.read())
    spot = Spot(spotify_app_creds)
