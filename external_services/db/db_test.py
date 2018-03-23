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

my_region = MY_REGION
my_aws_access_key_id = MY_AWS_ACCESS_KEY_ID
my_aws_secret_access_key = MY_AWS_SECRET_ACCESS_KEY

def connect_to_dynamodb():
    dynamodb = boto3.resource(
        'dynamodb',
        region_name = my_region,
        aws_access_key_id = my_aws_access_key_id,
        aws_secret_access_key = my_aws_secret_access_key
    )
    return dynamodb
dynamodb = connect_to_dynamodb()

def connect_to_s3_storage():
    s3 = boto3.resource(
        's3',
        region_name = my_region,
        aws_access_key_id = my_aws_access_key_id,
        aws_secret_access_key = my_aws_secret_access_key
    )
    return s3
s3 = connect_to_s3_storage()

def upload_file_to_s3(file):
    bucket = s3.Bucket('thesmileyappstorage')
    key = generate_unique_ID()
    obj = bucket.Object(key)
    obj.upload_fileobj(file)
    return key

def delete_file_from_s3(self, key):
    bucket = s3.Bucket('thesmileyappstorage')
    bucket.delete_key(key)



app = Flask(__name__)




# Routing from here
@app.route('/', methods=['GET', 'POST'])
def test():
    return jsonify({'one':1, 'two':2})

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
    return jsonify({'error':1})

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
            print('user email does not exist')
            return jsonify({'error': 'email does not exist'})
        item = email_response['Item']
        user_ID = item['user_ID']
        return user_ID

# assume valid input when creating new user
@app.route('/create_user', methods = ['GET', 'POST']) 
def create_user():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
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
        return jsonify(item)

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
        print(email)
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
        return jsonify({'one':1, 'two':2})
        
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
                'creation_time': current_time
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
                'creation_time': current_time
            }
        ) 
        smiley_user_table.put_item(
            Item = from_user
        )
        smiley_user_table.put_item(
            Item = to_user
        )
        return jsonify({'one':1, 'two':2})

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
        return jsonify({'one':1, 'two':2})


@app.route('/get_attraction', methods = ['GET', 'POST'])
def get_attraction():
    if request.method == 'GET':
        attraction_ID = request.args.get('attraction_ID')
        attraction_table = dynamodb.Table('Attractions')
        response = attraction_table.get_item(
            Key = {
                'attraction_ID': attraction_ID
            }
        )
        return jsonify(response['Item'])

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
        if_custom = request.files.get('if_costum')
        attraction_ID = generate_unique_ID()
        cover = upload_file_to_s3(cover_file)
        marker = upload_file_to_s3(marker_file)
        attraction_table = dynamodb.Table('Attractions')
        attraction_table.put_item(
            Item = {
                'attraction_ID': attraction_ID,
                'review_number': "1",    #number of reviews
                'explorer_ID': explorer_ID,
                'name': name,
                'lat': lat,
                'lng': lng,
                'intro': intro,
                'rating': rating,
                'if_custom': if_custom,
                'cover': cover,
                'marker': marker,
                'discoverer': [explorer_ID],
                'creation_time': strftime('%Y-%m-%d %H:%M:%S', gmtime()),
                'update_time': strftime('%Y-%m-%d %H:%M:%S', gmtime()),
            }
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
                'creation_time': strftime('%Y-%m-%d %H:%M:%S', gmtime()),
            }
        )
        attraction_location_table = dynamodb.Table('Attraction_locations')
        attraction_location_table.put_item(
            Item = {
                'partition_key': compute_partition_key(lat = lat, lng = lng),
                'lat': lat,
                'lng': lng,
                'attraction_ID': attraction_ID
            }
        )
        return attraction_ID


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
        review_number = int(attraction['review_number']) 
        review_table = dynamodb.Table('Reviews')
        review_table.put_item(
            Item = {
                'attraction_ID': attraction_ID,
                'review_ID': str(review_number),
                'reviewer_ID': user_ID,
                'intro': intro,
                'rating': rating,
                'cover': cover,
                'creation_time': strftime('%Y-%m-%d %H:%M:%S', gmtime()),
            }
        )
        response = attraction_table.update_item(
            Key = {
                'attraction_ID': attraction_ID
            },
            UpdateExpression = "set review_number = :n, update_time = :t",
            ExpressionAttributeValues = {
                ':n': str(review_number + 1),
                ':t': strftime('%Y-%m-%d %H:%M:%S', gmtime())
            },
            
            ReturnValues = "UPDATED_NEW"
        )
        return 'success post review'
        


if __name__ == '__main__':
    # app.debug = True
    print(strftime('%Y-%m-%d %H:%M:%S', gmtime()))
    print(strftime('%Y-%m-%d %H:%M:%S', gmtime()))
    print(strftime('%Y-%m-%d %H:%M:%S', gmtime()))
    print(strftime('%Y-%m-%d %H:%M:%S', gmtime()))
    print(strftime('%Y-%m-%d %H:%M:%S', gmtime()))
    print(strftime('%Y-%m-%d %H:%M:%S', gmtime()))
    app.run(host = '0.0.0.0', port = 5000)