import json
from flask import Flask, session, request, render_template, flash, redirect, url_for, g, jsonify
from model import session as db_session, User, Shipment, Location
from app import app, gmail
import email_helper, location_helper, path_helper
import sqlalchemy


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
    # Save token to the session for the immediately following gmail request
    session['gmail_token'] = (resp['access_token'], )
    # Check if that user already exists in the db
    gmail_user = gmail.get('userinfo')
    try:
        postal_user = db_session.query(User).filter_by(email_address=gmail_user.data['email']).one()
        # Choosing to just update the token the db
        postal_user.save_new_token(resp['access_token'])
        session['user_email'] = gmail_user.data['email']
        session['user_id'] = postal_user.id
    except sqlalchemy.orm.exc.NoResultFound, e:
        # If a new user, save them to the db
        postal_user = User(name=gmail_user.data['name'], 
                           email_address=gmail_user.data['email'],
                           access_token=resp['access_token'])
        postal_user.save()
        session['user_email'] = gmail_user.data['email']
        session['user_id'] = postal_user.id
    # Search the user's gmail for shipment confirmation emails
    email_ids = postal_user.request_email_ids()
    new_email_ids = email_helper.save_new_email_ids(email_ids)
    # Only ask for contents from new email ids
    email_contents = email_helper.get_emails(new_email_ids)
    tracking_numbers = email_helper.get_tracking_numbers(email_contents)
    # Only create shipments if a tracking number was found
    shipments = email_helper.create_shipments(tracking_numbers)
    #  TODO Track new and undelivered shipments
    #  currently only tracking new shipments
    activities = email_helper.track_shipments(shipments)
    email_helper.parse_locations(activities)
    return redirect(url_for('show_map'))


@app.route("/my_shipments")
def show_map():
    shipments_info = []
    shipments = db_session.query(Shipment).filter_by(user_id=session['user_id']).all()
    for shipment in shipments:
        shipment_info = []
        shipment_info.append(shipment)
        last_activity = shipment.get_last_activity()
        shipment_info.append(last_activity)
        shipments_info.append(shipment_info)
    return render_template('my_shipments.html',
                            shipments=shipments_info,
                            GOOGLE_MAPS=app.config.get('GOOGLE_MAPS'))

@app.route("/get_latlongs")
def get_latlongs():
    all_rows = db_session.query(Location).filter_by(latitude='None').all()
    #get just the unique locations
    unique_rows = location_helper.get_unique_rows(all_rows)
    jsonified_rows = []
    for row in unique_rows:
        # convert the SQL Alchemy row object to a dictionary
        row_dict = location_helper.row2dict(row)
        jsonified_rows.append(row_dict)
    # turn the list into a json object
    return jsonify({'resp': jsonified_rows})


@app.route("/save_location", methods=['POST'])
def save_location():
    data = request.form
    if data is None:
        return 'Did not receive any data: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description'])
    else:
        location_helper.save_location(data)
        location_helper.backfill(data)
    # What do I actually want to return here?...
    return jsonify({'data': data})


@app.route("/load_GeoJson", methods=['GET'])
def load_geojson():
    # MUST USE DOUBLE QUOTES AROUND THE GEO_JSON_DICT STRINGS
    # Query for shipments (ideally, undelivered)
    shipments = db_session.query(Shipment).filter_by(user_id=session['user_id']).all()
    # If shipments to draw, create template json dict
    if shipments:
        geo_json_dict = {
            "type": "FeatureCollection",
            "features": []
        }
        # For each shipment, create a template Feature, append to features
        for shipment in shipments:
            geo_json_dict["features"].append(path_helper.create_feature(shipment))
    else:
        geo_json_dict = {}
    geo_json = json.dumps(geo_json_dict)
    return geo_json


@gmail.tokengetter
def get_gmail_oauth_token():
    return session.get('gmail_token')

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


