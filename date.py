import time
def get_J2000(month, day, year):
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


#get current time in hours
print (time.strftime("%H"))

#get current date
x=time.strftime("%x")
print (x)
#month
print (x[0:2])
#day
print (x[3:5])
#year
print (x[6:8])

print (get_J2000(4,23,16))
