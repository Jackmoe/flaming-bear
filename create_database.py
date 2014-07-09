import sqlite3

conn = sqlite3.connect("tofire.db") #
 
cursor = conn.cursor()
 
# create a table

cursor.execute("""CREATE TABLE incidents
                  (Id INTEGER PRIMARY KEY, prime_street text, cross_street text, dispatch_time text, 
                   incident_number text, incident_type text, alarm_level text, area text, dispatched_units text, date_added text)
               """)