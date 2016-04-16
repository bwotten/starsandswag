from bs4 import BeautifulSoup
soup = BeautifulSoup(open("StarNames.html"))

#This parses the constellations correctly, just write the print string to
#a csv file.
for x in soup.find_all('tr'):
    for y in x.find_all('b'):
        print(y.text.split("(")[1].split(",")[0]+","+y.text.split(":")[1])

# for x in soup.find_all('tr'):
#     for y in x.find_all('td'):
#         print(y.text)
