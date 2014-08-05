# GoingPostal  
===========
## Summary  
A web app that lets you visually track your online purchases as they travel to 
their destinations.  It searches for shipment confirmation emails in Gmail, 
finds tracking numbers (currently only UPS tracking numbers), asks UPS for 
the package's movements, converts city names to latitude and longitude 
coordinates, and plots the package's progress on a Google map. 

GoingPostal was created during the Summer 2014 Hackbright Academy Software 
Engineering Fellowship.

## App Architecture  
Presentation Layer:  HTML, CSS, JS, jQuery, AJAX, JSON, and Bootstrap  
Application Layer:  Python, Flask  
Data Layer:  SQLite, SQLAlchemy  
APIs:  Google OAuth, Gmail, UPS Tracking, Google Geocoding, Google Maps Javascript v3  


## Installation Instructions  
### Download and Install  
1.  Clone or fork this repository. 
2.  Open a command line interface (terminal, shell, etc.) and type:  
    pip install -r requirements.txt

### Add your API Keys
To run GoingPostal, you will need to create your own Google Developer account 
and your own My UPS account in order to request the necessary access keys. 
Follow the service provider's instructions. 

1.  Google OAuth 2.0 credentials
   Create a Google Developer account and take note of where to find your Client ID
   and Client Secret for web applications in the developer console.
   [https://developers.google.com/accounts/docs/OAuth2]

2.  Configure the web app in your Google Developer Console
   Edit the web applications section to set the redirect URI to:
    http://localhost:5050/login/authorized
   to run GoingPostal out of the box locally.

3.  Google Geocoding and Google Maps Javascript API v3 browser key
   In your Google Developer Console, create a new Public API access key for browser
   applications.  Update the Referrers value to
    http://localhost:5050/*

4.  Turn on Google's web services
   In your Google Developer Console, turn the following services "on":
  * Gmail API
  * Geocoding
  * Google Maps JavaScript API v3

5.  UPS Developer Kit
   Register with My UPS and request an Access key.
[https://www.ups.com/upsdeveloperkit?loc=en_US]

6.  Create a Flask Secret Key
   In order to use sessions in Flask, you will need a secret key.  The Flask
   Sessions documentation shows you how to generate one.
   [http://flask.pocoo.org/docs/quickstart/#sessions]

I have stored my keys in my ~/.bash_profile, and then point to them in
config.py.  You should not need to change config.py, but your .bash_profile 
should look something like this:

    ## For Google OAuth
    export GOOGLE_ID=<put your CLIENT ID here, no quotes>
    export GOOGLE_SECRET=<your CLIENT SECRET here, no quotes>

    ## For Flask Sessions
    export SECRET_KEY="your key in quotes"

    ## For GoingPostal Google Maps
    export GOOGLE_MAPS="your browser API key in quotes"

###  Create the Database
To create the database and tables, cd into your local GoingPostal directory
and type the following commands into your command line interface:

    python -i run.py

hit ctrl + c to issue a keyboard interrupt and start the interactive python
interpreter

    from app import model
    model.create_db()
    quit()

### Run the App
In the GoingPostal directory, type this command to start the server:

    python run.py

Open a web browser and navigate to  
http://localhost:5050

##Contribute to GoingPostal  
I've got no shortage of potential features for GoingPostal.  Feel free to pitch
in on any of the ones below, or fork this repo and work on your own!

1.  More carriers!  FedEx and the US Postal Service would be handy.
2.  Add a marker to show a package's last location on the map.
3.  Expand a shipment table row on click to show all of the package's movements.
4.  Filter only for undelivered packages.
5.  Write a cron job to check for package location updates without needing 
    to be logged in and using the app.
6.  Send the user a text message when a package is marked as delivered.
