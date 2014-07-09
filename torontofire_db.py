# Toronto Fire Calls

import urllib2
import sqlite3
import time
import csv
import ipdb
import threading
from bs4 import BeautifulSoup

# Beautiful Soup imports the URL as html
def getincidents ():

	response = urllib2.urlopen('http://www.toronto.ca/fire/cadinfo/livecad.htm')

	html = response.read()

	# We give the html its own variable.

	soup = BeautifulSoup(html)

	# Find the table we want on the Toronto Fire Page

	table = soup.find("table", class_="info")

	# Find all the <td> tags in the table and assign them to variable.

	cols = table.find_all('td')

	# Find the length of rows, which is the number of <font> tags, and assign it to a variable num_cols.

	num_cols = len(cols)

	# Create an empty list to hold each of the <font> tags as an element

	colslist = []
	totalcols = 0
	# For each <font> in cols, append it to colslist as an element.

	for col in cols:
		colslist.append(col.string)
		totalcols = len(colslist)

	# Now colslist has every td as an element from [0] to totalcols = len(colslist)

	# The First 8 <font> entries are always the table headers i.e. Prime Street, Cross Street, etc.

	headers = colslist[0:8]

	# Prime Street
	# Cross Street
	# Dispatch Time
	# Incident Number
	# Incident Type
	# Alarm Level
	# Area
	# Dispatched Units

	# Get the indexes from 0 to the length of the original list, in steps of list_size, then create a sublist for each.
	# lists = [original_list[i:i+list_size] for i in xrange(0, len(original_list), list_size)]
	list_size = 8
	i = 0
	incidents = [colslist[i:i+list_size] for i in xrange(0, len(colslist), list_size)]

	# Works!

	num_inci = len(incidents) # Get the number of incidents
	added = time.strftime("%Y-%m-%d %H:%M")
	update = 'DB Updated @ ' + added

	# SQL TIME, Connect to our db.
	conn = sqlite3.connect("tofire.db")
	cursor = conn.cursor()

	# Now we put each incident into our database.
	for incident in incidents[1:num_inci]:
	    incident.append(added)
	    to_db = [i.strip() for i in incident]
	    cursor.execute(
	        """INSERT INTO incidents
	           (prime_street, cross_street, dispatch_time, incident_number,
	            incident_type, alarm_level, area, dispatched_units, date_added)
	           VALUES (?,?,?,?,?,?,?,?,?)""", to_db)
	    #lid = cursor.lastrowid

	conn.commit()
	print update
	print (cursor.lastrowid)
	threading.Timer(300, getincidents).start()

getincidents()
