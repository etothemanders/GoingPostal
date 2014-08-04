import urllib, re
from datetime import datetime, date, time

import packagetrack
from .xml_dict import dict_to_xml, xml_to_dict
from .data import TrackingInfo


class UPSInterface(object):
    api_url = 'https://wwwcie.ups.com/ups.app/xml/Track'

    def __init__(self):
        self.attrs = {'xml:lang': 'en-US'}

    def identify(self, tracking_number):
        return tracking_number.startswith('1Z')

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
        d = {'TrackRequest': {'TrackingNumber': tracking_number,
                              'Request': req}}
        return dict_to_xml(d)

    def build_request(self, tracking_number):
        request = (self.build_access_request() +
                   self.build_track_request(tracking_number))
        return (self.build_access_request() +
                self.build_track_request(tracking_number))

    def send_request(self, tracking_number):
        body = self.build_request(tracking_number)
        webf = urllib.urlopen(self.api_url, body)
        resp = webf.read()
        webf.close()
        return resp

    def preprocess_response(self, raw):
        """Remove unpaired XML tags from raw response. Return a string."""
        pattern = re.compile(r'<[a-zA-z]+/>')
        new_raw = pattern.sub('Unknown', raw)
        return new_raw

    def parse_response(self, raw):
        """Returns all activity paths in a list."""
        pattern = re.compile(r'<Activity>.*?</Activity>')
        activity_list = re.findall(pattern, raw)
        activities = []
        for activity in activity_list:
            thing = xml_to_dict(activity)['Activity']
            activities.append(thing)
        return activities

        
    def track(self, tracking_number):
        "Track a UPS package by number. Returns just a delivery date."
        resp = self.send_request(tracking_number)
        resp = self.preprocess_response(resp)
        return self.parse_response(resp)

    def url(self, tracking_number):
        "Return a tracking info detail URL by number."
        return ('http://wwwapps.ups.com/WebTracking/processInputRequest?'
                'TypeOfInquiryNumber=T&InquiryNumber1=%s' % tracking_number)
