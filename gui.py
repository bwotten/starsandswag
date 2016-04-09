from tkinter import *


class application(Tk):
	def __init__(self, parent):
		Tk.__init__(self, parent)
		self.parent = parent
		self.initialize()

	def initialize(self):
		#widgets created here
		self.grid()

		input_window = PanedWindow(self)
		input_window.grid(column=0, row=0, stick='EW')

		continue_window = PanedWindow(self)
		continue_window.grid(column=0, row=1, stick='EW')

		input_window.grid()
		continue_window.grid()

		self.x_label_var = StringVar()
		self.x_label_var.set("Longitude: ")
		x_label = Label(input_window, textvariable=self.x_label_var,anchor="w",fg="white",bg="blue")
		x_label.grid(column=0, row=0, stick='EW')

		self.x_entry = Entry(input_window)
		self.x_entry.grid(column=1, row=0, sticky='EW')

		self.y_label_var = StringVar()
		self.y_label_var.set("Latitude: ")
		y_label = Label(input_window, textvariable=self.y_label_var,anchor="w",fg="white",bg="blue")
		y_label.grid(column=0, row=1, stick='EW')

		self.y_entry = Entry(input_window)
		self.y_entry.grid(column=1, row=1, sticky='EW')

		self.submit_button = Button(continue_window, text="Submit", anchor="center", command=self.submit_coords)
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
		
		#do stuff with coordinates if we have the correct values
		if valid_x and valid_y:
			#we can move onto next thing
			print("We have valid coordinates")


if __name__ == "__main__":
    app = application(None)
    app.title('Stars & Swag')
    app.mainloop()



#top = tkinter.Tk();
#other code can go here
#top.mainloop();