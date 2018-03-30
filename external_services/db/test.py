import db_api.db_api
from db_api.db_api import user_db, attraction_db, review_db
import utility
from utility import *
from random import *

#testing user creation
user0 = user_db()
user0.post(email = 'email_user_0', name = 'name_user_0', experience = '0', exp_ID = 'user_exp_ID_0', password = 'password_user_0')
assert user0.email == 'email_user_0'
assert user0.name == 'name_user_0'
assert user0.password == 'password_user_0'
assert user0.exp_ID == 'user_exp_ID_0'
assert user0.experience == '0'
assert user0.explored_list == []
assert user0.discovered_list == []
assert user0.status == 'updated'
assert user0.user_ID != None
user_0_user_ID = user0.user_ID

#testing user get by ID
user1 = user_db()
user1.get(user_ID = user_0_user_ID)
user_ID = user1.user_ID
assert user1.email == 'email_user_0'
assert user1.name == 'name_user_0'
assert user1.password == 'password_user_0'
assert user1.exp_ID == 'user_exp_ID_0'
assert user1.experience == '0'
assert user1.explored_list == []
assert user1.discovered_list == []
assert user1.status == 'updated'

#testing user login
user2 = user_db()
user2.get(email = 'email_user_0', password = 'password_user_0')
assert user2.email == 'email_user_0'
assert user2.user_ID == user_ID
assert user2.name == 'name_user_0'
assert user2.password == 'password_user_0'
assert user2.exp_ID == 'user_exp_ID_0'
assert user2.experience == '0'
assert user2.explored_list == []
assert user2.discovered_list == []
assert user2.status == 'updated'

#testing attraction creation
f1 = open('test_resource/test_cover.jpg', 'rb')
f2 = open('test_resource/test_marker.png','rb')
lat = str(uniform(-50,50))
lng = str(uniform(-150,150))
#lat = '37.6573504'
#lng = '-121.8810736'
address = gps_to_address(lng = lng, lat = lat)
attraction0 = attraction_db()
attraction0.post(name = 'attraction_name', lng = lng, lat = lat, intro = 'attraction_intro', rating = '0', explorer_ID = user_ID, cover_file = f1, marker_file = f2, if_custom = 'False', address = address )
attraction_ID = attraction0.attraction_ID
assert attraction0.name == 'attraction_name'
assert attraction0.lng == lng
assert attraction0.lat == lat
assert attraction0.intro == 'attraction_intro'
assert attraction0.cover != None
assert attraction0.marker != None
assert attraction0.explorer_ID == user_ID
assert attraction0.if_custom == 'False'
assert attraction0.address == address
assert attraction0.review_number == '1'
assert attraction0.discoverer == [user_ID]
assert attraction0.creation_time != None
assert attraction0.update_time != None

#testing attraction get by ID
attraction1 = attraction_db()
attraction1.get(attraction_ID = attraction_ID)
assert attraction1.name == 'attraction_name'
assert attraction1.lng == lng
assert attraction1.lat == lat
assert attraction1.intro == 'attraction_intro'
assert attraction1.cover != None
assert attraction1.marker != None
assert attraction1.explorer_ID == user_ID
assert attraction1.if_custom == 'False'
assert attraction1.address == address
assert attraction1.review_number == '1'
assert attraction1.discoverer == [user_ID]
assert attraction1.creation_time != None
assert attraction1.update_time != None
assert attraction1.attraction_ID == attraction_ID

#testing attraction get by coordinate
attraction2 = attraction_db()
attraction2.get(lng = lng, lat = lat)
assert attraction2.name == 'attraction_name'
assert attraction2.lng == lng
assert attraction2.lat == lat
assert attraction2.intro == 'attraction_intro'
assert attraction2.cover != None
assert attraction2.marker != None
assert attraction2.explorer_ID == user_ID
assert attraction2.if_custom == 'False'
assert attraction2.address == address
assert attraction2.review_number == '1'
assert attraction2.discoverer == [user_ID]
assert attraction2.creation_time != None
assert attraction2.update_time != None
assert attraction1.attraction_ID == attraction_ID

#testing review creation
review0 = review_db()
review0.post(intro = 'review_intro', rating = 'review_rating', cover_file = f1, user_ID = user_ID, attraction_ID = attraction_ID, review_ID = None)
assert review0.intro == 'review_intro'
assert review0.rating == 'review_rating'
assert review0.cover != None
assert review0.user_ID == user_ID
assert review0.attraction_ID == attraction_ID
assert review0.review_ID == '1'

#testing review get by attraction_ID and review_ID
review1 = review_db()
review1.get(attraction_ID = attraction_ID, review_ID = '1')
print(review1.intro)
assert review1.intro == 'review_intro'
assert review1.rating == 'review_rating'
assert review1.cover != None
assert review1.user_ID == user_ID
assert review1.attraction_ID == attraction_ID
assert review1.review_ID == '1'