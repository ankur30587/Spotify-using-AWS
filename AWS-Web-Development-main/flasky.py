import boto3
import json
import os

from flask import (Flask, render_template, request, redirect, url_for,
        session, flash)

# API endpoint
generic_url = 'https://lambda.us-east-1.amazonaws.com/2015-03-31/functions' + \
        '/arn:aws:lambda:us-east-1:360758219905:function:{}/invocations'

# Create a session using AWS credentials
boto_session = boto3.Session()

# Make a request to the API endpoint
client = boto_session.client('lambda', region_name='us-east-1')

# Create an s3 client
s3 = boto3.client('s3', region_name = 'us-east-1')

def all_songs():
    """
    Retrieves all songs in the music table
    """
    # modify endpoint url
    endpoint_url = generic_url.format("all_songs")

    # define payload
    payload = {
            "operation": "retrieve_all_music",
            "tableName": "music"
            }
    
    # invoke lambda function
    response = client.invoke(
            FunctionName='all_songs',
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
            )

    # Extract the JSON string from the response body and parse it
    json_data = json.loads(response['Payload'].read().decode('utf-8'))
    data = json.loads(json_data['body'])

    return data


def add_subscription(email, song_title):
    """
    Adds a music item as part of user's subscription
    """
    # modify endpoint url
    endpoint_url = generic_url.format("add_subscription")

    # define payload
    payload = {
            "email" : email,
            "song_title" : song_title
            }
    
    # invoke lambda function
    response = client.invoke(
            FunctionName='add_subscription',
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
            )

    # Extract the JSON string from the response body and parse it
    json_data = json.loads(response['Payload'].read().decode('utf-8'))
    data = json.loads(json_data['body'])

    return data


def add_user(email, password, username):
    """
    Adds a new user to the login table in DynamoDB
    """
    # modify endpoint url
    endpoint_url = generic_url.format("add_user")

    # define payload
    payload = {
            "email": email,
            "password": password,
            "username": username
            }
    
    # invoke lambda function
    response = client.invoke(
            FunctionName='add_user',
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
            )

    # Extract the JSON string from the response body and parse it
    json_data = json.loads(response['Payload'].read().decode('utf-8'))
    data = json.loads(json_data['body'])

    return data

def delete_subscription(email, song_title):
    """
    Removes a subscription from a user's subscriptions record
    """
    # modify endpoint url
    endpoint_url = generic_url.format("delete_subscription")

    # define payload
    payload = {
            "email" : email,
            "song_title" : song_title
            }
    
    # invoke lambda function
    response = client.invoke(
            FunctionName='delete_subscription',
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
            )

    # Extract the JSON string from the response body and parse it
    json_data = json.loads(response['Payload'].read().decode('utf-8'))
    data = json.loads(json_data['body'])

    return data


def retrieve_user(email):
    """
    Retrieve data of single user from login table
    """
    # modify endpoint url
    endpoint_url = generic_url.format("retrieve_user")

    # define payload
    payload = {
            "email": email
            }
    
    # invoke lambda function
    response = client.invoke(
            FunctionName='retrieve_user',
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
            )

    # Extract the JSON string from the response body and parse it
    json_data = json.loads(response['Payload'].read().decode('utf-8'))
    data = json.loads(json_data['body'])

    return data


def unsubscribed(email):
    """
    Retrieve songs not subscribed by the user
    """
    # modify endpoint url
    endpoint_url = generic_url.format("unsubscribed")

    # define payload
    payload = {
            "email" : email
            }
    
    # invoke lambda function
    response = client.invoke(
            FunctionName='unsubscribed',
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
            )

    # Extract the JSON string from the response body and parse it
    json_data = json.loads(response['Payload'].read().decode('utf-8'))
    data = json.loads(json_data['body'])

    return data


def user_subscription(email):
    """
    Retrieve songs subscribed to the user
    """
    # modify endpoint url
    endpoint_url = generic_url.format("user_subscription")

    # define payload
    payload = {
            "email" : email
            }
    
    # invoke lambda function
    response = client.invoke(
            FunctionName='user_subscription',
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
            )

    # Extract the JSON string from the response body and parse it
    json_data = json.loads(response['Payload'].read().decode('utf-8'))
    data = json.loads(json_data['body'])

    return data


def get_url(image_url):
    """
    Retrieves the path to the image stored in our s3 bucket
    """
    filename = os.path.basename(image_url)
    url = s3.generate_presigned_url(
        ClientMethod = 'get_object',
        Params = {
            'Bucket' : 'artistsbucketkamau',
            'Key' : 'artists/' + filename
            },
        ExpiresIn = 3600
        )
    return url

