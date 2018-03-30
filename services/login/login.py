# Dummy Login
# All class name default as service
from services.login.api import db_api
class service():

    def __init__(self):
        pass

    def test(self):
        print('request login service succeed')

    def test_db_connection(self):
        data = db_api.test()
        return data

    def login(self, email, password):
        user_auth_obj = db_api.user_autheticate(email,password)
        result = user_auth_obj.post()
        if result:
            return True
        else:
            return False

    # def logout(self, email):
    #     pass

    def create_user(self, name, email, experience, exp_id, password):
        user_create_obj = db_api.user_post(name, email, experience, exp_id, password)
        response = user_create_obj.post()
        if response:
            return True
        else:
            return False

    def get_profile(self, user_id):
        profile_get_obj = db_api.profile_get(user_id)
        response = profile_get_obj.get()

        if response:
            profile = {
                'name': profile_get_obj.name,
                'email': profile_get_obj.email,
                'exp_id': profile_get_obj.exp_id,
                'experience': profile_get_obj.experience
            }

            return profile
            
        else:
            return None
