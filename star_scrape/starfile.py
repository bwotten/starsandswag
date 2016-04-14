from bs4 import BeautifulSoup
soup = BeautifulSoup(open("StarNames.html"))

#b gets you the constellation text
for x in soup.find_all('tr'):
    for y in x.find_all('b'):
        print(y.text)

for x in soup.find_all('tr'):
    for y in x.find_all('td'):
        print(y.text)
