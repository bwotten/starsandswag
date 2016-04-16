from bs4 import BeautifulSoup
soup = BeautifulSoup(open("list.html"))

const_names=open("const_names.csv","w")

text = soup.ul.text
for x in text.split('\n'):
    # print(x[0:5]+","+x[5:])
    const_names.write(x[1:4]+","+x[5:]+"\n")


const_names.close()
