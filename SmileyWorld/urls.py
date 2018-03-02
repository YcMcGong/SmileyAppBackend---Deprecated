from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('test', views.test, name='test'),
    path('test2', views.test2, name='test2'),

    # User & Login
    path('', views.welcome, name='welcome'),
    path('/user', views.user_login, name='user_login'),
    path('/user_logout', views.user_logout, name='user_logout'),
    path('/create_user', views.create_user, name='create_user'),
    path('/profile', views.get_profile, name='get_profile'),

    # Friendlist
    path('/friendlist', views.get_friendlist, name='friendlist'),

    # Map
    path('/map', views.get_map, name='get_map'),

    # Attraction
    path('/attraction', views.create_a_new_place_post, name='create_a_new_place_post'),
    path('/selectPlacesNearby', views.get_list_of_places_near_a_coordinate, name='get_list_of_places_near_a_coordinate'),

    # Place
    path('/LookUpPlace', views.request_place_look_up, name='request_place_look_up')
]