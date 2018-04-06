import db_api.db_api
from db_api.db_api import *
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
user_ID = user_0_user_ID

user1 = user_db()
user1.post(email = 'email_user_1', name = 'name_user_1', experience = '1', exp_ID = 'user_exp_ID_1', password = 'password_user_1')
assert user1.email == 'email_user_1'
assert user1.name == 'name_user_1'
assert user1.password == 'password_user_1'
assert user1.exp_ID == 'user_exp_ID_1'
assert user1.experience == '1'
assert user1.explored_list == []
assert user1.discovered_list == []
assert user1.status == 'updated'
assert user1.user_ID != None
user_1_user_ID = user1.user_ID
user_ID = user_0_user_ID

#testing user list create
user_list_0 = get_user_list_db([user_ID, user_1_user_ID])


'''
#testing user update
user1.update(email = 'email_user_1_update')
assert user1.email == 'email_user_1_update'
user1.update(name = 'nameupdate')
assert user1.name == 'nameupdate'
'''

#testing user get by ID
user0_check = user_db()
user0_check.get(user_ID = user_0_user_ID)
assert user0_check.email == 'email_user_0'
assert user0_check.name == 'name_user_0'
assert user0_check.exp_ID == 'user_exp_ID_0'
assert user0_check.experience == '0'
assert user0_check.explored_list == []
assert user0_check.discovered_list == []
assert user0_check.status == 'updated'
'''
#testing user login
user0_check2 = user_db()
user0_check2.get(email = 'email_user_0', password = 'password_user_0')
assert user0_check2.email == 'email_user_0'
assert user0_check2.user_ID == user_ID
assert user0_check2.name == 'name_user_0'
assert user0_check2.password == 'password_user_0'
assert user0_check2.exp_ID == 'user_exp_ID_0'
assert user0_check2.experience == '0'
assert user0_check2.explored_list == []
assert user0_check2.discovered_list == []
assert user0_check2.status == 'updated'
'''
#testing attraction creation
f1 = open('test_resource/test_cover.jpg', 'rb')
f2 = open('test_resource/test_marker.png','rb')
lat = str(uniform(-50,50))
lng = str(uniform(-150,150))
#lat = '37.6573504'
#lng = '-121.8810736'
address = gps_to_address(lng = lng, lat = lat)
attraction0 = attraction_db()
attraction0.post(name = 'attraction_name', lng = lng, lat = lat, intro = 'attraction_intro', rating = '0', explorer_ID = user_ID, cover_file = f1, marker_file = f2, is_protected = 'False', address = address )
attraction_ID = attraction0.attraction_ID
assert attraction0.name == 'attraction_name'
assert attraction0.lng == lng
assert attraction0.lat == lat
assert attraction0.intro == 'attraction_intro'
assert attraction0.cover != None
assert attraction0.marker != None
assert attraction0.explorer_ID == user_ID
assert attraction0.is_protected == 'False'
assert attraction0.address == address
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
assert attraction1.is_protected == 'False'
assert attraction1.address == address
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
assert attraction2.is_protected == 'False'
assert attraction2.address == address
assert attraction2.creation_time != None
assert attraction2.update_time != None
assert attraction1.attraction_ID == attraction_ID
review_ID = attraction2.review_list[0]['review_ID']
attraction_review = review_db()
attraction_review.get(review_ID = review_ID)
assert attraction_review.intro == 'attraction_intro'
assert attraction_review.rating == '0'
assert attraction_review.resource != None
assert attraction_review.reviewer_ID == user_ID
assert attraction_review.attraction_ID == attraction_ID
assert attraction_review.review_ID == review_ID


#testing review creation
review0 = review_db()
review0.post(intro = 'review_intro', rating = 'review_rating', resource_file = f1, reviewer_ID = user_ID, attraction_ID = attraction_ID, review_ID = None)
review0_ID = review0.review_ID
assert review0.intro == 'review_intro'
assert review0.rating == 'review_rating'
assert review0.resource != None
assert review0.reviewer_ID == user_ID
assert review0.attraction_ID == attraction_ID


#testing review get by attraction_ID and review_ID
review1 = review_db()
review1.get(review_ID = review0_ID)
assert review1.intro == 'review_intro'
assert review1.rating == 'review_rating'
assert review1.resource != None
assert review1.reviewer_ID == user_ID
assert review1.attraction_ID == attraction_ID
assert review1.review_ID == review0_ID