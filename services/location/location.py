# Dummy Attraction
# All class name default as service
from services.location.api import db_api
from services.location import gmap_utility
class service():

    def __init__(self):
        pass

    def test(self):
        print('request attraction service succeed')

    def test_db_connection(self):
        data = db_api.test()
        return data

    def find_nearby_attractions(self, lat, lng):
        """
        the return format consists:
        [
            {'name', 'lat', 'lng', 'attraction_ID (or None)', 'ifProtected'}
        ]
        """
        gmap_places = gmap_utility.gps_to_place_list(lat, lng)
        #  db_places = db_api.get(...)
        # gmap_places.extend(db_places)
        data =  gmap_places
        return data
