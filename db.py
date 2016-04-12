#Simple script to get the idea for connecting to the db
import psycopg2
import getpass

# Run this command to start ssh tunneling
# ssh -L 63333:localhost:5432 zpfallon@db.cs.wm.edu


password = getpass.getpass('Password: ')

params = {
  'database': 'group3_stars',
  'user': 'zpfallon',
  'password': password,
  'host': 'localhost',
  'port': 63333
}
#Open the connection
conn = psycopg2.connect(**params)
#Open the cursor
cur = conn.cursor()

#Simple select statement and then fetch to get results
cur.execute("select * from stars where mag < 0;")
print (cur.fetchall())

#Close everything out
cur.close()
conn.close()
