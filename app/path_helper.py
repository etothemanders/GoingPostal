from model import session as db_session, Location

"""
Two example Features
{
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [-104.9847, 39.9434],
                        [-122.4194, 37.8921]
                    ]
                },
                "properties": {
                    "strokeColor": "#FF0000",
                    "strokeOpacity": 1.0,
                    "strokeWeight": 2
                }
            },
            {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [-112.0740, 33.7243],
                        [-118.2436, 34.1981]
                    ]
                },
                "properties": {
                    "strokeColor": "blue",
                    "strokeOpacity": 1.0,
                    "strokeWeight": 2
                }
            }

"""

def create_feature(shipment):
	"""Receives a shipment object, builds a GeoJSON Feature."""
	locations = db_session.query(Location).filter_by(shipment_id=shipment.id).all()
	if not locations:
		pass
	elif len(locations) == 1:
		# Create Point type Feature
		pass
	else:
		feature_dict = {
			"type": "Feature",
			"geometry": {
				"type": "LineString",
				"coordinates": []
			},
			"properties": {
				"strokeColor": "#339999",
				"strokeOpacity": 1.0,
				"strokeWeight": 2
			}
		}
		for location in locations:
			latitude = float(location.latitude)
			longitude = float(location.longitude)
			# GeoJSON spec requires a position contain (at least) two numbers
			# in the following order (x, y, z) (easting, northing, altitude)
			# so longitude, then latitude
			# http://geojson.org/geojson-spec.html#positions
			coordinate = [longitude, latitude]
			feature_dict["geometry"]["coordinates"].append(coordinate)
		return feature_dict

