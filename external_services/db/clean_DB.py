import config
from config import *
import boto3
from boto3.dynamodb.conditions import Key, Attr
import utility
from utility import *


dynamodb.Table('Attractions').delete()
dynamodb.Table('Reviews').delete()
dynamodb.Table('Users').delete()
dynamodb.Table('Addresses').delete()
dynamodb.Table('Attraction_locations').delete()
dynamodb.Table('Emails').delete()
dynamodb.Table('smiley_user').delete()

