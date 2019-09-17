'''-------------------------------------------------------------------------
Name:        Dr Jay's Locations Scraper
Description: The Script scrapes all Dr Jay's locations from
             the website- all locations listed on one webpage
Date:        12/08/2017
Author:      pverma
-------------------------------------------------------------------------'''
from selenium import webdriver
import time
import csv
import sys

with open('DrJaysStores.csv', 'wb') as file:
    scrapedLocations = []  # Avoid duplicate addresses
    writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Address', 'City', 'State', 'Zipcode'])
    try:
        driver = webdriver.PhantomJS(executable_path='C:/Users/u760979/Desktop/Python/Executables/phantomjs.exe') #headless browser
        # driver = webdriver.Firefox(executable_path='C:/Users/u760979/Desktop/Python/Executables/geckodriver.exe')
        url = 'https://www.drjays.com/content/customerservice/walk-in-stores.html' #url for map
        driver.get(url) #retrieve url
        time.sleep(15)
        LocationType = driver.find_elements_by_xpath('//*[@id="content"]/div/div/div[3]/div[*]/div/div/table/tbody/tr[*]/td[1]') #get addresses
        Address = driver.find_elements_by_xpath('//*[@id="content"]/div/div/div[3]/div[*]/div/div/table/tbody/tr[*]/td[2]') #get city

        for l,a in zip(LocationType,Address):
            l = l.text
            a = a.text
            address = a.split('\n')[0]
            cityStateZip = a.split('\n')[1]
            city = cityStateZip.split(',')[0]
            stateZip = cityStateZip.split(',')[1]
            state = stateZip[-8:-6]
            zipcode = stateZip[-5:]
            if a != '':
                if a not in scrapedLocations: #Check if Location was pulled
                    scrapedLocations.append(a)
                    writer.writerow([l,address,city,state,zipcode]) #write to file
                    print l,address,city,state,zipcode
                    file.flush()
        driver.quit()
    except: #Error handling
        print "Unexpected error:", sys.exc_info()[0]
        driver.quit()
        pass