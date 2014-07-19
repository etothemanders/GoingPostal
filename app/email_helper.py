import base64
from flask import session
from app import gmail

def request_email_body(email):
    """Receives an email (dictionaries of messageId, threadId keys).
    Returns an email body (base64url decoded string)."""

    url = "https://www.googleapis.com/gmail/v1/users/%s/messages/%s" % (session.get('user_email'), email['id'])
    response = gmail.get(url)
    base64url_encoded_string = response.data["payload"]["body"]["data"]
    # To decode, replace '-' with '/' and '_' with '+'
    decoded = base64.b64decode(base64url_encoded_string.replace('-', '/').replace('_', '+'))
    return decoded

    tracking_number = parse_tracking_number(decoded)
    p = Package(tracking_number)
    print "request url is", p.url()
    return p.track()
    #return jsonify({"data": decoded})