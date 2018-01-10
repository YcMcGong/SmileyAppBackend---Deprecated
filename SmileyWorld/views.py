import json
import os
from django.http import JsonResponse
from SmileyWorld.config import *
from SmileyWorld.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

db = connect_to_dynamodb()
storage = connect_to_s3()

bucket = storage.get_bucket('smileyphototest')
test_key = bucket.get_key('thumbnail_IMG_3956.jpg')
test_url = test_key.generate_url(0, query_auth=False, force_http=True)
plans_key = bucket.get_key('thumbnail_IMG_3956.jpg')
plans_url = plans_key.generate_url(3600, query_auth=True, force_http=True)



"""
#  ________________________________________
# |Definition of the Login Class           |
# |________________________________________|
"""

def index(request):
    
    user = authenticate(request, user_id='john3', password='password')

    if user==None:
        user = User.objects.create_user(user_id='john3', password = 'password')

    user.experience = 90
    user.save()

    login(request, user)
    
    return JsonResponse({'one':plans_url, 'two':test_url})

@login_required
def test(request):
    return JsonResponse({'one':1, 'two':request.user.experience})