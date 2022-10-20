import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import traceback
import logging 
module_logger = logging.getLogger(__name__)

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
                scope="user-library-read,playlist-modify-private,playlist-modify-public")
            )
        self.user_id = user_id if user_id else spotify_app_creds.get('user_id')
    def get_playlists(self, user: str = 'spotify'):
        playlists = self.spot.user_playlists(user)
        # playlists = self.spot.current_user_playlists()
        all_playlists=[]
        while playlists:
            for i, playlist in enumerate(playlists['items']):
                # print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
                all_playlists.append(playlist)
            if playlists['next']:
                playlists = self.spot.next(playlists)
            else:
                playlists = None
        return all_playlists
    def set_user_playlists(self, user_id: str = None):
        if not user_id:
            user_id = self.user_id
        self.playlists = self.get_playlists(user = user_id)
    def create_playlist(self, name: str, user_id: str = None, public: bool = False, collaborative: bool = False, description: str = ''):
        if not user_id:
            user_id = self.user_id
        return self.spot.user_playlist_create(
            user = user_id,
            name = name,
            public = public, 
            collaborative= collaborative,
            description = description
        )
    def add_to_playlist(self, playlist_id: str = None, artists: list = []):
        added_tracks = {}
        for artist in artists:
            arts = self.lookup_artist(name = artist, return_type = 'track')
            tracks = [x['uri'] for x in arts['tracks']['items']]
            print(f"artist: {artist}")
            print(f"tracks: {tracks}")
            if len(tracks) > 0:
                try:
                    self.spot.playlist_add_items(
                        playlist_id = playlist_id,
                        items = tracks
                    )
                except Exception as e:
                    traceback.format_exc()
                    pass
            added_tracks[artist] = tracks
        return added_tracks
    def get_saved_tracks(self):
        results = self.spot.current_user_saved_tracks()
        for idx, item in enumerate(results['items']):
            track = item['track']
            print(idx, track['artists'][0]['name'], " – ", track['name'])
    def lookup_artist(self, name: str, return_type: str = 'track', limit: int = 10):
        '''
        return_type - the types of items to return. One or more of 'artist', 'album', 'track', 'playlist', 'show', and 'episode'. If multiple types are desired, pass in a comma separated string; e.g., 'track,album,episode'.
        limit - max items to return; <= 50
        '''
        results = self.spot.search(q = 'artist:' + name, type = return_type, limit = limit)
        return results


def main():
    with open('secrets/spotify_app_creds.json') as f:
        spotify_app_creds = json.loads(f.read())
    spot = Spot(spotify_app_creds, user_id = spotify_app_creds['user_id'])
