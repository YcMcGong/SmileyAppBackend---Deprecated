import config
from config import *
import boto3
from boto3.dynamodb.conditions import Key, Attr
import utility
from utility import *



dynamodb.create_table(
    TableName = 'Attractions',
    KeySchema = [
        {
            'AttributeName': 'attraction_ID',
            'KeyType': 'HASH'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'attraction_ID',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 1,
        'WriteCapacityUnits': 1
    }
)

dynamodb.create_table(
    TableName = 'Reviews',
    KeySchema = [
        {
            'AttributeName': 'review_ID',
            'KeyType': 'HASH'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'review_ID',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 1,
        'WriteCapacityUnits': 1
    }
)



dynamodb.create_table(
    TableName = 'Users',
    KeySchema = [
        {
            'AttributeName': 'user_ID',
            'KeyType': 'HASH'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'user_ID',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 1,
        'WriteCapacityUnits': 1
    }
)

dynamodb.create_table(
    TableName = 'smiley_user',
    KeySchema = [
        {
            'AttributeName': 'user_ID',
            'KeyType': 'HASH'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'user_ID',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 1,
        'WriteCapacityUnits': 1
    }
)

dynamodb.create_table(
    TableName = 'Emails',
    KeySchema = [
        {
            'AttributeName': 'email',
            'KeyType': 'HASH'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'email',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 1,
        'WriteCapacityUnits': 1
    }
)

dynamodb.create_table(
    TableName = 'Attraction_locations',
    KeySchema = [
        {
            'AttributeName': 'partitionKey',
            'KeyType': 'HASH'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'partitionKey',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 1,
        'WriteCapacityUnits': 1
    }
)

dynamodb.create_table(
    TableName = 'Addresses',
    KeySchema = [
        {
            'AttributeName': 'address',
            'KeyType': 'HASH'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'address',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 1,
        'WriteCapacityUnits': 1
    }
)