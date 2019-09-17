'''-------------------------------------------------------------------------
Name:        Finish line's Locations Scraper
Description: The Script scrapes all Finish line locations from
             the website- all links listed by state
             State Links are pulled into a text file
             Addresses are then scraped from each state
             Does not have auto-updating capability yet
Date:        01/11/2018
Author:      pverma
-------------------------------------------------------------------------'''

from selenium import webdriver
import time
import pandas as pd
from collections import defaultdict

_storesCurrentRun = pd.read_csv('FinishLineStores.csv',header=0) #Read all stores from previous run into dataframe
collectedStates = _storesCurrentRun['State'].tolist() #Store count for each state to compare to count on website
collectedAddresses = _storesCurrentRun['Address'].tolist() #Addresses from df for comparison
closedStores = pd.DataFrame(columns=_storesCurrentRun.columns) #New df for closed stores

# Dictionary of count by state
stateCount = defaultdict(int)
for state in collectedStates:
    stateCount[state] += 1
stateCount.pop('Zipcode')
print stateCount

driver = webdriver.Firefox(executable_path='C:/Users/u760979/Desktop/Python/Executables/geckodriver.exe')
url = 'https://stores.finishline.com/' #url for map
driver.get(url) #retrieve url
time.sleep(10)
state = driver.find_elements_by_class_name('c-directory-list-content-item-link')
stateCurCount = driver.find_elements_by_class_name('c-directory-list-content-item-count')

for s, c in zip(state, stateCurCount): #for each state on webpage
    stateAbbr = s.get_attribute('href')
    stateAbbr = stateAbbr.replace('https://stores.finishline.com/', "")
    stateAbbr = stateAbbr.replace('.html', "")
    stateAbbr = stateAbbr.upper() #state name
    if '/' in stateAbbr:
        stateAbbr = stateAbbr[:2]
    c = c.text
    c = c.replace('(', '')
    c = c.replace(')', '')
    c = int(c) #state count
    compare = stateCount[stateAbbr] # find count for state in existing locations
    if c == compare:  # no change in store counts
        print stateAbbr, "--No Change"
    else: #If the count is different from previous stores

        if compare < c:  # if new stores have been added in state
            citydriver = webdriver.Firefox(executable_path='C:/Users/u760979/Desktop/Python/Executables/geckodriver.exe')
            _citiesURL = s.get_attribute('href')
            citydriver.get(_citiesURL)

            #Count of stores by city from previous run
            if _citiesURL.count('/') == 3:
                df = list(_storesCurrentRun.loc[_storesCurrentRun.State == stateAbbr, 'City'])
                df = [w.replace(',', '') for w in df]
                df = [w.replace("'", '') for w in df]
                cityCount = defaultdict(int)
                for city in df:
                    cityCount[city] += 1
                #Check the count on webpage
                _City = citydriver.find_elements_by_class_name('c-directory-list-content-item-link')
                _CityCurCount = citydriver.find_elements_by_class_name('c-directory-list-content-item-count')
                for _city, _cityCount in zip(_City, _CityCurCount):
                    __city = _city.text
                    _cityCount = _cityCount.text
                    _cityCount = _cityCount.replace('(', '')
                    _cityCount = _cityCount.replace(')', '')
                    cc = int(_cityCount)
                    compare = cityCount[__city]
                    # If  the city has no change in number of stores on webpage and previous run
                    if cc == compare:
                        continue

                    else: # If there was a change in the number of stores within cities
                        print "Change in ", __city
                        storeurl = _city.get_attribute('href')
                        storeDriver = webdriver.Firefox(executable_path='C:/Users/u760979/Desktop/Python/Executables/geckodriver.exe')
                        storeDriver.get(storeurl)  # retrieve url
                        time.sleep(10)

                        Brand = storeDriver.find_elements_by_class_name('location-name-brand')
                        Locations = storeDriver.find_elements_by_class_name('location-name-geo')  # get all info
                        Addresses = storeDriver.find_elements_by_class_name('c-address-street-1')  # get all info
                        Cities = storeDriver.find_elements_by_class_name('c-address-city')  # get all info
                        States = storeDriver.find_elements_by_class_name('c-address-state')
                        Zipcodes = storeDriver.find_elements_by_class_name('c-address-postal-code')
                        addr = [addr.text for addr in Addresses]

                        print len(Addresses)
                        if cc > compare:  # If collected stores are less than website
                            if len(Addresses) == 1: # If one new store in new city not previously collected
                                _brnd = Brand[0].text
                                _add = Addresses[0].text
                                _loc = Locations[0].text
                                _city_ = Cities[0].text
                                _state = States[0].text
                                _zip = Zipcodes[0].text
                                _storesCurrentRun.loc[len(_storesCurrentRun)] = [ _loc, _add, _city_, _state,
                                                                                 _zip]
                                print _brnd, _loc, _add, _city_, _state, _zip
                            else: # If new store added to previously collected city
                                print "Addr",Addresses
                                for a in Addresses:
                                    _add = str(a.text)
                                    if _add not in collectedAddresses:
                                        i = addr.index(_add)
                                        _brnd = str(Brand[i].text)
                                        _loc = str(Locations[i].text)
                                        _addr = str(Addresses[i].text)
                                        _city_ = str(Cities[i].text)
                                        _state = str(States[i].text)
                                        _zip = str(Zipcodes[i].text)
                                        print _brnd, _loc, _add, _city_, _state, _zip
                                        _storesCurrentRun.loc[len(_storesCurrentRun)] = [_loc, _add, _city_,_state, _zip]
                        else:  # cc < compare:
                            if _add in collectedAddresses:
                                cur_df = _storesCurrentRun[_storesCurrentRun.Address == _add]  # Closed Store
                                frames = [closedStores, cur_df]
                                closedStores = pd.concat(frames)  # Add to df with closed stores
                                print closedStores
                                _storesCurrentRun = _storesCurrentRun[_storesCurrentRun.Address != _add]  # Remove from _storePreviousRun
                    storeDriver.quit()
            citydriver.quit()

driver.quit()
_storesCurrentRun.to_csv('FinishLineStores_Auto.csv', index=False)
closedStores.to_csv('FinishLineStores_Closed.csv', mode='a', index=False)

