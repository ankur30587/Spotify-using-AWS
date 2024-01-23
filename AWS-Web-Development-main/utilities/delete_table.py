import sys
import boto3

if len(sys.argv) < 2:
    print("Error: Table name not provided")
    sys.exit(1)

table_name = sys.argv[1]

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table(table_name)

table.delete()

print("Table deleted:", table_name)