#*********************************************************************************
#                               REQUEST ROUTES
#*********************************************************************************

# initialize our flask application
app = Flask(__name__)
app.secret_key = "$%vv%d6FEf7u"


@app.route('/filter_music', methods = ['GET', 'POST'])
def filter_music():
    """
    Returns filtered music based on provided parameter arguments
    """
    email = session['email']
    username = session['username']

    if request.method == 'POST':
        # get custom filters
        artist = request.form['artist']
        title = request.form['title']
        year = request.form['year']

        # query subscriptions
        subscribed_songs = user_subscription(email)
        unsubscribed_songs = unsubscribed(email)
        
        # append links to image files
        for item in subscribed_songs:
            item['filename'] = get_url(item['image_url'])

        for item in unsubscribed_songs:
            item['filename'] = get_url(item['image_url'])
        
        # actual filtering
        filtered_songs = []
        for song in unsubscribed_songs:
            if (artist == "" or artist in song['artist']) and (year == "" or year in song['year'])\
                    and (title == "" or title in song['title']):
                        filtered_songs.append(song)

        return render_template('dashboard.html', email = email, username = username,
                subscribed_songs = subscribed_songs, unsubscribed_songs = filtered_songs)


@app.route('/delete_music_subscription/<song_title>', methods = ['GET', 'POST'])
def delete_music_subscription(song_title):
    """
    Remove music item from current user's subscription
    """
    email = session['email']
    username = session['username']

    # delete subscription
    delete_subscription(email, str(song_title))

    # query subscriptions
    subscribed_songs = user_subscription(email)
    unsubscribed_songs = unsubscribed(email)

    # append url links to images of artists
    for item in subscribed_songs:
        item['filename'] = get_url(item['image_url'])

    for item in unsubscribed_songs:
        item['filename'] = get_url(item['image_url'])
        
    flash(f"{song_title} is no longer part of your subscription.")
    return render_template('dashboard.html', email = email, username = username,
                subscribed_songs = subscribed_songs, unsubscribed_songs = unsubscribed_songs)


@app.route('/add_music_subscription/<song_title>', methods = ['GET', 'POST'])
def add_music_subscription(song_title):
    """
    Add music item to current user's subscription
    """
    email = session['email']
    username = session['username']

    # add subscription
    add_subscription(email, str(song_title))

    # query subscriptions
    subscribed_songs = user_subscription(email)
    unsubscribed_songs = unsubscribed(email)

    # append url links to image of artists
    for item in subscribed_songs:
        item['filename'] = get_url(item['image_url'])

    for item in unsubscribed_songs:
        item['filename'] = get_url(item['image_url'])

    flash(f"{song_title} subscribed successfully.")
    return render_template('dashboard.html', email = email, username = username,
                subscribed_songs = subscribed_songs, unsubscribed_songs = unsubscribed_songs)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Add a new user to login table
    """
    if request.method == 'POST':
        # get user details
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        # check if email already exists in the login login_table
        try:
            if retrieve_user(email).get('email'):
                flash("The email address is already in use.")
                return redirect(url_for('register'))

        except KeyError:
            add_user(email, password, username)
            flash(f"Hi {username}. Your registration is successful. Welcome onboard.")
            # redirect to login page
            return redirect(url_for('login'))

    # render register page
    return render_template('register.html')


@app.route('/', methods = ['GET', 'POST'])
def index():
    """
    Root resource
    """
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Validate user credentials
    """
    if request.method == 'POST':
        # get user data
        email = request.form['email']
        password = request.form['password']
        
        # validate user credentials
        response = retrieve_user(email)
        if response.get("password") == password:
            # set the new values
            session['email'] = response.get('email')
            session['username'] = response.get('user_name')
            
            flash(f"Hi {session['username']}, welcome back to the dashboard.")
            return redirect(url_for('dashboard'))

        flash("Invalid email or password.")
        return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    """
    Terminate user session
    """
    session.clear()
    flash("You have successfully logged out. See you soon.")
    return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
    """
    Displays the dashboard
    """
    if 'email' in session:
        email = session['email']
        username = session['username']
        
        subscribed_songs = user_subscription(email)
        unsubscribed_songs = unsubscribed(email)

        for item in subscribed_songs:
            item['filename'] = get_url(item['image_url'])

        for item in unsubscribed_songs:
            item['filename'] = get_url(item['image_url'])
        
        return render_template('dashboard.html', email = email, username = username,
                subscribed_songs = subscribed_songs, unsubscribed_songs = unsubscribed_songs)
    else:
        return redirect(url_for('/'))


if __name__ == '__main__':
    app.run(debug=True)
