from flask import Flask, session, request, render_template, flash, redirect, url_for, g
from model import session as db_session, User, Shipment, Location, Alert, Courier
import model
import os
from datetime import datetime


app = Flask(__name__)
SECRET_KEY = "\xc3\xf5T\xa0e\xdf\x05\x93\xc1'\x89\x16\x97mv\xc4mnb\xa1\xe2k\xa6\xdc"
app.config.from_object(__name__)

@app.teardown_request
def shutdown_session(exception = None):
    db_session.remove()

@app.before_request
def load_user_id():
    g.user_id = session.get('user_id')

@app.route("/")
def index():
    if g.user_id:
        return redirect(url_for("my_shipments"))
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    email = request.form['email']
    password = request.form['password']

    try:
        user = db_session.query(User).filter_by(email=email, password=password).one()
    except:
        flash("Invalid username or password", "error")
        return redirect(url_for("index"))

    session['user_id'] = user.id
    session['user_email'] = user.email
    #print "session after login is", session
    return redirect(url_for("my_shipments"))

@app.route("/register", methods=["POST"])
def register():
    email = request.form['email']
    password = request.form['password']
    location = request.form['zipcode']
    default_alert_pref = request.form['default_alert_pref']
    existing = db_session.query(User).filter_by(email=email).first()
    if existing:
        flash("Email already in use", "error")
        return redirect(url_for("index"))

    u = User(email=email, password=password, location=location, default_alert_pref=default_alert_pref)
    db_session.add(u)
    db_session.commit()
    db_session.refresh(u)
    session['user_id'] = u.id
    session['user_email'] = u.email
    return redirect(url_for("my_shipments"))

@app.route("/my_shipments")
def my_shipments():
    if not g.user_id:
        flash("Please log in", "warning")
        return redirect(url_for("index"))

    shipments = db_session.query(Shipment).filter_by(user_id=g.user_id).all()
    return render_template("my_shipments.html", shipments=shipments)

@app.route("/add_shipment", methods=["GET"])
def add_shipment():
    return render_template("add_shipment.html")

@app.route("/add_shipment", methods=["POST"])
def post_shipment():
    order_date = datetime.strptime(request.form['order_date'], "%Y-%m-%d")
    item_name = request.form['item_name']
    courier_id = request.form['courier_id']
    tracking_number = request.form['tracking_number']
    est_delivery = datetime.strptime(request.form['est_delivery'], "%Y-%m-%d")
    user_id = g.user_id

    s = Shipment(order_date=order_date, 
                 item=item_name, 
                 courier_id=courier_id, 
                 tracking_no=tracking_number, 
                 est_delivery=est_delivery,
                 user_id=user_id)
    db_session.add(s)
    db_session.commit()
    return redirect(url_for("my_shipments"))

@app.route("/view_shipment/<int:ship_id>", methods=["GET"])
def view_shipment(ship_id):
    print ship_id
    print type(ship_id)
    return redirect(url_for("my_shipments"))


@app.route("/logout")
def logout():
    del session['user_id']
    del session['user_email']
    #print "session after logging out is", session
    return redirect(url_for("index"))

if __name__ == "__main__":
    db_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
    if not db_uri:
        db_uri = "sqlite:///shipments.db"
    model.connect(db_uri)
    app.run(debug=True, port=int(os.environ.get("PORT", 5050)), host="0.0.0.0")
