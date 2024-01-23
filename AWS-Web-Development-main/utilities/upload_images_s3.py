import json
import urllib.request
import boto3

# replace with your S3 bucket name and region
bucket_name = 'artistsbucketkamau'
region = 'us-west-1'

# create an S3 client and bucket
s3 = boto3.client('s3', region_name=region)

# load data from a1.json
with open('a1.json') as f:
    data = json.load(f)

# download and upload each image to S3
for song in data['songs']:
    img_url = song['img_url']
    filename = img_url.split('/')[-1]
    urllib.request.urlretrieve(img_url, filename)
    with open(filename, 'rb') as f:
        s3.upload_fileobj(f, bucket_name, 'artists/' + filename)

