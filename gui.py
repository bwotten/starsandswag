from tkinter import *
from drawable_methods import *
from random import *
from queue import *
from functools import partial
from PIL import Image, ImageTk
from math import *
from mapping import *
import getpass
import psycopg2
import csv
import time
class application(Tk):
	def __init__(self, parent):
		Tk.__init__(self, parent)
		self.parent = parent
		self.initialize()

	def initialize(self):
		#widgets created here
		self.grid()

		self.logo_window = PanedWindow(self,bg='#000000')
		self.logo_window.grid(column=0, row=0, stick='EW',columnspan=5)

		logo = ImageTk.PhotoImage(file="starsandswag.png")
		logo_label = Label(self.logo_window,image=logo,bg='black')
		logo_label.image = logo
		logo_label.pack()
		# logo_label.grid(column=0,row=0)
		self.input_window = PanedWindow(self,bg='#000000')
		self.input_window.grid(column=0, row=1, stick='EW')

		self.continue_window = PanedWindow(self,bg='#000000')
		self.continue_window.grid(column=0, row=2, stick='EW')

		self.input_window.grid()
		self.continue_window.grid()

		self.input_window.grid_columnconfigure(0, weight = 1)
		self.input_window.grid_columnconfigure(1, weight = 1)
		self.continue_window.grid_columnconfigure(0, weight = 1)

		self.x_label_var = StringVar()
		self.x_label_var.set("Longitude: ")
		x_label = Label(self.input_window, textvariable=self.x_label_var,anchor="w",fg="yellow",bg="black")
		x_label.grid(column=0, row=0, stick='E')

		self.x_entry = Entry(self.input_window)
		self.x_entry.grid(column=1, row=0, sticky='W')

		self.y_label_var = StringVar()
		self.y_label_var.set("Latitude: ")
		y_label = Label(self.input_window, textvariable=self.y_label_var,anchor="w",fg="yellow",bg="black")
		y_label.grid(column=0, row=1, stick='E')

		self.y_entry = Entry(self.input_window)
		self.y_entry.grid(column=1, row=1, sticky='W')

		self.submit_button = Button(self.continue_window, text="Submit", anchor="center", command=self.submit_coords,highlightbackground='black')
		self.submit_button.grid(column=0, row=0)


		self.grid_columnconfigure(0, weight=2)
		self.resizable(True,True)

	def submit_coords(self):
		#get the values in the text of the entry widgets and make them floats
		longitude = self.x_entry.get()
		valid_x = False
		valid_y = False
		try:
			longitude = float(longitude)
			if -180 <= longitude <= 180:
				valid_x = True
			else:
				valid_x = False
				print("Invalid Longitude Coordinate")
				self.x_entry.delete(0, END)
		except ValueError:
			print("Invalid Longitude Coordinate")
			self.x_entry.delete(0, END)
			valid_x = False


			#comment here
		latitude = self.y_entry.get();
		try:
			latitude = float(latitude)
			if -90 <= latitude <= 90:
				valid_y = True
			else:
				valid_y = False
				print("Invalid Latitude Coordinate")
				self.y_entry.delete(0, END)
		except ValueError:
			print("Invalid Latitude Coordinate")
			self.y_entry.delete(0, END)
			valid_y = False

		self.star_list = []
		#do stuff with coordinates if we have the correct values

		#select stars that we want to put in our night sky

		#Distance formula in to get x intercept

		if valid_x and valid_y:

			#we can move onto next thing
			self.clear_window()
			self.create_canvas()
			#self.attributes("-fullscreen", True)
			self.state('zoomed')
			#create random x & y values for drawing stars with random values from -2 to 7 for mag
			i = 0
			j = 0

			self.viewable_stars1 = []
			self.viewable_stars2 = []
			self.viewable_stars3 = []
			self.viewable_stars4 = []
			self.viewable_arrays = []
			self.viewable_arrays.append(self.viewable_stars1)
			self.viewable_arrays.append(self.viewable_stars2)
			self.viewable_arrays.append(self.viewable_stars3)
			self.viewable_arrays.append(self.viewable_stars4)
			#populate viewable_stars as an array of tuples [ tuples ]
			# Run this command to start ssh tunneling
			# ssh -L 63333:localhost:5432 zpfallon@db.cs.wm.edu
			# password = getpass.getpass('Password: ')
			#lat and lon come from user input
			self.lat = latitude
			self.lon = longitude
			#we will only be considering 8:00pm for time
			time_hour = 20
			#Eventually need a function to get
			date = time.strftime("%x")
			month = int(date[0:2])
			day = int(date[3:5])
			year = int(date[6:8])
			# j2000 = get_J2000(month,day,year)
			j2000 = 5965.5

			params = {
			  'database': 'group3_stars',
			  'user': 'zpfallon',
			  'password': 'Zpf1234!',
			  'host': 'localhost',
			  'port': 63333
			}
			#Open the connection
			conn = psycopg2.connect(**params)
			#Open the cursor
			cur = conn.cursor()

			#Simple select statement and then fetch to get results
			cur.execute("select ra,dec,mag,id,con from stars;")
			for x in cur.fetchall():
				alt_az = get_alt_az(float(x[0]),float(x[1]),self.lat,self.lon,time_hour,date)
				if alt_az[0] > 0 and alt_az[0] < 90:
					if alt_az[1] < 90:
						self.viewable_stars1.append((alt_az[0],alt_az[1],float(x[2]),str(x[3]),str(x[4])))
					elif alt_az[1] < 180:
						self.viewable_stars2.append((alt_az[0],alt_az[1],float(x[2]),str(x[3]),str(x[4])))
					elif alt_az[1] < 270:
						self.viewable_stars3.append((alt_az[0],alt_az[1],float(x[2]),str(x[3]),str(x[4])))
					else:
						self.viewable_stars4.append((alt_az[0],alt_az[1],float(x[2]),str(x[3]),str(x[4])))

			self.position = 0
			self.drawCanvas(0)
			#while i < 2500:
			#	i += 1
			#	x = randint(0, int(self.screen_width))
			#	y = randint(0, int(self.screen_height))
			#	a = randint(-2, 7)
			#	tag = "Star:" + str(i)
			#	star = draw_stars(self.canvas, x, y, a, tag)
			#	if a < 3:
			#		self.star_list.append(tag)
			#		self.canvas.tag_bind(star, "<Button-1>", self.click)
			#		self.canvas.tag_bind(star, "<Enter>", self.enter)
			#		self.canvas.tag_bind(star, "<Leave>", self.leave)

			print("We have valid coordinates")

	def drawCanvas(self, val):
		#integer passed for which array to pass to it
		# 0 = 0 --> 90
		# 1 = 90 --> 180
		# 2 = 180 --> 270
		# 3 = 270 --> 360
		self.star_list[:] = []
		for star in self.viewable_arrays[val]:
			star_x = self.getX(float(star[1]))
			star_y = self.getY(float(star[0]))
			a = star[2]
			tag = star[3]
			constellation = star[4]
			star_id = draw_stars(self.canvas, star_x, star_y, a, tag, constellation)
			self.star_list.append(tag)
			self.canvas.tag_bind(star_id, "<Button-1>", self.click)
			self.canvas.tag_bind(star_id, "<Enter>", self.enter)
			self.canvas.tag_bind(star_id, "<Leave>", self.leave)

		left_id = self.canvas.create_rectangle(0, 0, self.screen_width * .05, self.screen_height, fill = "yellow", tag = "leftArrow" )
		right_id = self.canvas.create_rectangle(self.screen_width * .95, 0, self.screen_width , self.screen_height, fill = "yellow", tag = "rightArrow")
		self.canvas.tag_bind(left_id, "<Button-1>", self.rotate_left)
		self.canvas.tag_bind(right_id, "<Button-1>", self.rotate_right)
		self.text = self.canvas.create_text(0, 0, text = "", fill = "white", state = "hidden", tag = "text")

	def rotate_right(self, event):
		self.position = (self.position - 1) % 4
		self.canvas.delete("all")
		self.drawCanvas(self.position)

	def rotate_left(self, event):
		self.position = (self.position + 1) % 4
		self.canvas.delete("all")
		self.drawCanvas(self.position)

	def getX(self, star_az):
		#fuckton of cool trig here
		#star_az in is degrees so we need to make sure we do it in radians when we do sin(star_az)
		phi = pi - radians(star_az) - (pi/4)
		radius = sqrt(pow(self.canvas_width, 2) / 2)
		x = ((radius) * sin(radians(star_az)))/sin(phi) + self.screen_width * .05
		#x is a percentage of the screen, we should probably now multiply it by how wide our screen is
		#star_az = star_az % 90
		#x = (star_az / float(90)) * self.screen_width
		return x

	def getY(self, star_alt):
		#y = mx + b
		phi = pi - radians(star_alt) - (pi/4)
		radius = sqrt(pow(self.screen_height, 2) / 2)
		y = ((radius) * sin(radians(star_alt))) / sin(phi)
		#y is a percentage of the screen, we should probably now multiply it by how tall our screen is, also since it scales downwards we want to invert
		y = self.screen_height - y

		return y


	def clear_window(self):
		self.continue_window.grid_forget()
		self.input_window.grid_forget()

	def create_canvas(self):
		self.canvas_window = PanedWindow(self)
		self.canvas_window.grid(column=0, row=0, stick='EW')
		self.screen_height = self.winfo_screenheight()
		self.screen_width = self.winfo_screenwidth()
		self.canvas_height = self.screen_height * .9
		self.canvas_width = self.screen_width * .9
		self.canvas = Canvas(self.canvas_window, bg='black', height=self.screen_width, width=self.screen_width)
		self.canvas.grid(column = 0, row = 0, stick='EW')

	def leave(self, event):
		constellation_tuple = self.canvas.find_withtag(self.canvas.gettags(self.entered)[1])
		self.canvas.itemconfig(self.text, text = "")
		self.canvas.update_idletasks()

		for star in constellation_tuple:
			self.canvas.itemconfig(star, fill = "white")

	def enter(self, event):
		#Change color / highlight
		#Link the constellation
		#Show text
		self.entered = self.canvas.find_withtag(CURRENT)
		self.star = self.canvas.find_closest(event.x, event.y)
		self.name = self.canvas.gettags(self.star)[1]
		self.star_coords = self.canvas.coords(self.star)
		self.words_coords = self.canvas.coords(self.text)
		self.x = ((self.star_coords[0] + self.star_coords[2]) / 2) - self.words_coords[0]
		self.y = ((self.star_coords[1] + self.star_coords[3]) / 2 - 15) - self.words_coords[1]
		self.canvas.move(self.text, self.x, self.y)
		self.canvas.itemconfig(self.text, text = self.name, state = "normal")
		self.canvas.update_idletasks()

		reference = self.canvas.find_withtag(CURRENT)
		constellation_tuple = self.canvas.find_withtag(self.canvas.gettags(reference)[1])
		for star in constellation_tuple:
			self.canvas.itemconfig(star, fill = "green")


	def click(self, event):
		reference = self.canvas.find_withtag(CURRENT)
		constellation_tuple = self.canvas.find_withtag(self.canvas.gettags(reference)[1])
		for star in constellation_tuple:
			self.canvas.itemconfig(star, fill = "green")
		#self.canvas.itemconfig(self.canvas.find_withtag(reference[1]), fill="green")


if __name__ == "__main__":
    app = application(None)
    app.title('Stars & Swag')
    app.mainloop()




#top = tkinter.Tk();
#other code can go here
#top.mainloop();
