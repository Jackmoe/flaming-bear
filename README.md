Toronto Fire Computerized Dispatch - Python Data Scraper
========================================================

Created a simple script to scrape the Toronto Fire Services Computerized Dispatch data feed located at:
<p>http://www.toronto.ca/fire/cadinfo/livecad.htm</p>

This project currently contains 3 files:
<ul>
<li>torontofire_csv.py</li>
<li>create_database.py</li>
<li>torontofire_db.py</li>
</ul>

torontofire_csv.py
------------------
This script uses beautiful soup to read the html table on the above page and collect the incidents into a
list of lists. The Toronto Fire Active Incidents page is refreshed every 5 minutes, so the script is set to run itself
accrodingly.
The list of incidents is then appended to a csv file by row. Currently, the script ignores the table headers.
You can create a blank csv file called 'tofire.csv' and put it in the same directory as this file,
and the script will write to that file automatically. Otherwise, create a csv and edit the script to show the correct
filename and path.

create_database.py
------------------
This script will create a Sqlite database in the current directory called 'tofire.db' - The database will contain
a table called 'incidents' which contains 10 columns, to hold the information collected.

torontofire_db.py
-----------------
This is a modified and slightly more advanced version of torontofire_csv.py. The idea is the same, however,
we now append the scrapped data to the database 'tofire.db' created with create_database. After the database
is updated each time, we print in the console the time of the update and the last row that was updated.

Notes:
------
Since some incidents will remain on the page after the 5 minute refresh, some duplicates may appear in both the csv,
and/or the database. Since the computerized dispatch assigns a unique 'Incident Number' to each incident, we are 
able to de-duplicate manually. I plan on adding the ability to detect duplicates, at a later date.
