import boto
import boto3
from boto.s3.key import Key
from boto import dynamodb2
from boto.dynamodb2.table import Table
import boto.s3.connection

import uuid


def generate_unique_ID():
    return str(uuid.uuid1())

def compute_partition_key(lat, lng):
    return str(int(lat) * 1000 + int(lng))

def generate_partition_key_list(lat, lng):
    return [
        str(int(lat + 1) * 1000 + int(lng + 1)),
        str(int(lat - 1) * 1000 + int(lng + 1)),
        str(int(lat) * 1000 + int(lng + 1)),
        str(int(lat + 1) * 1000 + int(lng - 1)),
        str(int(lat - 1) * 1000 + int(lng - 1)),
        str(int(lat) * 1000 + int(lng - 1)),
        str(int(lat + 1) * 1000 + int(lng)),
        str(int(lat - 1) * 1000 + int(lng)),
        str(int(lat) * 1000 + int(lng))
    ]

REVIEW_CAPACITY_PER_STORAGE_ITEM = 100

MY_REGION = 'us-west-1'
MY_AWS_ACCESS_KEY_ID = 'do not tell you'
MY_AWS_SECRET_ACCESS_KEY = 'do not tell you'
