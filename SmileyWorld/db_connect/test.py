
import Connect_to_db
from Connect_to_db import *
import time


db = Connect_to_db()
print('successfully connect to database\n')

db.create_user(email = 'testemail@testemail.com', password = 'testpassword', name = 'testname') 
testemail_ID = db.get_user_ID('testemail@testemail.com')
print('successfully create user\n')
'''
if db.login(email = 'not exist', password = 'password') != 0:
    print('wrong return with email not exsit\n')
elif db.login(email = 'testemail@testemail.com', password = 'wrongpassword') != 1:
    print('wrong return with incorrect password\n')
elif db.login(email = 'testemail@testemail.com', password = 'testpassword') != testemail_ID:
    print('wrong return with correct password\n')
else:
    print('successfully login\n') 
'''
db.create_user(email = 'testemail2@testemail.com', password = 'testpassword2', name = 'testname2')
testemail_ID2 = db.get_user_ID('testemail2@testemail.com')
'''
db.add_friend(from_user_ID = testemail_ID, to_user_ID = testemail_ID2)
if db.get_user(testemail_ID)['friends'][0]['user_ID'] != testemail_ID2:
    print('wrong with add friend\n')
elif db.get_user(testemail_ID2)['friends'][0]['user_ID'] != testemail_ID:
    print('wrong with add friend in two way\n')
else: 
    print('successfully add friendship\n')

db.delete_friend(from_user_ID = testemail_ID, to_user_ID = testemail_ID2)
if db.get_user(testemail_ID)['friends']:
    print('wrong with delete friend\n')
elif db.get_user(testemail_ID2)['friends']:
    print('wrong with delete friend in two way\n')
else:
    print('successfully delete friendship\n')
'''


attraction_ID = db.create_attraction(user_ID = testemail_ID, name = 'testattraction', lat = 100, lng = 50, intro = 'test_intro', rating = 2, if_private = False, cover = 'test_cover', marker = 'test_marker')
print('successfully create attraction\n')

db.create_review(user_ID = testemail_ID2, name = 'review name 000', intro = 'review intro 000', rating = 4, cover = 'review test cover0', marker = 'review test marker0', attraction_ID = attraction_ID)
#time.sleep(1)
db.create_review(user_ID = testemail_ID2, name = 'review name 001', intro = 'review intro 001', rating = 5, cover = 'review test cover1', marker = 'review test marker1', attraction_ID = attraction_ID)
#time.sleep(2)
db.create_review(user_ID = testemail_ID2, name = 'review name 002', intro = 'review intro 002', rating = 6, cover = 'review test cover2', marker = 'review test marker2', attraction_ID = attraction_ID)
#time.sleep(3)
db.create_review(user_ID = testemail_ID2, name = 'review name 003', intro = 'review intro 003', rating = 7, cover = 'review test cover3', marker = 'review test marker3', attraction_ID = attraction_ID)
#attraction_time = db.get_attraction(attraction_ID)

#db.add_friend(from_user_ID = testemail_ID, to_user_ID = testemail_ID2)
#print(db.get_all_friend_visited_attraction_IDs(testemail_ID))


#print(db.get_all_reviews(attraction_ID = attraction_ID))

#db.delete_all_reviews(attraction_ID = attraction_ID, user_ID = testemail_ID2)

#db.delete_attraction(attraction_ID = attraction_ID)
#print('successfully delete attraction')
#db.delete_user(email = 'testemail@testemail.com')



db.delete_user(email = 'testemail2@testemail.com')


if db.get_user_ID(email = 'testemail2@testemail.com') != 0:
    print('wrong with delete user\n')
else:
    print('successfully delete user\n')
