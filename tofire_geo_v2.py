import requests
import csv
import time
import threading
from bs4 import BeautifulSoup as bs
from geopy.geocoders import GoogleV3
import re
import psycopg2
import gc

_URL = 'http://www.toronto.ca/fire/cadinfo/livecad.htm'

def getincident():
    response = requests.get(_URL)
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

    geolocator = GoogleV3()

    conn = psycopg2.connect("dbname=firecad user=jm")
    cur = conn.cursor()

    for incident in incidents[1:num_inci]:
        prime = incident[0]
        prime = prime[:-4]
        cross = incident[1]
        cross = cross.split('/', 1)
        cross_one = cross[0]
        cross_two = cross[1]
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
	
	added = time.strftime("%Y-%m-%d %H:%M:%S")
    	update = 'DB Updated @ ' + added
    	print update
	time.sleep(299)

if __name__ == "__main__":
    gc.set_debug(gc.DEBUG_LEAK)
    print "\n== Without self reference =="
    no_self_reference()
    print "Uncollectable garbage", gc.garbage
    print "\n== With self reference =="
    self_reference()
    print "Uncollectable garbage", gc.garbage
    print "= Forcing full collection ="
    gc.collect()
    print "Uncollectable garbage", gc.garbage
    hw_thread = threading.Thread(target = getincident)
    hw_thread.daemon = True
    hw_thread.start()
    try:
        time.sleep(100000)
    except KeyboardInterrupt:
        print '\nGoodbye!'
        
