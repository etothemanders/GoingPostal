import base64, re
from datetime import datetime

from packagetrack import Package

from flask import session
import sqlalchemy
from app import gmail
from model import session as db_session, Email, Shipment, Location


def save_new_email_ids(email_ids):
    """Receives a list of email_ids (dictionaries), and saves new email objects
    to the database."""
    new_ids = []
    for email_id in email_ids:
        # If email id already exists, don't add it to the list
        try:
            email = db_session.query(Email).filter_by(gmail_id=email_id['id']).one()
        # If it doesn't already exist, add it to the database and the new
        # ids list
        except sqlalchemy.orm.exc.NoResultFound, e:
            email = Email(gmail_id=email_id['id'],
                          thread_id=email_id['threadId'],
                          belongs_to=session['user_id'])
            db_session.add(email)
            new_ids.append(email_id)
    db_session.commit()
    return new_ids


def get_emails(email_ids):
    """Receives a list of emails (dictionaries) with keys id and threadId.
    Returns a list of email contents (string)."""
    email_contents = []
    for email in email_ids:
        try:
            content = request_email_body(email)
            email_contents.append(content)
        except KeyError, e:
            pass
    return email_contents


def request_email_body(email):
    """Receives an email (dictionary of id, threadId keys).
    Returns an email body (base64url decoded string)."""

    url = "https://www.googleapis.com/gmail/v1/users/%s/messages/%s" % (session.get('user_email'), email['id'])
    response = gmail.get(url)
    base64url_encoded_string = response.data["payload"]["body"]["data"]
    # To decode base64url, replace '-' with '+' and '_' with '/' first
    decoded = base64.b64decode(base64url_encoded_string.replace('-', '+').replace('_', '/'))
    return decoded


def get_tracking_numbers(email_contents):
    """Receives a list of email contents (strings). 
    Returns a list of tracking numbers."""
    tracking_numbers = []
    for content in email_contents:
        tracking_number = parse_tracking_number(content)
        tracking_numbers.append(tracking_number)
    return tracking_numbers


def parse_tracking_number(decoded_string):
    """Receives a decoded string, looks for a tracking number pattern, and
    returns a tracking number (string)."""

    patterns = {
        'ups_pattern': r'1Z[A-Z0-9]{16}',
        # Don't look for unsupported tracking numbers for now
        #'fedex_pattern': r'[0-9]{22}',
        #'usps_pattern': r'[0-9]{26}'
    }
    for pattern in patterns:
        result = re.findall(patterns[pattern], decoded_string)
        if result:
            return result[0]
    return None


def create_shipments(tracking_numbers):
    """Receives a list of tracking numbers. Creates a shipments object for each
    tracking number, saves it to the database, and returns a list of shipment 
    objects."""
    shipments = []
    for tracking_number in tracking_numbers:
        if tracking_number is not None:
            shipment = Shipment(tracking_no=tracking_number,
                                user_id=session['user_id'])
            shipments.append(shipment)
            db_session.add(shipment)
    db_session.commit()
    return shipments


def track_shipment(shipment):
    """Receives a shipment object. Returns a dictionary of activities.

    activities = { 'shipment.id': [ {activity}, {activity} ] }"""

    activities = {}
    p = Package(shipment.tracking_no)
    activity_entries = p.track()
    activities[shipment.id] = activity_entries
    return activities


def track_shipments(shipments):
    """Receives a list of shipment objects.  Returns a list of shipment 
    activity dictionaries.

    activities = [ { shipment id: [ { activity }, { activity } ] }, 
                   { shipment id: [ { activity }, { activity } ] }
                 ]"""
    activities = []
    for shipment in shipments:
        activity_entries = track_shipment(shipment)
        activities.append(activity_entries)
    return activities


def parse_locations(activities):
    """Receives a list of shipment activity dictionaries and looks for a city
    and state location for each activity item."""
    for activity_dict in activities:
        parse_location(activity_dict)


def parse_location(activity_dict):
    """Receives a shipment activity dictionary. If the activity contains 
    a city and a state, saves the location to the database."""
    for shipment_id in activity_dict:
        activity_list = activity_dict[shipment_id]
        for activity in activity_list:
            if activity['ActivityLocation'] != 'Unknown':
                address_info = activity['ActivityLocation']['Address']
                if address_info.has_key('City') and address_info.has_key('StateProvinceCode'):
                    city = address_info['City']
                    state = address_info['StateProvinceCode']
                    shipment_id = shipment_id
                    date = datetime.strptime(activity['Date'], "%Y%m%d")
                    time = activity['Time']
                    status = activity['Status']['StatusType']['Description']
                    location = Location(shipment_id=shipment_id, 
                                        placename=city, 
                                        latitude="None",
                                        longitude="None",
                                        timestamp=date,
                                        status_description=status,
                                        tracking_url='Need to get this.')
                    db_session.add(location)
    db_session.commit()

