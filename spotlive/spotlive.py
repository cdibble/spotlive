from spotify import Spot
from ticketmaster import Shows
import json
from datetime import datetime, timedelta
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
        self.start_date = start_date if start_date else datetime.utcnow().replace(microsecond=0).isoformat()
        self.end_date = (parser.parse(self.start_date) + timedelta(days=days_forward)).isoformat()
    def get_events_by_venue(self, zipcode: str = None, latlong: str = None, radius_mi: int = None):
        venues = self.shows.venue_search(zipcode=zipcode, radius_mi=radius_mi, latlong=latlong)
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
                print(venue.name)
    def get_(self):
        pass


def main():
    with open('secrets/ticketmaster_app_creds.json') as f:
        ticketmaster_app_creds = json.loads(f.read())
    with open('secrets/spotify_app_creds.json') as f:
        spotify_app_creds = json.loads(f.read())
    sl = SpotLive(spotify_app_creds=spotify_app_creds, ticketmaster_app_creds=ticketmaster_app_creds)
    sl.get_events_by_venue(latlong='32,-123')

main()