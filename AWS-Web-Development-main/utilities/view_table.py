import boto3
import sys

# Check if the user provided the table name as a command line argument
if len(sys.argv) != 2:
    print("Usage: python view_table.py <table-name>")
    exit(1)

# Get the table name from the command line argument
table_name = sys.argv[1]

# Initialize the DynamoDB client with the region
dynamodb = boto3.client('dynamodb', region_name='us-east-1')

# Use describe_table to view the status of the table
response = dynamodb.describe_table(
    TableName=table_name
)

# Print the status of the table
print("Table status: ", response['Table']['TableStatus'])

# Initialize the DynamoDB resource with the region
dynamodb_resource = boto3.resource('dynamodb', region_name='us-east-1')

# Get a reference to the table
table = dynamodb_resource.Table(table_name)

# Use scan to retrieve the first 5 items in the table
response = table.scan(
    Limit=5
)

# Print the items
print("First 5 items in the table:")
for item in response['Items']:
    print(item)

