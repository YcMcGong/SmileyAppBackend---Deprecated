# This file specifies the communication protocol for the DB service layer
import requests
import config
from config import *
import json

def test():
    user1 = user_post(name = 'user1', email = 'email1', experience = 'experience1', exp_ID = 'exp_ID1', password = 'password1')
    print('user creation complete')
    user1_ID = json.loads(user1.post().text)
    print(user1_ID)
    print('user post complete')
    user1_login = user_autheticate(email = 'email1', password = 'password1')
    user1_ID_check = user1_login.post()
    if user1_ID_check == 'email not found' or user1_ID_check == 'wrong password':
        print(user1_ID_check)
    if (user1_ID_check == user1_ID):
        print('successfully login')
    else:
        print('login problem')
    user2_login = user_autheticate(email = 'email2', password = 'password1')
    user2_ID_check = user2_login.post()
    if user2_ID_check != 'email not found':
        print('problem with invalid email')
    user3_login = user_autheticate(email = 'email1', password = 'password2')
    user3_ID_check = user3_login.post()
    if user3_ID_check != 'wrong password':
        print('problem with invalid password')
    user1_profile = profile_get(user1_ID)
    user1_profile.get()
    if user1_profile.name != 'user1' or user1_profile.email != 'email1' or user1_profile.experience != 'experience1' or user1_profile.exp_ID != 'exp_ID1':
        print('problem with user_profile_get')
    else:
        print('successfully get profile')
    with open('thumbnail_IMG_3956.jpg', 'rb') as f:
        attraction1_post = attraction_post(name = 'attraction_name', lng = '-121.8810736', lat = '37.6573504', intro = 'attraction_intro', cover_file = f, marker_file = f, rating = '0', user_ID = user1_ID)
        attraction1_ID = attraction1_post.post()
        attraction1 = attraction_get(attraction_ID = attraction1_ID)
        attraction1.get()
        print(attraction1)



class user_post():
    
    def __init__(self, name, email, experience, exp_ID, password):
        self.name = name
        self.email = email
        self.experience = experience
        self.exp_ID = exp_ID
        self.password = password
        self.status = 'waiting for creation'

    def post(self):
        
        url = DB_ENDPOINT + '/create_user' # define end-point

        data = {
            'email': self.email,
            'name': self.name,
            'experience' : self.experience,
            'exp_ID': self.exp_ID,
            'password': self.password
        }
        response = requests.post(url, data = data) # return user_ID if valid
        self.status = 'created'
        return response

class user_autheticate():

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.status = 'not auth'

    def post(self):
        
        url = DB_ENDPOINT + '/user_autheticate' # define end-point

        data = {
            'email': self.email,
            'password':  self.password
        }

        response = requests.get(url, params = data) # return user_id if valid
        self.status = 'authorized'
        return response.text

class profile_get():

    def __init__(self, user_ID):
        self.user_ID = user_ID
        self.status = 'not auth'

    def get(self):
        
        url = DB_ENDPOINT + '/get_user' # define end-point

        params = {'user_ID': self.user_ID}
        response = requests.get(url, params = params) # send http request
        data = json.loads(response.text)
        if data:
            self.__assign_data(data)
            return True
        else:
            return False

    def __assign_data(self, data):
        self.experience = data['experience']
        self.exp_ID = data['exp_ID']
        self.email = data['email']
        self.name = data['name']
        self.status = 'data received'




"""
#  ________________________________________
# |Attraction                              |
# |________________________________________|
"""
# Post attraction
class attraction_post():

    def __init__(self, name, lat, lng, intro, rating, cover_file, marker_file,
            user_ID, if_custom = False):
        self.name = name
        self.lat = lat
        self.lng = lng
        self.intro = intro
        self.rating = rating
        self.cover_file = cover_file
        self.marker_file = marker_file
        self.user_ID = user_ID
        self.if_custom = if_custom
        # shows the status of this request object
        self.status = 'not post yet'

    def post(self):
        
        url = DB_ENDPOINT + '/post_attraction' # define end-point

        data = {
            'name': self.name,
            'lat':  self.lat,
            'lng':  self.lng,
            'intro':self.intro,
            'rating':self.rating,
            'user_ID': self.user_ID,
            'if_custom': self.if_custom
        }

        files = {'cover': self.cover_file, 'marker': self.marker_file}
        response = requests.post(url, files = files, data = data)
        self.status = 'sent'
        return response.text

# Get attraction by ID, or, coordinate, or address
class attraction_get():

    def __init__(self, attraction_ID = None, lat = None, lng = None, address = None):
        self.attraction_ID = attraction_ID
        self.lat = lat
        self.lng = lng
        self.address = address
        # Other info
        self.marker_url = None
        self.intro = None
        self.explorer_ID = None
        self.discover = None

    def get(self):
        
        # Get by ID
        if self.attraction_ID:
            url = DB_ENDPOINT + '/get_attraction_by_ID' # define end-point
            params = {'attraction_ID': self.attraction_ID}

        # Get by coordinate
        elif self.lat and self.lng:
            url = DB_ENDPOINT + '/get_attraction_by_coordinate' # define end-point
            params = {'lat': self.lat, 'lng': self.lng}

        # Get by address
        elif self.address:
            url = DB_ENDPOINT + 'attraction_get_by_address' # define end-point
            params = {'lat': self.address}

        # No input
        else:
            return False

        data = requests.get(url, params = params) # send http request
        if data:
            self.__assign_data(data.json())
            return True
        else:
            return False

    def __assign_data(self, data):
        
        self.attraction_ID = data['attraction_ID']
        self.lat = data['lat']
        self.lng = data['lng']
        self.address = data['address']
        # Other info
        self.marker_url = data['marker']
        self.intro = data['intro']
        self.explorer_ID = data['explorer_ID']
        self.discoverer = data['discoverer']


"""
#  ________________________________________
# |Attraction List                         |
# |________________________________________|
"""

# Get a list of attraction using a jsonified list of users
class get_multiple_attraction_list():

    def __init__(self, user_list_json):
        self.user_list_json = user_list_json

    def post(self):
        
        url = DB_ENDPOINT + '/get_multiple_attraction_list' # define end-point

        params = {'user_list': self.user_list_json}

        data = requests.get(url, params = params) # send http request

        return data


"""
#  ________________________________________
# |Review                                  |
# |________________________________________|
"""

class review_post():
    
    def __init__(self, intro, rating, cover_file, user_ID, attraction_ID):

        self.intro = intro
        self.rating = rating
        self.cover_file = cover_file
        self.user_ID = user_ID
        self.attraction_ID = attraction_ID

    def post(self):
        
        url = DB_ENDPOINT + '/post_review' # define end-point

        data = {
            'intro': self.intro,
            'rating':self.rating,
            'user_ID': self.user_ID,
            'attraction_ID':self.attraction_ID
        }

        files = {'cover': self.cover_file}

        response = requests.post(url, files = files, data = data)

        return response

"""
#  ________________________________________
# |Attraction Details                      |
# |________________________________________|
"""

class attraction_detail_object():
    
    def __init__(self, ID):
        self.ID = ID

    def get(self):
        
        
        review_url = DB_ENDPOINT + '/get_review_by_attraction_ID'
        params = {'ID': self.ID}
        
        attraction_data, review_data = request.get(review_url, params = params)
        return (attraction_data, review_data)




if __name__ == '__main__':
    test()
