import os
import boto
import boto3
from boto import dynamodb2
from boto.dynamodb2.table import Table
import boto.s3.connection
from boto.s3.connection import S3Connection, Bucket, Key
from time import gmtime, strftime
import config
from config import *
import json
from boto3.dynamodb.conditions import Key, Attr
import math

class Connect_to_db:
    def __init__(self):
        self.my_region = MY_REGION
        self.my_aws_access_key_id = MY_AWS_ACCESS_KEY_ID
        self.my_aws_secret_access_key = MY_AWS_SECRET_ACCESS_KEY
        self.dynamodb = self.connect_to_dynamodb()
        self.s3_bucket = self.connect_to_s3_storage()
    
###### connection    
    def connect_to_dynamodb(self):
        dynamodb = boto3.resource(
            'dynamodb',
            region_name = self.my_region,
            aws_access_key_id = self.my_aws_access_key_id,
            aws_secret_access_key = self.my_aws_secret_access_key
        )
        return dynamodb
    
    def connect_to_s3_storage(self):
        s3 = boto.s3.connect_to_region(
            self.my_region,
            aws_access_key_id = self.my_aws_access_key_id,
            aws_secret_access_key = self.my_aws_secret_access_key,
            # host = 's3-website-us-east-1.amazonaws.com',
            # is_secure=True,               # uncomment if you are not using ssl
            calling_format = boto.s3.connection.OrdinaryCallingFormat(),
        )
        bucket = s3.get_bucket('smileyphototest')
        return bucket
    
    def upload_file_to_s3(self, file_name):
        path = '' #Directory Under which file should get upload
        full_key_name = os.path.join(path, file_name)
        k = Key(self.s3_bucket)
        k.key = 'test_key'
        k.set_contents_from_filename(full_key_name)

    def delete_file_from_s3(self, file_name):
        k = Key(self.s3_bucket)
        k.key = file_name
        self.s3_bucket.delete_key(k)


    def download_file_from_s3(self, file_name):
        file_key = self.s3_bucket.get_key(file_name)
        file_url = file_key.generate_url(3600, query_auth=True, force_http=True)
        return file_url
    


####user 
# Get user ID from email
    def get_user_ID(self, email):
        email_table = self.dynamodb.Table('Emails')
        email_response = email_table.get_item(
            Key = {
                'email': email
            }
        )
        if not 'Item' in email_response.keys():
            print('user email does not exist')
            return 0
        item = email_response['Item']
        user_ID = item['user_ID']
        return user_ID

# login 
    def login(self, email, password):
        user_ID = self.get_user_ID(email)
        if user_ID == 0:
            return 0
        login_table = self.dynamodb.Table('Users')
        login_response = login_table.get_item(
            Key = {
                'user_ID': user_ID
            }
        )
        item = login_response['Item']
        if password != item['password']:
            return 1
        return item['user_ID']

# create user
    def create_user(self, email, password, name):
        email_table = self.dynamodb.Table('Emails')
        email_response = self.get_user_ID(email = email)
        if email_response != 0:
            print('user email already exist')
            return None
        user_ID = generate_unique_ID()
        email_table.put_item(
            Item = {
                'email': email,
                'user_ID': user_ID,
            }
        )
        login_table = self.dynamodb.Table('Users')
        login_table.put_item(
            Item = {
                'user_ID': user_ID,
                'password': password,
            }
        )
        user_table = self.dynamodb.Table('smiley_user')
        item = {
            'user_ID': user_ID,
            'discovered_list': [],
            'explore_list': [],
            'friends': [
                {
                    'user_ID': user_ID,
                    'creation_time': strftime('%Y-%m-%d %H:%M:%S', gmtime())
                }
            ],   
            'recently_visited': [],
            'name': name,
        }
        user_table.put_item(
            Item = item
        )
        # Automatically login after creating user
        return item

# Delete user
    def delete_user(self, email):
        user_ID = self.get_user_ID(email = email)
        user = self.get_user(user_ID = user_ID)
        #delete friends
        for friend in user['friends']:
            self.delete_friend(from_user_ID = user_ID, to_user_ID = friend['user_ID'])
        #delete explore list
        for attraction_ID in user['explore_list']:
            self.delete_attraction(attraction_ID = attraction_ID)
        #delete discover list
        for attraction_ID in user['discovered_list']:
            self.delete_all_reviews(attraction_ID = attraction_ID, user_ID = user_ID)
        # delete other staffs implement here
        
        email_table = self.dynamodb.Table('Emails')
        email_table.delete_item(
            Key = {
                'email': email
            }
        )
        user_table = self.dynamodb.Table('Users')
        user_table.delete_item(
            Key = {
                'user_ID': user_ID
            }
        )
        smiley_user_table = self.dynamodb.Table('smiley_user')
        smiley_user_table.delete_item(
            Key = {
                'user_ID': user_ID
            }
        )



