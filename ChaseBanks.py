#-------------------------------------------------------------------------------
# Name:        Chase Bank Locations
# Purpose:     Pulls locations of all chase banks in New York,NY
#              Writes output to a csv file
# Date:        07/08/2016
# Approx Run:  1 Min
# Author:      pverma
#-------------------------------------------------------------------------------

from BeautifulSoup import BeautifulSoup
import urllib2
import csv
import re
import time

print 'Start time: ',time.strftime('%X %x %Z')
Store = [] #to avoid duplicates
checkManhattan = [] #len returns number of stores picked up in manhattan
with open('ChaseManhattanLocations.csv', 'ab') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow(['StoreName', 'Address', 'City', 'State', 'Zip'])  # column headings
    #loops through 70 result pages. 5 branches listed on each page
    for page in range(70):
        try:
            buildurl = 'https://locator.chase.com/search/ny/manhattan?t=&q=Manhattan%2C+NY&page=' + str(
                page)+ '&filters=locationTypeFilter-_-locationType.branch'
            html_page = urllib2.urlopen(buildurl)

            soup = BeautifulSoup(html_page)

            for i in range(5):
                #to pick up each listing(5 in total on each page)
                curID = 'listing_' + str(i)
                soup2 = soup.find(id=curID)
                text = soup2.getText()
                if 'New York'in text:
                    checkManhattan.append(text)
                    #print len(checkManhattan)
                    tel = text.index('-')
                    fulladdress = text[tel + 9:]#parse address,city,state
                    storename = text[:tel - 3]#parse store name and remove phone num
                    address = re.sub('Driving directionsServices and Hours$', '', fulladdress)#remove additional stuff
                    address = re.sub('New York', ' ,New York,', address)#Add a space between address and city
                    address = re.sub(' NY ', ' ,NY,,', address) #to parse state
                    address = address.split(',')
                    #print address
                    if storename not in Store:
                        print storename
                        #write to csv
                        writer.writerow([storename, address[0], address[1], address[4], address[6]])
                    else:
                        print 'Skipped duplicate'
                        continue
                else:
                    #not in New York,NY will be skipped
                    print 'skip--',text
        except:
            continue
    file.close()

print 'End time: ',time.strftime('%X %x %Z')
