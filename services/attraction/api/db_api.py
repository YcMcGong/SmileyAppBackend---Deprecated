# This file specifies the communication protocol for the DB service layer
import requests
DB_ENDPOINT = 'http://0.0.0.0:5000'
def test():
    response = requests.get(DB_ENDPOINT)
    data = response.json()
    return data

class attraction_post():

    def __init__(self, name, lat, lng, 
            intro, rating, cover_file, marker_file,
            user_id):
        self.name = name
        self.lat = lat
        self.lng = lng
        self.intro = intro
        self.rating = rating
        self.cover_file = cover_file
        self.marker_file = marker_file
        self.user_id = user_id

    def push(self):
        
        url = DB_ENDPOINT + 'attraction_post' # define end-point

        data = {
            'name': self.name,
            'lat':  self.lat,
            'lng':  self.lng,
            'intro':self.intro,
            'rating':self.rating,
            'user_id': self.user_id
        }

        files = {'cover': self.cover_file, 'marker': self.marker_file}

        response = requests.post(url, files = files, data = data)

        return response

class place_look_up_object():
    
    def __init__(self, ID):
        self.ID = ID

    def get(self):
        
        url = DB_ENDPOINT + 'place_lookup' # define end-point

        params = {'ID': self.ID}
        data = requests.get(url, params = params)
        place_data = data['place']
        review_data = data['review']

        return (place_data, review_data)
