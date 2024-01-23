import boto3
import json

# API endpoint
endpoint_url = 'https://lambda.us-east-1.amazonaws.com/2015-03-31/functions/arn:aws:lambda:us-east-1:360758219905:function:all_songs/invocations'

# Create a session using AWS credentials
session = boto3.Session()

# Make a request to the API endpoint
client = session.client('lambda', region_name='us-east-1')
payload = {
        "operation": "retrieve_all_music",
        "tableName": "music"
        }
response = client.invoke(
        FunctionName='all_songs',
        InvocationType='RequestResponse',
        Payload=json.dumps(payload)
        )

# Extract the JSON string from the response body and parse it
json_data = json.loads(response['Payload'].read().decode('utf-8'))
song_data = json.loads(json_data['body'])

# Print the song data
for song in song_data:
        print(f"Title: {song['title']}")
        print(f"Artist: {song['artist']}")
        print(f"Year: {song['year']}")
        print(f"ID: {song['id']}")
        print(f"Image URL: {song['image_url']}")
        print(f"Web URL: {song['web_url']}")
