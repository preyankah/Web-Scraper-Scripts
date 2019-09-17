'''-------------------------------------------------------------------------
Name:        Dr City Gear's Locations Scraper
Description: The Script scrapes all City Gear's locations from
             the website- all locations listed on one webpage
             Error handling and auto-updating need to be added
Date:        12/08/2017
Author:      pverma
-------------------------------------------------------------------------'''
from selenium import webdriver
import time
import csv

with open('CityGearStores.csv', 'ab') as file:
    scrapedLocations = []  # Avoid duplicate addresses
    writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['location','Address', 'City', 'State', 'Zipcode'])
    driver = webdriver.PhantomJS(executable_path='C:/Users/u760979/Desktop/Python/Executables/phantomjs.exe') #headless browser
    # driver = webdriver.Firefox(executable_path='C:/Users/u760979/Desktop/Python/Executables/geckodriver.exe')
    url = 'https://www.citygear.com/store-locator/' #url for map
    driver.get(url) #retrieve url
    time.sleep(15)

    Address = driver.find_elements_by_class_name('aw-storelocator-description') #get all store info

    for a in Address:
        try:
            a = a.text
            print len(a.split('\n'))
            location = a.split('\n')[0]
            address = a.split('\n')[1]
            if len(a.split('\n')) == 9:
                cityStateZip = a.split('\n')[2]
            else:
                cityStateZip = a.split('\n')[3]
            city = cityStateZip.split(',')[0]
            stateZip = cityStateZip.split(',')[1]
            state = stateZip[-8:-6]
            zipcode = stateZip[-5:]
            if a != '':
                if a not in scrapedLocations: #Check if Location was pulled
                    scrapedLocations.append(a)
                    writer.writerow([location,address,city,state,zipcode]) #write to file
                    print location,address,city,state,zipcode
                    file.flush()
        except:
            continue
            print "Error: ",a

driver.quit()