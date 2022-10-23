import ticketpy
import json
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim
import logging
module_logger = logging.getLogger(__name__)

class Shows:
    def __init__(self, ticketmaster_app_creds: dict):
        self.tm_client = ticketpy.ApiClient(ticketmaster_app_creds.get('consumer_key'))
    def _city_lookup(self, city: str):
        geolocator = Nominatim(user_agent="your_app_name")
        return geolocator.geocode(city)
    def venue_search(self, city: str = None, latlong: str = None, radius_mi: int = None, keyword: str = None, limit = 50, **kwargs):
        # https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/#search-venues-v2
        if city:
            city = self._city_lookup(city = city)
            latlong = f"{city.latitude},{city.longitude}"
        venues = self.tm_client.venues.find(
            latlong = latlong,
            radius = radius_mi,
            unit = 'miles',
            keyword = keyword,
            size = limit
            )
        locales = []
        while len(locales) < limit:
            venue_set = venues.one()
            if len(venue_set) == 0:
                break
            locales.extend(venue_set)
        return list(set(locales))
    def event_search(self, start_date_time: str, end_date_time: str, classification_name: list = None, zipcode: str = None, latlong: str = None, radius_mi: int = None, venue_id: str = None, limit = 50, **kwargs):
        # https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/#search-events-v2
        # start_date_time = start_date_time+'Z' if not start_date_time.endswith('Z') else start_date_time
        # end_date_time = end_date_time+'Z' if not end_date_time.endswith('Z') else end_date_time
        module_logger.debug(f"getting events from: {start_date_time} {end_date_time}")
        events = self.tm_client.events.find(
            start_date_time = start_date_time+'Z' if not start_date_time.endswith('Z') else start_date_time,
            end_date_time = end_date_time+'Z' if not end_date_time.endswith('Z') else end_date_time,
            classification_name = classification_name,
            postal_code = zipcode,
            # state_code='GA',
            latlong = latlong,
            radius = radius_mi,
            venue_id = venue_id,
            size = limit
        )
        all_events = []
        while len(all_events) < limit:
            venue_set = events.one()
            if len(venue_set) == 0:
                break
            all_events.extend(venue_set)
        return list(set(all_events))
    def classification_search(self, keyword: str = None, limit = 100):
        # https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/#search-events-v2
        classifications = self.tm_client.classifications.find(
            keyword=keyword
        )
        all_classifications = []
        while len(all_classifications) < limit:
            venue_set = classifications.one()
            if len(venue_set) == 0:
                break
            all_classifications.extend(venue_set)
        return all_classifications


def main():
    with open('secrets/ticketmaster_app_creds.json') as f:
        ticketmaster_app_creds = json.loads(f.read())
    shows = Shows(ticketmaster_app_creds)
    # Venue approach
    # Get list of venues (latlon|zipcode, radius)
    # Get list of artists playing those venues for some time window
    venues = shows._city_lookup(city='San Diego')
    venues = shows.venue_search(city='San Diego')
    for venue in venues:
        events = shows.event_search(
            start_date_time='2022-10-10T00:00:00Z',
            end_date_time='2022-10-15T00:00:00Z',
            venue_id=venue.id,
            zipcode='92101'
            )
    # Event approach
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
