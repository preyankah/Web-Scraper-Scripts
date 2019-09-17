'''-------------------------------------------------------------------------
Name:        DTLR's Locations Scraper
Description: The Script scrapes all DTLR locations from
             the website- addresses listed under each state dropdown
             State Links are pulled into a text file
             Addresses are then scraped from each state
             Does not have updating capability yet
Date:        12/12/2017
Author:      pverma
-------------------------------------------------------------------------'''
from selenium import webdriver
import time
import csv

with open('PacSunStores.csv', 'wb') as file:
    scrapedLocations = []  # Avoid duplicate addresses
    storeLinkList = []
    writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Address', 'City', 'State', 'Zipcode'])
    # driver = webdriver.PhantomJS(executable_path='C:/Users/u760979/Desktop/Python/Executables/phantomjs.exe') #headless browser
    driver = webdriver.Firefox(executable_path='C:/Users/u760979/Desktop/Python/Executables/geckodriver.exe')
    storeLinkList = open("linksFile.txt").readlines()
    for link in storeLinkList:
        storeDriver = webdriver.Firefox(executable_path='C:/Users/u760979/Desktop/Python/Executables/geckodriver.exe')
        # storeDriver = webdriver.PhantomJS(executable_path='C:/Users/u760979/Desktop/Python/Executables/phantomjs.exe')
        storeDriver.get(link)
        '''---Get locations from links---'''
        Location = driver.find_elements_by_class_name('h2')
        fullAddress = driver.find_elements_by_class_name('addressPhoneInfo') #get addresses
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
                    writer.writerow([Address,City,State,Zipcode]) #write to file
                    print Address,City,State,Zipcode
                    file.flush()
        time.sleep(15)
