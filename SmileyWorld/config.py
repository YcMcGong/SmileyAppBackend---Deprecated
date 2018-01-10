import os
import boto
import boto3
from boto.s3.key import Key
from boto import dynamodb2
from boto.dynamodb2.table import Table
import boto.s3.connection


my_region = 'us-west-2'
my_aws_access_key_id = ''
my_aws_secret_access_key = ''

def connect_to_dynamodb():
    dynamodb = boto3.resource('dynamodb',region_name=my_region,aws_access_key_id=my_aws_access_key_id,aws_secret_access_key=my_aws_secret_access_key)
    return dynamodb

def connect_to_s3():
    s3 = boto.s3.connect_to_region(my_region,
                                     aws_access_key_id = my_aws_access_key_id,
                                     aws_secret_access_key = my_aws_secret_access_key,
                                     # host = 's3-website-us-east-1.amazonaws.com',
                                     # is_secure=True,               # uncomment if you are not using ssl
                                     calling_format = boto.s3.connection.OrdinaryCallingFormat(),
                                     )
    return s3
