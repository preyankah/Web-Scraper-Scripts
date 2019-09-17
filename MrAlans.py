'''-------------------------------------------------------------------------
Name:        Mr Alan's Locations Scraper
Description: The Script scrapes all Mr Alan's locations from
             the website- all locations listed on one webpage
Date:        12/11/2017
Author:      pverma
-------------------------------------------------------------------------'''
from selenium import webdriver
import time
import csv
import sys

with open('MrAlansStores.csv', 'wb') as file:
    scrapedLocations = []  # Avoid duplicate addresses
    writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Address', 'City', 'State', 'Zipcode'])
    try:
        #driver = webdriver.PhantomJS(executable_path='C:/Users/u760979/Desktop/Python/Executables/phantomjs.exe')
        driver = webdriver.Firefox(executable_path='C:/Users/u760979/Desktop/Python/Executables/geckodriver.exe')
        url = 'https://www.mralans.com/pages/mr-alans-locations-new' #url for map
        driver.get(url) #retrieve url
        time.sleep(15)

        Address = driver.find_elements_by_xpath('//*[@id="content_wrapper"]/div[2]/div/div/div[*]/div[*]/p') #get addresses

        for a in Address:
            a = a.text
            location = a.split('\n')[0]
            address = a.split('\n')[1]
            cityStateZip = a.split('\n')[2]
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
        driver.quit()
    except: #Error handling
        print "Unexpected error:", sys.exc_info()[0]
        driver.quit()
        pass