'''-------------------------------------------------------------------------
Name:        Lorna Jane's Locations Scraper
Description: The Script scrapes all Lorna Jane locations from
             the website- all store links listed on one webpage
             Does not have updating capability yet
Date:        12/11/2017
Author:      pverma
-------------------------------------------------------------------------'''
from selenium import webdriver
import time
import csv

scrapedLocations = []  # Avoid duplicate addresses

with open('LornaJaneStores.csv', 'ab') as file:
    writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Address', 'City', 'State', 'Zipcode'])
    driver = webdriver.PhantomJS(executable_path='C:/Users/u760979/Desktop/Python/Executables/phantomjs.exe')
    # driver = webdriver.Firefox(executable_path='C:/Users/u760979/Desktop/Python/Executables/geckodriver.exe')
    url = 'https://www.lornajane.com/store-finder' #url for map
    driver.get(url) #retrieve url
    time.sleep(5)

    '''---Get store links from the state page---'''
    linksFile = open('linksFile.txt', 'w')
    storeLinks = driver.find_elements_by_xpath('//*[@id="storeList"]/div[1]/div[*]/div[2]/ul/li[*]/a') #Store links
    for link in storeLinks:
        link = link.get_attribute("href")
        linksFile.write("%s\n" % link) #write link to file
    driver.quit()
    linksFile.close()

    '''---Get address from links---'''
    storeLinkList = open("linksFile.txt").readlines()
    for link in storeLinkList:
        storeDriver = webdriver.PhantomJS(executable_path='C:/Users/u760979/Desktop/Python/Executables/phantomjs.exe')
        storeDriver.get(link) #retrieve url
        time.sleep(15)
        #Process address
        fullAddress = storeDriver.find_element_by_xpath('/html/body/main/section[3]/div/div/div[1]/div[3]/'
                                                        'div/div[1]/div[1]/div[2]').text #get addresses
        AddLen = fullAddress.split('\n')
        if len(AddLen) > 4: #If mall/location is listed in address
            location = fullAddress.split('\n')[0]
            Address = fullAddress.split('\n')[1]
            City = fullAddress.split('\n')[2]
            Zip = fullAddress.split('\n')[3]
        else: #If address is listed
            location = ''
            Address = fullAddress.split('\n')[0]
            City = fullAddress.split('\n')[1]
            Zip = fullAddress.split('\n')[2]
        if Address not in scrapedLocations: #Check if Location was pulled
            scrapedLocations.append(Address)
            writer.writerow([location,Address,City,Zip]) #write to file
            print location,Address,City,Zip
            file.flush()
        storeDriver.quit()
        time.sleep(15)
