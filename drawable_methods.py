from tkinter import *

def draw_stars( c, x, y, apparent_magnitude, tag):

	width = 1
	if apparent_magnitude < -1:
		r = 5
	elif apparent_magnitude < 0:
		r = 4
	elif apparent_magnitude < 1:
		r = 3
	elif apparent_magnitude < 3:
		r = 2
	elif apparent_magnitude < 5:
		r = 1
	elif apparent_magnitude < 7:
		r = 1
		width = 0
	else:
		r = 0
		width = 0


	star = c.create_oval(x-r, y-r, x+r, y+r, width = width, fill="#ffffff")
	#if tag != "NONE":
		#add tag here


def display(star):
	#do nothing yet just see if it compiles
	star.itemconfig(fill="#ff0000")

def remove(star):
	#do nothing yet just see if it compiles
	star.itemconfig(fill="#ffffff")