# Get user information from dynamodb
    def get_user(self, user_ID):
        user_table = self.dynamodb.Table('smiley_user')
        user_response = user_table.get_item(
            Key = {
                'user_ID': user_ID
            }
        )
        return user_response['Item']


###friend
# Add a new friendship  rewrite using update function in the future
    def add_friend(self, from_user_ID, to_user_ID):
        from_item = self.get_user(from_user_ID)
        to_item = self.get_user(to_user_ID)
        current_time = strftime('%Y-%m-%d %H:%M:%S', gmtime())
        from_item['friends'].append( 
            {
            'user_ID': to_user_ID,    
            'creation_time': current_time
            }
        )
        to_item['friends'].append( 
            {
            'user_ID': from_user_ID,    
            'creation_time': current_time
            }
        )
        user_table = self.dynamodb.Table('smiley_user')
        user_table.put_item(
            Item = from_item
        )
        user_table.put_item(
            Item = to_item
        )

# Delete a friendship rewrite with update function in the future
    def delete_friend(self, from_user_ID, to_user_ID):
        from_item = self.get_user(from_user_ID)
        to_item = self.get_user(to_user_ID)
        from_friend_list = from_item['friends']
        for item in from_friend_list:
            if item['user_ID'] == to_user_ID:
                from_item['friends'].remove(item)
        to_friend_list = to_item['friends']
        for item in to_friend_list:
            if item['user_ID'] == from_user_ID:
                to_item['friends'].remove(item)
        user_table = self.dynamodb.Table('smiley_user')
        user_table.put_item(
            Item = from_item
        )
        user_table.put_item(
            Item = to_item
        )


###attraction

# Get attraction item with attraction_ID
    def get_attraction(self, attraction_ID):
        attraction_table = self.dynamodb.Table('Attractions')
        attraction_response = attraction_table.get_item(
            Key = {
                'attraction_ID': attraction_ID
            }
        )
        return attraction_response['Item']

# Create a new attraction
    def create_attraction(self, user_ID, name, lat, lng, intro, rating, if_private, cover, marker):
        attraction_table = self.dynamodb.Table('Attractions')
        attraction_ID = generate_unique_ID()
        attraction_table.put_item(
            Item = {
                'attraction_ID': attraction_ID,
                'sorting_key': 0,    #specific for basic info
                'review_list': 1,    #number of review_lists
                'explorer_ID': user_ID,
                'name': name,
                'lat': lat,
                'lng': lng,
                'intro': intro,
                'rating': rating,
                'if_private': if_private,
                'cover': cover,
                'marker': marker,
                'discoverer': [user_ID],
                'time': strftime('%Y-%m-%d %H:%M:%S', gmtime()),
            }
        )
        attraction_table.put_item(
            Item = {
                'attraction_ID': attraction_ID,
                'sorting_key':  1,
                'review_count': 1,
                'review_list': [
                    {
                        'reviewer_ID': user_ID,
                        'name': name,
                        'intro': intro,
                        'rating': rating,
                        'cover': cover,
                        'marker': marker,
                        'time': strftime('%Y-%m-%d %H:%M:%S', gmtime())
                    }
                ],
            }
        )
        user = self.get_user(user_ID)
        user['explore_list'].append(attraction_ID)
        user_table = self.dynamodb.Table('smiley_user')
        user_table.put_item(
            Item = user
        )
        attraction_location_table = self.dynamodb.Table('Attraction_locations')
        attraction_location_table.put_item(
            Item = {
                'partition_key': compute_partition_key(lat = lat, lng = lng),
                'lat': lat,
                'lng': lng,
                'attraction_ID': attraction_ID
            }
        )
        self.upload_file_to_s3(cover)
        self.upload_file_to_s3(maker)
        return attraction_ID

# Get nearby attraction_ID with latitude and longitude
    def get_attraction_ID_list(self, lat, lng, boundary):
        partition_key = compute_partition_key(lat = lat, lng = lng)
        attraction_location_table = self.dynamodb.Table('Attraction_locations')  
        response = attraction_location_table.query(
            KeyConditionExpression = Key('partition_key').eq(partition_key)
        )
        items = response['Items']
        attraction_ID_list = []
        for item in items:
            distance = math.sqrt((item['lat'] - lat) * (item['lat'] - lat) + (item['lng'] - lng) * (item['lng'] - lng))
            if distance < boundary:
                attraction_ID_list.append(item['attraction_ID'])
        return attraction_ID_list
        
