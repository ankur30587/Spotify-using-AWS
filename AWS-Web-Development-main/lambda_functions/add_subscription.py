import json
import boto3

dynamodb = boto3.resource('dynamodb', region_name = "us-east-1")
table = dynamodb.Table('subscription')

def lambda_handler(event, context):
    item = {
        'email': event['email'],
        'song_title': event['song_title']
    }
    table.put_item(Item=item)
    return {
        'statusCode': 200,
        'body': json.dumps('Song added to subscription successfully')
    }
