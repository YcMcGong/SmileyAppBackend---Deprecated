
'''
fundamental rules for collaboration
1.
all functions return true or false

2. 
all channels include a statue and auto-assign

3.
not assigned value is None

4.
all communications use jsonify dictionars containing only strings 
'''


# coding=utf-8
from flask import jsonify
from flask import Flask, render_template, request, redirect, url_for, flash, current_app



# delete unused library later
import os
import boto3
from time import gmtime, strftime
import config
from config import *
import json
from boto3.dynamodb.conditions import Key, Attr
import math
import utility
from utility import *










app = Flask(__name__)




# Routing from here
@app.route('/', methods=['GET', 'POST'])
def test():
    return jsonify({'one':1, 'two':2})

@app.route('/user_autheticate', methods = ['GET', 'POST'])
def user_autheticate():
    if request.method == 'GET':
        email = request.args.get('email')
        password = request.args.get('password')
        email_table = dynamodb.Table('Emails')
        email_response = email_table.get_item(
            Key = {
                'email': email
            }
        )
        if not 'Item' in email_response.keys():
           return jsonify({'errorMessage': 'email not found'})
        user_ID = email_response['Item']['user_ID']
        login_table = dynamodb.Table('Users')
        login_response = login_table.get_item(
            Key = {
                'user_ID': user_ID
            }
        )
        item = login_response['Item']
        if password != item['password']:
            return jsonify({'errorMessage': 'wrong password'})
        return jsonify({'user_ID': item['user_ID']})
    return jsonify({'errorMessage': 'not using get method'})

@app.route('/get_user', methods = ['GET', 'POST'])
def get_user():
    if request.method == 'GET':
        user_ID = request.args.get('user_ID')
        user_table = dynamodb.Table('smiley_user')
        user_response = user_table.get_item(
            Key = {
                'user_ID': user_ID
            }
        )
        return jsonify(user_response['Item'])
    return jsonify({'errorMessage': 'not using get method'})


@app.route('/get_user_ID', methods = ['GET', 'POST'])
def get_user_ID():
    if request.method == 'GET':
        email = request.args.get('email')
        email_table = dynamodb.Table('Emails')
        email_response = email_table.get_item(
            Key = {
                'email': email
            }
        )
        if not 'Item' in email_response.keys():
            return jsonify({'errorMessage': 'email does not exist'})
        item = email_response['Item']
        user_ID = item['user_ID']
        return jsonify({'user_ID': user_ID})
    return jsonify({'errorMessage': 'not using get method'})

# assume valid input when creating new user
@app.route('/create_user', methods = ['GET', 'POST']) 
def create_user():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        exp_ID = request.form.get('exp_ID')
        experience =request.form.get('experience')
        user_ID = generate_unique_ID()
        email_table = dynamodb.Table('Emails')
        email_table.put_item(
            Item = {
                'email': email,
                'user_ID': user_ID,
            }
        )
        login_table = dynamodb.Table('Users')
        login_table.put_item(
            Item = {
                'user_ID': user_ID,
                'password': password,
                'email': email,
            }
        )
        user_table = dynamodb.Table('smiley_user')
        item = {
            'user_ID': user_ID,
            'discovered_list': [],
            'explored_list': [],
            'friends': [
                {
                    'user_ID': user_ID,
                    'creationTime': strftime('%Y-%m-%d %H:%M:%S', gmtime())
                }
            ],   
            'recently_visited': [],
            'name': name,
            'exp_ID': exp_ID,
            'experience': experience,
            'email': email,
            'password': password,
        }
        user_table.put_item(
            Item = item
        )
        return jsonify(item)
    return jsonify({'errorMessage': 'not using post method'})

# delete user through user_ID assuming valid input
@app.route('/delete_user', methods = ['GET', 'POST']) 
def delete_user():
    if request.method == 'POST':
        user_ID = request.form.get('user_ID')
        
        user_table = dynamodb.Table('Users')
        user = user_table.get_item(
            Key = {
                'user_ID': user_ID
            }
        )
        
        email = user['Item']['email']
        user_table.delete_item(
            Key = {
                'user_ID': user_ID
            }
        )
        email_table = dynamodb.Table('Emails')
        email_table.delete_item(
            Key = {
                'email': email
            }
        )
        smiley_user_table = dynamodb.Table('smiley_user')
        smiley_user_table.delete_item(
            Key = {
                'user_ID': user_ID
            }
        )
        return jsonify({'status': 'success'})
    return jsonify({'errorMessage': 'not using post method'})
        