# Delete an attraction
    def delete_attraction(self, attraction_ID):
        attraction_table = self.dynamodb.Table('Attractions')
        attraction_response = attraction_table.get_item(
            Key = {
                'attraction_ID': attraction_ID,
                'sorting_key': 0
            }
        )
        if not 'Item' in attraction_response.keys():
            print('attraction does not exist')
            return 0
        item = attraction_response['Item']
        #print(item)
        #delete from all discoverers' visited
        user_table = self.dynamodb.Table('smiley_user')
        for user_ID in item['discoverer']:
            user = self.get_user(user_ID)
            for visited_place in user['discovered_list']:
                if visited_place['attraction_ID'] == attraction_ID:
                    user['discovered_list'].remove(visited_place)
            user_table.put_item(
                Item = user
            )
        #delete from explorer's explore_list
        user = self.get_user(item['explorer_ID'])
        user['explore_list'].remove(attraction_ID)
        user_table.put_item(
            Item = user
        )  
        #add more deletion here


        #delete from attraction table
        for i in range(0, item['review_list'] + 1):
            attraction_table.delete_item(
                Key = {
                    'attraction_ID': attraction_ID,
                    'sorting_key': i
                }
            )
        #delete from attraction_location table
        attraction_location_table = self.dynamodb.Table('Attraction_locations')
        attraction_location_table.delete_item(
            Key = {
                'partition_key': compute_partition_key(lat = item['lat'], lng = item['lng']),
                'attraction_ID': attraction_ID
            }
        ) 
        
###review

# Create a review
    def create_review(self, user_ID, name, intro, rating, cover, marker, attraction_ID):
        # Upload file to s3
        self.upload_file_to_s3(cover)
        self.upload_file_to_s3(maker)
        attraction_table = self.dynamodb.Table('Attractions')
        attraction_response = attraction_table.get_item(
            Key = {
                'attraction_ID': attraction_ID,
                'sorting_key': 0
            }
        )
        user_table = self.dynamodb.Table('smiley_user')
        user_response = user_table.get_item(
            Key = {
                'user_ID': user_ID
            }
        )
        user = user_response['Item']
        user['discovered_list'].append(attraction_ID)
        user_table.put_item(
            Item = user
        )
        attraction = attraction_response['Item']
        for i in range(1,attraction['review_list'] + 1):
            attraction_response = attraction_table.get_item(
                Key = {
                    'attraction_ID': attraction_ID,
                    'sorting_key': i
                }
            )
            if not 'Item' in attraction_response.keys():
                attraction_table.put_item(
                    Item = {
                        'attraction_ID': attraction_ID,
                        'sorting_key': i,
                        'review_count': 1,
                        'review_list': [
                            {
                                'reviewer_ID': user_ID,
                                'name': name,
                                'intro': intro,
                                'rating': rating,
                                'cover': cover,
                                'marker': marker,
                                'time': strftime('%Y-%m-%d %H:%M:%S', gmtime())
                            }
                        ],
                    }
                )
                return    
            if attraction_response['Item']['review_count'] < REVIEW_CAPACITY_PER_STORAGE_ITEM:
                item = attraction_response['Item']
                item['review_list'].append(
                    {
                        'reviewer_ID': user_ID,
                        'name': name,
                        'intro': intro,
                        'rating': rating,
                        'cover': cover,
                        'marker': marker,
                        'time': strftime('%Y-%m-%d %H:%M:%S', gmtime()),
                    }
                )
                item['review_count'] = item['review_count'] + 1
                attraction_table.put_item(
                    Item = item
                )
                return
        attraction['review_list'] = attraction['review_list'] + 1
        attraction_table.put_item(
            Item = attraction
        )
        attraction_table.put_item(
            Item = {
                'attraction_ID': attraction_ID,
                'sorting_key': attraction['sorting_key'] + 1,
                'review_count': 1,
                'review_list': [
                    {
                        'reviewer_ID': user_ID,
                        'name': name,
                        'intro': intro,
                        'rating': rating,
                        'cover': cover,
                        'marker': marker,
                        'time': strftime('%Y-%m-%d %H:%M:%S', gmtime())
                    }
                ],
            }
        )

