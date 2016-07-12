# coding=utf-8
import csv
from contextlib import closing
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from BeautifulSoup import BeautifulSoup
import time
from selenium import webdriver

print 'Start time: ',time.strftime('%X %x %Z')
stores = [] #for not repeating the ones that are written through the script run

with open('Existing.txt', 'r') as ExistingLocs:
    ExistingLocations = [line.strip() for line in ExistingLocs]#for stores already existing through previous run
    ExistingLocs.close()

with open('zip.txt', 'r') as zipfile:
    USZips = [line.strip() for line in zipfile]
    zipfile.close()

with open('StarbucksLocations_5.csv', 'wb') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow(['StoreName', 'Address', 'City', 'State','Zip'])
    print 'Headings Written'# column headings
    for zip in USZips:
        time.sleep(25)
        print 'Last Zip Processed: ',zip
        url = 'http://www.starbucks.com/store-locator/search/location/' + zip
        driver = webdriver.PhantomJS()
        browser = driver.get(url)
        # wait for the page to load
        # store it to string variable
        page_source = driver.page_source
        soup = BeautifulSoup(page_source)

        for link in soup.find(id="searchResults"):
            line = str(link)
            line = line.split('>')
            '''Parse Results'''
            # Storename
            storename = line[2]
            storename = storename.replace('</h2', "")
            storename = storename.replace('&amp;', "&")
            if storename not in ExistingLocations and storename not in stores:
                    print 'Writing Location'
                    stores.append(storename)
                    #Address
                    Address = line[5]
                    Address = Address.replace('</li',"")
                    #City,State,Zip
                    City = line[9]
                    City = City.replace('</li',"")
                    City = str(City)
                    FCity = City.split(',')
                    City = FCity[0]
                    StateZip= (FCity[1])
                    StateZip = StateZip.replace('&nbsp;',",")
                    StateZip = StateZip.split(',')
                    State = StateZip[1]
                    Zip = StateZip[2]
                    #print storename,City,StateZip
                    writer.writerow([storename, Address,City, State,Zip])
                    file.flush()
                    #sys.exit()
                    #except:
                    #   sys.exit()
file.close()
print 'End time: ',time.strftime('%X %x %Z')






