import requests
import config
from config import *
import json
class user_db():
    def __init__(self):
        self.user_ID = None
        self.name = None
        self.email = None
        self.experience = None
        self.exp_ID = None
        self.password = None
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
        if 'exploredList' in data.keys():
            self.explored_list = data['exploredList']
        if 'discoveredList' in data.keys():
            self.discovered_list = data['discoveredList'] 
        if 'recentlyVisited' in data.keys():
            self.recently_visited = data['recentlyVisited']
        self.status = 'updated'
    
    def post(self, name, email, experience, exp_ID, password):
        self.name = name
        self.email = email
        self.experience = experience
        self.exp_ID = exp_ID
        self.password = password
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
        self.get(user_ID = self.user_ID)
        return True

    def update(self, name = None, email = None, experience = None, exp_ID = None, password = None, user_ID = None):
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
        if user_ID:
            self.user_ID = user_ID
    
        url = DB_ENDPOINT + '/update_user'
        data = {
            'discovered_list': json.dumps(self.discovered_list),
            'email': self.email,
            'exp_ID': self.exp_ID,
            'experience': self.experience,
            'explored_list': json.dumps(self.explored_list),
            'friends': json.dumps(self.friends),
            'name': self.name,
            'password': self.password,
            'recently_visited': json.dumps(self.recently_visited),
            'user_ID': self.user_ID
        }
        response = requests.post(url, data = data).json()
        if 'error' in response.keys():
            self.status = response['errorMessage']
            return False
        self.assign(data = response)
        return True
    
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
    def __init__(self):
        self.name = None
        self.lat = None
        self.lng = None
        self.intro = None
        self.rating = None
        self.cover_file = None
        self.marker_file = None
        self.explorer_ID = None
        self.is_protected = None
        self.address = None
        self.attraction_ID = None
        self.discoverer = None
        self.creation_time = None
        self.update_time = None
        self.cover = None
        self.marker = None
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
        if 'discoverer' in data.keys():
            self.discoverer = data['discoverer']
        if 'creationTime' in data.keys():
            self.creation_time = data['creationTime']
        if 'updateTime' in data.keys():
            self.update_time = data['updateTime']
        if 'isProtected' in data.keys():
            self.is_protected = data['isProtected']
        if 'review_list' in data.keys():
            self.review_list = data['review_list']

        self.status = 'updated'

    def post(self, name = None, lat = None, lng = None, intro = None, rating = None, cover_file = None, marker_file = None, explorer_ID = None, is_protected = None, address = None, attraction_ID = None):
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
        if is_protected != None:
            self.is_protected = is_protected
        if not attraction_ID:
            url = DB_ENDPOINT + '/post_attraction'
            data = {
                'name': self.name,
                'lat':  self.lat,
                'lng':  self.lng,
                'intro':self.intro,
                'rating':self.rating,
                'explorer_ID': self.explorer_ID,
                'isProtected': self.is_protected
            }
            files = {'cover': self.cover_file, 'marker': self.marker_file}
            response = requests.post(url, files = files, data = data).json()
            if 'errorMessage' in response.keys():
                self.status = response['errorMessage']
                return False
            
            self.assign(data = response)
            self.get(attraction_ID = self.attraction_ID)
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
    def __init__(self):
        self.intro = None
        self.rating = None
        self.cover_file = None
        self.reviewer_ID = None
        self.attraction_ID = None
        self.review_ID = None
        self.resource = None
        self.status = 'not created'

    def assign(self, data):
        if 'intro' in data.keys():
            self.intro = data['intro']
        if 'rating' in data.keys():
            self.rating = data['rating']
        if 'resource' in data.keys():
            self.resource = data['resource']
        if 'reviewer_ID' in data.keys():
            self.reviewer_ID = data['reviewer_ID']
        if 'attraction_ID' in data.keys():
            self.attraction_ID = data['attraction_ID']
        if 'review_ID' in data.keys():
            self.review_ID = data['review_ID']
        self.status = 'updated'

    def post(self, intro = None, rating = None, resource_file = None, reviewer_ID = None, attraction_ID = None, review_ID = None):
        if intro:
            self.intro = intro
        if rating:
            self.rating = rating
        if resource_file:
            self.resource_file = resource_file
        if reviewer_ID:
            self.reviewer_ID = reviewer_ID
        if attraction_ID:
            self.attraction_ID = attraction_ID
        if not review_ID:
            url = DB_ENDPOINT + '/post_review'
            data = {
                'intro': self.intro,
                'rating':self.rating,
                'user_ID': self.reviewer_ID,
                'attraction_ID':self.attraction_ID
            }

            files = {'resource': self.resource_file}
            response = requests.post(url, files = files, data = data).json()
            if 'errorMessage' in response.keys():
                self.status = response['errorMessage']
                return False
            self.assign(data = response)
            self.get(review_ID = self.review_ID)
            return True
        #else: update attraction 
    
    def get(self, review_ID = None):
        if review_ID:
            self.review_ID = review_ID
        url = DB_ENDPOINT + '/get_review'
        params = {
            'review_ID': self.review_ID
        }
        response = requests.get(url, params = params).json()
        if 'errorMessage' in response.keys():
            self.status = response['errorMessage']
            return False
        self.assign(data = response)
        return True
'''

class user_list_db():
    def __init__(self):
        self.user_ID_list = None
        self.status = 'not created'
        self.user_list = None
    
    def assign(self, data):
        if 'user_list' in data.keys():
            self.user_list = data['user_list']

    def get(self, user_ID_list = None):
        if user_ID_list != None:
            self.user_ID_list = user_ID_list
            url = DB_ENDPOINT + '/get_user_list'
            params = {
                'user_ID_list': json.dumps(self.user_ID_list)
            }
            response = requests.get(url, params = params).json()
            if 'errorMessage' in response.keys():
                self.status = response['errorMessage']
                return False
            self.assign(data = response)
            return True
'''
def get_user_list_db(user_ID_list):
    url = DB_ENDPOINT + '/get_user_list'
    params = {
        'user_ID_list': json.dumps(user_ID_list)
    }
    response = requests.get(url, params = params).json()
    return response

def get_attraction_list_db(attraction_ID_list):
    url = DB_ENDPOINT + '/get_attraction_list'
    params = {
        'attraction_ID_list': json.dumps(attraction_ID_list)
    }
    response = requests.get(url, params = params).json()
    return response

def get_review_list_db(review_ID_list):
    url = DB_ENDPOINT + '/get_review_list'
    params = {
        'review_ID_list': json.dumps(review_ID_list)
    }
    response = requests.get(url, params = params).json()
    return response

def add_friend(user_ID_1, user_ID_2):
    url = DB_ENDPOINT + 'add_friend'
    data = {
        'from_user_ID': user_ID_1,
        'to_user_ID': user_ID_2
    }
    response = requests.post(url, data = data).json()
    return response

