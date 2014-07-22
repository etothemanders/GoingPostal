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
    session['gmail_token'] = (resp['access_token'], )

    gmail_user = gmail.get('userinfo')
    postal_user = User(name=gmail_user.data['name'], 
                       email_address=gmail_user.data['email'],
                       access_token=resp['access_token'])
    postal_user.save()
    session['user_email'] = gmail_user.data['email']

    email_ids = postal_user.request_email_ids()
    email_contents = get_emails(email_ids)
    tracking_numbers = get_tracking_numbers(email_contents)
    shipments = create_shipments(tracking_numbers)
    activities = track_shipments(shipments)
    parse_locations(activities)
    return redirect(url_for('show_map'))

def get_emails(email_ids):
    """Receives a list of emails (dictionaries) with keys id and threadId.
    Returns a list of email contents (string)."""
    email_contents = []
    for email in email_ids:
        content = email_helper.request_email_body(email)
        email_contents.append(content)
    return email_contents

def get_tracking_numbers(email_contents):
    """Receives a list of email contents (strings). 
    Returns a list of tracking numbers."""
    tracking_numbers = []
    for content in email_contents:
        tracking_number = email_helper.parse_tracking_number(content)
        tracking_numbers.append(tracking_number)
    return tracking_numbers

def create_shipments(tracking_numbers):
    """Receives a list of tracking numbers. Creates a shipments object for each
    tracking number, saves it to the database, and returns a list of shipment 
    objects."""
    shipments = []
    for tracking_number in tracking_numbers:
        if tracking_number is not None:
            shipment = Shipment(tracking_no=tracking_number,
                                user_id=99)
            shipments.append(shipment)
            db_session.add(shipment)
    db_session.commit()
    return shipments

def track_shipment(shipment):
    """Receives a shipment object. Returns a list of activities (dictionaries)."""
    p = Package(shipment.tracking_no)
    activity_entries = p.track()
    return activity_entries

def track_shipments(shipments):
    """Receives a list of shipment objects.  Returns a nested list of activities 
    (dictionaries)."""
    activities = []
    for shipment in shipments:
        activity_entries = track_shipment(shipment)
        activities.append(activity_entries)
    return activities

def parse_locations(activities):
    """Receives a list of activities (dictionaries) and looks for a location."""
    for activity in activities:
        parse_location(activity)

def parse_location(activity_list):
    """Receives a list of activities (dictionaries). If the activity contains 
    a city and a state, saves the location to the database."""
    for activity in activity_list:
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
                                    imdb_url='Need to get this.')
                db_session.add(location)
    db_session.commit()

@app.route("/my_shipments")
def show_map():
    return render_template('my_shipments.html')

@gmail.tokengetter
def get_gmail_oauth_token():
    return session.get('gmail_token')

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


