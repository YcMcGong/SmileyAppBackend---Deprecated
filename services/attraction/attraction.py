# Dummy Attraction
# All class name default as service
from services.attraction.api import db_api
from django.shortcuts import render

class service():

    def __init__(self):
        pass

    def test(self):
        print('request attraction service succeed')

    def test_db_connection(self):
        data = db_api.test()
        return data

    def look_up_place_data_and_render(self, ID):
        obj = db_api.place_look_up_object(ID)
        place_info, reviews_data = obj.get()
        reviews_data = reviews_data[0:-1]
        context = {'place_info': place_info, 'reviews_data': reviews_data}
        return render(None, 'services/attraction/templates/place.html', context)

    def post_attraction(self, name, lat, lng, 
            intro, rating, cover_file, marker_file,
            user_id
        ):
        obj = db_api.attraction_post(name, lat, lng, 
            intro, rating, cover_file, marker_file,
            user_id)

        return obj.push()

if __name__ == '__main__':
    pass