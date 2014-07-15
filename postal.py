import os, config, base64
from datetime import datetime
import re

from flask import Flask, session, request, render_template, flash, redirect, url_for, g, jsonify
from flask_oauthlib.client import OAuth
from model import session as db_session, User, Shipment, Location, Alert, Courier
import model
from packagetrack import Package

app = Flask(__name__)
SECRET_KEY = "\xc3\xf5T\xa0e\xdf\x05\x93\xc1'\x89\x16\x97mv\xc4mnb\xa1\xe2k\xa6\xdc"
app.config['GOOGLE_ID'] = config.GOOGLE_ID
app.config['GOOGLE_SECRET'] = config.GOOGLE_SECRET
app.config.from_object(__name__)

oauth = OAuth(app)

gmail = oauth.remote_app(
    'gmail',
    consumer_key=app.config.get('GOOGLE_ID'),
    consumer_secret=app.config.get('GOOGLE_SECRET'),
    request_token_params={
        'scope': ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/userinfo.email']
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    request_token_url=None,
)

@app.teardown_request
def shutdown_session(exception = None):
    db_session.remove()

@app.before_request
def load_user_id():
    g.user_id = session.get('user_id')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return gmail.authorize(callback=url_for('authorized', _external=True))

@app.route('/login/authorized')
@gmail.authorized_handler
def authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['gmail_token'] = (resp['access_token'],)
    user = gmail.get('userinfo')
    session['user_email'] = user.data['email']
    #  TODO Save user, user's email, and access token to the db
    return redirect(url_for('request_emails', _external=True))

@gmail.tokengetter
def get_gmail_oauth_token():
    return session.get('gmail_token')

@app.route('/my_shipments')
def map_shipments():
    emails = request_emails()
    contents = request_email_body(emails)
    shipping_numbers = parse_tracking_numbers(contents)
    # return render_template("my_shipments.html",
    #                         shipments=shipments)


@app.route('/request_emails')
def request_emails():
    """Builds a GMAIL API query for shipment emails in the last 6 months.
    Returns a function call asking for the contents of those shipping 
    emails."""

    query = "shipped shipping shipment tracking after:2014/1/14"
    url = "https://www.googleapis.com/gmail/v1/users/%s/messages" % session.get('user_email')
    response = gmail.get(url, data = {"q": query})
    print "response is: ", response
    data = response.data
    print "data is", data
    messages = data["messages"]
    print "messages are: ", messages
    # messages is a list of dictionaries [{ 'id': '12345', 'threadId': '12345'}, ]
    return request_email_body(messages)

def request_email_body(messages):
    """Receives a list of dictionaries of message id's.
    Returns a dictionary of tracking numbers."""

    for email in messages:
        url = "https://www.googleapis.com/gmail/v1/users/%s/messages/%s" % (session.get('user_email'), email["id"])
        response = gmail.get(url)
        base64url_encoded_string = response.data["payload"]["body"]["data"]
        decoded = base64.b64decode(base64url_encoded_string.replace('-', '/')).replace('_', '+')
        tracking_number = parse_tracking_number(decoded)
        p = Package(tracking_number)
        return p.url()
        #return jsonify({"data": decoded})

def parse_tracking_number(decoded_string):
    """Receives a decoded string, looks for a tracking number pattern, and
    returns a tracking number (string)."""

    patterns = {
        'ups_pattern': r'1Z[A-Z0-9]{16}',
        'fedex_pattern': r'[0-9]{22}',
        'usps_pattern': r'[0-9]{26}'
    }
    for pattern in patterns:
        print pattern
        result = re.findall(patterns[pattern], decoded_string)
        if result:
            print "pattern result is: ", result
            return result[0]
        else:
            continue

# @app.route('/logout')
# def logout():
#     session.pop('gmail_token', None)
#     return redirect(url_for('index'))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    db_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
    if not db_uri:
        db_uri = "sqlite:///shipments.db"
    model.connect(db_uri)
    app.run(debug=True, port=int(os.environ.get("PORT", 5050)), host="0.0.0.0")
