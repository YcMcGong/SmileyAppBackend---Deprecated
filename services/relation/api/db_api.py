# This file specifies the communication protocol for the DB service layer
import requests
DB_ENDPOINT = 'http://0.0.0.0:5000'
def test():
    response = requests.get(DB_ENDPOINT)
    data = response.json()
    return data

class friendlist_get():
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.friendlist = None

    def get(self):
        
        url = DB_ENDPOINT + '/friendlist_get' # define end-point

        params = {'user_id': self.user_id}

        data = requests.get(url, params = params) # send http request
        if data:
            self.__assign_data(data)
            return True
        else:
            return False

    def __assign_data(self, data):
        self.friendlist = data['friendlist']
        self.status = 'data received'

class follow_post():

    def __init__(self, user_id, to_email):
        self.user_id = user_id
        self.to_email = to_email

    def post(self):
        
        url = DB_ENDPOINT + '/user_autheticate' # define end-point

        data = {
            'user_id': self.user_id,
            'to_email':  self.to_email
        }

        response = requests.post(url, data = data) # return user_id if valid
        self.status = 'success'
        return response

class defollow_post():
    
    def __init__(self, user_id, to_email):
        self.user_id = user_id
        self.to_email = to_email

    def post(self):
        
        url = DB_ENDPOINT + '/user_autheticate' # define end-point

        data = {
            'user_id': self.user_id,
            'to_email':  self.to_email
        }

        response = requests.post(url, data = data) # return user_id if valid
        self.status = 'success'
        return response
        
