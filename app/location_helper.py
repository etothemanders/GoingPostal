from model import session as db_session, Location

def save_location(data):
	"""Receives a data object with location_id and latlong properties, 
	and updates	the latlong value in the db for that location id."""
	location_id = data['id']
	latlong = data['latlong']
	db_session.query(Location).filter_by(id=location_id).update({"latlong": latlong})
	db_session.commit()

def get_unique_rows(rows):
	"""Receives a list of Flask location objects, returns a list of Flask
	location objects that each have a unique placename."""
	unlocated_rows = rows
	cities = {}
	for row in unlocated_rows:
		city = row.placename
		if not cities.get(city, False):
			cities[city] = row
	return_rows = []
	for city in cities:
		return_rows.append(cities[city])
	return return_rows


def row2dict(row):
	"""Converts a sql alchemy query object to a dictionary.
	http://stackoverflow.com/questions/1958219/convert-sqlalchemy-row-object-to-python-dict
	"""
	d = {}
	for column in row.__table__.columns:
		d[column.name] = str(getattr(row, column.name))
	return d

