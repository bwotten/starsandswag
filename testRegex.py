import wikipedia, csv, re
from html.parser import HTMLParser
stars_name = []
constell = {}
wiki_constells = []

#open's csv
def input_csv(data_struct,address,line_num):
    with open(address, 'r', newline='') as fp:
        a = csv.reader(fp, delimiter=',')

        for row in a:
            #print(row[8])
            if row[line_num] != "NA":
                data_struct.append(row[line_num])
    return data_struct

#open's csv
with open('/Users/patrickjameswhite/Desktop/wiki_constellations.csv', 'r', newline='') as fp:
    a = csv.reader(fp, delimiter=',')

    for row in a:
        wiki_constells.append(row)
output_csv = []
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


prefix = "List_of_stars"
constellations = []
#constellation formatting

def constellation_summary(constell):
    constell_summary = {}
    for c,name in enumerate(constell.keys()):
        print(c,name)
        search = constell[name]
        search_plus = search + " (constellation)"

        if name in constell_summary.keys():
            pass
        else:
            fetched = fetchConstell(search_plus)
            constell_summary[name] = [search,fetched]
            #print([name,search,fetched])
    return constell_summary

#stars formatting
def stars_summary(stars_name):

    for c,name in enumerate(stars_name):
        print(c,name)
        name_list = name.split('or')
        for star in name_list:
            star = star.strip()
            fetched = fetchStar(star)

            if fetched:
                output_csv.append([name,star,fetched])

                break
        #if fetch(name):
            #hit_count += 1
    return output_csv

def findCount(list2,start):
    count = 0
    for x in list2[start:]:

        if x == "":
            count += 1
        else:
            return count
    return 0

