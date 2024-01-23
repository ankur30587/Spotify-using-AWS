import json
import boto3

dynamodb = boto3.resource('dynamodb', region_name = "us-east-1")
table = dynamodb.Table('subscription')
songs_table = dynamodb.Table('music')

def lambda_handler(event, context):
    response = table.query(
        KeyConditionExpression='email = :email',
        ExpressionAttributeValues={
            ':email': event['email']
        }
    )

    songs = []
    for item in response['Items']:
        song_title = item['song_title']
        response = songs_table.get_item(
            Key={
                'title': song_title
            }
        )
        songs.append(response['Item'])

    return {
        'statusCode': 200,
        'body': json.dumps(songs)
    }
