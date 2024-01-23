import boto3

# create the DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name = "us-east-1")

# create the "login" table
table = dynamodb.create_table(
    TableName='login',
    KeySchema=[
        {
            'AttributeName': 'email',
            'KeyType': 'HASH'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'email',
            'AttributeType': 'S'
        }
    ],
    BillingMode='PAY_PER_REQUEST'
)

# wait for the table to be created
table.meta.client.get_waiter('table_exists').wait(TableName='login')
