import json
import os
from django.http import JsonResponse
from SmileyWorld.config import *
from django.contrib.auth.decorators import login_required

# import service locator
from services.services_locator import service_locator

# import utility
from utility import current_user

"""
#  ________________________________________
# |Loading services                        |
# |________________________________________|
"""
service_locator = service_locator()
login_service = service_locator.provide('login')
attraction_service = service_locator.provide('attraction')
login_service.test()
attraction_service.test()

"""
#  ________________________________________
# |Definition of the Login Class           |
# |________________________________________|
"""

def index(request):
    
    current_user.login_user(request, '1234')
    return JsonResponse({'one':'plans_url', 'two':'test'})

@login_required
def test(request):
    request.user.edit_username('xxjo')
    return JsonResponse({'one':1, 'two':request.user.get_username()})

@login_required
def test2(request):
    # return JsonResponse({'one':1, 'two':current_user.get_user_id(request)})
    data = login_service.test_db_connection()
    return JsonResponse(data)

"""
#  ________________________________________
# |User & Login Related Sessions           |
# |________________________________________|
"""
# Login function
def user_login(request):
    if request.method == 'POST':
        # Read data
        email = request.form.get('email')
        password = request.form.get('password')

        user_id = login_service.login(email)

        if user_id:
            # Associate the request with the user_id on local session DB
            current_user.login_user(request, user_id)
            return JsonResponse({'status': 'success'}), 201
        
        else:
            return "", 400

# Logout function
def user_logout(request):
    if request.method == 'GET':
        current_user.logout_user(request)
        return JsonResponse({'status': 'success'}), 201

# Create User
def create_user(request):
    if request.method == 'POST':

        # Read data
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')

        # Check if all fields valid
        if email and password and name:
            status = login_service.create_user(email, password, name)

            if status:
                # Automatically log in the use after sign up
                current_user.login_user(email)