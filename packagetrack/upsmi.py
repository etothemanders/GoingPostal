import urllib
from datetime import datetime, date, time
from flask import jsonify

import packagetrack
from .xml_dict import dict_to_xml, xml_to_dict
from .data import TrackingInfo


class UPSMIInterface(object):
    """UPS Mail Innovations tracking numbers.  Formats can be found here:
        http://www.ups.com/content/us/en/tracking/help/tracking/tnh.html"""

    api_url = 'https://wwwcie.ups.com/ups.app/xml/Track'

    def __init__(self):
        self.attrs = {'xml:lang': 'en-US'}

    def identify(self, tracking_number):
        try:
            if int(tracking_number):
                return (21 < len(tracking_number) < 35) or (len(tracking_number) == 18)
            elif tracking_number.startswith('MI'):
                return tracking_number[2:8].isnumeric() and tracking_number[8:].isalnum() and (len(tracking_number[8:]) < 23)
        except ValueError:
            return False

    def build_access_request(self):
        config = packagetrack.config
        d = {'AccessRequest':
             {'AccessLicenseNumber': config.get('UPS', 'license_number'),
              'UserId': config.get('UPS', 'user_id'),
              'Password': config.get('UPS', 'password')}}
        return dict_to_xml(d, self.attrs)

    def build_track_request(self, tracking_number):
        req = {'RequestOption': '1',
               'TransactionReference': {'RequestAction': 'Track'}}
        d = {'TrackRequest': {'TrackingOption': '03',
                              'TrackingNumber': tracking_number,
                              'Request': req}}
        return dict_to_xml(d)

    def build_request(self, tracking_number):
        return (self.build_access_request() +
                self.build_track_request(tracking_number))

    def send_request(self, tracking_number):
        body = self.build_request(tracking_number)
        #TODO remove print statement
        print body
        webf = urllib.urlopen(self.api_url, body)
        resp = webf.read()
        webf.close()
        # TODO remove print statements
        print "response was", resp
        print "end of response"
        return resp

    def parse_response(self, raw):
        root = xml_to_dict(raw)['TrackResponse']
        response = root['Response']
        status_code = int(response['ResponseStatusCode'])
        status_description = response['ResponseStatusDescription']
        # Check status code?

        # Parse delivery date, status, and last update.
        try:
            est_delivery_date = datetime.strptime(
                root['Shipment']['ScheduledDeliveryDate'],
                "%Y%m%d")
        except KeyError:
            est_delivery_date = 'Unknown'

        try:
            est_delivery_time = datetime.strptime(
                root['Shipment']['ScheduledDeliveryTime'],
                "%H%M%S")
        except KeyError:
            est_delivery_time = 'Unknown'

        package = root['Shipment']['Package']
        activity = package['Activity']
        last_update_date = datetime.strptime(activity['Date'], "%Y%m%d").date()
        last_update_time = datetime.strptime(activity['Time'], "%H%M%S").time()
        last_update = datetime.combine(last_update_date, last_update_time)
        status = activity['Status']['StatusType']['Description']

        return jsonify(root)

        # return TrackingInfo(last_update=last_update,
        #                     delivery_date=est_delivery_date,
        #                     status=status)
        
    def track(self, tracking_number):
        "Track a UPS package by number. Returns just a delivery date."
        resp = self.send_request(tracking_number)
        print "tracking function call response was", resp
        return self.parse_response(resp)

    def url(self, tracking_number):
        "Return a tracking info detail URL by number."
        return ('http://wwwapps.ups.com/WebTracking/processInputRequest?'
                'TypeOfInquiryNumber=T&InquiryNumber1=%s' % tracking_number)
