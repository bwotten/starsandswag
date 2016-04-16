from bs4 import BeautifulSoup
soup = BeautifulSoup(open("StarNames.html"))

constellations = open("con.csv","w")
starstrans = open("star_trans.csv","w")


#Constellation abbreviations and translations
for x in soup.find_all('tr'):
    for y in x.find_all('b'):
        translation = y.text.split(":")[1]
        constellations.write(y.text.split("(")[1].split(",")[0]+","+translation.replace(',',' ').replace('\n',' ')+"\n")

#Star names and translations
for x in soup.find_all('tr'):
    for y in x.find_all('td'):
        for z in y.find_all('i'):
            translation = str(z.parent.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text)
            starstrans.write(z.text.replace(',',' ')+","+translation.replace('\n',' ').replace(',',' ')+"\n")

starstrans.close()
constellations.close()
