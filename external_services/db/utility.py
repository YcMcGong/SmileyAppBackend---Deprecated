import uuid
import googlemaps

import boto3
import config
from config import MY_REGION, MY_AWS_ACCESS_KEY_ID, MY_AWS_SECRET_ACCESS_KEY


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



def generate_unique_ID():
    return str(uuid.uuid1())

def compute_partition_key(lat, lng):
    return str(int(float(lat) * 1000 + int(float(lng))))

def generate_partition_key_list(lat, lng):
    return [
        str(int(float(lat) + 1) * 1000 + int(float(lng) + 1)),
        str(int(float(lat) - 1) * 1000 + int(float(lng) + 1)),
        str(int(float(lat)) * 1000 + int(float(lng) + 1)),
        str(int(float(lat) + 1) * 1000 + int(float(lng) - 1)),
        str(int(float(lat) - 1) * 1000 + int(float(lng) - 1)),
        str(int(float(lat)) * 1000 + int(float(lng) - 1)),
        str(int(float(lat) + 1) * 1000 + int(float(lng))),
        str(int(float(lat) - 1) * 1000 + int(float(lng))),
        str(int(float(lat)) * 1000 + int(float(lng)))
    ]

def gps_to_address(lat, lng):
    gmaps = googlemaps.Client(key='AIzaSyBWI6d4t99Hpdxv8DSUXBoPwn1m10QxCCc')
    data = gmaps.reverse_geocode((lat, lng))
    if data:
        address = data[0]['formatted_address']
        return address
    else: 
        return 'Not exist'