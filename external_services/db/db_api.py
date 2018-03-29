import requests
import config
from config import *
import json

class user_db():
    def __init__(self, user_ID = None, name = None, email = None, experience = None, exp_ID = None, password = None):
        self.user_ID = user_ID
        self.name = name
        self.email = email
        self.experience = experience
        self.exp_ID = exp_ID
        self.password = password
        self.status = 'not created'
        self.explored_list = None
        self.discovered_list = None
        self.friends = None
        self.recently_visited = None
        self.others = None
    
    def assign(self, data):
        if 'user_ID' in data.keys():
            self.user_ID = data['user_ID']
        if 'email' in data.keys():
            self.email = data['email']
        if 'name' in data.keys():
            self.name = data['name']
        if 'experience' in data.keys():
            self.experience = data['experience']
        if 'exp_ID' in data.keys():
            self.exp_ID = data['exp_ID']
        if 'password' in data.keys():
            self.password = data['password']
        if 'explored_list' in data.keys():
            self.explored_list = data['explored_list']
        if 'discovered_list' in data.keys():
            self.discovered_list = data['discovered_list'] 
        self.status = 'updated'

    def post(self, name = None, email = None, experience = None, exp_ID = None, password = None):
        if email:
            self.email = email
        if name:
            self.name = name
        if experience:
            self.experience = experience
        if exp_ID:
            self.exp_ID = exp_ID
        if password:
            self.password = password
        if not self.user_ID: 
            url = DB_ENDPOINT + '/create_user'
            data = {
                'email': self.email,
                'name': self.name,
                'experience': self.experience,
                'exp_ID': self.exp_ID,
                'password': self.password,
            }
            response = requests.post(url, data = data).json()
            if 'error' in response.keys():
                self.status = response['errorMessage']
                return False
            self.assign(data = response)
            return True
        #else: update user info

    
    def get(self, user_ID = None, email = None, password = None):
        if user_ID:
            self.user_ID = user_ID
            url = DB_ENDPOINT + '/get_user'
            params = {
                'user_ID': self.user_ID
            }
            response = requests.get(url, params = params).json()
            if 'errorMessage' in response.keys():
                self.status = response['errorMessage']
                return False
            self.assign(data = response)
            return True

        if email and password: 
            self.email = email
            self.password = password
            url = DB_ENDPOINT + '/user_autheticate'
            params = {
                'email': self.email,
                'password': self.password
            }
            response = requests.get(url, params = params).json()
            if 'errorMessage' in response.keys():
                self.status = response['errorMessage']
                return False
            self.assign(data = response)
            if 'user_ID' in response.keys():
                self.get(response['user_ID'])
                return True
            self.status = 'user creation method error'
            return False
        
