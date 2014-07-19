import os, config, base64
from datetime import datetime
import re

from flask import Flask, session, request, render_template, flash, redirect, url_for, g, jsonify
from model import session as db_session, User
from packagetrack import Package
from sqlalchemy import desc

from app import app, gmail
import email_helper


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
    # Save access token to session for subsequent Gmail API requests
    session['gmail_token'] = (resp['access_token'], )

    gmail_user = gmail.get('userinfo')
    postal_user = User(name=gmail_user.data['name'], 
                       email_address=gmail_user.data['email'],
                       access_token=resp['access_token'])
    postal_user.save()
    # Save user email to session for subsequent Gmail API requests
    session['user_email'] = gmail_user.data['email']
    # emails is a list of dictionaries [{ 'id': '12345', 'threadId': '12345'}, ]
    emails = postal_user.request_emails()
    contents = []
    for email in emails:
        content = email_helper.request_email_body(email)
        contents.append(content)

    return str(contents)
    #return redirect(url_for('request_emails', _external=True))

@gmail.tokengetter
def get_gmail_oauth_token():
    return session.get('gmail_token')


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


