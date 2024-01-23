import json
import boto3

dynamodb = boto3.resource('dynamodb', region_name = "us-east-1")
table = dynamodb.Table('login')

def lambda_handler(event, context):
    item = {
        'email': event['email'],
        'password': event['password'],
        'user_name': event['username']
    }
    table.put_item(Item=item)
    return {
        'statusCode': 200,
        'body': json.dumps('User added successfully')
    }
