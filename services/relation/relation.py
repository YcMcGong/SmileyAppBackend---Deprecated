# Dummy Login
# All class name default as service
from services.login.api import db_api
class service():

    def __init__(self):
        pass

    def test(self):
        print('request relation service succeed')

    def test_db_connection(self):
        data = db_api.test()
        return data

    def show_all_friends(self, usr_id):
        pass

    def add_follow(self, user_id, to_email, status):
        pass

    def delete_follow(self, user_id, to_email):
        pass