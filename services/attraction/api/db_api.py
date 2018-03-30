# This file specifies the communication protocol for the DB service layer
import requests
DB_ENDPOINT = 'http://0.0.0.0:5000'
def test():
    response = requests.get(DB_ENDPOINT)
    data = response.json()
    return data

"""
#  ________________________________________
# |Attraction                              |
# |________________________________________|
"""
# Post attraction
class attraction_post():

    def __init__(self, name, lat, lng, intro, rating, cover_file, marker_file,
            user_id, if_custom = False):
        self.name = name
        self.lat = lat
        self.lng = lng
        self.intro = intro
        self.rating = rating
        self.cover_file = cover_file
        self.marker_file = marker_file
        self.user_id = user_id
        self.if_custom = if_custom
        # shows the status of this request object
        self.status = 'not post yet'

    def post(self):
        
        url = DB_ENDPOINT + 'attraction_post' # define end-point

        data = {
            'name': self.name,
            'lat':  self.lat,
            'lng':  self.lng,
            'intro':self.intro,
            'rating':self.rating,
            'user_id': self.user_id,
            'if_custom': self.if_custom
        }

        files = {'cover': self.cover_file, 'marker': self.marker_file}

        response = requests.post(url, files = files, data = data)
        self.status = 'sent'
        return response

# Get attraction by ID, or, coordinate, or address
class attraction_get():

    def __init__(self, ID = None, lat = None, lng = None, address = None):
        self.ID = ID
        self.lat = lat
        self.lng = lng
        self.address = address
        # Other info
        self.marker_url = None
        self.intro = None
        self.explorer = None
        self.discover = None

    def get(self):
        
        # Get by id
        if self.ID:
            url = DB_ENDPOINT + 'attraction_get_by_id' # define end-point
            params = {'ID': self.ID}

        # Get by coordinate
        elif self.lat and self.lng:
            url = DB_ENDPOINT + 'attraction_get_by_coordinate' # define end-point
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
            self.__assign_data(data)
            return True
        else:
            return False

    def __assign_data(self, data):
        
        self.ID = data['ID']
        self.lat = data['lat']
        self.lng = data['lng']
        self.address = data['address']
        # Other info
        self.marker_url = data['maker']
        self.intro = data['intro']
        self.explorer = data['explorer']
        self.discover = data['discover']


"""
#  ________________________________________
# |Attraction List                         |
# |________________________________________|
"""

# Get a list of attraction using a jsonified list of users
class attraction_list_get():

    def __init__(self, user_list_json):
        self.user_list_json = user_list_json

    def post(self):
        
        url = DB_ENDPOINT + 'attraction_post' # define end-point

        params = {'user_list': self.user_list_json}

        data = requests.get(url, params = params) # send http request

        return data


"""
#  ________________________________________
# |Review                                  |
# |________________________________________|
"""

class review_post():
    
    def __init__(self, intro, rating, cover_file, user_id, attraction_id):

        self.intro = intro
        self.rating = rating
        self.cover_file = cover_file
        self.user_id = user_id
        self.attraction_id = attraction_id

    def post(self):
        
        url = DB_ENDPOINT + 'review_post' # define end-point

        data = {
            'intro': self.intro,
            'rating':self.rating,
            'user_id': self.user_id,
            'attraction_id':self.attraction_id
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
        
        url = DB_ENDPOINT + 'place_lookup' # define end-point

        params = {'ID': self.ID}
        data = requests.get(url, params = params)
        place_data = data['place']
        review_data = data['review']

        return (place_data, review_data)
