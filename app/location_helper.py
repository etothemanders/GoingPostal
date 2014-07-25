from model import session as db_session, Location

def save_location(data):
	"""Receives a data object with location_id and latlong properties, 
	and updates	the latlong value in the db for that location id."""
	location_id = data['id']
	latlong = data['latlong']
	db_session.query(Location).filter_by(id=location_id).update({"latlong": latlong})
	db_session.commit()
