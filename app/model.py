import os

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, DateTime, Date
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref

#import your app modules
from app import gmail


db_uri = os.environ.get("DATABASE_URL", "sqlite:///shipments.db")
    
engine = create_engine(db_uri, echo=False)
session = scoped_session(sessionmaker(bind=engine,
                         autocommit = False,
                         autoflush = False))

Base = declarative_base()
Base.query = session.query_property

### Class declarations go here

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    name = Column(String(64), nullable=False)
    email_address = Column(String(64), nullable=False)
    access_token = Column(String(64), nullable=False)        
    sms_phone = Column(String(64), nullable=True)
    call_phone = Column(String(64), nullable=True)
    location = Column(String(64), nullable=True)
    default_alert_pref = Column(String(15), nullable=True)

    #put methods here
    def save(self):
        session.add(self)
        session.commit()

    def request_email_ids(self):
        """Builds a GMAIL API query for shipment emails in the last 6 months.
        Returns a list of emails (dictionaries with keys 'id' and 'threadId'."""

        query = "shipped shipping shipment tracking after:2014/1/14"
        url = "https://www.googleapis.com/gmail/v1/users/%s/messages" % self.email_address
        response = gmail.get(url, data = {"q": query})
        data = response.data
        messages = data["messages"]
        # messages is a list of dictionaries [{ 'id': '12345', 'threadId': '12345'}, ]
        return messages

class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True)
    gmail_id = Column(String(64), nullable=False)
    thread_id = Column(String(64), nullable=False)
    tracking_no = Column(String(64), nullable=True)
    belongs_to = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship("User", backref="emails")

    #put methods here
    def save(self):
        session.add(self)
        session.commit()


class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key = True)
    #order_date = Column(Date, nullable=False)
    #item = Column(String, nullable=False)
    #courier_id = Column(Integer, ForeignKey('couriers.id'), nullable=True)
    tracking_no = Column(Integer, nullable=False)
    est_delivery = Column(Date, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    #description = Column(String(128), nullable=True)
    #retailer = Column(String(64), nullable=True)

    user = relationship("User", backref="shipments")
    #courier = relationship("Courier", backref="shipments")

    def get_last_activity(self):
        last_activty = session.query(Location).filter_by(shipment_id=self.id).order_by(Location.timestamp.desc()).first()
        print last_activty
        return last_activty

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key = True)
    shipment_id = Column(Integer, ForeignKey('shipments.id'), nullable=False)
    placename = Column(String(128), nullable=False)
    latitude = Column(String(64), nullable=True)
    longitude = Column(String(64), nullable=True)
    timestamp = Column(Date, nullable=False)
    status_description = Column(String(128), nullable=False)
    tracking_url = Column(String(256))

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key = True)
    shipment_id = Column(Integer, ForeignKey('shipments.id'), nullable=False)
    mode = Column(Integer, nullable=True)

class Courier(Base):
    __tablename__ = "couriers"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    logo = Column(String(256), nullable=True)
    url = Column(String(256), nullable=False)


### End class declarations

def create_db():
    Base.metadata.create_all(engine)

def connect(db_uri="sqlite:///shipments.db"):
    global engine
    global session
    engine = create_engine(db_uri, echo=False) 
    session = scoped_session(sessionmaker(bind=engine,
                             autocommit = False,
                             autoflush = False))

def main():
    """Calls create_db()"""
    #create_db()
    pass


if __name__ == "__main__":
    #u1 = session.query(User).get(1)
    #s1 = session.query(Shipment).get(1)
    main()
