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

		x_def = StringVar(value='37')

		self.x_entry = Entry(self.input_window,textvariable=x_def)
		self.x_entry.grid(column=1, row=0, sticky='W')

		self.y_label_var = StringVar()
		self.y_label_var.set("Latitude: ")
		y_label = Label(self.input_window, textvariable=self.y_label_var,anchor="w",fg="yellow",bg="black")
		y_label.grid(column=0, row=1, stick='E')

		y_def = StringVar(value='-67')

		self.y_entry = Entry(self.input_window,textvariable=y_def)
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

			self.viewable_stars = []
			#populate viewable_stars as an array of tuples [ tuples ]
			# Run this command to start ssh tunneling
			# ssh -L 63333:localhost:5432 zpfallon@db.cs.wm.edu
			# password = getpass.getpass('Password: ')
			#lat and lon come from user input
			self.lat = latitude
			self.lon = longitude
			#we will only be considering 8:00pm for time
			self.time_hour = 20
			#Eventually need a function to get
			self.date = time.strftime("%x")
			month = int(self.date[0:2])
			day = int(self.date[3:5])
			year = int(self.date[6:8])
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

			
			self.az_range = 120
			self.alt_range = self.az_range * self.screen_height / self.screen_width
			self.alt_base = 0 
			self.az_base = 0
			#self.steps = int((90 - self.alt_range/2) / 10)
			#if (self.alt_range/2) % 10 != 0:
			#	self.steps += 1

			#self.az_increment = 240 / self.steps

			self.conn = psycopg2.connect(**params)
			#Open the cursor
			self.query()		

			self.position = 0
			self.drawCanvas()
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

	def drawCanvas(self):
		#integer passed for which array to pass to it
		# 0 = 0 --> 90
		# 1 = 90 --> 180
		# 2 = 180 --> 270
		# 3 = 270 --> 360
		self.star_list[:] = []
		for star in self.viewable_stars:
			star_x = self.getX(float(star[1]))
			star_y = self.getY(float(star[0]))
			a = star[2]
			tag = star[3]
			constellation = star[4]
			color_index = star[5]
			star_id = draw_stars(self.canvas, star_x, star_y, a, tag, constellation, color_index)
			self.star_list.append(tag)
			self.canvas.tag_bind(star_id, "<Button-1>", self.constellation_clicked)
			self.canvas.tag_bind(star_id, "<Enter>", self.enter)
			self.canvas.tag_bind(star_id, "<Leave>", self.leave)
		self.text = self.canvas.create_text(0, 0, text = "", fill = "white", state = "hidden", tag = "text")

		file = "right_arrow.png"
		self.right_photo = Image.open(file)
		self.right_photo = self.right_photo.resize((int(self.screen_width * .02), int(self.screen_height * .016666)))
		self.right_photo = ImageTk.PhotoImage(self.right_photo)
		self.right_image = self.canvas.create_image((self.screen_width * .95, self.screen_height * .05),image=self.right_photo)

		file = "left_arrow.png"
		self.left_photo = Image.open(file)
		self.left_photo = self.left_photo.resize((int(self.screen_width * .02), int(self.screen_height * .016666)))
		self.left_photo = ImageTk.PhotoImage(self.left_photo)
		self.left_image = self.canvas.create_image((self.screen_width * .925, self.screen_height * .05),image=self.left_photo)

		file = "up_arrow.png"
		self.up_photo = Image.open(file)
		self.up_photo = self.up_photo.resize((int(self.screen_width * .015), int(self.screen_height * .021)))
		self.up_photo = ImageTk.PhotoImage(self.up_photo)
		self.up_image = self.canvas.create_image((self.screen_width * .9375, self.screen_height * .025),image=self.up_photo)

		file = "down_arrow.png"
		self.down_photo = Image.open(file)
		self.down_photo = self.down_photo.resize((int(self.screen_width * .015), int(self.screen_height * .021)))
		self.down_photo = ImageTk.PhotoImage(self.down_photo)
		self.down_image = self.canvas.create_image((self.screen_width * .9375, self.screen_height * .075),image=self.down_photo)

		self.canvas.tag_bind(self.left_image, "<Button-1>", self.rotate_left)
		self.canvas.tag_bind(self.right_image, "<Button-1>", self.rotate_right)
		self.canvas.tag_bind(self.up_image, "<Button-1>", self.rotate_up)
		self.canvas.tag_bind(self.down_image, "<Button-1>", self.rotate_down)
		
		#right_photo = ImageTk.PhotoImage(right_image)
		#self.right_arrow = self.canvas.create_image((500, 500), image = right_photo)
		#self.left_arrow = self.canvas.create_image((0,0), image = left_arrow)
		

	def rotate_right(self, event):
		self.az_base = (self.az_base - 10) % 360
		self.query()
		self.canvas.delete("all")
		self.drawCanvas()

	def rotate_left(self, event):
		self.az_base = (self.az_base + 10) % 360
		self.query()
		self.canvas.delete("all")
		self.drawCanvas()

	def rotate_up(self, event):
		if self.alt_base + self.alt_range / 2 + 10 <= 90:
			#self.az_base += self.az_increment
			self.alt_base = (self.alt_base + 10)
			self.query()
			self.canvas.delete("all")
			self.drawCanvas()
		elif self.alt_base + self.alt_range / 2 == 90:
			#we do nothing
			self.alt_base = self.alt_base
		else:
			#self.az_base += self.az_increment
			self.alt_base = 90 - self.alt_range / 2
			self.query()
			self.canvas.delete("all")
			self.drawCanvas()

	def rotate_down(self, event):
		if self.alt_base - 10 >= 0:
			#self.az_base -= self.az_increment
			self.alt_base = self.alt_base - 10
			self.query()
			self.canvas.delete("all")
			self.drawCanvas()
		elif self.alt_base == 0:
			#we do nothing
			self.alt_base = self.alt_base
		else:
			self.alt_base = 0
			#self.az_base -= self.az_increment
			self.query()
			self.canvas.delete("all")
			self.drawCanvas()


	def query(self):
		self.viewable_stars[:] = []
		cur = self.conn.cursor()
		#Simple select statement and then fetch to get results
		cur.execute("select ra,dec,mag,id,con,ci,bf from stars;")
		for x in cur.fetchall():
			alt_az = get_alt_az(float(x[0]),float(x[1]),self.lat,self.lon,self.time_hour,self.date)
			if alt_az[0] > self.alt_base and alt_az[0] < self.alt_base + self.alt_range:
				if self.az_base < (self.az_base + self.az_range ) % 360:
					if alt_az[1] > self.az_base and alt_az[1] < (self.az_base + self.az_range) % 360:
						self.viewable_stars.append((alt_az[0],alt_az[1],float(x[2]),str(x[3]),str(x[4]),str(x[5])))
				else:
					if alt_az[1] > self.az_base or alt_az [1] < (self.az_base + self.az_range) % 360:
						self.viewable_stars.append((alt_az[0],alt_az[1],float(x[2]),str(x[3]),str(x[4]),str(x[5])))
		cur.close()

	def getX(self, star_az):
		#fuckton of cool trig here
		#star_az in is degrees so we need to make sure we do it in radians when we do sin(star_az)
		#need to convert viable star_az to 0 --> 120 on screen
		star_az = (star_az - self.az_base) % 360
		#star_az = star_az % self.az_range
		phi = pi - radians(star_az) - (pi/4)
		self.radius = sqrt(pow(self.screen_width, 2) / 2)
		x = self.screen_width - ((self.radius) * sin(radians(star_az)))/sin(phi)

		#x is a percentage of the screen, we should probably now multiply it by how wide our screen is
		#star_az = star_az % 90
		#x = (star_az / float(90)) * self.screen_width
		if x > self.screen_width:
			print("fuck")

		return x

	def getY(self, star_alt):
		#y = mx + b
		#ratio = self.screen_height / self.screen_width
		#phi = pi - radians(star_alt) - (pi/4)
		#radius = sqrt(pow(self.screen_height, 2) / 2)
		#y = ((radius) * sin(radians(star_alt))) / sin(phi)
		
		top_angle = asin((sin(radians(self.alt_base + self.alt_range))/self.radius) * self.screen_height)
		bottom_angle = pi - top_angle - radians(self.alt_base + self.alt_range)

		new_top_angle = pi - radians(star_alt-self.alt_base) - bottom_angle
		y = ((self.radius) / sin(new_top_angle)) * sin(radians(star_alt-self.alt_base)) 
		#y is a percentage of the screen, we should probably now multiply it by how tall our screen is, also since it scales downwards we want to invert
		y = self.screen_height - y

		if y > self.screen_height:
			print("fuck")

		return y


	def clear_window(self):
		self.continue_window.grid_forget()
		self.input_window.grid_forget()

	def create_canvas(self):
		self.canvas_window = PanedWindow(self)
		self.canvas_window.grid(column=0, row=0, stick='EW')
		self.screen_height = self.winfo_screenheight()
		self.screen_width = self.winfo_screenwidth()
		self.canvas = Canvas(self.canvas_window, bg='black', height=self.screen_width, width=self.screen_width)
		self.canvas.grid(column = 0, row = 0, stick='EW')

	def leave(self, event):
		constellation_tuple = self.canvas.find_withtag(self.canvas.gettags(self.entered)[1])
		self.canvas.itemconfig(self.text, text = "")
		self.canvas.update_idletasks()

		for star in constellation_tuple:
			self.canvas.itemconfig(star, fill = self.canvas.gettags(star)[2])

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
			self.canvas.itemconfig(star, fill = "blue")


	def constellation_clicked(self, event):
		reference = self.canvas.find_withtag(CURRENT)
		constellation_abrv = self.canvas.gettags(reference)[1]

		self.canvas.delete("all")
		return_button = Button(self, text = "Return", command = self.return_to_starmap, anchor = W,highlightbackground='black')
		return_button.configure(width = 10, activebackground = "#33B5E5")
		return_button_window = self.canvas.create_window(10, 10, anchor = NW, window = return_button)
		con_cur = self.conn.cursor()
		SQL = "select name,summary from const_names where abb=%s;"
		con_cur.execute(SQL,(constellation_abrv,))
		#const_info[0] is name, const_info[1] is summary
		const_info = con_cur.fetchone()

		string_title = const_info[0]
		string_desc = const_info[1].replace("Unicode", "")
		width = self.screen_width*.9

		self.const_title = self.canvas.create_text((self.screen_width*.5, self.screen_height * .10), text = string_title,fill='blue',font=("Purisa", 24))
		self.const_desc = self.canvas.create_text((self.screen_width*.5, self.screen_height*.175), text = string_desc, width = width,fill='black',font=("Purisa", 12))
		self.height = self.canvas.bbox(self.const_desc)[3] - self.canvas.bbox(self.const_desc)[1]
		self.canvas.move(self.const_desc, 0, self.height/2)
		self.canvas.itemconfig(self.const_desc, fill = 'white')


		#Dont actually want to select all.
		SQL="select const,proper,bayer,flamsteed,gold,variable,hd,hip,vis_mag,abs_mag,dist,sp_class from const_names,star_info where abb=%s and const=name;"
		con_cur.execute(SQL,(constellation_abrv,))

		self.star_list = []
		max_length = 0
		for x in con_cur.fetchall():
			#Do something
			string = str(x[2]) +" "+str(x[1])
			self.star_list.append((x, string))
			if len(string) > max_length:
				max_length = len(string)

		rows = len(self.star_list) / 5
		if len(self.star_list) % 5 != 0:
			rows = rows + 1

		temp = self.canvas.create_text((self.screen_width, self.screen_height), fill = 'black', text = 'a'*max_length,font = ("Purisa", 10))
		self.x_change = self.canvas.bbox(temp)[2] - self.canvas.bbox(temp)[0]
		self.y_change = (self.canvas.bbox(temp)[3] - self.canvas.bbox(temp)[1]) * 2
		self.canvas.delete(temp)
		self.total_y = self.y_change * rows

		self.x_start = self.screen_width * .75 - self.x_change * 2.5
		self.x_position = self.x_start
		self.y_start = self.screen_height - ((self.screen_height - (self.screen_height *.175 + self.height)) / 2) - (self.total_y / 2)
		self.y_position = self.y_start
		self.x_count = 0
		self.y_count = 0
		count = 0
		for star in self.star_list:
			text_id = self.canvas.create_text((self.x_position, self.y_position), text = star[1], fill = 'white', tag = str(count), font = ("Purisa", 10))
			self.x_count+=1
			self.x_position = self.x_position + self.x_change
			if(self.x_count == 5):
				self.y_count+=1
				self.x_count=0
				self.x_position = self.x_position - self.x_change * 5
				self.y_position = self.y_position + self.y_change
			count += 1
			self.canvas.tag_bind(text_id, "<Enter>", self.enter_text)
			self.canvas.tag_bind(text_id, "<Leave>", self.leave_text)


	def enter_text(self, event):
		self.entered = self.canvas.find_withtag(CURRENT)
		index = self.canvas.gettags(self.entered)[0]
		index = int(index)
		self.info_list = []

		#we're only giving the data tables a width of 2
		self.x_count = 0
		self.y_count = 0
		sql_index = 0
		max_length = 0
		for info in self.star_list[index][0]:
			if info != "NA" and info != None:
				if sql_index != 0 and sql_index != 1:
					string = self.return_column_title(sql_index) + info
					if len(string) > max_length:
						max_length = len(string)
				sql_index+=1

		new_temp = self.canvas.create_text((self.screen_width/2, self.screen_height/2), text = 'a'*max_length, fill = 'black',font=("Purisa", 10))
		self.x_change = self.canvas.bbox(new_temp)[2] - self.canvas.bbox(new_temp)[0]
		self.canvas.delete(new_temp)

		total_y = self.y_change * 5
		self.x_position = self.screen_width * .3 - self.x_change
		self.y_position = self.screen_height - ((self.screen_height - (self.screen_height *.175 + self.height)) / 2) - (total_y / 2)
		sql_index = 0
		for info in self.star_list[index][0]:
			if info != "NA" and info != None:
				if sql_index == 0 or sql_index == 1:
					#do nothing
					if sql_index == 1:
						string = info
						self.info_list.append(self.canvas.create_text((self.x_position + self.x_change / 2 , self.y_position - self.y_change * 1.1), text = string, fill = 'blue',font=("Purisa", 20)))

				else:
					string = self.return_column_title(sql_index) + info
					if sql_index == 10:
						string = string + " ly"
					self.info_list.append(self.canvas.create_text((self.x_position, self.y_position), text = string, fill = 'white',font=("Purisa", 10)))
					self.x_count+=1
					self.x_position = self.x_position + self.x_change
					if self.x_count == 2:
						self.x_count = 0
						self.x_position = self.x_position - self.x_change * 2
						self.y_position = self.y_position + self.y_change
						self.y_count += 1
			sql_index+=1


		#SQL="select const,proper,bayer,flamsteed,gold,variable,hd,hip,vis_mag,abs_mag,dist,sp_class from const_names,star_info where abb=%s and const=name;"



	def leave_text(self, event):
		for star_info in self.info_list:
			self.canvas.delete(star_info)

	def return_to_starmap(self):
		self.canvas.delete("all")
		self.drawCanvas()

	def return_column_title(self, num):
		#SQL="select const,proper,bayer,flamsteed,gold,variable,hd,hip,vis_mag,abs_mag,dist,sp_class from const_names,star_info where abb=%s and const=name;"
		string = ""
		if num == 0:
			string = "Constellation: "
		elif num == 1:
			string = "Proper Name: "
		elif num == 2:
			string = "Bayer Designation: "
		elif num == 3:
			string = "Flamsteed Number: "
		elif num == 4:
			string = "Gold Designation: "
		elif num == 5:
			string = "Variable Designation: "
		elif num == 6:
			string = "Henry Draper ID: "
		elif num == 7:
			string = "Hipparcos ID: "
		elif num == 8:
			string = "Visual Magnitude: "
		elif num == 9:
			string = "Absolute Magnitude: "
		elif num == 10:
			string = "Distance: "
		elif num == 11:
			string = "Spectral Class: "

		return string

if __name__ == "__main__":
    app = application(None)
    app.title('Stars & Swag')
    app.mainloop()




#top = tkinter.Tk();
#other code can go here
#top.mainloop();
