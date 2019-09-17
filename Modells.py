'''-------------------------------------------------------------------------
Name:        Modell's Locations Scraper
Description: The Script scrapes all Modell's locations from
             the website- all locations listed on one webpage
Date:        12/08/2017
Author:      pverma
-------------------------------------------------------------------------'''
from selenium import webdriver
import time
import csv
import sys

with open('ModellsStores_.csv', 'wb') as file:
    scrapedLocations = []  # Avoid duplicate addresses
    writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Address', 'City', 'State', 'Zipcode'])
    try:
        driver = webdriver.PhantomJS(executable_path='C:/Users/u760979/Desktop/Python/Executables/phantomjs.exe') #headless browser
        # driver = webdriver.Firefox(executable_path='C:/Users/u760979/Desktop/Python/Executables/geckodriver.exe')
        url = 'https://www.modells.com/store-locator/all-stores.do' #url for map
        driver.get(url) #retrieve url
        time.sleep(15)

        address= driver.find_elements_by_class_name('eslAddress1') #get addresses
        city = driver.find_elements_by_class_name('eslCity') #get city
        state = driver.find_elements_by_class_name('eslStateCode') #get state
        zipcode = driver.find_elements_by_class_name('eslPostalCode') #get zip

        for a,c,s,z in zip(address,city,state,zipcode):
            a = a.text
            c = c.text
            s = s.text
            z = z.text
            if a != '':
                if a not in scrapedLocations: #Check if Location was pulled
                    scrapedLocations.append(a)
                    writer.writerow([a,c,s,z]) #write to file
                    print a,c,s,z
                    file.flush()
        driver.quit()
    except: #Error handling
        print "Unexpected error:", sys.exc_info()[0]
        driver.quit()
        pass