import os, config, base64
from datetime import datetime
import re

from flask import Flask, session, request, render_template, flash, redirect, url_for, g, jsonify
from model import session as db_session, User, Shipment
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
    tracking_numbers = []
    shippers = []
    tracking = []
    for email in emails:
        content = email_helper.request_email_body(email)
        contents.append(content)

    for content in contents:
        tracking_number = email_helper.parse_tracking_number(content)
        tracking_numbers.append(tracking_number)

    for tracking_number in tracking_numbers:
        if tracking_number is not None:
            p = Package(tracking_number)
            shipper = p.shipper
            shippers.append(shipper)
            tracking_info = p.track()
            tracking.append(tracking_info)


    return str(tracking)
    #return redirect(url_for('request_emails', _external=True))

@gmail.tokengetter
def get_gmail_oauth_token():
    return session.get('gmail_token')

# @app.route('/logout')
# def logout():
#     session.pop('gmail_token', None)
#     return redirect(url_for('index'))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


