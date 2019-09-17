'''-------------------------------------------------------------------------
Name:        Lids's Locations Scraper
Description: The Script scrapes all Lids locations from
             the website- all links listed by state
             State Links are pulled into a text file
             Addresses are then scraped from each state
             Does not have auto-updating capability yet
Date:        12/12/2017
Author:      pverma
-------------------------------------------------------------------------'''
from selenium import webdriver
import time
import csv

with open('LidsStores.csv', 'wb') as file:
    scrapedLocations = [] # Avoid duplicate addresses
    writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Address', 'City', 'State', 'Zipcode'])
    driver = webdriver.PhantomJS(executable_path='C:/Users/u760979/Desktop/Python/Executables/phantomjs.exe')
    url = 'https://www.lids.com/stores/states' #url for map
    driver.get(url) #retrieve url
    time.sleep(5)

    '''---Get links from the state page---'''
    linksFile = open('linksFile.txt', 'w')
    storeLinks = driver.find_element_by_id('listOfStatesHavingStores') #Link Element
    linksList= storeLinks.find_elements_by_css_selector('a') #Links
    for l in linksList: #Get all
        link = l.get_attribute('href')
        linksFile.write("%s\n" % link) #Write links to file
    driver.quit()
    linksFile.close()

    '''---Get locations from links---'''
    storeLinkList = open("linksFile.txt").readlines() #Reads all links into a list
    for link in storeLinkList:
        storeDriver = webdriver.PhantomJS(executable_path='C:/Users/u760979/Desktop/Python/Executables/phantomjs.exe')
        storeDriver.get(link)  # retrieve url
        time.sleep(15)
        fullAddress = storeDriver.find_elements_by_class_name('store-finder-navigation-list-entry-info') #get all info
        #Process addresses
        for Add in fullAddress:
            Add = Add.text
            if Add != '':
                Location = Add.split('\n')[0]
                Address = Add.split('\n')[1]
                cityStateZip = Add.split('\n')[2]
                City = cityStateZip.split(',')[0]
                stateZip = cityStateZip.split(',')[1]
                State = stateZip[-8:-6]
                Zipcode = stateZip[-5:]
                if Address not in scrapedLocations: #Check if Location was pulled
                    scrapedLocations.append(Address)
                    writer.writerow([Location,Address,City,State,Zipcode]) #write to file
                    print Location,Address,City,State,Zipcode
                    file.flush()
        storeDriver.quit()
        time.sleep(15)
