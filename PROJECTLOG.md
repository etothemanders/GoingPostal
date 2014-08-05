===

# Daily Stand-Up Notes

## 2014-08-05

### Accomplished yesterday:
1.  Wrote README.md installation instructions
2.  Wrote a test case

### Plan for today:
1.  Make a video recording of my app
2.  Write a blog post about how my app works
3.  Practice giving my presentation

### Blockers
None right now.

## 2014-08-04

### Accomplished Friday:
1.  Finished coloring corresponding paths and table rows
2.  Tweaked email search query, now grabbing more shipment emails
3.  Added check to not duplicate db entries for the same user, email, shipment
    or activities.
3.  Now handling circumstances when no data (shipment emails, tracking numbers,
    package activity) is found.  Table shows no shipments found.

### Plan for today:
1.  Write README.md
2.  Write some Python tests

### Blockers
None right now.

## 2014-08-01

### Accomplished yesterday:
1.  Colored package paths on mouseover event
2.  Finished styling cover page and my_shipments.html page

### Plan for today:
1.  Color corresponding table row when package path is moused-over
2.  Color corresponding package path when table row is moused-over

### Blockers
1.  Still just scared to touch my code.


## 2014-07-31

### Accomplished yesterday:
1.  Used layoutit.com to help create cover page positioning.
2.  Have a half-way decent cover page.

### Plan for today:
1.  Do some map styling.
    1.  Color the package routes different colors
    2.  Highlight routes when mousing over the package's row in the table

### Blockers
1.  Scared to change my code at this point.

## 2014-07-30

### Accomplished yesterday:
1.  Added table of shipments to my_shipments page.
2.  Added Bootstrap to the app, started styling

### Plan for today:
1.  Investigate adding a map marker for package's last location
2.  Style the cover page.

### Blockers
None right now.

## 2014-07-29

### Accomplished yesterday:
1.  Drew my package paths on a Google map!!

### Plan for today:
Oh gosh, so much to do.
1.  Add a list of shipments to my_shipments page.
2.  Add a marker showing where the package originated, add a marker showing
    where it was delivered?

### Blockers
None right now.

## 2014-07-28

### Accomplished Friday:
1.  Got latlongs for all locations after map initializes, not from console call

### Plan for today:
1.  Draw a polyline of a shipment's path on the map

### Blockers:
1.  None right now, just a lot to do this week.

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

===
# TODO

0.  Check for logged in user - DONE
1.  Check for new shipments - DONE
  1.  Connect to Gmail API (Gmail OAuth) - DONE
  2.  Fetch shipment emails (last 6 months) - DONE
  3.  Parse tracking number and determine courier - DONE
  4.  If a new tracking number from a courier that I can track, add to db - DONE
2.  Check for new package locations
  1.  Look up the current status of all tracking numbers
  2.  If current status is not delivered, get tracking info from the courier
  3.  If location is new, add location data to db
3.  Display shipment paths on a map
  1.  Add a map to html page - DONE
  2.  Determine lat/long for each location from Google Maps Geocoding API, 
      save to db - DONE
  3.  Create polyline for each shipment from Google Maps Javascript API, 
      add to map - DONE
4.  Write job scheduler to check for package updates (once per day?)
5.  Send a text message after being delivered
