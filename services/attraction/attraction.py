# Dummy Attraction
# All class name default as service
from services.attraction.api import db_api
class service():

    def __init__(self):
        pass

    def test(self):
        print('request attraction service succeed')

    def test_db_connection(self):
        data = db_api.test()
        return data

    def look_up_place_data_and_render(self):
        pass

    def post_attraction(self, name, lat, lng, 
            intro, rating, cover_file, marker_file,
            user_id
        ):
        pass