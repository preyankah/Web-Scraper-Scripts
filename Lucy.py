'''----------------------------------------------------------------------------------------------------------------
Name:        Lucy Locations Scraper
Description: The Script scrapes all Lucy Retail & Outlet locations from the website.
             Store Locations are retrieved by searching on the page by state
             Stores returned from the previous run of the code(LucyStores.csv) are stored in a dataframe:
             - Stores that have been collected previously & are still on the webpage are left in the df
             - New locations (locations not in df) are geocoded using Mapbox API and append to the df
             - Stores that are in the df but not on the webpage anymore are removed from the df at the end
               of the run and appended to LucyStores_Old.csv
Date:        01/23/2018
Author:      pverma
----------------------------------------------------------------------------------------------------------------'''
from selenium import webdriver
import time
import mapbox
import pandas

_storesCurrentRun = pandas.read_csv('LucyStores.csv',header=0) #Read all stores from previous run into dataframe
collectedAddress = _storesCurrentRun['Address'].tolist() #Addresses from df for comparison

geocoder = mapbox.Geocoder( #Mapbox Geocoder Access Key
        access_token='pk.eyJ1IjoiZm9vdGxvY2tlciIsImEiOiJjamMyZ2xuNjUwbnBsMzNwZjcwazBvbXMwIn0.IbEIR3WCP2MPN1Av7gUaKg')

#Store file from previous run under _Old
_storesCurrentRun.to_csv('LucyStores_Old.csv',index = False)

States = open("StateNames.txt").readlines() #list of states from txt file

scrapedLocations = []  # Addresses collected in this run / To avoid duplicate addresses
for state in States:
    searchInput = state
    # print searchInput
    try:
        driver = webdriver.PhantomJS(executable_path='phantomjs.exe') #headless browser
        # driver = webdriver.Firefox(executable_path='geckodriver.exe')
        url = 'http://hosted.where2getit.com/lucy/index-2015.html?redirection=no' #url for map & search results iframe
        driver.get(url) #retrieve url
        time.sleep(10)

        searchBox = driver.find_element_by_id('search_address')
        searchBox.clear() #clear default text
        searchBox.send_keys(searchInput) #search for state
        distance = driver.find_element_by_xpath('/html/body/div[1]/form[2]/''section/section[1]/div/div/'
                                                'div/div[4]/select/option[8]').click() #Within 200 Miles
        driver.find_element_by_xpath('/html/body/div[1]/form[2]/section/section[1]/div/div/div/div[5]/input').click() #Search
        time.sleep(7)

        driver.find_element_by_xpath('//*[@id="offlab"]').click() #return retail stores
        driver.find_element_by_xpath('//*[@id="outlab"]').click()#return outlet stores
        time.sleep(3)
        addresses= driver.find_elements_by_class_name('address-content') #get addresses
        for a in addresses:
            a = a.text
            if a != '':
                address = a.split('\n')[0]
                cityStateZip = a.split('\n')[1]
                city = cityStateZip.split(',')[0]
                stateZip = cityStateZip.split(',')[1]
                state = stateZip[-8:-6]
                zipcode = stateZip[-5:]
                fullAddress = "%s %s %s %s" % (address, city, state, zipcode)
                # print fullAddress
                # Pulls new locations + validates that they have not been pulled before in this run
                if address not in collectedAddress and address not in scrapedLocations:
                    # print "--New Location"
                    scrapedLocations.append(address)
                    response = geocoder.forward(fullAddress) # Pass address through geocoder
                    if response.status_code == 200:  # If geocoding is successful get geo-coordinates
                        jsonResponse = response.json()
                        Results = jsonResponse['features']
                        # Extract lat lon from json response
                        lat = Results[0]['geometry']['coordinates'][1]
                        long = Results[0]['geometry']['coordinates'][0]
                        # Append new store to existing df
                        _storesCurrentRun.loc[len(_storesCurrentRun)] = [address, city, state, zipcode, lat, long]
                # Any previously collected stores that are still open
                elif address in collectedAddress and address not in scrapedLocations:
                    scrapedLocations.append(address) #Append to list with stores collected in this run
                    # print "--Store Exists in df"
    except BaseException as e:
        #when no stores are returned in state
        driver.quit()
        continue
    time.sleep(60) #search every 1 minute

closedStores = pandas.DataFrame(columns=_storesCurrentRun.columns) #New df for closed stores
#Collect closed stores
for address in collectedAddress:
    if address not in scrapedLocations:
        cur_df =_storesCurrentRun[_storesCurrentRun.Address == address] #Closed Store
        frames = [closedStores,cur_df]
        closedStores = pandas.concat(frames) #Add to df with closed stores
        _storesCurrentRun = _storesCurrentRun[_storesCurrentRun.Address != address] #Remove from _storePreviousRun
_storesCurrentRun.to_csv('LucyStores.csv',index = False)
closedStores.to_csv('LucyStores_Closed.csv',mode = 'a',index = False)

# print _storesCurrentRun
# print closedStores