class attraction_db():
    def __init__(self, name = None, lat = None, lng = None, intro = None, rating = None, cover_file = None, marker_file = None, explorer_ID = None, if_custom = None, address = None, attraction_ID = None):
        self.name = name
        self.lat = lat
        self.lng = lng
        self.intro = intro
        self.rating = rating
        self.cover_file = cover_file
        self.marker_file = marker_file
        self.explorer_ID = explorer_ID
        self.if_custom = if_custom
        self.address = address
        self.attraction_ID = attraction_ID
        self.discoverer = None
        self.creation_time = None
        self.update_time = None
        self.cover = None
        self.marker = None
        self.review_number = None
        self.status = 'not created'

    def assign(self, data):
        if 'attraction_ID' in data.keys():
            self.attraction_ID = data['attraction_ID']
        if 'name' in data.keys():
            self.name = data['name']
        if 'lat' in data.keys() and 'lng' in data.keys():
            self.lat = data['lat']
            self.lng = data['lng']
        if 'intro' in data.keys():
            self.intro = data['intro']
        if 'cover' in data.keys():
            self.cover = data['cover']
        if 'marker' in data.keys():
            self.marker = data['marker']
        if 'explorer_ID' in data.keys():
            self.explorer_ID = data['explorer_ID']
        if 'address' in data.keys():
            self.address = data['address']
        if 'reviewNumber' in data.keys():
            self.review_number = data['reviewNumber']
        if 'discoverer' in data.keys():
            self.discoverer = data['discoverer']
        if 'creationTime' in data.keys():
            self.creation_time = data['creationTime']
        if 'updateTime' in data.keys():
            self.update_time = data['updateTime']
        if 'ifCustom' in data.keys():
            self.if_custom = data['ifCustom']
        self.status = 'updated'

    def post(self, name = None, lat = None, lng = None, intro = None, rating = None, cover_file = None, marker_file = None, explorer_ID = None, if_custom = None, address = None, attraction_ID = None):
        if attraction_ID:
            self.attraction_ID = attraction_ID
        if name:
            self.name = name
        if lat and lng:
            self.lat = lat
            self.lng = lng
        if intro:
            self.intro = intro
        if rating:
            self.rating = rating
        if cover_file:
            self.cover_file = cover_file
        if marker_file:
            self.marker_file = marker_file
        if explorer_ID:
            self.explorer_ID = explorer_ID
        if if_custom != None:
            self.if_custom = if_custom
        if not attraction_ID:
            url = DB_ENDPOINT + '/post_attraction'
            data = {
                'name': self.name,
                'lat':  self.lat,
                'lng':  self.lng,
                'intro':self.intro,
                'rating':self.rating,
                'explorer_ID': self.explorer_ID,
                'ifCustom': self.if_custom
            }
            files = {'cover': self.cover_file, 'marker': self.marker_file}
            response = requests.post(url, files = files, data = data).json()
            if 'errorMessage' in response.keys():
                self.status = response['errorMessage']
                return False
            self.assign(data = response)
            return True
        #else: update attraction
    
    def get(self, attraction_ID = None, lat = None, lng = None, address = None):
        if attraction_ID:
            self.attraction_ID = attraction_ID
            url = DB_ENDPOINT + '/get_attraction_by_ID'
            params = {
                'attraction_ID': attraction_ID 
            }
            response = requests.get(url, params = params).json()
            if 'errorMessage' in response.keys():
                self.status = response['errorMessage']
                return False
            self.assign(data = response)
            return True
        
        if lat and lng:
            self.lat = lat
            self.lng = lng
            url = DB_ENDPOINT + '/get_attraction_by_coordinate'
            params = {
                'lat': lat,
                'lng': lng
            }
            response = requests.get(url, params = params).json()
            if 'errorMessage' in response.keys():
                self.status = response['errorMessage']
                return False
            self.assign(data = response)
            return True
                
        
class review_db():
    def __init__(self, intro = None, rating = None, cover_file = None, user_ID = None, attraction_ID = None, review_ID = None):
        self.intro = intro
        self.rating = rating
        self.cover_file = cover_file
        self.user_ID = user_ID
        self.attraction_ID = attraction_ID
        self.review_ID = review_ID
        self.cover = None
        self.status = 'not created'

    def assign(self, data):
        if 'intro' in data.keys():
            self.intro = data['intro']
        if 'rating' in data.keys():
            self.rating = data['rating']
        if 'cover' in data.keys():
            self.cover = data['cover']
        if 'user_ID' in data.keys():
            self.user_ID = data['user_ID']
        if 'attraction_ID' in data.keys():
            self.attraction_ID = data['attraction_ID']
        if 'review_ID' in data.keys():
            self.review_ID = data['review_ID']
        self.status = 'updated'

    def post(self, intro = None, rating = None, cover_file = None, user_ID = None, attraction_ID = None, review_ID = None):
        if intro:
            self.intro = intro
        if rating:
            self.rating = rating
        if cover_file:
            self.cover_file = cover_file
        if user_ID:
            self.user_ID = user_ID
        if attraction_ID:
            self.attraction_ID = attraction_ID
        if not review_ID:
            url = DB_ENDPOINT + '/post_review'
            data = {
                'intro': self.intro,
                'rating':self.rating,
                'user_ID': self.user_ID,
                'attraction_ID':self.attraction_ID
            }

            files = {'cover': self.cover_file}
            response = requests.post(url, files = files, data = data).json()
            if 'errorMessage' in response.keys():
                self.status = response['errorMessage']
                return False
            self.assign(data = response)
            return True
        #else: update attraction 
    
    def get(self, attraction_ID = None, review_ID = None):
        if attraction_ID and review_ID:
            self.attraction_ID = attraction_ID
            self.review_ID = review_ID
        url = DB_ENDPOINT + '/get_review_by_attraction_ID_and_review_ID'
        params = {
            'attraction_ID': attraction_ID,
            'review_ID': review_ID
        }
        response = requests.get(url, params = params).json()
        if 'errorMessage' in response.keys():
            self.status = response['errorMessage']
            return False
        self.assign(data = response)
        return True
