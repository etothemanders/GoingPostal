GoingPostal
===========

Track your online shipments in this responsive web app.

GoingPostal is the final project created during the Summer 2014 Hackbright Academy Software Engineering Fellowship.



===
# TODO

0.  Check for logged in user
1.  Check for new shipments
  1.  Connect to Gmail API (Gmail OAuth) - DONE
  2.  Fetch shipment emails (last 6 months) - DONE
  3.  Parse tracking number and determine courier - DONE
  4.  If a new tracking number from a courier that I can track, add to db
2.  Check for new package locations
  1.  Look up the current status of all tracking numbers
  2.  If current status is not delivered, get tracking info from the courier
  3.  If location is new, add location data to db
3.  Display shipment paths and current location on a map
  1.  Add a map to html page
  2.  Determine lat/long for each location from Google Maps Geocoding API, save to db
  3.  Create polyline for each shipment from Google Maps Javascript API, add to map
4.  Write job scheduler to check for package updates (once per day?)
5.  Send a text message after being delivered

===

# Daily Stand-Ups

## 2014-07-25

### Accomplished yesterday:
1.  Able to call getLatLong() from browser console and save a latlong for one 
    location to the db

### Plan for today:
1.  Get latlongs for all locations that need them
2.  Call getLatLong() after browser loads rather than from the console
3.  Figure out how to draw a polyline on the map of a shipment's path

### Blockers
None at the moment.

## 2014-07-24

### Accomplished yesterday:
1.  Added a map to my_shipments.html
2.  Figured out how to get a latlong from Google's Geocoding API

### Plan for today:
1.  Get a latlong for all locations
2.  Save the lat longs to the db

### Blockers:
1.  Need to learn how to write an ajax request to send the latlong back to my 
    Flask app.

## 2014-07-23

### Accomplished yesterday:
1.  Finished refactoring some Python code
2.  Created route and template html stub for my_shipments.html

### Plan for today:
1.  Add a map to html
2.  Get lat/long for each shipment location using Google Maps Geocoding API

### Blockers:
None right now.

## 2014-07-22

### Accomplished Monday:
1.  Finished pre-processing UPS XML data
2.  Successfully saving it to my database
3.  Created a new route and stub template for my map page.  
4.  Started some refactoring/code clean-up in my routes

### Plan for Tuesday:
1.  Finish refactoring/code clean-up in my routes
2.  Attend Heroku Lunch and Learn

No Blockers

## 2014-07-21

### Accomplished Friday:
1.  Got help from Nick to refactor my code

### Plan for today:
1.  Write pre-processing function to strip out unpaired XML tags
2.  Parse out all activities that have a location
2.  Create my_shipments route and template to render
3.  Add a Google map to the template

### Blockers:
1.  None right now

## 2014-07-18

### Accomplished yesterday:
1.  Fixed UPS Mail Innovations XML request, but only getting one response back

### Blockers:
1.  UPS deleted my package's tracking information

### Plan for today:
1.  Write code to ignore that tracking number pattern

## 2014-07-17 Stand-Up

### Accomplished yesterday:
1.  Finished blog post on OAuth
2.  Emailed UPS for help

### Plan for today:
1.  Attend HB sponsored negotiation workshop
2.  Fix UPS Mail Innovations SOAP request

### Blockers:
No longer blocked on UPS Mail Innovations Tracking request!
1.  Not sure how to get all tracking information, currently just getting first 
    entry...

## 2014-07-16 Stand-Up

### Accomplished yesterday:
1.  Modified email query for shipment emails in the last 6 months
2.  Used packagetrack library to create a UPS request
3.  Went to Survey Monkey LnL
4.  Met with Astha, got feedback on my project

### Plan for today:
1.  Troubleshoot request for Mail Innovations tracking number from UPS
2.  Finish blog post on OAuth

### Blockers
1.  Non-standard tracking number

## 2014-07-15 Stand-Up

