# This file specifies the communication protocol for the DB service layer
import requests
DB_ENDPOINT = 'http://0.0.0.0:5000'
def test():
    response = requests.get(DB_ENDPOINT)
    data = response.json()
    return data

class new_user:
    def __init__(self, name, password, email):
        self.name = name
        self.email = email
        self.password = password

    def push(self):
        
        url = DB_ENDPOINT + '/user_create' # define end-point

        data = {
            'name': self.name,
            'email': self.email,
            'password': self.password
        }

       

        response = requests.post(url, data = data)

        return response


class user:
    def __init__(self, name, password, email, user_ID):
        if user_ID == None:  #create new user
            self.name = name
            self.email = email
            self.password = password
        else:    #get information from database
            self.user_ID = user_ID
            url = DB_ENDPOINT + '/get_user?user_ID=' + user_ID
            response = requests.get(url)
            print(response)
            
    def return_user():
        return self.user_ID

if __name__ == '__main__':
    test_user = user(user_ID = )

