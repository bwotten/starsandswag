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

#latitude taken from input in the real program
latitude = 40
co_lat = 90 - latitude
#Simple select statement and then fetch to get results
SQL = "select x,y,y from stars where (%s+dec) > 0 and mag < 5.5;"
cur.execute(SQL,(co_lat,))
for x in cur.fetchall():
    print ("x= "+str(float(x[0]))+", y= "+str(float(x[1]))+", z= "+str(float(x[2])))

cur.execute("select * from const_names;")
for x in cur.fetchall():
    print (str(x[0])+","+str(x[1])+"\n")

#Close everything out
cur.close()
conn.close()
