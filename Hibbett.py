'''-------------------------------------------------------------------------
Name:        Hibbett's Locations Scraper
Description: The Script scrapes all Hibbett locations from
             the website- all links listed by state
             State Links are pulled into a text file
             Addresses are then scraped from each state
             Does not have auto-updating capability yet
Date:        12/12/2017
Author:      pverma
-------------------------------------------------------------------------'''
from selenium import webdriver
import time
import csv
import pandas

_storesCurrentRun = pandas.read_csv('HibbettsStores.csv',header=0) #Read all stores from previous run into dataframe
collectedAddress = _storesCurrentRun['Address'].tolist() #Addresses from df for comparison

with open('HibbettStores.csv', 'ab') as file:
    scrapedLocations = [] # Avoid duplicate addresses
    writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Address', 'City', 'State', 'Zipcode'])
    # driver = webdriver.PhantomJS(executable_path='C:/Users/u760979/Desktop/Python/Executables/phantomjs.exe')
    driver = webdriver.Firefox(executable_path='C:/Users/u760979/Desktop/Python/Executables/geckodriver.exe')
    url = 'https://www.hibbett.com/storedirectory' #url for map
    driver.get(url) #retrieve url
    time.sleep(5)

    '''---Get links from the state page---'''
    StatelinksFile = open('StatelinksFile.txt', 'w')
    linksList= driver.find_elements_by_xpath('//*[@id="primary"]/ul/li[*]/a') #Links
    for l in linksList: #Get all
        link = l.get_attribute('href')
        print link
        StatelinksFile.write("%s\n" % link) #Write links to file
    StatelinksFile.close()
    time.sleep(20)
    '''---Get links from the City page---'''
    stateLinkList = open("StatelinksFile.txt").readlines()  # Reads all links into a list
    CitylinksFile = open('CitylinksFile.txt', 'w')
    for sLink in stateLinkList:
        citydriver = webdriver.Firefox(executable_path='C:/Users/u760979/Desktop/Python/Executables/geckodriver.exe')
        citydriver.get(sLink)  # retrieve url
        time.sleep(5)
        linksList = citydriver.find_elements_by_xpath('//*[@id="primary"]/ul/li[*]/a')  # Link Element
        for l in linksList:  # Get all
            link = l.get_attribute('href')
            print link
            CitylinksFile.write("%s\n" % link)  # Write links to file
        citydriver.quit()
    CitylinksFile.close()

    '''---Get locations from links---'''
    storeLinkList = open("Citylinks3.txt").readlines() #Reads all links into a list
    for link in storeLinkList:
        try:
            storeDriver = webdriver.Firefox(executable_path='C:/Users/u760979/Desktop/Python/Executables/geckodriver.exe')
            # storeDriver = webdriver.PhantomJS(executable_path='C:/Users/u760979/Desktop/Python/Executables/phantomjs.exe')
            storeDriver.get(link) # retrieve url
            time.sleep(15)
            Location = storeDriver.find_elements_by_class_name('name')
            fullAddress = storeDriver.find_elements_by_class_name('address') #get all info
            #Process addresses
            if len(fullAddress) > 1:
                for l,a in zip(Location,fullAddress):
                    location = l.text
                    a = a.text
                    Address = a.split('\n')[0]
                    cityStateZip = a.split('\n')[1]
                    City = cityStateZip.split(',')[0]
                    stateZip = cityStateZip.split(',')[1]
                    State = stateZip[-8:-6]
                    Zipcode = stateZip[-5:]
                    if Address not in scrapedLocations: #Check if Location was pulled
                        scrapedLocations.append(Address)
                        writer.writerow([location,Address,City,State,Zipcode]) #write to file
                        print location,Address,City,State,Zipcode
                        file.flush()
                storeDriver.quit()
                time.sleep(15)
            else:
                storeDriver.quit()
                time.sleep(15)
                continue
        except BaseException as e:
            print str(e)
            storeDriver.quit()
            print "Error in: ", link
            continue
