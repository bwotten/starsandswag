from math import *
import psycopg2
import getpass

def get_alt_az(ra, dec, lat, lon, time, date):
	ra_deg  = ra * 15
	ra_rad = radians(ra_deg)
	lat_rad = radians(lat)
	lon_rad = radians(lon)
	dec_rad = radians(dec)
	#NEED TO IMPLEMENT ACTUAL FUNCTION
	j2000 = 5956.5
	lst = (100.46 + (.985647 * j2000) + lon + (15 * time)) % 360
	lst_rad= radians(lst)
	ha = (lst - ra_deg) % 360
	ha_rad= radians(ha)
	alt_sin = (sin(dec_rad) * sin(lat_rad)) + (cos(dec_rad)*cos(lat_rad)*cos(ha_rad))
	alt = asin(alt_sin)

	az_cos = (sin(dec_rad) - sin(alt)*sin(lat_rad)) / (cos(alt) * cos(lat_rad))
	az = acos(az_cos)
	if degrees(sin(ha_rad)) >= 0:
		az = 360 - degrees(az)
	else:
		az = degrees(az)

	return (degrees(alt), az)


# Run this command to start ssh tunneling
# ssh -L 63333:localhost:5432 zpfallon@db.cs.wm.edu
password = getpass.getpass('Password: ')
lat = 35.780953
lon = 90.803196
time = 20
date = 0

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
cur.execute("select ra,dec from stars;")
count=0
for x in cur.fetchall():
	# print("ra: "+str(float(x[0]))+", dec: "+str(float(x[1]))+"\n")
	alt_az = get_alt_az(float(x[0]),float(x[1]),lat,lon,time,date)
	if alt_az[0] > 0 and alt_az[0] < 90 and alt_az[1] < 90:
		count+=1
	# print(alt_az)
print(count)
