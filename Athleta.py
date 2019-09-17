'''-------------------------------------------------------------------------
Name:        Athleta's Locations Scraper
Description: The Script scrapes all Athleta locations from
             the website- All City links are listed under each state
             The links to each city/store is scraped and processed
             Does not have auto-updating capability yet
Date:        12/11/2017
Author:      pverma
-------------------------------------------------------------------------'''
from selenium import webdriver
import time
import csv

with open('AthletaStores.csv', 'ab') as file:
    scrapedLocations = []  # Avoid duplicate addresses
    storeLinkList = []
    writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Address', 'City', 'State', 'Zipcode'])
    driver = webdriver.PhantomJS(executable_path='C:/Users/u760979/Desktop/Python/Executables/phantomjs.exe') #headless browser
    # driver = webdriver.Firefox(executable_path='C:/Users/u760979/Desktop/Python/Executables/geckodriver.exe')
    url = 'http://stores.athleta.net/' #url for map
    driver.get(url) #retrieve url
    time.sleep(5)

    '''---Get links from the state page---'''
    linksFile = open('linksFile.txt', 'w')
    storeLinks = driver.find_elements_by_xpath('/html/body/div[1]/div[4]/div[2]/div/div/div[*]/div[*]/a')
    for link in storeLinks:
        link = link.get_attribute("href")
        linksFile.write("%s\n" % link)
    driver.quit()
    linksFile.close()
    storeLinkList = open("linksFile.txt").readlines()

    '''---Get Address from links---'''
    for link in storeLinkList:
        storeDriver = webdriver.PhantomJS(executable_path='C:/Users/u760979/Desktop/Python/Executables/phantomjs.exe')
        storeDriver.get(link)  # retrieve url
        time.sleep(15)
        Address = storeDriver.find_element_by_xpath('//*[@id="widget_Athleta_Stores_Details_div"]/div[1]/address/span[1]').text #get addresses
        City = storeDriver.find_element_by_xpath('//*[@id="widget_Athleta_Stores_Details_div"]/div[1]/address/span[2]').text
        State = storeDriver.find_element_by_xpath('//*[@id="widget_Athleta_Stores_Details_div"]/div[1]/address/span[3]').text
        Zipcode = storeDriver.find_element_by_xpath('//*[@id="widget_Athleta_Stores_Details_div"]/div[1]/address/span[4]').text
        if Address != '':
            Address = Address.split('\n')[0]
            if Address not in scrapedLocations: #Check if Location was pulled
                scrapedLocations.append(Address)
                writer.writerow([Address,City,State,Zipcode]) #write to file
                print Address,City,State,Zipcode
                file.flush()
        storeDriver.quit()
        time.sleep(15)