@app.route('/add_friend', methods = ['GET', 'POST']) 
def add_friend():
    if request.method == 'POST':
        from_user_ID = request.form.get('from_user_ID')
        to_user_ID = request.form.get('to_user_ID')
        current_time = strftime('%Y-%m-%d %H:%M:%S', gmtime())
        smiley_user_table = dynamodb.Table('smiley_user')
        from_user_response = smiley_user_table.get_item(
            Key = {
                'user_ID': from_user_ID
            }
        )
        from_user = from_user_response['Item']
        from_user['friends'].append(
            {
                'user_ID': to_user_ID,
                'creationTime': current_time
            }
        )
        to_user_response = smiley_user_table.get_item(
            Key = {
                'user_ID': to_user_ID
            }
        )
        to_user = to_user_response['Item']
        to_user['friends'].append(
            {
                'user_ID': from_user_ID,
                'creationTime': current_time
            }
        ) 
        smiley_user_table.put_item(
            Item = from_user
        )
        smiley_user_table.put_item(
            Item = to_user
        )
        return jsonify({'status': 'success'})
    return jsonify({'errorMessage': 'not using post method'})

@app.route('/delete_friend', methods = ['GET', 'POST']) 
def delete_friend():
    if request.method == 'POST':
        from_user_ID = request.form.get('from_user_ID')
        to_user_ID = request.form.get('to_user_ID')
        smiley_user_table = dynamodb.Table('smiley_user')
        from_user_response = smiley_user_table.get_item(
            Key = {
                'user_ID': from_user_ID
            }
        )
        from_user = from_user_response['Item']
        from_friend_list = from_user['friends']
        for item in from_friend_list:
            if item['user_ID'] == to_user_ID:
                from_user['friends'].remove(item)
        from_friend_list = from_user['friends']
        to_user_response = smiley_user_table.get_item(
            Key = {
                'user_ID': to_user_ID
            }
        )
        to_user = to_user_response['Item']
        to_friend_list = to_user['friends']
        for item in to_friend_list:
            if item['user_ID'] == from_user_ID:
                to_user['friends'].remove(item)
        to_friend_list = to_user['friends']
        smiley_user_table.put_item(
            Item = from_user
        )
        smiley_user_table.put_item(
            Item = to_user
        )
        return jsonify({'status': 'success'})
    return jsonify({'errorMessage': 'not using post method'})

@app.route('/get_attraction_by_ID', methods = ['GET', 'POST'])
def get_attraction_by_ID():
    if request.method == 'GET':
        attraction_ID = request.args.get('attraction_ID')
        attraction_table = dynamodb.Table('Attractions')
        response = attraction_table.get_item(
            Key = {
                'attraction_ID': attraction_ID
            }
        )
        return jsonify(response['Item'])
'''
@app.route('/get_multiple_attraction_list', methods = ['GET', 'POST'])
def get_multiple_attraction_list():
    if request.method == 'GET':
        user_list_string = request.args.get('user_list')
        print(user_list_string)
        user_list = json.loads(user_list_string)
        print(user_list)
        ans = []
        user_table = dynamodb.Table('smiley_user')
        for user_ID in user_list:
            print(user_ID)
            user_response = user_table.get_item(
                Key = {
                    'user_ID': user_ID
                }
            )
            
            ans = ans + user_response['Item']['discovered_list'] + user_response['Item']['explore_list']
        print(ans)
        return jsonify(ans)
'''

