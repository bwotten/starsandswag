from bs4 import *
import requests

list_url = "https://en.wikipedia.org/wiki/List_of_stars_in_Andromeda"
list_soup = BeautifulSoup(requests.get(list_url).text, "html.parser")
for superscript in list_soup.find_all("sup"):
    superscript.decompose()

f = open("whateverpenis.csv", "wb")
star_table = list_soup.find("table", {"class":"wikitable"})
star_rows = star_table.findAll("tr")
for star in star_rows:
	column = star.findAll("td")
	#populate url
	if len(column) == 13:
		url =column[0].find('a')
		if url != None:
			url =  "https://en.wikipedia.org" + url.get('href')
			print(url)
			soup = BeautifulSoup(requests.get(url).text, "html.parser")
			for superscript in soup.find_all("sup"):
			    superscript.decompose()

			table = soup.find("table", {"class" : "infobox"})
			if table != None:
				mass = "NA"
				radius = "NA"
				surface_g = "NA"
				temp = "NA"
				age = "NA"
				for row in table.findAll("tr"):
					cells = row.findAll("td")
					if len(cells) == 2:
						if cells[0].find(text=True) in "Mass" and mass == "NA":
							mass = cells[1].find(text=True)
						elif cells[0].find(text=True) in "Radius" and radius == "NA":
							radius = cells[1].find(text=True)
						elif cells[0].find(text=True) in "Surface gravity" and surface_g == "NA":
							surface_g = cells[1].find(text=True)
						elif cells[0].find(text=True) in "Temperature" and temp == "NA":
							temp = cells[1].find(text=True)
						elif cells[0].find(text=True) in "Age" and age == "NA":
							age = cells[1].find(text=True)
				f.write("\"".encode('utf-8'))
				f.write(mass.encode('utf-8'))
				f.write("\"".encode('utf-8'))
				f.write(",".encode('utf-8'))
				f.write("\"".encode('utf-8'))
				f.write(radius.encode('utf-8'))
				f.write("\"".encode('utf-8'))
				f.write(",".encode('utf-8'))
				f.write("\"".encode('utf-8'))
				f.write(surface_g.encode('utf-8'))
				f.write("\"".encode('utf-8'))
				f.write(",".encode('utf-8'))
				f.write("\"".encode('utf-8'))
				f.write(temp.encode('utf-8'))
				f.write("\"".encode('utf-8'))
				f.write(",".encode('utf-8'))
				f.write("\"".encode('utf-8'))
				f.write(age.encode('utf-8'))
				f.write("\"".encode('utf-8'))
				f.write("\n".encode('utf-8'))
