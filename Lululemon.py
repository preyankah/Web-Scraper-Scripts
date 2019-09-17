'''-------------------------------------------------------------------------
Name:        Athleta's Locations Scraper
Description: The Script scrapes all Athleta locations from
             the website- all links listed on one webpage
Date:        12/11/2017
Author:      pverma
-------------------------------------------------------------------------'''
from selenium import webdriver
import time
import csv
import sys

with open('LululemonStores.csv', 'ab') as file:
    scrapedLocations = []  # Avoid duplicate addresses
    storeLinkList = []
    newStoreList = []
    writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Address', 'City', 'State', 'Zipcode'])
    driver = webdriver.PhantomJS(executable_path='C:/Users/u760979/Desktop/Python/Executables/phantomjs.exe') #headless browser
    # driver = webdriver.Firefox(executable_path='C:/Users/u760979/Desktop/Python/Executables/geckodriver.exe')
    url = 'https://info.lululemon.com/shopLocation' #url for map
    driver.get(url) #retrieve url
    time.sleep(5)
    storeLinks = driver.find_elements_by_class_name('store-link')

    storeLinkList = open("linksFile.txt").readlines()
    print storeLinkList
    linksFile = open('linksFile.txt', 'a')
    for link in storeLinks:
            link = link.get_attribute("href")
            if (link+'\n') not in storeLinkList and '/us/' in link:
                print link
                newStoreList.append(link)
                linksFile.write("%s\n" % link)
    driver.quit()
    linksFile.close()

    for link in newStoreList:
        try:
            storeDriver = webdriver.PhantomJS(executable_path='C:/Users/u760979/Desktop/Python/Executables/phantomjs.exe')
            storeDriver.get(link)  # retrieve url
            time.sleep(15)
            fullAddress = storeDriver.find_element_by_class_name('address').text #get addresses
            if fullAddress != '':
                lenAdd = fullAddress.split('\n') #If suite exists
                if len(lenAdd) > 2:
                    Address = fullAddress.split('\n')[0]
                    CityState = fullAddress.split('\n')[2]
                    City = CityState.split(',')[0]
                    State = CityState.split(',')[1]
                else:
                    Address = fullAddress.split('\n')[0]
                    CityState = fullAddress.split('\n')[1]
                    City = CityState.split(',')[0]
                    State = CityState.split(',')[1]
                if Address not in scrapedLocations: #Check if Location was pulled
                    scrapedLocations.append(Address)
                    writer.writerow([Address,City,State]) #write to file
                    print Address,City,State
                    file.flush()
            storeDriver.quit()
            time.sleep(15)
        except:
            print "Unexpected error:", sys.exc_info()[0],link
            storeDriver.quit()
            continue