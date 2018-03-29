import json
import os
from django.http import JsonResponse
from SmileyWorld.config import *
from django.contrib.auth.decorators import login_required
from django.template import Context, Template

# import Applications
from Map.Map import Map

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
relation_service = service_locator.provide('relation')
location_service = service_locator.provide('location')
login_service.test()
attraction_service.test()

"""
#  ________________________________________
# |Loading Application                     |
# |________________________________________|
"""
Map_App = Map(attraction_service, relation_service)
Map_App.test()

"""
#  ________________________________________
# |Definition of the Login Class           |
# |________________________________________|
"""

def welcome(request):
    
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
# PreLogin check if session expired
def pre_user_login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return JsonResponse({'status': 'success'}), 201
        else:
            return "", 400

# Login function
def user_login(request):
    if request.method == 'POST':
        # Read data
        email = request.form.get('email')
        password = request.form.get('password')

        response = login_service.login(email, password)
        status = response['status']

        if status:
            # Associate the request with the user_id on local session DB
            user_id = response['user_ID']
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
        exp_ID = request.form.get('exp_ID')
        experience = 0

        # Check if all fields valid
        if email and password and name:
            response = login_service.create_user(name, email, experience, exp_ID, password)
            status = response['status']
            if status:
                # Automatically log in the use after sign up
                current_user.login_user(request, email)
                return JsonResponse({'status': 'success'}), 201
            else:
                return JsonResponse({'status': 'DB failed'}), 400
        else:
            return JsonResponse({'status': 'fields not valid'}), 400
                

"""
#  ________________________________________
# | Profile Session                        |
# |________________________________________|
"""

# Get profile information
def get_profile(request):
    if request.method == 'GET':
        # Read data
        email = request.form.get('email')
        data = login_service.get_profile(current_user.get_user_id(request))

        if data['status']:
            return JsonResponse({
                'user_ID':data['exp_ID'], 
                'experience': data['experience'], 
                'name': data['name'], 
                'email': data['email']
                })

        else:
            return "", 400
    else:
        return "", 400

"""
#  ________________________________________
# | Friend & Relationship Section          |
# |________________________________________|
"""
def get_friendlist(request):

    # Get friend list
    if request.method == 'GET':
       
        data = relation_service.show_all_friends(current_user.get_user_id(request))
        status = data['status']
        if status:
            friendlist = data['friendlist']
            return JsonResponse(friendlist)
        else:
            return "", 400

    # Follow a friend
    elif request.method == 'POST':
        to_email = request.form.get('email')
        relation = 1

        response = relation_service.add_follow(current_user.get_user_id(request), to_email, relation)
        status = response['status']
        if status:
            return JsonResponse({'status': 'success'}), 201
        else:
            return "", 400

    # Delete a friend
    elif request.method == 'DELETE':
        email = request.args.get('email')
        response = relation_service.delete_follow(current_user.get_user_id(request), email)
        status = response['status']
        if status:
            return JsonResponse({'status': 'success'}), 201
        else:
            return "", 400
    else:
        return "", 400

"""
#  ________________________________________
# | Map related Session                    |
# |________________________________________|
"""
# Map view
def get_map(request):
    if request.method == 'GET':
        
        rule = request.form.get('rule')
        if not rule: rule = 'default' # Set default rule
        data = Map_App.get_map_attractions(current_user.get_user_id(request), rule)
        if data['status']:
            return JsonResponse(data)
        else:
            return "", 400
    else:
        return "", 400

"""
#  ________________________________________
# | Attraction related Session             |
# |________________________________________|
"""

# Attraction View
def create_a_new_place_post(request):
    # Create an attraction
    if request.method == 'POST':
        # Read Data
        name = request.form.get('name')
        lat = request.form.get('lat')
        lng = request.form.get('lng')
        intro = request.form.get('intro')
        rating = request.form.get('rating')
        cover_file = request.files.get('cover')
        marker_file = request.files.get('marker')

        # Calculate the score based on the user experience and the rating
        score = (float(rating) + 10)

        user_id = current_user.get_user_id(request)
        
        response = attraction_service.post_moment(
            name, lat, lng, intro, rating, cover_file, marker_file,
            user_id
        )
        if response['status']:
            return JsonResponse({'status': 'success'}), 201
        else:
            return "", 400

    else:
        return '', 404
# return marker

"""
#  ________________________________________
# | Location Service section               |
# |________________________________________|
"""
# Return the places nearby to the front end for selection
def get_list_of_places_near_a_coordinate(request):
    if request.method == 'GET':
        lat = request.args.get('lat')
        lng = request.args.get('lng')
        data = location_service.find_nearby_attractions(lat, lng)
        if data['status']:
            JsonResponse(data['place_list'])
        else:
            return "", 400


# # Return the places nearby to the front end for selection
# def get_list_of_places_near_a_coordinate(request):
#     if request.method == 'GET':
#         lat = request.args.get('lat')
#         lng = request.args.get('lng')
#         place_list = Map_App.gps_to_place_list(lat, lng)
#         if place_list != "_new":
#             return JsonResponse(place_list)
#         else:
#             return "", 400

"""
#  ________________________________________
# |All Web Relation Content below this line|
# |________________________________________|
"""

# No login required
def request_place_look_up(request):
    if request.method == 'GET':
        
        ID = request.args.get('attraction')
        # print(ID)
        rendered_page = attraction_service.look_up_place_data_and_render(ID)
        if rendered_page:
            return rendered_page, 201
        else:
            return '', 400