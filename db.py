#Simple script to get the idea for connecting to the db
import psycopg2
import getpass

# Run this command to start ssh tunneling
# ssh -L 63333:localhost:5432 zpfallon@db.cs.wm.edu

f = open('test_stars.csv','w')

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
cur.execute("select x,y,z from stars where con='UMa';")
for x in cur.fetchall():
    f.write(str(float(x[0]))+","+str(float(x[1]))+","+str(float(x[2]))+"\n")
#Close everything out
cur.close()
conn.close()
f.close()
