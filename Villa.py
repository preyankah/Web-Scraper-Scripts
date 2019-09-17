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

with open('VillaStores2.csv', 'ab') as file:
    scrapedLocations = []  # Avoid duplicate addresses
    writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['location','Address', 'City', 'State', 'Zipcode'])
    # driver = webdriver.PhantomJS(executable_path='C:/Users/u760979/Desktop/Python/Executables/phantomjs.exe') #headless browser
    driver = webdriver.Firefox(executable_path='C:/Users/u760979/Desktop/Python/Executables/geckodriver.exe')
    url = 'https://www.ruvilla.com/storelocator/' #url for map
    driver.get(url) #retrieve url
    time.sleep(60)

    Address = driver.find_elements_by_tag_name('address') #get all store info

    for a in Address:
        try:
            a = a.text
            location = a.split('\n')[0]
            address = a.split('\n')[1]
            cityStateZip = a.split('\n')[2]
            city = cityStateZip.split(',')[0]
            state = cityStateZip.split(',')[1]
            zipcode = cityStateZip[-5:]
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