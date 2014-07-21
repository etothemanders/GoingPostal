import os, config, base64
from datetime import datetime
import re

from flask import Flask, session, request, render_template, flash, redirect, url_for, g, jsonify
from model import session as db_session, User, Shipment, Location
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
    activities = []
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
            activity_entries = p.track()
            tracking.append(activity_entries)
            # For activity in activity_entries, 
            # if it has a city & state (zipcode?)
            # create a location object, save to db
            for activity in activity_entries:
                if activity['ActivityLocation'] != 'Unknown':
                    address_info = activity['ActivityLocation']['Address']
                    print "activity location is", address_info
                    if address_info.has_key('City') and address_info.has_key('StateProvinceCode'):
                        print "Found a city and state!"
                        city = address_info['City']
                        state = address_info['StateProvinceCode']
                        shipment_id = 99
                        date = datetime.strptime(activity['Date'], "%Y%m%d")
                        time = activity['Time']
                        status = activity['Status']['StatusType']['Description']
                        print 'City: ', city
                        print 'State: ', state
                        print 'Date: ', date
                        print 'Time: ', time
                        print 'Status: ', status
                        location = Location(shipment_id=shipment_id, 
                                            placename=city, 
                                            latitude=99,
                                            longitude=99,
                                            timestamp=date,
                                            title=status,
                                            imdb_url=p.url())
                        db_session.add(location)
            db_session.commit()

    return redirect(url_for('show_map'))
    #return redirect(url_for('request_emails', _external=True))

@app.route("/my_shipments")
def show_map():
    return render_template('my_shipments.html')

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


