#-------------------------------------------------------------------------------
# Name:        AMC Locations
# Purpose:     Pulls locations of all AMCs in the country
#              Writes output to a csv file
# Date:        07/06/2016
# Author:      pverma
#-------------------------------------------------------------------------------

from BeautifulSoup import BeautifulSoup
import urllib2
import json
import csv
import time

print 'Start time: ',time.strftime('%X %x %Z')
linklist = [] #all links on page
locationsurl = [] #all links of locations
addresslist = [] #all addresses

html_page = urllib2.urlopen("https://www.amctheatres.com/movie-theatres")

soup = BeautifulSoup(html_page)
for link in soup.findAll('a'):
     linklist.append(link.get('href')) #get links fro,m <a element

for loc in linklist: #picks out the locations only
    if '/movie-theatres/' in str(loc):
        locationsurl.append(loc)

with open('AMC.csv', 'wb') as f: #write to csv
    writer = csv.writer(f, delimiter=',')
    writer.writerow(['Address', 'City', 'Latitude', 'Longitude', 'PostalCode', 'State']) #column headings
    for url in locationsurl: #for every url
        url = urllib2.urlopen(url)
        soup = BeautifulSoup(url)
        a = soup.find(id="theatre-area-inline-data")

        #remove html elements from json object
        line = str(a)
        line = line.replace('<script app-inline-data="" id="theatre-area-inline-data" type="application/json">',"")
        line = line.replace('</script>', "")
        #convert to json
        d = json.loads(line)
        try:
            for i in range(17): #Max number of theatres in one city is 17
                #pull out information from the page
                AddressLine1= d['theatres'][i]['AddressLine1']
                City = d['theatres'][i]['City']
                Latitude=d['theatres'][i]['Latitude']
                Longitude=d['theatres'][i]['Longitude']
                PostalCode=d['theatres'][i]['PostalCode']
                State=d['theatres'][i]['State']

                if AddressLine1 not in addresslist:
                    addresslist.append(AddressLine1)
                    to_write = str(AddressLine1),str(City),str(Latitude),str(Longitude),str(PostalCode),str(State)
                    writer.writerow([AddressLine1,City,Latitude,Longitude,PostalCode,State])
                f.flush()
        except: #if end of theatres for a city that does not have 17 theatres, the script skips and continues
            continue

f.close()
print 'End time: ',time.strftime('%X %x %Z')










