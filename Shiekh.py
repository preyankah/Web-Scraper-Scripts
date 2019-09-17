'''-------------------------------------------------------------------------
Name:        Shiekh's Locations Scraper
Description: The Script scrapes all Shiekh locations from
             the website- all links listed on one webpage
             For
Date:        12/11/2017
Author:      pverma
-------------------------------------------------------------------------'''
from selenium import webdriver
import time
import csv
import sys

with open('ShiekhStores.csv', 'ab') as file:
    scrapedLocations = []  # Avoid duplicate addresses
    storeLinkList = []
    newStores  = []
    writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Address', 'City', 'State', 'Zipcode'])
    storeLinkList = open("linksFile.txt").readlines()
    # driver = webdriver.PhantomJS(executable_path='C:/Users/u760979/Desktop/Python/Executables/phantomjs.exe')
    driver = webdriver.Firefox(executable_path='C:/Users/u760979/Desktop/Python/Executables/geckodriver.exe')
    url = 'https://www.shiekh.com/store-list' #url for map
    driver.get(url) #retrieve url
    time.sleep(5)
    storeLinks = driver.find_elements_by_class_name('brand-item-link')
    linksFile = open('linksFile.txt', 'a')
    for link in storeLinks:
            link = link.get_attribute("href")
            if (link + '\n') not in storeLinkList:
                print link
                newStores.append(link)
                linksFile.write("%s\n" % link)
    driver.quit()


    for link in newStores:
        try:
            storeDriver = webdriver.Firefox(executable_path='C:/Users/u760979/Desktop/Python/Executables/geckodriver.exe')
            storeDriver.get(link)  # retrieve url
            time.sleep(10)
            Address = storeDriver.find_element_by_xpath('//*[@id="maincontent"]/div[2]/div/div/div[4]/div[1]/div/p[1]/span/span[1]').text #get addresses
            CityState = storeDriver.find_element_by_xpath('//*[@id="maincontent"]/div[2]/div/div/div[4]/div[1]/div/p[1]/span/span[2]').text
            if Address != '':
                City = CityState.split(',')[0]
                State = CityState.split(',')[1]
                if Address not in scrapedLocations: #Check if Location was pulled
                    scrapedLocations.append(Address)
                    writer.writerow([Address,City,State]) #write to file
                    print Address,City,State
                    file.flush()
            storeDriver.quit()
            time.sleep(10)
        except:  # Error handling
            print "Unexpected error:", sys.exc_info()[0],link
            storeDriver.quit()
            continue