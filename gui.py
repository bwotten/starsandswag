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

		self.logo_window = PanedWindow(self,bg='#000000',borderwidth=0)
		self.logo_window.grid(column=0, row=0, stick='EW')

		logo = ImageTk.PhotoImage(file="starsandswag.png")
		logo_label = Label(self.logo_window,image=logo)
		logo_label.image = logo
		logo_label.pack()
		# logo_label.grid(column=0,row=0)

		self.input_window = PanedWindow(self,bg='#000000')
		self.input_window.grid(column=0, row=1, stick='EW')

		self.continue_window = PanedWindow(self,bg='#000000')
		self.continue_window.grid(column=0, row=2, stick='EW')

		self.input_window.grid()
		self.continue_window.grid()

		self.x_label_var = StringVar()
		self.x_label_var.set("Longitude: ")
		x_label = Label(self.input_window, textvariable=self.x_label_var,anchor="w",fg="white",bg="blue")
		x_label.grid(column=0, row=0, stick='EW')

		self.x_entry = Entry(self.input_window,bg='#000000')
		self.x_entry.grid(column=1, row=0, sticky='EW')

		self.y_label_var = StringVar()
		self.y_label_var.set("Latitude: ")
		y_label = Label(self.input_window, textvariable=self.y_label_var,anchor="w",fg="white",bg="blue")
		y_label.grid(column=0, row=1, stick='EW')

		self.y_entry = Entry(self.input_window,bg='#000000')
		self.y_entry.grid(column=1, row=1, sticky='EW')

		self.submit_button = Button(self.continue_window, text="Submit", anchor="center", command=self.submit_coords,fg='white',bg='#000000')
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
		self.text_queue = Queue()
		#do stuff with coordinates if we have the correct values


		if valid_x and valid_y:
			#we can move onto next thing
			self.clear_window()
			self.create_canvas()

			#create random x & y values for drawing stars with random values from -2 to 7 for mag
			i = 0
			j = 0
			while i < 80:
				i += 1
				x = randint(0, int(self.screen_width))
				y = randint(0, int(self.screen_height))
				a = randint(-2, 7)
				tag = "Star:" + str(i)
				star = draw_stars(self.canvas, x, y, a, tag)
				if a < 3:
					self.star_list.append(tag)
					self.canvas.tag_bind(star, "<Button-1>", self.click)
					self.canvas.tag_bind(star, "<Enter>", self.enter)
					self.canvas.tag_bind(star, "<Leave>", self.leave)

			self.text = self.canvas.create_text(0, 0, text = "", fill = "white", state = "hidden", tag = "text")
			print("We have valid coordinates")

	def clear_window(self):
		self.continue_window.grid_forget()
		self.input_window.grid_forget()

	def create_canvas(self):
		self.canvas_window = PanedWindow(self)
		self.canvas_window.grid(column=0, row=0, stick='EW')
		self.screen_height = self.winfo_screenheight()*.8
		self.screen_width = self.winfo_screenwidth()*.8
		self.canvas = Canvas(self.canvas_window, bg='black', height=self.screen_width, width=self.screen_width)
		self.canvas.grid(column = 0, row = 0, stick='EW')

	def leave(self, event):
		self.canvas.itemconfig(self.entered, fill="white")
		#self.canvas.itemconfig(self.text, text = "")
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
		self.y = ((self.star_coords[1] + self.star_coords[3]) / 2 - 10) - self.words_coords[1]
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
