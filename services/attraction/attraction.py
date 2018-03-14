# Dummy Attraction
# All class name default as service
from services.attraction.api import db_api
from services.attraction import utility
from django.shortcuts import render
import json

class service():

    def __init__(self):
        pass

    def test(self):
        print('request attraction service succeed')

    def test_db_connection(self):
        data = db_api.test()
        return data

#  ________________________________________
# |Moment Post                             |
# |________________________________________|

    def post_moment(self, name, lat, lng, 
            intro, rating, cover_file, user_id, is_custom = False):
        
        attraction_found = db_api.attraction_get(lat = lat, lng = lng)
        is_found = attraction_found.get()

        if is_found: # Attraction exist
            attraction_id = attraction_found.ID
            review = db_api.review_post(intro, rating, cover_file, user_id, attraction_id)
            review.post()

        else:
            marker_file = utility.resize_to_marker(cover_file) # resize the full image into marker image
            attraction = db_api.attraction_post(name, lat, lng, intro, rating, 
                cover_file, marker_file, user_id, is_custom)
            attraction_id = attraction.post()

            # # Post review
            # if attraction_id:
            #     review = db_api.review_post(intro, rating, cover_file, user_id, attraction_id)
            #     return True
            # else:
            #     return False

#  ________________________________________
# |Attraction List Retrieval               |
# |________________________________________|

    """ 
    Input a list of [user_id, user_id...]
    Return a list of (attraction_id, date_time) object.
    """
    def attraction_list_get(self, user_list):
        user_list_json = json.dumps(user_list)
        attraction_list_json = db_api.attraction_list_get(user_list_json)
        attraction_list = json.loads(attraction_list_json)
        return attraction_list

#  ________________________________________
# |DB Access                               |
# |________________________________________|

    # # Post attraction
    # def post_attraction(self, name, lat, lng, 
    #         intro, rating, cover_file, marker_file,
    #         user_id
    #     ):
    #     obj = db_api.attraction_post(name, lat, lng, 
    #         intro, rating, cover_file, marker_file,
    #         user_id)
    #     return obj.post()

    # # Post review
    # def post_review(self, intro, rating, cover_file, marker_file, user_id):
        
    #     obj = db_api.review_post(intro, rating, cover_file, user_id)
    #     return obj.post()

#  ________________________________________
# |Attraction Details                      |
# |________________________________________|

    def look_up_place_data_and_render(self, ID):
        obj = db_api.attraction_detail_object(ID)
        place_info, reviews_data = obj.get()
        reviews_data = reviews_data[0:-1]
        context = {'place_info': place_info, 'reviews_data': reviews_data}
        return render(None, 'services/attraction/templates/place.html', context)

    def look_up_attraction_detail(self, ID):
        obj = db_api.attraction_detail_object(ID)
        place_info, reviews_data = obj.get()
        reviews_data = reviews_data[0:-1]
        return (place_info, reviews_data)

if __name__ == '__main__':
    pass