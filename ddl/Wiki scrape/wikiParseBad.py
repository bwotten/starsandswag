__author__ = 'patrickjameswhite'
#finish csv
#add if statements
#
import lxml.etree
import urllib, urllib.parse,urllib.request
import csv
import re

def fetchResult(title):
    #print("**",title)
    params = { "format":"xml", "action":"query", "prop":"revisions", "rvprop":"timestamp|user|comment|content" }
    params["titles"] = "API|%s" % urllib.parse.quote(title.encode("utf8"))
    qs = "&".join("%s=%s" % (k, v)  for k, v in params.items())
    url = "http://en.wikipedia.org/w/api.php?%s" % qs
    #print(urllib.request.urlopen(url))
    tree = lxml.etree.parse(urllib.request.urlopen(url))

    revs = tree.xpath('//rev')

    return revs[-1].text

def capture_str(string,first,second):

    start = string.find(first) + len(first)
    end = string[start:].find(second) + start
    #print(string)
    #print(start,end)
    #print(string[start:end])
    if start != -1 and end != -1:
        return string[start:end]
    else:
        return False

fileGood = open("outputGood.txt","w")
fileBad = open("outputBad.txt","w")

stars_name = []
#/Users/patrickjameswhite/Desktop/starsandswag/ddl/star_scrape/star_trans.csv
#/Users/patrickjameswhite/Downloads/starnames.csv
with open('/Users/patrickjameswhite/Desktop/starsandswag/ddl/star_scrape/star_trans.csv', 'r', newline='') as fp:
    a = csv.reader(fp, delimiter=',')

    for row in a:
        stars_name.append(row[0])



hit_count = 0
csv_headers = ['original name','wikipedia name','equinox','constellation',
           'right ascension','declination','magnitude','parallax','temperature','gravity','rotational velocity',
            ]
good_count = 0
stars_name = ['Category:Constellations']
for num,title in enumerate(stars_name):


    #print(num,title)
    #print(num,title,title.split("or"))
    result = fetchResult(title)
    csv_line = [title,'','','','','','','','','','','','','','']
    #csv_line = [title]
    while "#redirect" in result or "#REDIRECT" in result:
        new_title = re.search( r"\[\[(.+)\]\]", result)

        try:
            result = fetchResult(new_title.group(1))

        except AttributeError:
            print("None type encountered")
            break
    #print(result)
    if "may refer to" in result:
        split_result = result.split('\n')
        #print(split_result)
        for line in split_result:
            if "star" in line:
                #print("line:",line)

                new_title = re.search( r"\[\[(.+)\]\]", line)

                try:
                    new_title = new_title.group(1)
                    if "|" in new_title:
                        new_title = new_title.split("|")[0]
                        #print(new_title)
                    #print(new_title)
                    result = fetchResult(new_title)
                except AttributeError:
                    print("None type encountered")
                    break

    if "Starbox" not in result:
        fileBad.write("\n\n**Scrape for : %s\n\n" % title)
        fileBad.write(result)
        #print("Bad result")
        #print("Bad result")
    else:
        hit_count += 1
        fileGood.write("\n\n**Scrape for : %s\n\n" % title)
        fileGood.write(result)
    begin1 = 0
    begin2 = 0
    begin3 = 0
    begin4 = 0
    for line in result.split("\n"):

        if "Starbox end" in line:
            #print(1)
            begin1 = 1
        #print(capture_str(line,"'''","'''"))
        if begin1 == 1 and capture_str(line,"'''","'''"):
            #print(2)
            capture = capture_str(line,"'''","'''")
            csv_line[1] = capture
            begin1 = 0
        if "Starbox observe" in line:
            #print(3)
            begin2 = 1
        if begin2 == 1 and re.search("equinox\s*=",line):
            #print(4)
            capture = capture_str(line,"[[","]]")

            csv_line[2] = capture
        if begin2 == 1 and re.search("constell\s*=",line):
            capture = capture_str(line,"[[","]]")
            csv_line[3] = capture
        if begin2 == 1 and re.search("ra\s*=",line):
            #print(line)
            capture = capture_str(line,"{{","}}")
            csv_line[4] = capture

        if begin2 == 1 and re.search("dec\s*=",line):
            capture = capture_str(line,"{{","}}")
            csv_line[5] = capture


        if begin2 == 1 and re.search("appmag_v\s*=",line):
            #print(line)
            capture = re.search(r"=([0-9. ]+)[(<]?\n?",line)
            #print(capture.groups())
            try:
                csv_line[6] = capture.group(1)
            except AttributeError:
                pass

            begin2 = 0

        if "Starbox astrometry" in line:
            begin3 = 1
        if begin3 == 1 and re.search("parallax\s*=",line):
            capture = re.search(r"parallax\s*=\s*(.+)",line)
            try:
                csv_line[7] = capture.group(1)
            except AttributeError:
                pass
            begin3 = 0
        if "Starbox detail" in line:
            begin4 = 1
        if begin4 == 1 and re.search("temperature\s*=",line):
            capture = re.search(r"temperature\s*=\s*(.+)<",line)
            try:
                csv_line[8] = capture.group(1)
            except AttributeError:
                pass
        if begin4 == 1 and re.search("gravity\s*=",line):
            capture = re.search(r"gravity\s*=\s*(.+)<",line)
            try:
                csv_line[9] = capture.group(1)
            except AttributeError:
                pass

        if begin4 == 1 and re.search("rotational_velocity\s*=",line):
            capture = re.search(r"rotational_velocity\s*=\s*",line)
            try:
                csv_line[10] = capture.group(1)
            except AttributeError:
                pass
            begin4 = 0


    print(csv_line)



        #print(csv_line)
    #print(revs[-1].text)
print(hit_count,good_count,len(stars_name))

fileGood.close()
fileBad.close()


