
'''
fundamental rules for collaboration
1.
all functions return true or false

2. 
all channels include a statue and auto-assign

3.
not assigned value is None

4.
all communications use json.dumps dictionars containing only strings 
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



# writing part
def write_user(
    discovered_list,email, exp_ID, experience, 
    explored_list, friends, name, recently_visited, 
    user_ID):
    table = dynamodb.Table('smiley_user')
    table.put_item(
        Item = {
            'discoveredList': discovered_list,
            'email': email,
            'exp_ID': exp_ID,
            'experience': experience,
            'friends': friends,
            'name': name,
            'recentlyVisited': recently_visited,
            'user_ID': user_ID,
            'exploredList': explored_list
        }
    )
    return True

def write_attraction(address, attraction_ID, 
    cover, explorer_ID, is_protected, intro, 
    lat, lng, marker, name, rating, review_list, 
    update_time):
    table = dynamodb.Table('Attractions')
    table.put_item(
        Item = {
            'address': address,
            'attraction_ID': attraction_ID,
            'cover': cover,
            'creationTime': strftime('%Y-%m-%d %H:%M:%S', gmtime()),
            'explorer_ID': explorer_ID,
            'intro': intro,
            'lat': lat,
            'lng': lng,
            'marker': marker,
            'name': name,
            'rating': rating,
            'review_list': review_list,
            'updateTime': update_time,
            'isProtected': is_protected
        }
    )
    return True

def write_review(attraction_ID, resource,
    intro, rating, review_ID, reviewer_ID):
    table = dynamodb.Table('Reviews')
    table.put_item(
        Item = {
            'attraction_ID': attraction_ID,
            'resource': resource,
            'creationTime': strftime('%Y-%m-%d %H:%M:%S', gmtime()),
            'intro': intro,
            'rating': rating,
            'review_ID': review_ID,
            'reviewer_ID': reviewer_ID
        }
    )
    return True

def write_address(attraction_ID, address):
    table = dynamodb.Table('Addresses')
    table.put_item(
        Item = {
            'address': address,
            'attraction_ID': attraction_ID
        }
    )
    return True

def write_attraction_location(attraction_ID, lat, lng):
    table = dynamodb.Table('Attraction_locations')
    partition_key = compute_partition_key(lat = float(lat), lng = float(lng))
    try:
        table.update_item(
            Key = {
                'partitionKey': partition_key
            },
            UpdateExpression = "set attraction_ID_list = list_append(:attraction_ID, attraction_ID_list)",
            ExpressionAttributeValues = {
                ':attraction_ID': attraction_ID
            },
            ReturnValues = "UPDATED_NEW"
        )
    except:
        table.put_item(
            Item = {
                'partitionKey': partition_key,
                'attraction_ID_list': [attraction_ID]
            }
        )
    return True

def write_email(email, user_ID, password):
    table = dynamodb.Table('Emails')
    response = table.get_item(
        Key = {
            'email': email
        }
    )
    if 'Item' in response.keys():
        return False
    else:
        table.put_item(
            Item = {
                'email': email,
                'user_ID': user_ID,
                'password': password
            }
        )
        return True

def write_friends(user_ID_1, user_ID_2, relation = '0'):
    table = dynamodb.Table('smiley_user')
    table.update_item(
        Key = {
            'user_ID': user_ID_1
        },
        UpdateExpression = "set friends = list_append(:friend, friends)",
        ExpressionAttributeValues = {
            ':friend': {
                'user_ID': user_ID2,
                'relation': relation,
                'creationTime': strftime('%Y-%m-%d %H:%M:%S', gmtime())
            }
        },
        ReturnValues = 'UPDATED_NEW'
    )


#########
#update section
#########

def update_attraction_by_review(attraction_ID, review_ID, user_ID):
    table = dynamodb.Table('Attractions')
    table.update_item(
        Key = {
            'attraction_ID': attraction_ID
        },
        UpdateExpression = "set update_time = :t, review_list = list_append(:vals ,review_list) ",
        ExpressionAttributeValues = {
            ':t': strftime('%Y-%m-%d %H:%M:%S', gmtime()),
            ':vals':[{
                'review_ID': review_ID,
                'time': strftime('%Y-%m-%d %H:%M:%S', gmtime()),
                'user_ID': user_ID
            }]   
        },
        ReturnValues = "UPDATED_NEW"
    )




# Routing from here
@app.route('/', methods=['GET', 'POST'])
def test():
    return json.dumps({'one':1, 'two':2})

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
           return json.dumps({'errorMessage': 'email not found'})
        user_ID = email_response['Item']['user_ID']
        login_table = dynamodb.Table('Users')
        login_response = login_table.get_item(
            Key = {
                'user_ID': user_ID
            }
        )
        item = login_response['Item']
        if password != item['password']:
            return json.dumps({'errorMessage': 'wrong password'})
        return json.dumps({'user_ID': item['user_ID']})
    return json.dumps({'errorMessage': 'not using get method'})

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
        return json.dumps(user_response['Item'])
    return json.dumps({'errorMessage': 'not using get method'})


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
            return json.dumps({'errorMessage': 'email does not exist'})
        item = email_response['Item']
        user_ID = item['user_ID']
        return json.dumps({'user_ID': user_ID})
    return json.dumps({'errorMessage': 'not using get method'})

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
        write_email(email = email, password = password, user_ID = user_ID)
        user_table = dynamodb.Table('smiley_user')
        item = {
            'user_ID': user_ID,
        }
        write_user(discovered_list = [], email = email, exp_ID = exp_ID, experience = experience, explored_list = [], friends = [], name = name, recently_visited = [], user_ID = user_ID)
        return json.dumps(item)
    return json.dumps({'errorMessage': 'not using post method'})
'''
@app.route('/update_user', methods = ['GET', 'POST']) 
def update_user():
    if request.method == 'POST':
        discovered_list = json.loads(request.form.get('discovered_list'))
        email = request.form.get('email')
        exp_ID = request.form.get('exp_ID')
        experience = request.form.get('exp_ID')
        explored_list = json.loads(request.form.get('explored_list'))
        friends = json.loads(request.form.get('friends'))
        name = request.form.get('name')
        password = request.form.get('password')
        recently_visited = json.loads(request.form.get('recently_visited'))
        user_ID = request.form.get('user_ID')
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
            'discovered_list': discovered_list,
            'explored_list': explored_list,
            'friends': friends,   
            'recently_visited': recently_visited,
            'name': name,
            'exp_ID': exp_ID,
            'experience': experience,
            'email': email,
            'password': password,
        }
        user_table.put_item(
            Item = item
        )
        return json.dumps(item)
    return json.dumps({'errorMessage': 'not using post method'})

