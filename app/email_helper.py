import base64, re
from datetime import datetime

from packagetrack import Package

from flask import session
from app import gmail
from model import session as db_session, Shipment, Location


def get_emails(email_ids):
    """Receives a list of emails (dictionaries) with keys id and threadId.
    Returns a list of email contents (string)."""
    email_contents = []
    for email in email_ids:
        content = request_email_body(email)
        email_contents.append(content)
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
            print "pattern result is: ", result
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

