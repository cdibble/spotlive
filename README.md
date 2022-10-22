# SpotLive
Create Spotify playlists based on upcoming shows at your chosen venues

## Requirements
Uses Python 3.8+ and these modules (see `requirements.txt` for updates).
```python
spotipy
ticketpy
geopy
```

## Credentials
Needs API credentials for Spotify and Ticketmaster.

Ticketmaster looks like:
```json
{"consumer_key": "**", "consumer_secret": "**"}
```
For info on creating Ticketmaster credentials: go [here](https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/#search-events-v2)



Spotify looks like:
```json
{"app_name": "Whatever", "client_id": "***", "client_secret": "***", "redirect_uri": "https://localhost", "user_id": "***"}
```
For info on creating Spotify credentials: go [here](https://developer.spotify.com/documentation/general/guides/authorization/code-flow/)


## Usage
### CLI
This package includes a CLI program for creating/updating playlists from configs or via command line arguments that specify venues or areas of interest.

Update playlist(s) from a json config
```bash
spotlive update --tm_path TICKETMASTER_CREDS_APTH --spotify_path SPOTIFY_CREDS_PATH CONFIG_PATH
```
### Configs

```json
{
    "playlist_name": "Casbah_1",
    "venues": ["Casbah"],
    "city": ["San Diego"],
    "venue_exclude": [],
    "artist_exclude": [],
    "days_ahead": null
}
```
### Python Modules
You can of course invoke the python modules directly. To update from a config json, for example:

```python
with open('secrets/ticketmaster_app_creds.json') as f:
    ticketmaster_app_creds = json.loads(f.read())
with open('secrets/spotify_app_creds.json') as f:
    spotify_app_creds = json.loads(f.read())
sl = SpotLive(spotify_app_creds=spotify_app_creds, ticketmaster_app_creds=ticketmaster_app_creds)
sl.update_from_config(config = 'test/test_config.json')
```

You can use `SpotLive` to link together `Spotify` and `Shows` and perform artists and venue lookups, etc., to decide how to build playlists. See below for some example usage.

**SpotLive**
```python
sl = SpotLive(spotify_app_creds=spotify_app_creds, ticketmaster_app_creds=ticketmaster_app_creds)
# update a playlist from a config json
sl.update_from_config(config = 'test/test_config.json')
# get events for a venue search
all_events = sl.get_events_by_venue(venues = ['Casbah'], city = 'San Diego')
# pull artists from event objects
artists = []
for venue, events in all_events.items():
    artists.extend(
        [e.name for e in events]
    )
# append playlist with artists
sl.append_playlist(playlist_name='tester_list2', artists = artists)
```


**Spotify**
```python
spot = Spot(spotify_app_creds, user_id = spotify_app_creds['user_id'])
# get existing playlist
playlist_name = 'my_example'
existing_playlists = spot.get_playlists()
playlist = [x for x in existing_playlists if x.get('name','') == playlist_name]
# create new playlist
playlist = spot.create_playlist(
    name = playlist_name
)
# add artist to playlist
spot.add_to_playlist(
    playlist_id = playlist['id']
    artists = ['Talking Heads']
)
# lookup artist tracks
artists = ['Minus The Bear']
for artist in artists:
    arts = spot.lookup_artist(artist, return_type='artist,track')
    tracks = [x['uri'] for x in arts['tracks']['items']]
```

**Ticketmaster**
```python
shows = Shows(ticketmaster_app_creds)
city_info = shows._city_lookup(city='San Diego')
# Look up Venues
venues = shows.venue_search(city='San Diego')
# Look up Events at a venue
for venue in venues:
    events = shows.event_search(
        start_date_time='2022-10-10T00:00:00Z',
        end_date_time='2022-10-15T00:00:00Z',
        venue_id=venue.id,
        zipcode='92101'
        )
# Lookup shows based on location and classification
# Get a list of upcoming artists (latlon|zipcode, radius)
classi = shows.classification_search(keyword='Music', limit = 500)
classification_names = list(set([g.name for g in x.segment.genres for x in classi]))
for classification_name in classification_names:
    events = shows.event_search(
        start_date_time='2022-01-10T00:00:00Z',
        end_date_time='2022-09-12T00:00:00Z',
        classification_name=classification_name,
        zipcode='92101'
        )
    [x.local_start_date for x in events]
```
