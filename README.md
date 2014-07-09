Flaming Bear
========================================================
<h3>Toronto Fire - Computer Assisted Dispatch Scrapper in Python</h3>
<h3>Github auto-suggested the name. For real.</h3>

Created a simple script to scrape the Toronto Fire Services Computerized Dispatch data feed located at:
<p>http://www.toronto.ca/fire/cadinfo/livecad.htm</p>

This project currently contains (many) files:
<ul>
<li>tofire_geo_v1.py - WIP</li>
<li>tofire_geo_v2.py - WIP</li>
<li>torontofire_csv.py - Outdated</li>
<li>create_database.py - Outdated</li>
<li>torontofire_db.py - Outdated</li>
</ul>

torontofire_csv.py - Outdated
------------------
This script uses beautiful soup to read the html table on the above page and collect the incidents into a
list of lists. The Toronto Fire Active Incidents page is refreshed every 5 minutes, so the script is set to run itself
accrodingly.

create_database.py - Outdated
------------------
This script will create a Sqlite database in the current directory called 'tofire.db' - The database will contain
a table called 'incidents' which contains 10 columns, to hold the information collected.

torontofire_db.py - Outdated
-----------------
This is a modified and slightly more advanced version of torontofire_csv.py. The idea is the same, however,
we now append the scrapped data to the database 'tofire.db' created with create_database. After the database
is updated each time, we print in the console the time of the update and the last row that was updated.

Notes:
------
Under construction - will update readme soon. (July 9th, 2014)