def fetch_constellation_stars(constellation):
    wiki_page = wikipedia.page('List_of_stars_in_'+constellation)
    begin = 0
    header_row = ["","","","","","","","","","",""]
    constellation_stars = []
    row_count = 0
    dont_add = 0
    for line in wiki_page.html().split('\n'):

        if "<th> Notes" in line:
            begin = 1
        elif begin == 0:

            if "Proper_names_(astronomy)" in line:
                header_row[0] = 0
            elif "Bayer_designation" in line:
                header_row[1] = 1
            elif "Flamsteed_designation" in line:
                header_row[2] = 2
            elif "Gould_designation" in line:
                header_row[3] = 3
            elif "Variable_star_designation" in line:
                header_row[4] = 4
            elif "Henry_Draper_Catalogue" in line:
                header_row[5] = 5
            elif "Hipparcos_Catalogue" in line:
                header_row[6] = 6
            elif "Apparent_magnitude" in line:
                header_row[7] = 7
            elif "Absolute_magnitude" in line:
                header_row[8] = 8
            elif "Stellar_distance" in line:
                header_row[9] = 9
            elif "Stellar_classification" in line:
                header_row[10] = 10

        #start of a star within a constellation
        elif begin == 1:
            if 'href="/wiki/' in line and "title=" in line or "page does not exist" in line:
                #print(line)
                dont_add = 0
                star_row = ["NA","NA","NA","NA","NA","NA","NA","NA","NA","NA","NA"]
                row_count = 0
                found = re.search(r'title="(.+)"',line)

                group = found.group(1)
                #print(group)
                if '"' in group:
                    index = group.find('"')
                    group = group[0:index]
                elif "(page does not exist)":
                    index = group.find("(")
                    group = group[0:index]
                star_row[0] = group
            else:
                offset = 0
                if line.count("td") == 2 and "</td></tr></table></td></tr>" not in line:
                    row_count += 1

                    #error handling because right ascension and declination are not used
                    #in the count, plus adding in an offset if a consetllation if missing a
                    #column
                    try:
                        if row_count > 8:
                            if row_count != header_row[row_count - 2]:
                                #print(1)
                                offset = findCount(header_row,row_count)
                                row_count += offset
                        else:
                            if row_count != header_row[row_count]:
                                #print(1)
                                offset = findCount(header_row,row_count)
                                row_count += offset
                    except IndexError:

                        pass
                        #print(row_count,line)


                    #capturing the b value
                    if row_count == 1:
                        found = re.search(r'>(.+)<',line)
                        try:
                            found = found.group(1).strip()
                            if "<" in found:
                                index = found.find('<')
                                found = found[0:index]
                                star_row[1] = found
                            else:
                                star_row[1] = found
                            if "&#" in star_row[1] and "" in star_row[1]:
                                dont_add = 1
                        except AttributeError:
                            print(1)
                            star_row[1] = 'NA'



                        if star_row[1].strip() == '':
                            dont_add = 1
                    #capturing the f value
                    elif row_count == 2:
                        #print(2)
                        found = re.search(r'>(.+)<',line)
                        try:
                            star_row[2] = found.group(1).strip()
                            if re.search("\d+",found.group(1).strip()) == False or "&#" in found.group(1).strip():
                                dont_add = 1
                        except AttributeError:
                            star_row[2] = 'NA'



                    #capturing the g value
                    elif row_count == 3:
                        #print(3)
                        found = re.search(r'>(.+)<',line)
                        try:
                            star_row[3] = found.group(1).strip()
                            if re.search("\d+",found.group(1).strip()) == False or "&#" in found.group(1).strip():
                                dont_add = 1
                        except AttributeError:
                            star_row[3] = 'NA'

                    #capturing the var value
                    elif row_count == 4:
                        #print(4)
                        found = re.search(r'>(.+)<',line)
                        try:
                            star_row[4] = found.group(1).strip()
                            if re.search("[0-9a-zA-Z]+",found.group(1).strip()) == False or "&#" in found.group(1).strip():
                                dont_add = 1
                        except AttributeError:
                            star_row[4] = 'NA'

                    #capturing HD value
                    elif row_count == 5:
                        #print(5)
                        found = re.search(r'>(.+)<',line)
                        try:
                            star_row[5] = found.group(1).strip()
                            if re.search("\d+",found.group(1).strip()) == False or "&#" in found.group(1).strip():
                                dont_add = 1
                        except AttributeError:
                            star_row[5] = 'NA'

                    #capturing the HIP value
                    elif row_count == 6:
                        #print(8,6)
                        found = re.search(r'>(.+)<',line)
                        try:
                            star_row[6] = found.group(1).strip()
                            if re.search("[0-9.]+",found.group(1).strip()) == False or "&#" in found.group(1).strip():
                                dont_add = 1
                        except AttributeError:
                            star_row[6] = 'NA'

                    #capturing the Vis Mag
                    elif row_count == 9:
                        #print(9,7)
                        found = re.search(r'>(.+)<',line)
                        try:
                            star_row[7] = found.group(1).strip()
                            if re.search("[0-9.]+",found.group(1).strip()) == False or "&#" in found.group(1).strip():
                                dont_add = 1
                        except AttributeError:
                            star_row[7] = 'NA'

                    #capturing the abs mag
                    elif row_count == 10:
                        #print(10,8)
                        found = re.search(r'>(.+)<',line)
                        try:
                            star_row[8] = found.group(1).strip()
                            if re.search("[\-+0-9]",found.group(1).strip()) == False or "&#" in found.group(1).strip():
                                dont_add = 1
                        except AttributeError:
                            star_row[8] = 'NA'

                    #capturing the dist
                    elif row_count == 11:
                        #print(11,9)
                        #print(line)
                        found = re.search(r'>(.+)<',line)
                        try:
                            star_row[9] = found.group(1).strip()
                            if re.search("\d+",found.group(1).strip()) == False or "&#" in found.group(1).strip():
                                dont_add = 1
                        except AttributeError:
                            star_row[9] = 'NA'

                    #capturing the sp
                    elif row_count == 12:
                        #print(12)
                        #print(line)
                        found = re.search(r'>([0-9a-zA-Z ]+)<',line)
                        try:
                            star_row[10] = found.group(1).strip()
                        except AttributeError:
                            star_row[10] = 'NA'
                        if dont_add == 0:
                            constellation_stars.append(star_row)



    return constellation_stars

'''fetch_constellation_stars("Camelopardalis")
wiki_page = wikipedia.page("List_of_stars_in_Orion")
for x in fetch_constellation_stars("Orion"):
    print(x)'''
count = 0
new_constellation = []
for constellation in wiki_constells:
    print(constellation)
    for fetched in fetch_constellation_stars(constellation[0]):
        print(fetched)
        new_list = [constellation[0]]
        for x in fetched:
            if x.strip() == "" or x.strip() == "NA":
                new_list.append("NA")
            else:
                new_list.append(x)
        new_constellation.append(new_list)
        count += 1
print(count)







with open('/Users/patrickjameswhite/Desktop/contellations_wiki_outputFinal.csv', 'w', newline='') as fp:
    a = csv.writer(fp, delimiter=',')
    for row in new_constellation:
        a.writerow(row)