'''

@app.route('/get_user_list', methods = ['GET', 'POST']) 
def get_user_list():
    if request.method == 'GET':
        user_ID_list = json.loads(request.args.get('user_ID_list'))
        user_table = dynamodb.Table('smiley_user')
        ans = {}
        for user_ID in user_ID_list:
            response = user_table.get_item(
                Key = {
                    'user_ID': user_ID
                }
            )
            if 'Item' in response.keys():
                ans[str(response['Item']['user_ID'])] = response['Item']
            else:
                return json.dumps({'errorMessage': 'user get error'})
        return json.dumps({'status': 'success', 'user_list': ans, 'return': True})

 

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
        return json.dumps({'status': 'success'})
    return json.dumps({'errorMessage': 'not using post method'})
        
@app.route('/add_friend', methods = ['GET', 'POST']) 
def add_friend():
    if request.method == 'POST':
        from_user_ID = request.form.get('from_user_ID')
        to_user_ID = request.form.get('to_user_ID')
        relation = request.form.get('relation')
        current_time = strftime('%Y-%m-%d %H:%M:%S', gmtime())
        write_friends(user_ID_1 = from_user_ID, user_ID_2 = to_user_ID, relation = relation)
        write_friends(user_ID_1 = to_user_ID, user_ID_2 = from_user_ID, relation = relation)
        return json.dumps({'status', 'success'})

    return json.dumps({'errorMessage': 'not using post method'})

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
        return json.dumps({'status': 'success'})
    return json.dumps({'errorMessage': 'not using post method'})

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
        return json.dumps(response['Item'])
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
        return json.dumps(ans)
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
            return json.dumps({'errorMessage': 'attraction not found'})
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
                    return json.dumps(response['Item'])
        return json.dumps({'errorMessage': 'attraction not found'})
    return json.dumps({'errorMessage': 'not using get method'})

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
        return json.dumps(response['Item'])
'''

@app.route('/get_attraction_list', methods = ['GET','POST'])
def get_attraction_list():
    if request.method == 'GET':
        attraction_ID_list = json.loads(request.args.get('attraction_ID_list'))
        attraction_table = dynamodb.Table('Attractions')
        ans = {}
        for attraction_ID in attraction_ID_list:
            response = attraction_table.get_item(
                Key = {
                    'attraction_ID': attraction
                }
            )
            if 'Item' in response.keys():
                ans[str(response['Item']['attraction_ID'])] = response['Item']
            else:
                return json.dumps({'errorMessage': 'user get error'})
        return json.dumps({
            'status': 'success', 
            'attraction_list': ans, 
            'return': True
            })


