from math import *
import time
def get_alt_az(ra, dec, lat, lon, time, date,j2000):
	ra_deg  = ra * 15
	ra_rad = radians(ra_deg)
	lat_rad = radians(lat)
	lon_rad = radians(lon)
	dec_rad = radians(dec)
	
    #converts the passed values to altitude and azumith based on astronomical formulas
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

def get_J2000(month, day, year):
    #conversion to j2000
    m = 0.0
    d = float(day)
    y = 0.0
    if month == 1:
    	m = 0
    elif month == 2:
    	m = 31
    elif month == 3:
    	m = 59
    elif month == 4:
    	m = 90
    elif month == 5:
    	m = 120
    elif month == 6:
    	m = 151
    elif month == 7:
    	m = 181
    elif month == 8:
    	m = 212
    elif month == 9:
    	m = 243
    elif month == 10:
    	m = 273
    elif month == 11:
    	m = 304
    else:
    	m = 334

    if year == 16:
    	y = 5842.5
    elif year == 17:
    	y = 6208.5
    else:
        print ("We cant go that far ahead")
    # j2000 = (20/24) + m + d + y
    return ((20/24) + m + d + y)
