from tkinter import *
from math import *

#http://stackoverflow.com/questions/21977786/star-b-v-color-index-to-apparent-rgb-color

def draw_stars( c, x, y, apparent_magnitude, tag, constellation):

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
	
	star = c.create_oval(x-r, y-r, x+r, y+r, width = width, fill="#ffffff", tags = (tag, constellation))
	
	return star;

def display(star):
	#do nothing yet just see if it compiles
	star.itemconfig(fill="#ff0000")

def remove(star):
	#do nothing yet just see if it compiles
	star.itemconfig(fill="#ffffff")





def color_to_rgb(color_index):
	t = 4600 * ((1 / ((0.92 * bv) + 1.7)) +(1 / ((0.92 * bv) + 0.62)) )
	x, y = 0
	if t >= 1667 and t <= 4000:
		x = ((-0.2661239 * pow(10,9)) / pow(t,3)) + ((-0.2343580 * pow(10,6)) / pow(t,2)) + ((0.8776956 * pow(10,3)) / t) + 0.179910
	elif t > 4000 and t <= 2222:
		x = ((-3.0258469 * pow(10,9)) / pow(t,3)) + ((2.1070379 * pow(10,6)) / pow(t,2)) + ((0.2226347 * pow(10,3)) / t) + 0.240390

	if t >= 1667 and t <= 2222:
  		y = -1.1063814 * pow(x,3) - 1.34811020 * pow(x,2) + 2.18555832 * x - 0.20219683
	elif t > 2222 and t <= 4000:
  		y = -0.9549476 * pow(x,3) - 1.37418593 * pow(x,2) + 2.09137015 * x - 0.16748867
	elif t > 4000 and t <= 25000:
  		y = 3.0817580 * pow(x,3) - 5.87338670 * pow(x,2) + 3.75112997 * x - 0.37001483