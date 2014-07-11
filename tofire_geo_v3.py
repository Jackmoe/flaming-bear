import requests
import csv
import time
import threading
from bs4 import BeautifulSoup as bs
from geopy.geocoders import GoogleV3
import re
import psycopg2
import gc

gc.enable()

_URL = 'http://www.toronto.ca/fire/cadinfo/livecad.htm'
_DB = psycopg2.connect("dbname=firecad user=jm")
_digits = re.compile('\d')

def contains_digits(d):
    return bool(_digits.search(d))

def getincident(url,conn):
    response = requests.get(url)
    r_code = 'Status = ' + str(response.status_code)
    r_encoding = 'Encoding = ' + str(response.encoding)

    soup = bs(response.text)
    table = soup.find("table", class_="info")
    cols = table.find_all('td')
    num_cols = len(cols)
    colslist = []
    totalcols = 0

    for col in cols:
        colslist.append(col.string)
        totalcols = len(colslist)

    headers = colslist[0:7]
    list_size = 8
    i = 0
    incidents = [colslist[i:i+list_size] for i in xrange(0, len(colslist), list_size)]

    num_inci = len(incidents) # Get the number of incidents
    added = time.strftime("%Y-%m-%d %H:%M:%S")

    geolocator = GoogleV3()

    cur = conn.cursor()

    for incident in incidents[1:num_inci]:
        prime = incident[0]
        prime = prime[:-4]
        cross = incident[1]
        cross = cross.split('/', 1)
        cross_one = cross[0]
        cross_two = cross[1]
        if contains_digits(incident[2]) == True:
            incident[2] = incident[2]
        else:
            incident[2] = added
        if prime and not prime.isspace() and cross_one and not cross_one.isspace():
            lookup = str(prime) + ' at ' + str(cross_one) + ', ' + 'Toronto, ON'
        elif prime and not prime.isspace() and cross_two and not cross_two.isspace():
            lookup = str(prime) + ' at ' + str(cross_two) + ', ' + 'Toronto, ON'
        elif cross_one and not cross_one.isspace() and cross_two and not cross_two.isspace():
            lookup = str(cross_one) + ' at ' + str(cross_two) + ', ' + 'Toronto, ON'
        address, (latitude, longitude) = geolocator.geocode(lookup)
	incident[7] = incident[7].replace("\n", "").replace("\r", "")
        incident[7] = incident[7][:-2]
	incident.append(address)
        incident.append(latitude)
        incident.append(longitude)
        to_db = [i for i in incident]
        cur.execute("INSERT INTO incidents (prime_street, cross_street, time, eid, etype, alarm, beat, units, address, latitude, longitude) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", to_db)        
   	conn.commit()
	
    	update = 'DB Updated @ ' + added
    	print update

if __name__ == "__main__":
    try:
        while True:
            getincident(_URL, _DB)
            time.sleep(299)
    except KeyboardInterrupt:
        print '\nGoodbye!'
        
