#----------------------------------------------------------------------------#
# Name:        Dunkin Donuts
# Author:      pverma
# Created:
# Copyright:   (c) pverma 2016
# Description:  Collects locations from STORES page.
#----------------------------------------------------------------------------#

from selenium import webdriver
import csv
import requests
import time

with open('ManhattanZipcodes.txt', 'r') as StoreLinks:
    StorePages = [line.strip() for line in StoreLinks]
    #print (len(StoreLinkList))
    StoreLinks.close()

with open('DunkinDonuts1.csv','a',newline='') as CollectionFile: #successful
    storeinsession = []
    with open('LogFile_all.txt','a') as logfile:#errors
        writer = csv.writer(CollectionFile, delimiter=',')
        for p in StorePages:
            driver = webdriver.Firefox()
            url = 'https://www.dunkindonuts.com/en/locations?input='+str(p)
            print (url)
            driver.get(url)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            Address = driver.find_elements_by_class_name('store-item__address--line1')
            City = driver.find_elements_by_class_name('store-item__address--line3')
            for a,c in zip(Address,City):
                try:
                    Address = a.text
                    City = c.text
                    City = str(City).replace('\n', ' ')
                    if Address not in storeinsession:
                        storeinsession.append(Address)
                        fullAddress = str(Address).replace('\n', ', ')
                        writer.writerow(['Dunkin Donuts',Address,City])
                        print(Address,City)

                except:
                    logfile.write(Address)
                    logfile.write('\n')
                    logfile.flush()
                    pass
            time.sleep(10)
            driver.quit()
            CollectionFile.flush()

        CollectionFile.close()
    logfile.close()