# Dummy Login
# All class name default as service
from services.relation.api import db_api
class service():

    def __init__(self):
        pass

    def test(self):
        print('request relation service succeed')

    def test_db_connection(self):
        data = db_api.test()
        return data

    def show_all_friends(self, usr_id):
        friendlist_obj = db_api.friendlist_get(usr_id)
        friendlist_obj.get()
        return friendlist_obj.friendlist

    def add_follow(self, user_id, to_email, status):
        add_follow_obj = db_api.follow_post(user_id, to_email)
        add_follow_obj.post()
        if add_follow_obj.status == 'success':
            return True
        else:
            return False

    def delete_follow(self, user_id, to_email):
        del_follow_obj = db_api.defollow_post(user_id, to_email)
        del_follow_obj.post()
        if del_follow_obj.status == 'success':
            return True
        else:
            return False