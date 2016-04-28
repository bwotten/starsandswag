from bs4 import *
import requests
import csv

wiki_constells = []
with open('wiki_constellation.csv', 'r', newline='') as fp:
    a = csv.reader(fp, delimiter=',')

    for row in a:
        wiki_constells.append(row)
f = open("star_results.csv", "wb")
for constellation in wiki_constells:
	list_url = "https://en.wikipedia.org/wiki/List_of_stars_in_" + constellation[0]
	list_url.strip()
	list_soup = BeautifulSoup(requests.get(list_url).text, "html.parser")
	for superscript in list_soup.find_all("sup"):
	    superscript.decompose()

	
	star_table = list_soup.find("table", {"class":"wikitable"})
	if star_table != None:
		star_rows = star_table.findAll("tr")
		for star in star_rows:
			column = star.findAll("td")
			#populate url
			if len(column) == 13:
				proper = "NA"
				bayer = "NA"
				flamsteed = "NA"
				variable = "NA"
				hd = "NA"
				hip = "NA"
				vis_mag = "NA"
				abs_mag = "NA"
				dist = "NA"
				sp_class = "NA"
				index = 0
				for col in column:
					if col.find(text=True) != None:
						if index != 12 and index != 6 and index != 7:
							#proper,bayer,flamsteed,variable,hd,hip,vis_mag,abs_mag,dist,sp_class from const_names,star_info where abb=%s and const=name;"
							if index == 0:
								if len(col.find(text=True)) < 20:
									proper = col.find(text=True)
							elif index == 1:
								if len(col.find(text=True)) < 20:
									bayer = col.find(text=True)
							elif index == 2:
								if len(col.find(text=True)) < 20:
									flamsteed = col.find(text=True)
							elif index == 3:
								if len(col.find(text=True)) < 20:
									variable = col.find(text=True)
							elif index == 4:
								if len(col.find(text=True)) < 20:
									hd = col.find(text=True)
							elif index == 5:
								if len(col.find(text=True)) < 20:
									hip = col.find(text=True)
							elif index == 8:
								if len(col.find(text=True)) < 20:
									vis_mag = col.find(text=True)
							elif index == 9:
								if len(col.find(text=True)) < 20:
									abs_mag = col.find(text=True)
							elif index == 10:
								if len(col.find(text=True)) < 20:
									dist = col.find(text=True)
							elif index == 11:
								if len(col.find(text=True)) < 20:
									sp_class = col.find(text=True)
					index += 1

				url = column[0].find('a')
				if url != None and column[1].find(text=True) != None:
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
							if len(cells) == 2 and cells[0].find(text=True) != None:
								if cells[0].find(text=True) in "Mass" and mass == "NA" and len(cells[1].find(text=True)) < 20:
									mass = cells[1].find(text=True)
								elif cells[0].find(text=True) in "Radius" and radius == "NA" and len(cells[1].find(text=True)) < 20:
									radius = cells[1].find(text=True)
								elif cells[0].find(text=True) in "Surface gravity" and surface_g == "NA" and len(cells[1].find(text=True)) < 20:
									surface_g = cells[1].find(text=True)
								elif cells[0].find(text=True) in "Temperature" and temp == "NA" and len(cells[1].find(text=True)) < 20:
									temp = cells[1].find(text=True)
								elif cells[0].find(text=True) in "Age" and age == "NA" and len(cells[1].find(text=True)) < 20:
									age = cells[1].find(text=True)

					#proper,bayer,flamsteed,variable,hd,hip,vis_mag,abs_mag,dist,sp_class from const_names,star_info where abb=%s and const=name;"
					f.write("\"".encode('utf-8'))
					f.write(proper.encode('utf-8'))
					f.write("\"".encode('utf-8'))
					f.write(",".encode('utf-8'))
					f.write("\"".encode('utf-8'))
					f.write(bayer.encode('utf-8'))
					f.write("\"".encode('utf-8'))
					f.write(",".encode('utf-8'))
					f.write("\"".encode('utf-8'))
					f.write(flamsteed.encode('utf-8'))
					f.write("\"".encode('utf-8'))
					f.write(",".encode('utf-8'))
					f.write("\"".encode('utf-8'))
					f.write(variable.encode('utf-8'))
					f.write("\"".encode('utf-8'))
					f.write(",".encode('utf-8'))
					f.write("\"".encode('utf-8'))
					f.write(hd.encode('utf-8'))
					f.write("\"".encode('utf-8'))
					f.write(",".encode('utf-8'))
					f.write("\"".encode('utf-8'))
					f.write(hip.encode('utf-8'))
					f.write("\"".encode('utf-8'))
					f.write(",".encode('utf-8'))
					f.write("\"".encode('utf-8'))
					f.write(vis_mag.encode('utf-8'))
					f.write("\"".encode('utf-8'))
					f.write(",".encode('utf-8'))
					f.write("\"".encode('utf-8'))
					f.write(abs_mag.encode('utf-8'))
					f.write("\"".encode('utf-8'))
					f.write(",".encode('utf-8'))
					f.write("\"".encode('utf-8'))
					f.write(dist.encode('utf-8'))
					f.write("\"".encode('utf-8'))
					f.write(",".encode('utf-8'))
					f.write("\"".encode('utf-8'))
					f.write(sp_class.encode('utf-8'))
					f.write("\"".encode('utf-8'))
					f.write(",".encode('utf-8'))
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