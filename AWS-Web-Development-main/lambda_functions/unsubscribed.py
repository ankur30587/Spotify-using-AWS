import json
import boto3

dynamodb = boto3.resource('dynamodb', region_name = "us-east-1")
subscription_table = dynamodb.Table('subscription')
songs_table = dynamodb.Table('music')

def lambda_handler(event, context):
    # Get all songs in the songs table
    response = songs_table.scan()
    all_songs = response['Items']
    
    # Get songs subscribed by user
    response = subscription_table.query(
        KeyConditionExpression='email = :email',
        ExpressionAttributeValues={
            ':email': event['email']
        }
    )
    subscribed_songs = response['Items']
    
    # Find the songs that are not subscribed by the user
    unsubscribed_songs = [song for song in all_songs if song not in subscribed_songs]
    
    return {
        'statusCode': 200,
        'body': json.dumps(unsubscribed_songs)
    }
