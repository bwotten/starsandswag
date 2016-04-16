from bs4 import BeautifulSoup
soup = BeautifulSoup(open("StarNames.html"))

constellations = open("con.csv","w")
# starstrans = open("star_trans.csv","w")


#This csv file is complete so dont run this for loop anymore.
for x in soup.find_all('tr'):
    for y in x.find_all('b'):
        # print(y.text.split("(")[1].split(",")[0]+","+y.text.split(":")[1])
        translation = y.text.split(":")[1]
        constellations.write(y.text.split("(")[1].split(",")[0]+","+translation.replace(',',' ').replace('\n',' ')+"\n")

#This gets starnames and translations correctly. Some weird formatting stuff happening though.
# for x in soup.find_all('tr'):
#     for y in x.find_all('td'):
#         for z in y.find_all('i'):
#             translation = str(z.parent.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text)
#             # print (z.text+",\""+translation.replace('\n',' ')+"\"\n")
#             starstrans.write(z.text.replace(',',' ')+","+translation.replace('\n',' ').replace(',',' ')+"\n")

# starstrans.close()
constellations.close()
#test comment