### Accomplished yesterday:
1.  Found UPS tracking number formats 
(http://www.ups.com/content/us/en/tracking/help/tracking/tnh.html)
2.  Found library to help with package tracking
(https://github.com/storborg/packagetrack)
3.  Wrote regular expressions to look for tracking numbers in tracking.py
4.  Encapsulated parsing tracking numbers in to function parse_tracking_numbers()

### Plan for today:
1.  Integrate packagetrack library with my project
2.  Use packagetrack library to issue request for package status

### Blockers:
1.  My current tracking number is not a typical UPS tracking number, having
    trouble getting tracking info back from UPS


## 2014-07-14 Stand-Up

### Accomplished Friday:
1.  Successfully received emails from Gmail API
2.  Modified request query to search for shippment keywords
3.  Successfully retrieved email body
4.  Successfully decoded HTML email body from base64url encoding to something
    readable

### Plan for Monday:
1.  My single test email was sent using UPS, so go to UPS see if I can find the
    format of their tracking numbers,
2.  Write regular expression to search for the tracking number in UPS emails
3.  Encapsulate the tracking number extraction into a function
4.  Process another email/courier...

## 2014-07-11 Stand-Up

### Accomplished yesterday:
1.  In gmail OAuth prototype, moved gmail client id and 
    secret to more secure location in ~/.bash_profile
2.  Authorization granted to gmail, not the random sample service

### Plan for today:
1.  get email body, email query limit

### Blockers
1.  How to work with Gmail's response object

## 2014-07-10 Stand-Up

### Accomplished yesterday:
1.  Got a Reddit OAuth sample app working in Flask
2.  Got a stand-alone Google OAuth sample app working in Flask

### Plan for today:
1.  Get an email from Gmail

### Blockers
1.  OAuth is hard

## 2014-07-09 Stand-Up

### Accomplished yesterday:
1.  Lunch with Astha (hints on OAuth)
2.  Finished login/logout
3.  Added form to manually enter shipments
4.  Display shipments list
5.  Decided not to stub out the remaining templates or routes

### Plan for Today:
1.  Read about Gmail OAuth

### Blockers:
OAuth


## 2014-07-08 Stand-Up

### Accomplished yesterday:
1.  Project approval
2.  Created GitHub repo
3.  Sketched out (4) wireframes of main pages
4.  Created db (v1)
5.  Drafted rough project timeline
6.  Able to manually register a user, save to db

### Plan for Today:
1.  Manually enter a shipment to track
2.  Finish login flow
3.  Ask for a code review
4.  Stub out remaining template pages
5.  Stub out remaining routes
6.  Read about Gmail API (OAuth)

### Blockers:
1.  Need to research more about options for getting emails

## 2014-07-07 Stand-Up

### Accomplished last week:
1. Picked a project idea
2. Picked a project name

### Plan for Today:
1.  Project Approval
2.  Wireframes
3.  Database tables
4.  Create GitHub repo
5.  Project timeline

### Blockers:
1.  Project approval
2.  How to fake shipment data??

### Questions:
1.  git init locally vs. creating a repo on GitHub
Can git init on GitHub, just git init in one place or the other. 
If you init on GitHub, don't forget to check the init checkbox.
2.  How do I fake shipment data?
Check the courier APIs for test data.
Create a page of tracking numbers.
3.  How to get email data??  Nick suggested 3 options:
  1.  Browser extension - add a tracking number from a web page to my app
  2.  Use IMAP to actually read my email - invasive.  Would need to store
      encrypted, hashed email password
  3.  OAuth might be possible - check Gmail API docs. Also check Flask mega-
      tutorial for a Google accounts OAuth example of account creation.

### Ways to Expand on the Project
1.  Additional email providers
2.  Store the info retrieved from carriers for offline support
3.  Predict the next location
	1.  Based on time of year (winter)
	2.  Postal traffic (holidays)
4.  Map viewing options
	1.  Show timing by time of year
	2.  By shipping priority (regular, express, priority, etc.)
	3.  Bad weather, holidays...

