"""
# current_user is a package of functions to access the local DB to track the sessions
"""
from django.contrib.auth import authenticate, login
from SmileyWorld.models import User

def get_user_id(request):
    return request.user.get_user_id()

def get_username(request):
    return request.user.get_username()

def get_experience(request):
    return request.user.get_experience()

def login_user(request, user_id):
    user = authenticate(request, user_id = user_id, password = 'password')

    if user==None:
        user = User.objects.create_user(user_id=user_id, password = 'password')

    login(request, user)