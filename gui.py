from tkinter import *
from drawable_methods import *
from random import *
from queue import *
from functools import partial
from PIL import Image, ImageTk

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

		self.submit_button = Button(self.continue_window, text="Submit", anchor="center", command=self.submit_coords,fg='yellow',highlightbackground='black')
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

			viewable_stars = []
			#populate viewable_stars as an array of tuples [ tuples ]
			#each entry should have [0] = x, [1] = y, [2] = z, [3] = magnitude, [4] = tag

			self.z_screen = 1
			self.y_screen = 1
			self.x_screen = 1

			for star in viewable_stars:
				star_x = self.getX(star[0], star[2])
				star_y = self.getY(star[1], star[2])
				a = star[3]
				tag = star[4]
				star = draw_stars(self.canvas, x, y, a, tag)
				if a < 3:
					self.star_list.append(tag)
					self.canvas.tag_bind(star, "<Button-1>", self.click)
					self.canvas.tag_bind(star, "<Enter>", self.enter)
					self.canvas.tag_bind(star, "<Leave>", self.leave)

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

			self.text = self.canvas.create_text(0, 0, text = "", fill = "white", state = "hidden", tag = "text")
			print("We have valid coordinates")

	def getX(self, star_x, star_z):
		#y = mx + b
		slope = star_z / star_x
		z_intercept = self.z_screen
		#how much does it rise while it runs for 'the z distance away'
		x_intercept = z_intercept * slope
		return x_intercept

	def getY(self, star_y, star_z):
		#y = mx + b
		slope = star_z / star_y
		z_intercept = self.z_screen
		#how much does it rise while it runs for 'the z distance away'
		y_intercept = z_intercept * slope
		return y_intercept		


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
		self.canvas.itemconfig(self.entered, fill="white")
		self.canvas.itemconfig(self.text, text = "")
		self.canvas.update_idletasks()

	def enter(self, event):
		#Change color / highlight
		#Link the constellation
		#Show text
		self.entered = self.canvas.find_withtag(CURRENT)
		self.canvas.itemconfig(self.entered, fill="#ffffe6")
		self.star = self.canvas.find_closest(event.x, event.y)
		self.name = self.canvas.gettags(self.star)[0]
		self.star_coords = self.canvas.coords(self.star)
		self.words_coords = self.canvas.coords(self.text)
		self.x = ((self.star_coords[0] + self.star_coords[2]) / 2) - self.words_coords[0]
		self.y = ((self.star_coords[1] + self.star_coords[3]) / 2 - 15) - self.words_coords[1]
		self.canvas.move(self.text, self.x, self.y)
		self.canvas.itemconfig(self.text, text = self.name, state = "normal")
		self.canvas.update_idletasks()

	def click(self, event):
		self.canvas.itemconfig(self.canvas.find_withtag(CURRENT), fill="green")

if __name__ == "__main__":
    app = application(None)
    app.title('Stars & Swag')
    app.mainloop()




#top = tkinter.Tk();
#other code can go here
#top.mainloop();
