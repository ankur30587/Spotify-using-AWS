import json
import boto3

dynamodb = boto3.resource('dynamodb', region_name = "us-east-1")
table = dynamodb.Table('login')

def lambda_handler(event, context):
    response = table.get_item(
        Key={
            'email': event['email']
        }
    )
    return {
        'statusCode': 200,
        'body': json.dumps(response['Item'])
    }
