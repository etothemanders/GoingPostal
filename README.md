GoingPostal
===========

A responsive web app that checks for shipment confirmation emails in Gmail,
finds tracking numbers (currently only UPS tracking numbers), and plots a 
shipment's progress to its destination on a map.

# App Architecture
Uses the Flask web framework, sqlite3 for the database, and Bootstrap for 
styling.

# Web Services
Uses Gmail OAuth for Gmail access, the UPS SOAP API for package tracking 
information, and Google's Geocoding and Maps APIs for location translation
and path mapping.

GoingPostal is the final project created during the Summer 2014 Hackbright 
Academy Software Engineering Fellowship.

Installation Instructions
===========
