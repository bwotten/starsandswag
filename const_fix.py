f = open("const_dump.txt", "r")

write_to = open("constellations.txt", "w")

results = f.readlines()
for line in results:
	if "List" in line:
		total_tuple = line.split(" ")
		count = 0
		found_in = False
		string = ""
		for item in total_tuple:
			if item == "in":
				found_in = True
			elif found_in:
				string = string + "_" +str(item)
		#compose string
		string.strip()
		write_to.write(str(string))