@app.route('/post_attraction', methods = ['GET', 'POST'])
def post_attraction():
    if request.method == 'POST':
        # Read data
        user_ID = request.form.get('explorer_ID')
        name = request.form.get('name')
        lat = request.form.get('lat')
        lng = request.form.get('lng')
        intro = request.form.get('intro')
        rating = request.form.get('rating')
        cover_file = request.files.get('cover')
        marker_file = request.files.get('marker')
        is_protected = request.form.get('isProtected')
        attraction_ID = generate_unique_ID()
        review_ID = generate_unique_ID()
        cover = upload_file_to_s3(cover_file)
        marker = upload_file_to_s3(marker_file)
        address = gps_to_address(lat = float(lat), lng = float(lng))
        current_time = strftime('%Y-%m-%d %H:%M:%S', gmtime())
        write_attraction(
            address = address, 
            attraction_ID = attraction_ID, 
            cover = cover, 
            explorer_ID = user_ID, 
            is_protected = is_protected, 
            intro = intro, 
            lat = lat, 
            lng = lng, 
            marker = marker, 
            name = name, 
            rating = rating, 
            review_list = [{'review_ID': review_ID, 'user_ID': user_ID, 'time': current_time}], 
            update_time = current_time
        )
        write_review(
            attraction_ID = attraction_ID,
            resource = cover,
            intro = intro, 
            rating = rating, 
            review_ID = review_ID, 
            reviewer_ID = user_ID
        )
        write_address(address = address, attraction_ID = attraction_ID)
        write_attraction_location(attraction_ID = attraction_ID, lat = lat, lng = lng)


        
        return json.dumps({'status': 'success', 'attraction_ID': attraction_ID})
    return json.dumps({'errorMessage': 'not using post method'})


@app.route('/post_review', methods = ['GET', 'POST'])
def post_review():
    if request.method == 'POST':
        attraction_ID = request.form.get('attraction_ID')
        intro = request.form.get('intro')
        rating = request.form.get('rating')
        resource_file = request.files.get('resource')
        user_ID = request.form.get('user_ID')
        resource = upload_file_to_s3(resource_file)
        review_ID = generate_unique_ID()
        write_review(
            attraction_ID = attraction_ID,
            resource = resource,
            intro = intro, 
            rating = rating, 
            review_ID = review_ID, 
            reviewer_ID = user_ID
        ) 
        update_attraction_by_review(review_ID = review_ID, attraction_ID = attraction_ID, user_ID = user_ID)
        return json.dumps({'status': 'success', 'review_ID': review_ID})
    return json.dumps({'errorMessage': 'not using post method'})
'''
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
                ans.append(review_response['Item'])
        return json.dumps({'attraction_ID': attraction_ID, 'review_list': ans})
    return json.dumps({'errorMessage': 'not using get method'})
'''
@app.route('/get_review', methods = ['GET', 'POST'])
def get_review():
    if request.method == 'GET':
        review_ID = request.args.get('review_ID')
        review_table = dynamodb.Table('Reviews')
        
        response = review_table.get_item(
            Key = {
                'review_ID': review_ID
            }
        )
        if 'Item' in response.keys():
            return json.dumps(response['Item'])
        return json.dumps({'errorMessage': 'review not exist'})
    return json.dumps({'errorMessage': 'not using get method'})


@app.route('/get_review_list', methods = ['GET','POST'])
def get_review_list():
    if request.method == 'GET':
        review_ID_list = json.loads(request.args.get('review_ID_list'))
        review_table = dynamodb.Table('Reviews')
        ans = {}
        for attraction_ID in attraction_ID_list:
            response = attraction_table.get_item(
                Key = {
                    'review_ID': attraction
                }
            )
            if 'Item' in response.keys():
                ans[str(response['Item']['attraction_ID'])] = response['Item']
            else:
                return json.dumps({'errorMessage': 'user get error'})
        return json.dumps({
            'status': 'success', 
            'attraction_list': ans, 
            'return': True
            })




if __name__ == '__main__':
    # app.debug = True
    print(strftime('%Y-%m-%d %H:%M:%S', gmtime()))
    app.run(host = '0.0.0.0', port = 5000)