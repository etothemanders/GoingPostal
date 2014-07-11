GoingPostal
===========

Track your online shipments in this responsive web app.

GoingPostal is the final project created during the Summer 2014 Hackbright Academy Software Engineering Fellowship.



===
# TODO

1.  Fetch my shipment emails from Gmail
  1.  Login
  2.  Connect to Gmail API (Gmail OAuth?)
  3.  Fetch emails (all? last 60 days? upper limit?)
  4.  Parse shipment confirmation emails
  5.  Parse shipment number (and courier?)
2.  Get package tracking numbers
  1.  Add tracking number, courier info to db
3.  Looks up their status and location from the courier
  1.  Add location data to db
4.  Display their paths and current location on a map
5.  Send a text message (or call?) after being delivered

===

# Daily Stand-Ups

## 2014-07-11 Stand-Up

### Accomplished yesterday:
1.  In gmail OAuth prototype, moved gmail client id and 
    secret to more secure location in ~/.bash_profile
2.  Authorization granted to gmail, not the random sample service

### Plan for today:
1.  Work on passing access code in the header, encoding problem

### Blockers
1.  Encoding problem

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

