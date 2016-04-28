from tkinter import *
from math import *

#http://stackoverflow.com/questions/21977786/star-b-v-color-index-to-apparent-rgb-color

def draw_stars( c, x, y, apparent_magnitude, tag, constellation, color_index):

	#draws a circle with different color based on color index and radius based on magnitude and places that at x and y coordinates on map 

	if color_index != "NA":
		color = color_to_rgb(float(color_index))
	else:
		color = 'white'

	width = 1
	if apparent_magnitude < -1:
		r = 7
	elif apparent_magnitude < 0:
		r = 6
	elif apparent_magnitude < 1:
		r = 5
	elif apparent_magnitude < 2:
		r = 4
	elif apparent_magnitude < 3:
		r = 3
	elif apparent_magnitude < 4:
		r = 2
	elif apparent_magnitude < 5:
		r = 1
	elif apparent_magnitude < 7:
		r = 1
		width = 0
	else:
		r = 0
		width = 0
	
	star = c.create_oval(x-r, y-r, x+r, y+r, width = width, fill=color, tags = (tag, constellation, str(color)))
	
	return star;

def color_to_rgb(bv):
	#rough conversion of colors
	if bv < 0:
		rgb = "#9bb0ff"
	elif bv < .31:
		rgb = "#b9c9ff"
	elif bv < .5:
		rgb = "#e0e5ff"
	elif bv < .59:
		rgb = "#f6f3ff"
	elif bv < .82:
		rgb = "#fff8fc"
	elif bv < 1.41:
		rgb = "#ffeedd"
	elif bv < 2.00:
		rgb = "#ffc38b"
	else:
		rgb = "#ffc66d"

	return rgb