@app.route('/get_attraction_by_coordinate', methods = ['GET', 'POST'])
def get_attraction_by_coordinate():
    if request.method == 'GET':
        lat = request.args.get('lat')
        lng = request.args.get('lng')
        attraction_table = dynamodb.Table('Attractions')
        attraction_location_table = dynamodb.Table('Attraction_locations')
        partition_key = compute_partition_key(lat = lat, lng = lng)
        response = attraction_location_table.get_item(
            Key = {
                'partitionKey': partition_key
            }
        )
        
        if not 'Item' in response.keys():
            return jsonify({'errorMessage': 'attraction not found'})
        attraction_ID_list = response['Item']['attraction_ID_list']
        attraction_table = dynamodb.Table('Attractions')
        for attraction_ID in attraction_ID_list:
            response = attraction_table.get_item(
                Key = {
                    'attraction_ID': attraction_ID
                }
            )
            if 'Item' in response.keys():
                attraction = response['Item']
                if attraction['lat'] == lat and attraction['lng'] == lng:
                    return jsonify(response['Item'])
        return jsonify({'errorMessage': 'attraction not found'})
    return jsonify({'errorMessage': 'not using get method'})

'''
@app.route('/get_nearby_attractions_by_coordinate', methods = ['GET', 'POST'])  # this method returns a list of attractions
def get_nearby_attractions_by_coordinate():
    if request.method == 'GET':
        lat = request.args.get('lat')
        lng = request.args.get('lng')
        attraction_location_table = dynamodb.Table('Attraction_locations')
        partition_key_list = generate_partition_key_list(lat = lat, lng = lng)
        ans_ID_list = []
        for partition_key in partition_key_list:
            attraction_location_response = attraction_location_table.query(
                KeyConditionExpression = Key('partitionKey').eq(partition_key)
            )
            if 'Item' in attraction_location_response.keys():
                for item in attraction_location_response['Item']:
                    distance = math.sqrt((item['lat'] - lat) * (item['lat'] - lat) + (item['lng'] - lng) * (item['lng'] - lng))
                    if distance < boundary:
                        ans_ID_list.append(item['attraction_ID'])
        return ans_ID_list
'''
'''
@app.route('/get_attraction_by_address', methods = ['GET', 'POST'])
def get_attraction_by_address():
    if request.method == 'GET':
        address = request.args.get('address')
        address_table = dynamodb.Table('Adresses')
        response = address_table.get_item(
            Key = {
                'address': address
            }
        )
        if not 'Item' in response.keys():
            return 'address not found'
        attraction_ID = response['Item']['attraction_ID']
        attraction_table = dynamodb.Table('Attractions')
        response = attraction_table.get_item(
            Key = {
                'attraction_ID': attraction_ID
            }
        )
        return jsonify(response['Item'])
'''


@app.route('/post_attraction', methods = ['GET', 'POST'])
def post_attraction():
    if request.method == 'POST':
        # Read data
        explorer_ID = request.form.get('explorer_ID')
        name = request.form.get('name')
        lat = request.form.get('lat')
        lng = request.form.get('lng')
        intro = request.form.get('intro')
        rating = request.form.get('rating')
        cover_file = request.files.get('cover')
        marker_file = request.files.get('marker')
        if_custom = request.form.get('ifCustom')
        attraction_ID = generate_unique_ID()
        cover = upload_file_to_s3(cover_file)
        marker = upload_file_to_s3(marker_file)
        address = gps_to_address(lat = float(lat), lng = float(lng))
        attraction_table = dynamodb.Table('Attractions')
        attraction = {
            'address': address,
            'attraction_ID': attraction_ID,
            'reviewNumber': "1",    #number of reviews
            'explorer_ID': explorer_ID,
            'name': name,
            'lat': lat,
            'lng': lng,
            'intro': intro,
            'rating': rating,
            'ifCustom': if_custom,
            'cover': cover,
            'marker': marker,
            'discoverer': [explorer_ID],
            'creationTime': strftime('%Y-%m-%d %H:%M:%S', gmtime()),
            'updateTime': strftime('%Y-%m-%d %H:%M:%S', gmtime()),
        }
        attraction_table.put_item(
            Item = attraction
        )
        review_table = dynamodb.Table('Reviews')
        review_table.put_item(
            Item = {
                'attraction_ID': attraction_ID,
                'review_ID': "0",
                'reviewer_ID': explorer_ID,
                'intro': intro,
                'rating': rating,
                'cover': cover,    
                'creationTime': strftime('%Y-%m-%d %H:%M:%S', gmtime()),
            }
        ) 
        address_table = dynamodb.Table('Addresses')
        address_table.put_item(
            Item = {
                'address': address,
                'attraction_ID': attraction_ID
            }
        )
        partition_key = compute_partition_key(lat = float(lat), lng = float(lng))
        attraction_location_table = dynamodb.Table('Attraction_locations')
        attraction_ID_list_response = attraction_location_table.get_item(
            Key = {
                'partitionKey': partition_key
            }
        )
        attraction_ID_list = []
        if 'Item' in attraction_ID_list_response.keys():
            attraction_ID_list = attraction_ID_list_response['Item']['attraction_ID_list']
            print(attraction_ID_list)
            print([attraction_ID])
            attraction_ID_list = attraction_ID_list + [attraction_ID]
        else:
            attraction_ID_list = [attraction_ID]
        attraction_location_table.put_item(
            Item = {
                'partitionKey': compute_partition_key(lat = lat, lng = lng),
                'attraction_ID_list': attraction_ID_list
            }
        )
        return jsonify(attraction)
    return jsonify({'errorMessage': 'not using post method'})