# Delete all reviews under an attraction by a user
    def delete_all_reviews(self, attraction_ID, user_ID):
        attraction_table = self.dynamodb.Table('Attractions')
        attraction_info = attraction_table.get_item(
            Key = {
                'attraction_ID': attraction_ID,
                'sorting_key': 0
            }
        )
        review_number = attraction_info['Item']['review_list']
        for i in range(1,review_number + 1):
            review_list_response = attraction_table.get_item(
                Key = {
                    'attraction_ID': attraction_ID,
                    'sorting_key': i
                }
            )
            review_list = review_list_response['Item']
            for_loop_review_list_count = review_list['review_count']
            for j in range(for_loop_review_list_count - 1, -1, -1):
                if review_list['review_list'][j]['reviewer_ID'] == user_ID:
                    self.delete_file_from_s3(review_list['review_list'][j]['marker'])
                    self.delete_file_from_s3(review_list['review_list'][j]['cover'])
                    review_list['review_list'].pop(j)
                    review_list['review_count'] = review_list['review_count'] - 1

            if review_list['review_count'] == 0:
                attraction_table.delete_item(
                    Key = {
                        'attraction_ID': attraction_ID,
                        'sorting_key': i
                    }
                )
            else:
                attraction_table.put_item(
                    Item = review_list
                )

# Delete one review under an attraction by a user with time stamp
    def delete_one_reviews(self, attraction_ID, user_ID, time_stamp):
        attraction_table = self.dynamodb.Table('Attractions')
        attraction_info = attraction_table.get_item(
            Key = {
                'attraction_ID': attraction_ID,
                'sorting_key': 0
            }
        )
        review_number = attraction_info['Item']['review_list']
        for i in range(1,review_number + 1):
            review_list_response = attraction_table.get_item(
                Key = {
                    'attraction_ID': attraction_ID,
                    'sorting_key': i
                }
            )
            review_list = review_list_response['Item']
            for_loop_review_list_count = review_list['review_count']
            for j in range(for_loop_review_list_count - 1, -1, -1):
                if review_list['review_list'][j]['reviewer_ID'] == user_ID and review_list['review_list'][j]['time'] == time_stamp:
                    self.delete_file_from_s3(review_list['review_list'][j]['marker'])
                    self.delete_file_from_s3(review_list['review_list'][j]['cover'])
                    review_list['review_list'].pop(j)
                    review_list['review_count'] = review_list['review_count'] - 1
                    if review_list['review_count'] == 0:
                        attraction_table.delete_item(
                            Key = {
                                'attraction_ID': attraction_ID,
                                'sorting_key': i
                            }
                        )
                    else:
                        attraction_table.put_item(
                            Item = review_list
                        )
                    return

# Get all the reviews under an attraction
    def get_all_reviews(self, attraction_ID):
        ans_list = []
        attraction_table = self.dynamodb.Table('Attractions')
        attraction_info = attraction_table.get_item(
            Key = {
                'attraction_ID': attraction_ID,
                'sorting_key': 0
            }
        )
        review_number = attraction_info['Item']['review_list']
        for i in range(1,review_number + 1):
            review_list_response = attraction_table.get_item(
                Key = {
                    'attraction_ID': attraction_ID,
                    'sorting_key': i
                }
            )
            review_list = review_list_response['Item']
            for review in review_list['review_list']:
                ans_list.append(review)
        return ans_list

# Get all friend visited attraction_IDs
    def get_all_friend_visited_attraction_IDs(self, user_ID):
        user_table = self.dynamodb.Table('smiley_user')
        user_response = user_table.get_item(
            Key = {
                'user_ID': user_ID
            }
        )
        ans_ID_list = []
        friend_list = user_response['Item']['friends']
        print(friend_list)
        for friendship in friend_list:
            friend = self.get_user(user_ID = friendship['user_ID'])
            for attraction_ID in friend['discovered_list']:
                if attraction_ID not in ans_ID_list:
                    ans_ID_list.append(attraction_ID)
        return ans_ID_list 

# Get all nearby attraction_IDs
    def get_nearby_attraction_ID(self, lat, lng):
        attraction_location_table = self.dynamodb.Table('Attraction_locations')
        partition_key_list = generate_partition_key_list(lat = lat, lng = lng)
        ans_ID_list = []
        for partition_key in partition_key_list:
            attraction_location_response = attraction_location_table.query(
                KeyConditionExpression = Key('partition_key').eq(partition_key)
            )
            if not 'Item' in attraction_location_response.keys():
                for item in attraction_location_response['Item']:
                    ans_ID_list.append(item['attraction_ID'])
        return ans_ID_list
    
