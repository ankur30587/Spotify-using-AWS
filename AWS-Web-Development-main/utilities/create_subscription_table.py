import boto3

dynamodb = boto3.resource('dynamodb', region_name = 'us-east-1')
table_name = 'subscription'

table = dynamodb.create_table(
    TableName=table_name,
    KeySchema=[
        {
            'AttributeName': 'email',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'song_title',
            'KeyType': 'RANGE'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'email',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'song_title',
            'AttributeType': 'S'
        }
    ],
    BillingMode='PAY_PER_REQUEST'
)

print('Table created:', table.table_status)
