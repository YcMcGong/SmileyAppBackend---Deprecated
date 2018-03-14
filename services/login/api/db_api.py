# This file specifies the communication protocol for the DB service layer
import requests
DB_ENDPOINT = 'http://0.0.0.0:5000'
def test():
    response = requests.get(DB_ENDPOINT)
    data = response.json()
    return data

class user_post():
    
    def __init__(self, name, email, experience, exp_id, password):
        self.name = name
        self.email = email
        self.experience = experience
        self.exp_id = exp_id
        self.password = password
        self.status = 'waiting for creation'

    def post(self):
        
        url = DB_ENDPOINT + 'user_autheticate' # define end-point

        data = {
            'email': self.email,
            'name': self.name,
            'experience' : self.experience,
            'exp_id': self.exp_id,
            'password': self.password
        }

        response = requests.post(url, data = data) # return user_id if valid
        self.status = 'created'
        return response

class user_autheticate():

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.status = 'not auth'

    def post(self):
        
        url = DB_ENDPOINT + 'user_autheticate' # define end-point

        data = {
            'email': self.email,
            'password':  self.password
        }

        response = requests.post(url, data = data) # return user_id if valid
        self.status = 'authorized'
        return response

class profile_get():

    def __init__(self, user_id):
        self.user_id = user_id
        self.status = 'not auth'

    def get(self):
        
        url = DB_ENDPOINT + 'profile_get' # define end-point

        params = {'user_id': self.user_id}

        data = requests.get(url, params = params) # send http request
        if data:
            self.__assign_data(data)
            return True
        else:
            return False

    def __assign_data(self, data):
        self.experience = data['experience']
        self.exp_id = data['exp_id']
        self.email = data['email']
        self.name = data['name']
        self.status = 'data received'