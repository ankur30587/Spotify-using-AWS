import json
import boto3

dynamodb = boto3.resource('dynamodb', region_name = "us-east-1")
table = dynamodb.Table('subscription')

def lambda_handler(event, context):
    response = table.delete_item(
        Key={
            'email': event['email'],
            'song_title': event['song_title']
        }
    )
    return {
        'statusCode': 200,
        'body': json.dumps('Subscription deleted successfully')
    }
