import json
import boto3

dynamodb = boto3.resource('dynamodb', region_name = "us-east-1")
table = dynamodb.Table('music')

def lambda_handler(event, context):
    response = table.scan()
    items = response['Items']
    return {
        'statusCode': 200,
        'body': json.dumps(items)
    }
