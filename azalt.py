import math

def get_alt_az(ra, dec, lat, lon, time, date):
	ra_deg  = ra * 15
	#NEED TO IMPLEMENT ACTUAL FUNCTION
	j2000 = 5956.5
	lst = (100.46 + (.985647 * j2000) + lon + (15 * time)) % 360
	ha = (lst - ra_deg) % 360
	alt_sin = (sin(dec) * sin(lat)) + (cos(dec)*cos(lat)*cos(ha))
	alt = asin(alt_sin)

	az_cos = (sin(dec) - sin(alt)*sin(lat)) / (cos(alt) * cos(lat))
	az = acos(az_cos)
	if sin(ha) >= 0:
		az = 360 - az

	return (alt, az)