@app.route('/post_review', methods = ['GET', 'POST'])
def post_review():
    if request.method == 'POST':
        attraction_ID = request.form.get('attraction_ID')
        intro = request.form.get('intro')
        rating = request.form.get('rating')
        cover_file = request.files.get('cover')
        user_ID = request.form.get('user_ID')
        cover = upload_file_to_s3(cover_file)
        attraction_table = dynamodb.Table('Attractions')
        response = attraction_table.get_item(
            Key = {
                'attraction_ID': attraction_ID
            }
        )
        attraction = response['Item']
        review_number = int(attraction['reviewNumber']) 
        review = {
            'attraction_ID': attraction_ID,
            'review_ID': str(review_number),
            'reviewer_ID': user_ID,
            'intro': intro,
            'rating': rating,
            'cover': cover,
            'creationTime': strftime('%Y-%m-%d %H:%M:%S', gmtime()),
        }
        review_table = dynamodb.Table('Reviews')
        review_table.put_item(
            Item = review
        )
        response = attraction_table.update_item(
            Key = {
                'attraction_ID': attraction_ID
            },
            UpdateExpression = "set reviewNumber = :n, update_time = :t",
            ExpressionAttributeValues = {
                ':n': str(review_number + 1),
                ':t': strftime('%Y-%m-%d %H:%M:%S', gmtime())
            },
            
            ReturnValues = "UPDATED_NEW"
        )
        return jsonify(review)
    return jsonify({'errorMessage': 'not using post method'})

@app.route('/get_review_by_attraction_ID', methods = ['GET', 'POST'])
def get_review_by_attraction_ID():
    if request.method == 'GET':
        attraction_ID = request.args.get('attraction_ID')
        attraction_table = dynamodb.Table('Attractions')
        attraction_response = attraction_table.get_item(
            Key = {
                'attraction_ID': attraction_ID
            }
        )
        attraction = attraction_response['Item']
        review_number = int(attraction['review_number'])
        review_table = dynamodb.Table('Reviews')
        ans = []
        for i in range(review_number):
            review_response = review_table.get_item(
                Key = {
                    'attraction_ID': attraction_ID,
                    'review_ID': str(i)
                }
            )
            if 'Item' in review_response.keys():
                print(review_response['Item'])
                ans.append(review_response['Item'])
        return jsonify({'attraction_ID': attraction_ID, 'review_list': ans})
    return jsonify({'errorMessage': 'not using get method'})

@app.route('/get_review_by_attraction_ID_and_review_ID', methods = ['GET', 'POST'])
def get_review_by_attraction_ID_and_review_ID():
    if request.method == 'GET':
        attraction_ID = request.args.get('attraction_ID')
        review_ID = request.args.get('review_ID')
        review_table = dynamodb.Table('Reviews')
        response = review_table.get_item(
            Key = {
                'attraction_ID': attraction_ID,
                'review_ID': review_ID
            }
        )
        if 'Item' in response.keys():
            return response['Item']
        return jsonify({'errorMessage': 'review not exist'})
    return jsonify({'errorMessage': 'not using get method'})



if __name__ == '__main__':
    # app.debug = True
    print(strftime('%Y-%m-%d %H:%M:%S', gmtime()))
    app.run(host = '0.0.0.0', port = 5000)