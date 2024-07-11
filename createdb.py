import os

import boto3


def create_user_table():
    USER_STORAGE_URL='https://docapi.serverless.yandexcloud.net/ru-central1/**************/***********'
    AWS_ACCESS_KEY_ID='****************'
    AWS_SECRET_ACCESS_KEY='***************'
    dynamodb = boto3.resource(
        'dynamodb',
        endpoint_url=USER_STORAGE_URL,
        region_name = 'ru-central1',
        aws_access_key_id = AWS_ACCESS_KEY_ID,
        aws_secret_access_key = AWS_SECRET_ACCESS_KEY
        )
    table = dynamodb.create_table(
        TableName = 'Users',
        KeySchema=[
            {
                'AttributeName': 'user_id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {'AttributeName': 'user_id', 'AttributeType': 'S'}
        ]
    )
    return table

create_user_table()