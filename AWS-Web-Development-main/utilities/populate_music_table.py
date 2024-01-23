import boto3
import json
import uuid

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb', region_name = "us-east-1")
table = dynamodb.Table('music')

# Load data from a1.json
with open('a1.json', 'r') as f:
    data = json.load(f)

# Iterate over songs and add to table
for song in data['songs']:
    table.put_item(
        Item={
            'id' : str(uuid.uuid4()),
            'title': song['title'],
            'artist': song['artist'],
            'year': song['year'],
            'web_url': song['web_url'],
            'image_url': song['img_url']
        }
    )
    
print("Data loaded successfully!")
