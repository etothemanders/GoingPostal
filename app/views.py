import json
from flask import Flask, session, request, render_template, flash, redirect, url_for, g, jsonify
from model import session as db_session, User, Location
from app import app, gmail
import email_helper, location_helper


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
    session['user_id'] = postal_user.id

    email_ids = postal_user.request_email_ids()
    email_contents = email_helper.get_emails(email_ids)
    tracking_numbers = email_helper.get_tracking_numbers(email_contents)
    shipments = email_helper.create_shipments(tracking_numbers)
    activities = email_helper.track_shipments(shipments)
    email_helper.parse_locations(activities)
    return redirect(url_for('show_map'))


@app.route("/my_shipments")
def show_map():
    all_rows = db_session.query(Location).filter_by(latlong='None').all()
    # get just the unique locations
    unique_rows = location_helper.get_unique_rows(all_rows)
    jsonified_rows = []
    for row in unique_rows:
        # convert the row object to a dictionary
        row_dict = location_helper.row2dict(row)
        print row_dict
        # append to jsonified_rows list
        jsonified_rows.append(row_dict)
    # turn the list into json
    jsonified_rows = json.dumps(jsonified_rows)
    return render_template('my_shipments.html',
                            all_rows=jsonified_rows)


@app.route("/save_location", methods=['POST'])
def save_location():
    data = request.form
    if data is None:
        return 'Did not receive any data: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description'])
    else:
        location_helper.save_location(data)
    # I don't think this return is actually working...oh, wait, is it
    # returning 'data' to the javascript callback?
    return jsonify({'data': data})


@app.route("/backfill_latlongs", methods=['POST'])
def backfill_locations():
    data = request.form
    if data is None:
        return 'Did not receive any data: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description'])
    else:
        location_helper.backfill(data)
    return jsonify({ 'backfill_response': data })


@gmail.tokengetter
def get_gmail_oauth_token():
    return session.get('gmail_token')

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


