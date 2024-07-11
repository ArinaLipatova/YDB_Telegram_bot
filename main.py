import json
import logging
import os

import boto3
from botocore.exceptions import ClientError

def read_user(user_id, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource(
                'dynamodb',
                endpoint_url=os.environ.get('USER_STORAGE_URL'),
                region_name = 'ru-central1',
                aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
                )
    table = dynamodb.Table('Users')
    try:
        response = table.get_item(Key={'user_id': str(user_id)})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response

def create_user(user_id, first_name, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource(
                'dynamodb',
                endpoint_url=os.environ.get('USER_STORAGE_URL'),
                region_name = 'ru-central1',
                aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
                )

    table = dynamodb.Table('Users')
    response = table.put_item(
        Item={
        'user_id': str(user_id),
        'first_name': str(first_name)
        }
    )
    return response

def handler(event, context):
    dynamodb = boto3.resource(
                'dynamodb',
                endpoint_url=os.environ.get('USER_STORAGE_URL'),
                region_name = 'ru-central1',
                aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
                )
    body = json.loads(event['body'])
    user_query = read_user(body['message']['chat']['id'], dynamodb)
    if 'Item' not in user_query:
        create_user(body['message']['chat']['id'], body['message']['from']['first_name'], dynamodb)
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'method': 'sendMessage',
                'chat_id': body['message']['chat']['id'],
                'text':  'Привет! Теперь я знаю как тебя зовут'
            }),
            'isBase64Encoded': False
        }
    user = user_query['Item']
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'method': 'sendMessage',
            'chat_id': body['message']['chat']['id'],
            'text':  f'Привет, {user["first_name"]}, давно не виделись!'
        }),
        'isBase64Encoded': False
    }