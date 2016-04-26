import wikipedia, csv
stars_name = []
constell = {}

#open's csv
with open('/Users/patrickjameswhite/Desktop/starsandswag/ddl/stars_trim_bf.csv', 'r', newline='') as fp:
    a = csv.reader(fp, delimiter=',')

    for row in a:
        #print(row[8])
        if row[8] != "NA":
            stars_name.append(row[8])

#open's csv
with open('/Users/patrickjameswhite/Desktop/abbrevs.csv', 'r', newline='') as fp:
    a = csv.reader(fp, delimiter=',')

    for row in a:
        row = row[0].split(' ',1)
        constell[row[0]] = row[1]



output_csv = [['Original Name','Wiki Name','Summary']]
hit_count = 0


#fetch's a star name given just a string, searches through all the results until it founds a star
def fetchStar(name):
    if name.strip() == "":
        return False
    fetched = wikipedia.search(name)

    for s in fetched:
        try:

            wiki_page = wikipedia.page(s,None,True,True,False)
            star_check = wiki_page.summary
            if "star" in star_check and "constellation" in star_check:
                return wiki_page.summary
        except wikipedia.exceptions.PageError:
            return False
        except wikipedia.exceptions.DisambiguationError as e:
            pass

    return False


#star name taken from the db, then formatted so I don't have to search
def fetchConstell(star):
    if star.strip() == "":
        return False


    wiki_page = wikipedia.page(star,None,True,True,False)
    try:
        return wiki_page.summary
    except wikipedia.exceptions.PageError:
        return False
    except wikipedia.exceptions.DisambiguationError as e:
        return False

    #categories
    #content
    #coordinates
    #html
    #images
    #links
    #original_title
    #pageid
    #parent_id
    #references
    #revision_id
    #section
    #sections
    #summary
    #title
    #url




constell_summary = {}
prefix = "List_of_stars"
constellations = []
#constellation formatting
for c,name in enumerate(stars_name):
    search = constell[name]
    search_plus = search + " (constellation)"
    fetched = fetchConstell(search_plus)

    constellations.append([name,search,fetched])

    print([name,search,fetched])


#stars formatting
'''hit_count = 0
for c,name in enumerate(stars_name):
    print(c,name)
    name_list = name.split('or')
    for star in name_list:
        star = star.strip()
        fetched = fetchStar(star)

        if fetched:
            output_csv.append([name,star,fetched])
            hit_count += 1
            break
    #if fetch(name):
        #hit_count += 1
print(hit_count)



with open('/Users/patrickjameswhite/Desktop/stars_trim_wiki_output.csv', 'w', newline='') as fp:
    a = csv.writer(fp, delimiter=',')
    for row in output_csv:
        a.writerow(row)'''


