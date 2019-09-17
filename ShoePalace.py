'''-------------------------------------------------------------------------
Name:        Shoe Palace's Locations Scraper
Description: The Script scrapes all Shoe Palace locations from
             the website- all locations listed on one webpage +
             Show more results
Date:        12/11/2017
Author:      pverma
-------------------------------------------------------------------------'''
from selenium import webdriver
import time
import csv

with open('ShoePalaceStores.csv', 'wb') as file:
    scrapedLocations = []  # Avoid duplicate addresses
    writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Address', 'City', 'State', 'Zipcode'])

    #driver = webdriver.PhantomJS(executable_path='C:/Users/u760979/Desktop/Python/Executables/phantomjs.exe')
    driver = webdriver.Firefox(executable_path='C:/Users/u760979/Desktop/Python/Executables/geckodriver.exe')
    url = 'http://www.shoepalace.com/index.php/find-store' #url for map
    driver.get(url) #retrieve url
    time.sleep(15)
    # driver.find_element_by_xpath('//*[@id="map"]/area[6]').click()
    # time.sleep(15)
    try:
        for i in range(4, 50, 3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            moreResults = '//*[@id="more%s"]' % (i,)
            print moreResults
            time.sleep(15)
            addXpath = '//*[@id="country%s"]/div[*]/div[1]/div[2]' % (i,)
            cityXpath = '//*[@id="country%s"]/div[*]/div[1]/div[3]' % (i,)
            Address = driver.find_elements_by_xpath(addXpath)  # get addresses
            CityStateZip = driver.find_elements_by_xpath(cityXpath)
            for a, c in zip(Address, CityStateZip):
                address = a.text
                c = c.text
                print address, c
                city = c.split(',')[0]
                stateZip = c.split(',')[1]
                state = stateZip[-8:-6]
                zipcode = stateZip[-5:]
                if address != '':
                    writer.writerow([address, city, state, zipcode])  # write to file
                    print address, city, state, zipcode
                    file.flush()

            driver.find_element_by_xpath(moreResults).click()
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    except:
        pass
