import base64, re
from flask import session
from app import gmail

def request_email_body(email):
    """Receives an email (dictionaries of messageId, threadId keys).
    Returns an email body (base64url decoded string)."""

    url = "https://www.googleapis.com/gmail/v1/users/%s/messages/%s" % (session.get('user_email'), email['id'])
    response = gmail.get(url)
    base64url_encoded_string = response.data["payload"]["body"]["data"]
    # To decode, replace '-' with '/' and '_' with '+'
    decoded = base64.b64decode(base64url_encoded_string.replace('-', '+').replace('_', '/'))
    return decoded


def parse_tracking_number(decoded_string):
    """Receives a decoded string, looks for a tracking number pattern, and
    returns a tracking number (string)."""

    patterns = {
        'ups_pattern': r'1Z[A-Z0-9]{16}',
        'fedex_pattern': r'[0-9]{22}',
        'usps_pattern': r'[0-9]{26}'
    }
    for pattern in patterns:
        result = re.findall(patterns[pattern], decoded_string)
        if result:
            print "pattern result is: ", result
            return result[0]
    return None