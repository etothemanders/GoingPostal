import os, config, base64
from datetime import datetime
import re

from flask import Flask, session, request, render_template, flash, redirect, url_for, g, jsonify
from model import session as db_session, User, Shipment, Location, Alert, Courier
import model
from packagetrack import Package

from app import app, gmail


@app.teardown_request
def shutdown_session(exception = None):
    db_session.remove()

# Don't think this does anything
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
    # Save access token to session for subsequent gmail.get
    session['gmail_token'] = (resp['access_token'],)

    gmail_user = gmail.get('userinfo')
    postal_user = User(name=gmail_user.data['name'], 
                       email_address=gmail_user.data['email'],
                       access_token=resp['access_token'])
    postal_user.save()
    # Save user email to session for subsequent email request
    session['user_email'] = gmail_user.data['email']

    emails = postal_user.request_emails()
    return str(emails)
    #return redirect(url_for('request_emails', _external=True))

@gmail.tokengetter
def get_gmail_oauth_token():
    return session.get('gmail_token')


# @app.route('/request_emails')
# def request_emails():
#     """Builds a GMAIL API query for shipment emails in the last 6 months.
#     Returns a function call asking for the contents of those shipping 
#     emails."""

#     query = "shipped shipping shipment tracking after:2014/1/14"
#     url = "https://www.googleapis.com/gmail/v1/users/%s/messages" % session.get('user_email')
#     response = gmail.get(url, data = {"q": query})
#     print "response is: ", response
#     data = response.data
#     print "data is", data
#     messages = data["messages"]
#     print "messages are: ", messages
#     # messages is a list of dictionaries [{ 'id': '12345', 'threadId': '12345'}, ]
#     return request_email_body(messages)

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
        print "request url is", p.url()
        return p.track()
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


