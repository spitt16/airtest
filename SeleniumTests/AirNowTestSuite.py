# AirNow Drupal Python based Selenium tests
# Chris Wilkes
#
# v 1.0.0; Intial set up; Bringing sample tests over from IDE cw 2019-03-21
# v 2.0.0; Changes for AirNowDrupal 2.0.0 cw 2019-03-21
# v 2.1.0; Changes for AirNowDrupal 2.1.0; Added Version labels to output cw 2019-06-04
# v 2.2.0; Changes for AirNowDrupal 2.2.0 cw 2019-07-08
#          Added Version check against new Content Item for Version above 2.2.0 cw 2019-07-11
# V 2.2.1; Site URLs must now include Basic Authenication cw 2019-07-15
# V 2.3.0; Now verifing database version by Content Band Item called "AirNowDrupal Version" cw 2019-09-12
# V 2.5.0; Now verifing content version by Content Band Item called "AirNow Content Version" & "AirNow Code Version" cw 2020-01-28
# V 2.6.0; Getting close to re launch, manny updates cw 2020-04-03
# V 2.6.1; airnow.gov domain migration, Hard Launch on 04/15/20, Revised Correct path used by icons. cw 2020-04-17
# v 2.7.0; Ready for Air Quality Awareness Week; Final Content Version is 55 cw 2020-05-04
# V 2.8.0;
# V 3.0.0; Updated to run on Python 3.10.8 at command line; IDLE no longer needed! cw 2022-10-28

import os
import sys

import urllib.request
#import numpy
import time
import datetime
from selenium.common.exceptions import NoSuchElementException
import json
from selenium.webdriver.support.ui import Select
#from PIL import ImageChops
#from PIL import Image
#from PIL import ImageFile
# Supporting driver / browser waiting cw 2019-08-08
#    https://stackoverflow.com/questions/26566799/wait-until-page-is-loaded-with-selenium-webdriver-for-python#26567563
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

# supress warnings about xpath deprecation of older tests cw 2022-10-28
import warnings
warnings.filterwarnings("ignore")

#Set up colors
#try: color = sys.stdout.shell
#except AttributeError: raise RuntimeError("Use IDLE")
#Set up colors
### https://pypi.org/project/colorama/
from colorama import Fore
from colorama import Back
from colorama import Style
from colorama import init
init()
print(Fore.RED + 'some red text')
print(Back.GREEN + 'and with a green background')
print(Style.DIM + 'and in dim text')
print(Style.RESET_ALL)
print('back to normal now')
##
print(f'This is {Fore.GREEN}green{Style.RESET_ALL}')
print(f'This is {Fore.RED}red{Style.RESET_ALL}')
#
# set the server here... Site must be defined
#
contentVersion = '169'
codeVersion = '3.0.40'

# sample with variables
#print(f'{Fore.GREEN}{codeVersion}-{contentVersion}{Style.RESET_ALL}')
#print(' ')

# DEV Servers5
site0 = '   ... Development ...3'
site1 = 'http://preview:Welcome1@airnowgov.lndo.site/'
site2 = 'https://preview:Welcome1@dev-airnowgov.pantheonsite.io/'
site3 = 'https://preview:Welcome1@mytest.app.cloud.gov/'
site4 = 'https://preview:Welcome1@airnowdev.app.cloud.gov/'

# Staging  Servers
site5 = '   ... Staging / Test ...6'
site6 = 'https://preview:Welcome1@airnowstage.app.cloud.gov/'
site7 = 'https://preview:Welcome1@airnowgovmqyangevx7.devcloud.acquia-sites.com/'
site8 = 'https://airnowdev-green.app.cloud.gov/'

# Production Servers
site9 = '   ... Production ...11'
site10 = 'https://preview:Welcome1@airnowgovhsra53cw7w.devcloud.acquia-sites.com/'
site11 = 'https://www.airnow.gov/'
site12 = 'https://preview:Welcome1@airnow.app.cloud.gov/'
site13 = 'https://a6680c90-dbef-4ec2-8098-9feb5308c453.web.ahdev.cloud/'

# cloud.gov servers
site20 = '   ... cloud.gov ...33'
site21 = 'https://airnowstage.app.cloud.gov/'
site22 = 'https://airnow.app.cloud.gov/'
site23 = 'https://preview:Welcome1@spanishtest.app.cloud.gov/'
site24 = 'https://airnow-cdn.epa.gov/'
site25 = 'https://airnow.gov/'
site26 = '   ... Pantheon ...'
site27 = 'https://preview:Welcome1@dev-airnowgov.pantheonsite.io/'
site28 = 'https://preview:Welcome1@airnowspanish.app.cloud.gov/'
site29 = '   ...            ..'
site33 = 'https://www.airnow.gov/'
site40 = '-'
site41 = 'https://airnow-green.app.cloud.gov/'
site42 = 'https://airnow-blue.app.cloud.gov/'


# Fire & Smoke Map Test URLs
site49 = '-'
site50 = '   ... fire.airnow.gov ...55...66...77'
site51 = '-'
site54 = 'https://fire:smoke2021@maps.airfire.org/pilot/'
site55 = 'https://airfire:smokemaps@maps.airfire.org/airnowfire-staging/'
site65 = '-'
site66 = 'https://sensor:pilot@airnowfirestage.app.cloud.gov/'
site67 = 'https://airnowmobilefirestage.app.cloud.gov/'
site70 = '-'
site71 = 'https://airnowfire-green.app.cloud.gov/'
site72 = 'https://airnowfire-blue.app.cloud.gov/'
site73 = 'https://airnowmobilefire-green.app.cloud.gov/'
site74 = 'https://airnowmobilefire-blue.app.cloud.gov/'
site77 = 'https://fire.airnow.gov/'
site78 = 'https://mobilefire.airnow.gov/'
site79 = '-'
site80 = '   ... Spanish Translation ... 23 and 83...'
site82 = '-'
site83 = 'https://preview:Welcome1@spanishtestfire.app.cloud.gov/'

#
# User Feedback
print ('Here we go...')
print(' ')
### Continuous running loop
# Program will run in loop forever cw 2019-04-01
runAgain = 'True'
while (runAgain):
  print('AirNowDrupal Python-based Selenium Test Script.')
  print(' ')
  print('Site Number: URL ')
  # make site list
  site = site1
  i = 0
  while i < 105:
    # check if that site # exisits
    try:
      eval('site' + str(i)) 
      print( str(i) +': ' + str( eval('site' + str(i)) ) )
    except NameError:
      i = i # site i does not exist... Move along.
    i += 1
  print(' ')
  print('Which Site Number?')
  x = input()
  # Use selected site

  # clear the screen
  os.system('cls')

  site = eval('site' + str(x) )
  print('Site ' + x +' selected.')
  print(' ')
  print('Testing the site:')
  #color.write(site,"STRING")
  print(f'{Fore.GREEN}{site}{Style.RESET_ALL}')
  if int(x) < 44:
    print(f'{Fore.GREEN}{codeVersion}-{contentVersion}{Style.RESET_ALL}')
    print(' ')
  ts = time.time()
  now = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
  print (now)
  print(' ')
  #
  from selenium.webdriver.common.keys import Keys
  #from selenium.webdriver.common.by import By
  #from selenium.webdriver.support.ui import WebDriverWait
  #from selenium.webdriver.support import expected_conditions as EC
  # Set up a Chrome Browser
  #  Referance: https://stackoverflow.com/questions/49914832/loading-of-unpacked-extensions-is-disabled-by-administrator
  from selenium import webdriver
  # Import Special Libary for #354
  ## https://pypi.org/project/selenium-wire/
  #from seleniumwire import webdriver as wiredriver  # Import from seleniumwire

  chromeOptions = webdriver.ChromeOptions()
  chromeOptions.add_experimental_option('useAutomationExtension', False)
  chromeOptions.add_experimental_option('excludeSwitches', ['enable-logging'])
  chromeOptions.add_argument('--ignore-certificate-errors')

  capabilities = webdriver.DesiredCapabilities().CHROME
  capabilities['acceptSslCerts'] = True

  driver = webdriver.Chrome(options=chromeOptions, desired_capabilities=chromeOptions.to_capabilities())

  driver.implicitly_wait(30)
  #driver.maximize_window()
  driver.set_window_position(0, 0)
  driver.set_window_size(1024, 1024)
  # Start Testing and Handle Simple Password if needed.
  # Good example of a basic assert test
  if int(x) < 44:
    driver.get(site+'?city=Durham&state=NC&country=USA')
    try:
        testName = 'Home Page AirNow Logo'
        assert 'AirNow.gov' in driver.title
        
        # verify AirNow Logo Graphic
        xpath = "//img[contains(@alt,'Air Now Logo')]"
        element = driver.find_element(By.XPATH,xpath)
        value = element.get_attribute("src")
        assert 'AirNow_Logo_White.svg' in value

        print(f'{Fore.GREEN}Pass: {Style.RESET_ALL}{testName}')
    except AssertionError:
        print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}')
    except Exception:
        print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}')
  

# FIRE FIRE FIRE #


  if int(x) > 43:
    #
    ###########
    # Fire & Smoke Map Tests...
    ###########
    print(' ')
    print('         Fire & Smoke Map Tests')
    ###########


##    # Smoke Outlook Info Dialog cw 2022-08-04
##    #   
##    try:   
##        driver.get(site);
##        # Wait for the National Maps page to load cw 2020-03-11
##        delay = 40 # seconds
##        try:
##          myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//img[@class='leaflet-marker-icon leaflet-zoom-animated leaflet-interactive']")))
##        except TimeoutException:
##          print ('Loading '+site+' took too long!')
##        # Translate
##        xpath = "//a[contains(.,'View the Smoke Outlook')]"
##        element = driver.find_element_by_xpath(xpath);
##        value = element.get_attribute("outerHTML")
##        print(value)
##        
##        color.write("Pass: ","STRING") 
##    except Exception:
##        color.write("FAIL: ","COMMENT")
##    except AssertionError:
##        color.write("FAIL: ","COMMENT")
##    print('Smoke Outlook Info Dialog - v3.0.3')
##
##    sys.exit()

    
    # Fire & Smoke Map Available cw 2022-10-31
    #   
    try:
        testName = 'Fire & Smoke Map Available'
        driver.get(site)
        # Wait for the National Maps page to load cw 2020-03-11
        delay = 40 # seconds
        try:
          myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//img[contains(@alt,'Air Now Logo')]")))
        except TimeoutException:
          print ('Loading '+site+' took too long!')
        # AirNow Logo
        xpath = "//img[contains(@alt,'Air Now Logo')]"
        element = driver.find_element(By.XPATH,xpath)
        # IWAQRP Logo
        xpath="//img[contains(@alt,'IWFAQRP Logo')]"
        element = driver.find_element(By.XPATH,xpath)

        print(f'{Fore.GREEN}Pass: {Style.RESET_ALL}{testName}')
    except AssertionError:
        print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}')
    except Exception:
        print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}')

    # Fire & Smoke Map Spanish Available cw 2022-11-18
    #   
    try:
        testName = 'Fire & Smoke Map Spanish Available'
        driver.get(site+'es');
        # Wait for the National Maps page to load cw 2020-03-11
        delay = 40 # seconds
        try:
          myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//img[contains(@alt,'Air Now Logo')]")))
        except TimeoutException:
          print ('Loading '+site+' took too long!')
        # AirNow Logo
        xpath = "//img[contains(@alt,'Air Now Logo')]"
        element = driver.find_element(By.XPATH,xpath)
        # IWAQRP Logo
        xpath="//img[contains(@alt,'IWFAQRP Logo')]"
        element = driver.find_element(By.XPATH,xpath)

        print(f'{Fore.GREEN}Pass: {Style.RESET_ALL}{testName}')
    except AssertionError:
        print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}')
    except Exception:
        print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}')

    
    # ColorVision Assist Available cw 2022-10-31
    #   
    try:
        testName = 'ColorVision Assist Available'
        driver.get(site);
        # Wait for the National Maps page to load cw 2020-03-11
        delay = 40 # seconds
        try:
          myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//img[contains(@alt,'Air Now Logo')]")))
        except TimeoutException:
          print ('Loading '+site+' took too long!')
        # Translate
        xpath = "//div[contains(@id,'navbar')]"
        element = driver.find_element(By.XPATH,xpath)
        value = element.get_attribute("outerHTML")
        #print(value)
        assert 'ColorVision Assist' in value

        print(f'{Fore.GREEN}Pass: {Style.RESET_ALL}{testName}')
    except AssertionError:
        print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}')
    except Exception:
        print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}')


    # fire.airnow.gov version cw 2020-09-16
    #   
    try:
        testName = 'Fire and Smoke Map version: '
        driver.get(site);
        # Wait for the National Maps page to load cw 2020-03-11
        delay = 30 # seconds
        try:
          myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//img[contains(@alt,'Air Now Logo')]")))
        except TimeoutException:
          print ('Loading '+site+' took too long!')
        element = driver.find_element(By.XPATH,xpath)  
        value = element.get_attribute("outerHTML")

        #thisVersion
        #print(value)
        #print(' ')
        #print(value.find('<strong>Version'))
        #print(value[value.find('<strong>Version')+15:value.find('<strong>Version')+15+6])
        #
        # Updated for Version 3 format; pulling the version from the top bar cw 2022-07-06
        thisVersion = value[value.find('site-version">&nbsp;&nbsp;v')+27:value.find('site-version">&nbsp;&nbsp;v')+27+3]
        #print(thisVersion)     
        assert 'site-version\">&nbsp;&nbsp;v' in value

        print(f'{Fore.GREEN}Pass: {Style.RESET_ALL}{testName}{thisVersion}')
    except AssertionError:
        print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}{thisVersion}')
    except Exception:
        print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}{thisVersion}')

    #fire.airnow.gov built on date cw 2022-01-24
    #
    # Using the "wire" driver to pull the headers and find the last modified date
    #
    #### restart the Selenium driver
    driver.close()
    driver.quit()
    ## Build a Selenium Wire Driver
    from seleniumwire import webdriver as wiredriver
    chromeOptions = wiredriver.ChromeOptions()
    chromeOptions.add_experimental_option('useAutomationExtension', False)
    chromeOptions.add_experimental_option('excludeSwitches', ['enable-logging'])
    capabilities = wiredriver.DesiredCapabilities().CHROME
    capabilities['acceptSslCerts'] = True
    driver2 = wiredriver.Chrome(options=chromeOptions, desired_capabilities=chromeOptions.to_capabilities())
    driver2.implicitly_wait(30)
    driver2.set_window_position(0, 0)
    driver2.set_window_size(1024, 1024)
        
    timeOut = 0
    value = 0
    try:
        testName = 'F&S Map site was last built on: '# Go to the site with Selenium wire driver
        driver2.get(site+'/index.html')
        # Access requests via the `requests` attribute
        for request in driver2.requests:
            if request.response:
                if request.response.headers['Content-Type']:
                  # we check the text/html request ONLY
                  if (request.response.headers['Content-Type'].find('text/html; charset=utf-8') == 0):
                    #print("    Hit!")
                    value = request.response.headers['Last-Modified']
                    #print(value)
                    break

        if (value == 0): # something didn't work
          assert 1==2                      

        print(f'{Fore.GREEN}Pass: {Style.RESET_ALL}{testName}{str(value)}')
    except AssertionError:
        print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}')
    except Exception:
        print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}')

    #### shutdown Selenium wire driver
    driver2.close()
    driver2.quit()
    #### rebuild the Selenium driver
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_experimental_option('useAutomationExtension', False)
    chromeOptions.add_experimental_option('excludeSwitches', ['enable-logging'])
    capabilities = webdriver.DesiredCapabilities().CHROME
    capabilities['acceptSslCerts'] = True
    driver = webdriver.Chrome(options=chromeOptions, desired_capabilities=chromeOptions.to_capabilities())
    driver.implicitly_wait(30)
    driver.set_window_position(0, 0)
    driver.set_window_size(1024, 1024)
    #
    ## END of fire.airnow.gov built on datetime

  ###########
  # END Fire & Smoke Map Tests
  #########
    print(' ')
    print('END Fire & Smoke Map Tests')
    driver.close()
    driver.quit()
    sys.exit()
  ###########
  # END Fire & Smoke Map Tests
  ###########

  # FIRE UP FIRE UP FIRE UP from here #



  ##############################
  # Put tests ALL BELOW here...
  #




  #42##########
  # In Progress items BELOW here...
  ###########
  print(' ')
  print('         Things in Progress...')
  ###########




  #sys.exit()



##  #AIR-508 Double Link Bug Fix cw 2022-01-06
##  #   
##  try:       
##      # first URL
##      driver.get(site+"?city=Sacramento&state=CA&country=USA")
##      # reset location; make sure it loads
##      driver.get(site+"?city=Sacramento&state=CA&country=USA")
##      #
##      xpath="//div[contains(@class,'marquee-dataprovider-col')]"
##      element = driver.find_element_by_xpath(xpath)
##      value = element.get_attribute("outerHTML")
##      #print(value)
##      #print( value.count("California Air Resources Board") )
##      # string should only appear once
##      assert value.count("California Air Resources Board") < 2
##
##      # second URL
##      driver.get(site+"?city=Phoenix&state=AZ&country=USA")
##      # reset location; make sure it loads
##      driver.get(site+"?city=Phoenix&state=AZ&country=USA")
##      #
##      xpath="//div[contains(@class,'marquee-dataprovider-col')]"
##      element = driver.find_element_by_xpath(xpath)
##      value = element.get_attribute("outerHTML")
##      #print(value)
##      #print( value.count("Maricopa County Air Quality Department") )
##      # string should only appear once
##      assert value.count("Maricopa County Air Quality Department") < 2
##
##      color.write("Pass: ","STRING") 
##  except Exception:
##      color.write("FAIL: ","COMMENT")
##  except AssertionError:
##      color.write("FAIL: ","COMMENT")
##  print('#AIR-508 Double Link Bug Fix')




  #sys.exit()
  


  





  #sys.exit()
































##  #AIR-382 Site Improve: Remove "i" tags cw 2021-01-22
##  #   
##  try:   
##      driver.get(site+ '/fires/using-airnow-during-wildfires')
##      # Drupal Content change
##      element = driver.find_element_by_xpath("//div[@id='ftn1']")
##      value = element.get_attribute("innerHTML")
##      #print(value)
##      assert '<i>' not in value
##
##      driver.get(site+ 'international/us-embassies-and-consulates')
##      ## Tantus Tech controls this iframe content
##      element = driver.find_element_by_xpath("//div[@class='aboutWrapper']")
##      value = element.get_attribute("innerHTML")
##      #print(value)
##      assert '</i>' not in value
##      
##      color.write("Pass: ","STRING") 
##  except Exception:
##      color.write("FAIL: ","COMMENT")
##  except AssertionError:
##      color.write("FAIL: ","COMMENT")
##  print('#AIR-382 Site Improve: Remove \"i\" tags






  #42########
  # failing BELOW ...
  ###########
  #print(' ')
  #print('         Tests that MAY have issues... Watch these...')
  ###########






  

  

  #sys.exit()

  ###########
  # GIS Test items BELOW here...
  ###########
  print(' ')
  print('         GIS Test Items')
  ###########


  # National Maps Images cw 2020-07-22
  #   Updated cw 2022-07-06
  #   
  try:   
      testName = 'National Maps Images updated: '
      # set init values to clean up output in FAIL
      value = ''
      ago = 0
      ts = time.time()
      #
      driver.get('https://www.airnow.gov/national-maps/')
      # 
      delay = 30
      myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "(//span[@class='timestamp'][contains(.,'Updated')])[1]")))
      #
      xpath = "//span[contains(@id,'currenttimestamp')]"
      element = driver.find_element(By.XPATH,xpath)
      value = element.get_attribute("innerHTML")
      value = value[8:-5]
      # convert to datetime object
      mapTime = time.mktime(datetime.datetime.strptime(value,"%B %d, %Y %I:%M %p").timetuple());
      # how long ago was that?
      ago = ts-mapTime
      # ago's unit is seconds; FAIL is greater than 120 minutes
      assert ago/60 < 120

      print(f'{Fore.GREEN}Pass: {Style.RESET_ALL}{testName}{value}')
      print(f'                                    Minutes ago: {str(round(ago/60))}')
  except AssertionError:
      print(f'{Fore.GREEN}Pass: {Style.RESET_ALL}{testName}{value}')
      print(f'                                    Minutes ago: {str(round(ago/60))}')
  except Exception:
      print(f'{Fore.GREEN}Pass: {Style.RESET_ALL}{testName}{value}')
      print(f'                                    Minutes ago: {str(round(ago/60))}')
  
  # GIS Pub Timestamp cw 2022-07-06
  #   
  try:
      testName = 'GIS Pub Timestamp updated: '
      # set init values to clean up output in FAIL
      value = ''
      ago = 0
      ts = time.time()
      #
      driver.get('https://gispub.epa.gov/airnow/?contours=ozonepm&monitors=ozonepm&xmin=-8796029.24843073&xmax=-8752918.764477948&ymin=4265415.489397727&ymax=4294155.812032914');
      delay = 45
      myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//div[@class='zoomLocateButton']")))
      #
      xpath = "//span[contains(@id,'warndate')]"
      element = driver.find_element(By.XPATH,xpath)
      value = element.get_attribute("innerHTML")
      #
      value = value[4:-15] + value[value.find('at')+3:-4] # strip the sting to make it simpler
      #print(value)
      # convert to datetime object
      mapTime = time.mktime(datetime.datetime.strptime(value,"%B %d, %Y %I:%M %p").timetuple());
      # how long ago was that?
      ago = ts-mapTime
      # ago's unit is seconds; FAIL is greater than 120 minutes
      assert ago/60 < 120

      print(f'{Fore.GREEN}Pass: {Style.RESET_ALL}{testName}{value}')
      print(f'                                    Minutes ago: {str(round(ago/60))}')
  except AssertionError:
      print(f'{Fore.GREEN}Pass: {Style.RESET_ALL}{testName}{value}')
      print(f'                                    Minutes ago: {str(round(ago/60))}')
  except Exception:
      print(f'{Fore.GREEN}Pass: {Style.RESET_ALL}{testName}{value}')
      print(f'                                    Minutes ago: {str(round(ago/60))}')

  # ArcGIS Login NOT required cw 2020-11-09
  #   
  try:   
      testName = 'ArcGIS Login NOT required'
      delay = 45
      driver.get('https://gispub.epa.gov/airnow/?xmin=-9532003.17527462&ymin=3818182.4369011233&xmax=-8044844.352958232&ymax=4759886.625374498&clayer=ozonepm&mlayer=ozonepm');
      # get entire page
      xpath = "(//div[contains(.,'Data updated')])[2]"
      myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
      # get everything
      value = driver.find_element(By.XPATH,"//*").get_attribute("outerHTML")
      #print(value)
      # Look for things in the Login dialog box that should NOT be present
      #
      #if driver.find_element_by_xpath("//div[contains(.,'Please sign in to access the item on ArcGIS Online')]"):
      #  raise Exception

      print(f'{Fore.GREEN}Pass: {Style.RESET_ALL}{testName}')
  except AssertionError:
      print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}')
  except Exception:
      print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}')


  # Monitors Available cw 2020-08-13
  #   
  try:   
      testName = 'Monitors Available'
      delay = 30
      driver.get('https://gispub.epa.gov/airnow/?xmin=-9532003.17527462&ymin=3818182.4369011233&xmax=-8044844.352958232&ymax=4759886.625374498&clayer=ozonepm&mlayer=ozonepm');
      # verify one of the last gis layers to load
      myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@id,'viewDiv')]")))
      myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@data-scale,'4622324.434309')]")))
      #print(myElem.get_attribute("data-scale"));
      # find the "labels layer"
      xpath = "//div[@id='viewDiv_gc']"
      element = driver.find_element(By.XPATH,xpath)
      # assert that it is visible
      value = element.get_attribute("style")
      #print(value);
      assert 'visible' in value

      print(f'{Fore.GREEN}Pass: {Style.RESET_ALL}{testName}')
  except AssertionError:
      print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}')
  except Exception:
      print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}')


  #
  # AirNowLatestContoursCombined ESRI Service cw 2019-03-28
  #
  driver.get('https://services.arcgis.com/cJ9YHowT8TU7DUyn/ArcGIS/rest/services/AirNowLatestContoursCombined/FeatureServer');
  try:
      testName = 'AirNowLatestContoursCombined ESRI Service'
      # title
      assert 'AirNowLatestContoursCombined' in driver.title
      
      # xpath - title; must get to the HTML element and pull the text
      #               Then can Assert the element, to catch the error as AssertionError:
      xpath = "//h2[contains(.,'AirNowLatestContoursCombined (FeatureServer)')]"
      element = driver.find_element(By.XPATH,xpath)

      print(f'{Fore.GREEN}Pass: {Style.RESET_ALL}{testName}')
  except AssertionError:
      print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}')
  except Exception:
      print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}')
  
  
  ###########
  # Critical Test items BELOW here...
  ###########
  print(' ')
  print('         Critical Items. It is very important that these PASS.')
  ###########
  
  # Verify AirNowDrupal Code Version Number cw 2019-07-11
  #         Updated cw 2020-01-28
  #   only ABOVE 2.2.0
  if float(codeVersion[:3]) > 2.2:
    driver.get(site + 'about-airnow');
    try:
      testName = 'AirNow Code Version is '
      assert 'About AirNow' in driver.title
      
      # Find the Version Number element
      xpath = "//p[contains(.,'AirNow Version')]"
      element = driver.find_element(By.XPATH,xpath)
      value = element.get_attribute("innerHTML")
      #print(value)
      assert codeVersion in value

      print(f'{Fore.GREEN}Pass: {Style.RESET_ALL}{testName}{codeVersion}')
    except AssertionError:
      print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}{codeVersion}')
    except Exception:
      print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}{codeVersion}')

  # Verify AirNowDrupal Content Version Number cw 2029-01-28
  #   only ABOVE 2.2.0
  if float(contentVersion[:3]) > 2.2:
    driver.get(site + 'about-airnow')
    try:
      assert 'About AirNow' in driver.title
      
      # Find the Version Number element
      xpath = "//p[contains(.,'AirNow Content Version')]"
      element = driver.find_element(By.XPATH,xpath)
      value = element.get_attribute("innerHTML")
      assert contentVersion in value

      testName = 'AirNow Content Version is '
      print(f'{Fore.GREEN}Pass: {Style.RESET_ALL}{testName}{contentVersion}')
    except AssertionError:
      print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}{contentVersion}')
    except Exception:
      print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}{contentVersion}')

  # CSS & JS Aggregation
  #  look for the /themes/anblue/css/base.css as MISSING; it has been aggregated.
  #
  #FIRST verify the site is Up
  delay = 30
  try:
    driver.get(site)
    # verify the AirNow Logo
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//img[contains(@alt,'Air Now Logo')]")))
  except Exception:
    color.write("FAIL: ","COMMENT")
  #END verify the site is Up

  try:  
      testName = 'CSS & JS Aggregation'
      # New Method to pull out all the HTML source cw 2023-01-18
      xpath = "//*"
      element = driver.find_element(By.XPATH,xpath)
      value = element.get_attribute("outerHTML")
      # END New Method...

      # If this string exists then the site is NOT using Agregation
      #  cloud.gov needs this stings to be shorter; it has "custom" directory cw 2019-08-08
      assert '/anblue/css/base.css' not in value
      
      #### Looking for Missing string ###
      print(f'{Fore.GREEN}Pass: {Style.RESET_ALL}{testName}')
  except AssertionError:
      print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}')
  except Exception:
      print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}')

  # Theme Debuging OFF cw 2019-04-04
  #
  #FIRST verify the site is Up
  delay = 30
  try:
    driver.get(site)
    # verify the AirNow Logo
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//img[contains(@alt,'Air Now Logo')]")))
  except Exception:
    color.write("FAIL: ","COMMENT")
  #END verify the site is Up  
  try:
      testName = 'Theme Debuging OFF'
      # verify Theme Debugging is off

      # New Method to pull out all the HTML source cw 2023-01-18
      xpath = "//*"
      element = driver.find_element(By.XPATH,xpath)
      value = element.get_attribute("outerHTML")
      # END New Method...

      # If this string exists then the site is using Theme Debuging and not running at full speed
      #   This assertion should throw an Exception
      assert '<!-- FILE NAME SUGGESTIONS:' not in value
      
      print(f'{Fore.GREEN}Pass: {Style.RESET_ALL}{testName}')
  except AssertionError:
      print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}')
  except Exception:
      print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}')

  # Verify Path used by icons cw 2020-02-03
  #  Revised after Hard Launch cw 2020-04-17
  driver.get(site)
  try:
    testName = 'Correct Path used by icons. Revised 2020-04-17'
    # Find the Fire Icon element
    xpath = "//img[contains(@alt,'Fire Icon')]"
    element = driver.find_element(By.XPATH,xpath)
    value = element.get_attribute("src")
    #print(value)
    #print(site.replace('preview:Welcome1@',''))
    # ONLY while not using DevDesktop cw 2020-04-17
    if 'airnowgov.dev.dd' not in site:
      # make sure NOT using DevDesktop's path
      assert 'airnowgov.dev.dd' not in value
    # Try the icon
    driver.get(value)
    # Verify NOT a 404 page
    #print(driver.title)
    assert '404' not in driver.title
    
    print(f'{Fore.GREEN}Pass: {Style.RESET_ALL}{testName}')
  except AssertionError:
    print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}')
  except Exception:
    print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}')
  
  # Historic State JSON Data Available cw 2020-02-19
  #   
  month = str(int(datetime.datetime.fromtimestamp(ts).strftime('%m')))
  yesterday = str(int(datetime.datetime.fromtimestamp(ts).strftime('%d'))-1)
  # testing edge case   yesterday = 0;
  # only if first day of month; special date cw 2020-03-31
  if (yesterday == "0"):
    month = str(int(month) - 1)
    yesterday = "28"
  #print('http://airnowgovapi.com/andata/States/West_Virginia/2020/'+month+'/'+yesterday+'.json')
  try:
      testName = 'Historic State JSON Data Available'
      driver.get('http://airnowgovapi.com/andata/States/West_Virginia/2020/'+month+'/'+yesterday+'.json')
      #print('http://airnowgovapi.com/andata/States/West_Virginia/2020/'+month+'/'+yesterday+'.json')
      # New Method to pull out all the HTML source cw 2023-01-18
      xpath = "//*"
      element = driver.find_element(By.XPATH,xpath)
      value = element.get_attribute("outerHTML")
      # END New Method...
      #print(value)
      assert "error" not in value
      
      print(f'{Fore.GREEN}Pass: {Style.RESET_ALL}{testName}')
  except AssertionError:
      print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}')
  except Exception:
      print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}')
   
  # National Map Timestamp Current on National Maps page cw 2020-02-26
  #   
  today = str(int(datetime.datetime.fromtimestamp(ts).strftime('%d')))
  try:   
      testName = 'National Map Timestamp Current on National Maps page'
      driver.get(site + 'national-maps/')
      # Wait for the National Maps page to load cw 2020-03-11
      delay = 45 # seconds
      try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "(//h1[contains(.,'National Maps')])")))
      except TimeoutException:
        print ("Loading the dial took too long!")
      # END Wait for the National Maps page to load cw 2020-03-11
      # New Method to pull out all the HTML source cw 2023-01-18
      xpath = "(//span[@class='timestamp'])[1]"
      element = driver.find_element(By.XPATH,xpath)
      value = element.get_attribute("innerHTML")
      # END New Method...
      print(today)
      print(value)
      commaSpot = value.find(",")
      #print(commaSpot);
      displayDate = value[commaSpot-2:commaSpot]
      #print(displayDate);
      assert int(today) == int(displayDate)
      
      print(f'{Fore.GREEN}Pass: {Style.RESET_ALL}{testName}')
  except AssertionError:
      print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}')
  except Exception:
      print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}')

  # fire.airnow.gov available cw 2020-08-12
  #   
  try:   
      testName = 'fire.airnow.gov Available'
      driver.get('https://fire.airnow.gov')
      # Wait for the National Maps page to load cw 2020-03-11
      delay = 45 # seconds
      try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//img[contains(@alt,'Air Now Logo')]")))
      except TimeoutException:
        print ("Loading fire.airnow.gov took too long!")

      print(f'{Fore.GREEN}Pass: {Style.RESET_ALL}{testName}')
  except AssertionError:
      print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}')
  except Exception:
      print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}')

##  # fire.airnow.gov as Sensor Pilot available cw 2020-08-12
##  #   
##  try:   
##      driver.get('https://fire.airnow.gov');
##      # Wait for the National Maps page to load cw 2020-03-11
##      delay = 45 # seconds
##      try:
##        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//img[contains(@alt,'Air Now Logo')]")))
##      except TimeoutException:
##        print ("Loading fire.airnow.gov took too long!")
##
##      value = driver.find_element_by_xpath("(//div[contains(.,'×Notice: The Sensor Data Pilot adds a new layer of air quality data from low-cost sensors. Learn more here.')])[4]");
##
##      color.write("Pass: ","STRING") 
##  except Exception:
##      color.write("FAIL: ","COMMENT")
##  except AssertionError:
##      color.write("FAIL: ","COMMENT")
##  print('fire.airnow.gov Available as Sensor Data Pilot')

  # Production fire.airnow.gov version cw 2020-09-16
  #   
  try:   
      testName = 'Production fire.airnow.gov version: '
      driver.get('https://fire.airnow.gov')
      # Wait for the National Maps page to load cw 2020-03-11
      delay = 30 # seconds
      try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//img[contains(@alt,'Air Now Logo')]")))
      except TimeoutException:
        print ("Loading fire.airnow.gov took too long!")
        
      value = driver.find_element(By.XPATH,"//*").get_attribute("outerHTML")
      # Creation Date?
      
      #thisVersion
      #print(value)
      #print(' ')
      #print(value.find('<strong>Version'))
      #print(value[value.find('<strong>Version')+15:value.find('<strong>Version')+15+6])
      #
      # Updated for Version 3 format; pulling the version from the top bar cw 2022-07-06
      thisVersion = value[value.find('site-version">&nbsp;&nbsp;v')+27:value.find('site-version">&nbsp;&nbsp;v')+27+3]
      #print(thisVersion)     
      assert 'site-version\">&nbsp;&nbsp;v' in value

      print(f'{Fore.GREEN}Pass: {Style.RESET_ALL}{testName}{thisVersion}')
  except AssertionError:
      print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}{thisVersion}')
  except Exception:
      print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}{thisVersion}')

  #fire.airnow.gov built on date cw 2022-01-24
  #
  # Using the "wire" driver to pull the headers and find the last modified date
  #
  #### restart the Selenium driver
  driver.close()
  driver.quit()
  ## Build a Selenium Wire Driver
  chromeOptions = webdriver.ChromeOptions()
  chromeOptions.add_experimental_option('useAutomationExtension', False)
  chromeOptions.add_experimental_option('excludeSwitches', ['enable-logging'])
  capabilities = webdriver.DesiredCapabilities().CHROME
  capabilities['acceptSslCerts'] = True
  driver2 = webdriver.Chrome(options=chromeOptions, desired_capabilities=chromeOptions.to_capabilities())
  driver2.implicitly_wait(30)
  driver2.set_window_position(0, 0)
  driver2.set_window_size(1024, 1024)

  timeOut = 0
  value = 0
  try:
      testName = 'F&S Map site was last built on: '
      # Go to the site with Selenium wire driver
      driver2.get('https://fire.airnow.gov/index.html')
      # Access requests via the `requests` attribute
      for request in driver2.requests:
          if request.response:
              if request.response.headers['Content-Type']:
                # we check the text/html request ONLY
                if (request.response.headers['Content-Type'].find('text/html; charset=utf-8') == 0):
                  #print("    Hit!")
                  value = request.response.headers['Last-Modified']
                  #print(value)

      print(f'{Fore.GREEN}Pass: {Style.RESET_ALL}{testName}{value}')
  except AssertionError:
      print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}{value}')
  except Exception:
      print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}{value}')
  #### shutdown Selenium wire driver
  driver2.close()
  driver2.quit()
  #### rebuild the Selenium driver
  chromeOptions = webdriver.ChromeOptions()
  chromeOptions.add_experimental_option('useAutomationExtension', False)
  chromeOptions.add_experimental_option('excludeSwitches', ['enable-logging'])
  capabilities = webdriver.DesiredCapabilities().CHROME
  capabilities['acceptSslCerts'] = True
  driver = webdriver.Chrome(options=chromeOptions, desired_capabilities=chromeOptions.to_capabilities())
  driver.implicitly_wait(30)
  driver.set_window_position(0, 0)
  driver.set_window_size(1024, 1024)
  #
  ## END of fire.airnow.gov built on date


  # DoSAir iframe content (Embassies & Consulates Page) cw 2021-04-07
  #   
  try:   
      testName = 'DoSAir iframe content (Embassies & Consulates Page)'
      driver.get(site+ 'international/us-embassies-and-consulates')
      ## Tantus Tech controls this iframe content
      element = driver.find_element_by_xpath("//div[@class='aboutWrapper']")

      print(f'{Fore.GREEN}Pass: {Style.RESET_ALL}{testName}')
  except AssertionError:
      print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}')
  except Exception:
      print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}')

  # ColdFusion Server Apache Domain Name Forward cw 2021-04-06
  #    
  try:
    testName = 'ColdFusion Server Apache Domain Name Forward'
    driver.get('https://airnow.gov')
    # verify AirNow Logo Graphic
    element = driver.find_element_by_xpath("//img[@alt='Air Now Logo']")
    value = element.get_attribute("src")
    assert 'AirNow_Logo_White.svg' in value

    print(f'{Fore.GREEN}Pass: {Style.RESET_ALL}{testName}')
  except AssertionError:
    print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}')
  except Exception:
    print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}')

  #Temporary: Factsheet Links to PDF in 2021-06 Directory cw 2020-10-09
  #   
  try:   
      testName = 'Temporary: Factsheet Links to PDF in 2021-06 Directory'
      # Check for that EXACT PDF in the same directory  ^^^^^^^
      driver.get(site+'sites/default/files/2021-06/prepare-for-fire-season_1.pdf');
      # Check for that EXACT PDF in the exact ^^^^ directory
      # And that it is NOT a 404 page...
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      if ( value.find("Sorry, But This Web Page Does Not Exist") > 0 ):
        # it is a 404 page
        assert 1 == 2

      print(f'{Fore.GREEN}Pass: {Style.RESET_ALL}{testName}')
  except AssertionError:
      print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}')
  except Exception:
      print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}')

  #Security Message NOT present cw 2022-01-27
  #   
  try:   
      testName = 'Security Message NOT present'
      # Check for the Secuirty Mesage that shows up on Mobile
      driver.get(site);
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      assert 'There is a security update available for your version of Drupal.' not in value
      # Check for the Secuirty Mesage that shows up on Mobile on the About AirNow page
      driver.get(site+'about-airnow');
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      assert 'There is a security update available for your version of Drupal.' not in value

      print(f'{Fore.GREEN}Pass: {Style.RESET_ALL}{testName}')
  except AssertionError:
      print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}')
  except Exception:
      print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}')

  #State Notifications List cw 2021-11-0233
  #
  # Special Looping here...
  #
  try:   
      testName = 'State Notifications List: '
      #ONLY on "Cloud.gov" sites...
      if ( site.find("app.cloud.gov") > 0 or site.find("www.airnow.gov") > 0):
        driver.get(site+'/stateNotifications.json')
        element = driver.find_element_by_xpath("//*")
        value = element.get_attribute("innerHTML")
        #print(value)
        
        # Dig out the state two letters
        states = ""
        position = 25
        while position < len(value):
          #print(position)
          statePosition = value.find("state\":\"", position)
          #print(statePosition)
          state = value[statePosition+8:statePosition+10] # the NEXT state
          if (statePosition != -1): # next state found, add it to the list
            if (state == "TE" or state == "TF" or state == "TG" ):  
              states = states # Skip the "test states"
            else:
              #print(states.find(state))
              if (states.find(state) == 0): # This state is already in the list of states cw 2022-01-27
                #print(' double hit!')
                states = states # then skip it
              else:
                states = states + state + ", " # add it to the list
                
              position += 25 # skip over this state
              #print("   "+states)

          position += 50 # just keep swimming...
        
        print(f'{Fore.GREEN}Pass: {Style.RESET_ALL}{testName}{states[:-1]}')
      else:
        # Not a "Cloud.gov" Site
        states = "n/a"

  except AssertionError:
      print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}{states[:-1]}')
  except Exception:
      print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}{states[:-1]}')




  ###########
  # Completed Version 3.0.39 items BELOW here...
  ###########
  print(' ')
  print('         Version 3.0.39')
  ###########

  #AIR-576 Wildfires Landing Page iPad Fixes cw 2022-10-14
  #
  #
  try:
      testName = '#AIR-576 Wildfires Landing Page iPad Fixes'
      driver.set_window_size(375, 667)
      driver.get(site+'wildfires/')
      xpath = "(//img[@class='links-card-image'])[1]"
      element = driver.find_element(By.XPATH,xpath)
      value = element.get_attribute("width")
      #print(value)
      assert "423" in value

      print(f'{Fore.GREEN}Pass: {Style.RESET_ALL}{testName}')
  except AssertionError:
      print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}')
  except Exception:
      print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}')
  driver.set_window_size(1024,1024)

  #AIR-577 Flag Program Coco Red Video cw 2022-10-14
  #
  #
  try:
      testName = '#AIR-577 Flag Program Coco Red Video'
      driver.get(site+'education/why-is-coco-red/')
      xpath = "//h2[contains(.,'Watch on YouTube')]"
      element = driver.find_element(By.XPATH,xpath)
      #print(value)

      print(f'{Fore.GREEN}Pass: {Style.RESET_ALL}{testName}')
  except AssertionError:
      print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}')
  except Exception:
      print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}')

  #AIR-589 R9 Admin Reading Coco Red Video cw 2022-10-14
  #
  try:
      testName = '#AIR-589 R9 Admin Reading Coco Red Video'
      driver.get(site+'air-quality-videos/')
      xpath = "//td[contains(.,'Why is Coco Red? Read Along Martha Guzman')]"
      element = driver.find_element(By.XPATH,xpath)
      print(element)

      print(f'{Fore.GREEN}Pass: {Style.RESET_ALL}{testName}')
  except AssertionError:
      print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}')
  except Exception:
      print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}')


  ###########
  # Completed Version 3.0.38 items BELOW here...
  ###########
  print(' ')
  print('         Version 3.0.38')
  ###########
  print('         nothing to report')


  ###########
  # Completed Version 3.0.37 items BELOW here...
  ###########
  print(' ')
  print('         Version 3.0.37')
  ###########

  #AIR-565 Remove References to NSCEP cw 2022-09-08
  #   
  #
  try:   
      testName = '#AIR-565 Remove References to NSCEP - Content 163'
      driver.get(site+'air-quality-and-health/online-training-for-health-professionals/')
      # New Method to pull out all the HTML source cw 2023-01-18
      xpath = "//*"
      element = driver.find_element(By.XPATH,xpath)
      value = element.get_attribute("outerHTML")
      # END New Method...
      #print(value)
      assert "NSCEP" not in value

      driver.get(site+'education/why-is-coco-orange/')
      # New Method to pull out all the HTML source cw 2023-01-18
      xpath = "//*"
      element = driver.find_element(By.XPATH,xpath)
      value = element.get_attribute("outerHTML")
      # END New Method...
      #print(value)
      assert "<!-- AIR-565" in value

      driver.get(site+'contact-us/')
      # New Method to pull out all the HTML source cw 2023-01-18
      xpath = "//*"
      element = driver.find_element(By.XPATH,xpath)
      value = element.get_attribute("outerHTML")
      # END New Method...
      #print(value)
      assert "<!-- AIR-565" in value
      
      print(f'{Fore.GREEN}Pass: {Style.RESET_ALL}{testName}')
  except AssertionError:
      print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}')
  except Exception:
      print(f'{Fore.RED}FAIL: {Style.RESET_ALL}{testName}')




  sys.exit()














  #AIR-564 Wildfires Map Broken Out of Box cw 2022-08-27
  #   
  #
  try:   
      driver.get(site+'wildfires/when-smoke-is-in-the-air/')
      xpath="//img[contains(@id,'fire-smoke-map-image')]"
      element = driver.find_element_by_xpath(xpath)
      #print(element)
      value = element.get_attribute("width")
      #print(value)
      assert "700" in value
      
      color.write("Pass: ","STRING")   
  except Exception:
      color.write("FAIL: ","COMMENT")  
  print('#AIR-564 Wildfires Map Broken Out of Box - Content 162')

  #sys.exit()

  #AIR-561 Remove 'EPA's' from Factsheet Bands cw 2022-08-23
  #   
  #
  try:   
      driver.get(site+'wildfires/after-a-fire/')
      xpath="//a[@href='/publications/wildfire-guide-factsheets/protect-yourself-from-ash']"
      element = driver.find_element_by_xpath(xpath)
      #print(element)
      value = element.get_attribute("outerHTML")
      #print(value)
      assert "EPA" not in value
      
      color.write("Pass: ","STRING")   
  except Exception:
      color.write("FAIL: ","COMMENT")  
  print('#AIR-561 Remove \'EPA\'s\' from Factsheet Bands - Content 161')

  #sys.exit()
  
  
  #AIR-560 Wildfire Landing Pages Link Fixes cw 2022-08-23
  #   
  #
  try:   
      driver.get(site+'wildfires/')
      xpath="//a[@href='/wildfire-guide-information/'][contains(.,'Wildfire Guide for Public Health Officials')]"
      element = driver.find_element_by_xpath(xpath)

      color.write("Pass: ","STRING")   
  except Exception:
      color.write("FAIL: ","COMMENT") 
  print('#AIR-560 Wildfire Landing Pages Link Fixes - Content 161')


  ###########
  # Completed Version 3.0.36 items BELOW here...
  ###########
  print(' ')
  print('         Version 3.0.36')
  ###########

  #AIR-559 Wildfire Landing Page Issues cw 2022-08-09
  #   
  #
  try:   
      driver.get(site+'wildfires/')
      xpath="//img[@alt='text block be smoke ready']"
      element = driver.find_element_by_xpath(xpath)

      color.write("Pass: ","STRING")   
  except Exception:
      color.write("FAIL: ","COMMENT") 
  print('AIR-559 Wildfire Landing Page Issues - Content 160')




  ###########
  # Completed Version 3.0.35 items BELOW here...
  ###########
  print(' ')
  print('         Version 3.0.35')
  ###########

  #AIR-555 Spanish Resources Announcment cw 2022-08-04
  #   
  #
  try:   
      driver.get(site+'recursos-de-airnow-en-espanol')
      xpath="//h1[@class='article-title'][contains(.,'Recursos de AirNow en español')]"
      element = driver.find_element_by_xpath(xpath)

      color.write("Pass: ","STRING")   
  except Exception:
      color.write("FAIL: ","COMMENT") 
  print('#AIR-555 Spanish Resources Announcment - Content 159')

  #AIR-469 Wildfires Landing Page cw 2022-07-28
  #   
  #
  try:   
      driver.get(site+'wildfires/')
      xpath="//h2[contains(.,'Before a Fire')]"
      element = driver.find_element_by_xpath(xpath)
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT") 
  print('#AIR-469 Wildfires Landing Page - Content 158')
  
  #Add Why is Coco Red to Spainsh Hub cw 2022-07-25
  #   
  try:   
      driver.get(site+'spanish-resources');
      xpath="//a[contains(.,'¿Por qué Coco está rojo?')]"
      element = driver.find_element_by_xpath(xpath)
      # 
      
      color.write("Pass: ","STRING") 
  except TimeoutException:
      color.write("FAIL: ","COMMENT")
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('Add Why is Coco Red to Spainsh Hub - Content 157')

  #Simpler Coco Red Education Page cw 2022-07-21
  #   
  try:   
      driver.get(site+'education/why-is-coco-red/');
      xpath="//h2[contains(.,'\"Why is Coco Red?\" in English and Spanish')]"
      element = driver.find_element_by_xpath(xpath)
      # 
      
      color.write("Pass: ","STRING") 
  except TimeoutException:
      color.write("FAIL: ","COMMENT")
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('Simpler Coco Red Education Page - Content 156')

  #Spanish Resoucres Page Other Agengies Update cw 2022-07-12
  #   
  try:   
      driver.get(site+'spanish-resources');
      xpath="//h3[contains(.,'Socios federales')]"
      element = driver.find_element_by_xpath(xpath)
      
      color.write("Pass: ","STRING") 
  except TimeoutException:
      color.write("FAIL: ","COMMENT")
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('Spanish Resoucres Page Other Agengies Update - Content 155')

  #Spanish Resoucres Page Nav Link cw 2022-07-12
  #   
  try:   
      driver.get(site);
      xpath="//a[contains(.,'Recursos en español')]"
      element = driver.find_element_by_xpath(xpath)
      
      color.write("Pass: ","STRING") 
  except TimeoutException:
      color.write("FAIL: ","COMMENT")
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('Spanish Resoucres Page Nav Link - Content 154')


  ###########
  # Completed Version 3.0.34 items BELOW here...
  ###########
  print(' ')
  print('         Version 3.0.34')
  ###########

  # Fire and Smoke Map Information Page - Content 153 cw 2022-06-29
  #   
  try:   
      driver.get(site+ '/fasm-info')
      # 
      xpath = "//h1[@class='band-title-light'][contains(.,'Fire and Smoke Map Information')]"
      element = driver.find_element_by_xpath(xpath)
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('Fire and Smoke Map Information Page - Content 153')

  # Remove Sentence Fragment on FASM Information Page - Content 153 cw 2022-06-29
  #   
  try:   
      driver.get(site+ '/fasm-info')
      # 
      xpath = "//div[@class='panel-heading'][contains(.,'Follow links on this page for information and documents related to the AirNow Fire and Smoke Map.')]"
      element = driver.find_element_by_xpath(xpath)
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('Remove Sentence Fragment on FASM Info Page - Content 153')
  

  ###########
  # Completed Version 3.0.33 items BELOW here...
  ###########
  print(' ')
  print('         Version 3.0.33')
  ###########
  

  # Fire and Smoke Map Information Page - Content 153 cw 2022-06-29
  #   
  try:   
      driver.get(site+ '/fasm-info')
      # 
      xpath = "//h1[@class='band-title-light'][contains(.,'Fire and Smoke Map Information')]"
      element = driver.find_element_by_xpath(xpath)
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('Fire and Smoke Map Information Page - Content 153')

  # Remove Sentence Fragment on FASM Information Page - Content 153 cw 2022-06-29
  #   
  try:   
      driver.get(site+ '/fasm-info')
      # 
      xpath = "//div[@class='panel-heading'][contains(.,'Follow links on this page for information and documents related to the AirNow Fire and Smoke Map.')]"
      element = driver.find_element_by_xpath(xpath)
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('Remove Sentence Fragment on FASM Info Page - Content 153 - Content 153')


  ###########
  # Completed Version 3.0.32 items BELOW here...
  ###########
  print(' ')
  print('         Version 3.0.32')
  ###########
  

  # Fix Link for NM on Smoke Advisories Page cw 2022-06-16
  #   
  try:   
      driver.get(site+ '/air-quality-and-health/fires/smoke-advisories')
      # 
      xpath = "//a[@href='https://nmfireinfo.com']"
      element = driver.find_element_by_xpath(xpath)
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('Fix Link for NM on Smoke Advisories Page - Content 152')

  # Last of 19 Redirects for Spanish Publication Group Renaming  cw 2022-06-10
  #   
  try:   
      driver.get(site+ '/publications/air-quality-flag-program-en-espanol/coco-book-spanish')
      # 
      xpath = "//h1[contains(.,'Libro de niños- ¿Por qué Coco es de color naranja?')]"
      element = driver.find_element_by_xpath(xpath)
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('Last of 19 Redirects for Spanish Publication Group Renaming - Content 151')

  # Add Asheville-Buncombe Air Quality Agency as Partner  cw 2022-06-02
  #   
  try:   
      driver.get(site+ 'partners/state-and-local-partners')
      # 
      xpath = "//a[contains(.,'Asheville-Buncombe Air Quality Agency')]"
      element = driver.find_element_by_xpath(xpath)
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('Add Asheville-Buncombe Air Quality Agency as Partner - Content 150')
  

  ###########
  # Completed Version 3.0.31 items BELOW here...
  ###########
  print(' ')
  print('         Version 3.0.31')
  ###########

  #Remove Teacher Toolkit from Teachers Page - Content 149 cw 2022-05-24
  #   
  try:   
      driver.get(site+'education/teachers/')
      xpath="//a[contains(.,'Air Quality Index (AQI) Toolkit for Teachers')]"
      element = driver.find_element_by_xpath(xpath)
      
  # REVIRSED !!!
      color.write("FAIL: ","COMMENT") 
  except Exception:
      color.write("Pass: ","STRING")
      
  print('Remove Teacher Toolkit from Teachers Page - Content 149')

  #Remove Teacher Toolkit PDF File - Content 149 cw 2022-05-24
  #   
  try:   
      driver.get(site+'sites/default/files/2018-03/teachers-toolkit-508.pdf')
      # Verify NOT a 404 page
      #print(driver.title)
      assert '404' in driver.title
      
      color.write("Pass: ","STRING")
  except Exception:
      color.write("FAIL: ","COMMENT")
      
  print('Remove Teacher Toolkit PDF File - Content 149')

  #Add Guzman Be Smoke Ready Videos - Content 149 cw 2022-05-24
  #   
  try:   
      driver.get(site+'air-quality-videos#epa-pacific-southwest-wildfire')
      xpath="//p[contains(.,'Air Quality Awareness Means Being Smoke Ready')]"
      element = driver.find_element_by_xpath(xpath)
      
      color.write("Pass: ","STRING")
  except Exception:
      color.write("FAIL: ","COMMENT")
      
  print('Add Guzman Be Smoke Ready Videos - Content 149')

  #Add ¿Por qué Coco está rojo? - Content 149 cw 2022-05-25
  #   
  try:   
      driver.get(site+'/publications/why-is-coco-red-en-español/why-is-coco-red-picture-book-en-español')
      xpath="//h1[contains(.,'¿Por qué Coco está rojo?')]"
      element = driver.find_element_by_xpath(xpath)
      
      color.write("Pass: ","STRING")
  except Exception:
      color.write("FAIL: ","COMMENT")
      
  print('Add ¿Por qué Coco está rojo? - Content 149')

  #Add New & Nueva links to AQFP for ¿Por qué Coco está rojo? - Content 149 cw 2022-05-25
  #   
  try:   
      # English
      driver.get(site+'/air-quality-flag-program')
      xpath="//p[contains(.,'NEW Why is Coco Red? A children’s book about wildfire smoke and air quality. Also available in Spanish, ¿Por qué Coco está rojo?')]"
      element = driver.find_element_by_xpath(xpath)
      # Spanish
      driver.get(site+'/air-quality-flag-program-in-spanish')
      xpath="//p[contains(.,'NUEVA Un libro para ninos sobre los incendios forestales y la calidad del aire: ¿Por qué Coco está rojo?')]"
      element = driver.find_element_by_xpath(xpath)
      
      color.write("Pass: ","STRING")
  except Exception:
      color.write("FAIL: ","COMMENT")
      
  print('Add New & Nueva links to AQFP for ¿Por qué Coco está rojo? - Content 149')
  


  ###########
  # Completed Version 3.0.30 items BELOW here...
  ###########
  print(' ')
  print('         Version 3.0.30')
  ###########

  #Why is Coco Red? Description Update - Content 147 cw 2022-05-12
  #   
  try:       
      driver.get(site + 'publications/why-is-coco-red/why-is-coco-red-picture-book');
      xpath="//p[contains(.,'In this sequel, Coco and his friends solve a mystery as they learn about wildfire smoke and air quality.')]"
      element = driver.find_element_by_xpath(xpath)
      
      color.write("Pass: ","STRING")   
  except Exception:
      color.write("FAIL: ","COMMENT") 
  print('Why is Coco Red? Description Update - Content 147')

  #Add Why is Coco Red? on AQFP Page - Content 147 cw 2022-05-12
  #   
  try:       
      driver.get(site + 'air-quality-flag-program');
      xpath="//p[contains(.,'NEW Why is Coco Red? A children’s book about wildfire smoke and air quality.')]"
      element = driver.find_element_by_xpath(xpath)
      
      color.write("Pass: ","STRING")   
  except Exception:
      color.write("FAIL: ","COMMENT") 
  print('Add Why is Coco Red? on AQFP Page - Content 147')

  #Remove Earth Day Crossword Puzzle Link from AQFP Page - Content 147 cw 2022-05-12
  #   
  try:       
      driver.get(site + 'air-quality-flag-program/');
      xpath="//a[contains(.,'Earth Day crossword puzzle and activities')]"
      element = driver.find_element_by_xpath(xpath)
      
 # REVIRSED !!!
      color.write("FAIL: ","COMMENT") 
  except Exception:
      color.write("Pass: ","STRING")
  print('Remove Earth Day Crossword Puzzle Link from AQFP Page - Content 147')  

  ###########
  # Completed Version 3.0.29 items BELOW here...
  ###########
  print(' ')
  print('         Version 3.0.29')
  ###########

  #AQAW Add NJ to General Resources - Content 146 cw 2022-05-03
  #   
  #
  try:       
      driver.get(site + 'aqaw/educational-resources-events-activities/');
      # 
      xpath="//a[contains(.,'New Jersey Dept. of Environmental Protection Air Quality Awareness Week')]"
      element = driver.find_element_by_xpath(xpath)

      color.write("Pass: ","STRING")   
  except Exception:
      color.write("FAIL: ","COMMENT") 
  print('AQAW Add NJ to General Resources - Content 146')

  #AQAW Announcement - Content 146 cw 2022-05-03
  #   
  #
  try:       
      driver.get(site + 'announcement/4636');
      #
      xpath="//h1[@class='article-title'][contains(.,'Celebrate Air Quality Awareness Week')]"
      element = driver.find_element_by_xpath(xpath)

      color.write("Pass: ","STRING")   
  except Exception:
      color.write("FAIL: ","COMMENT") 
  print('AQAW Announcement - Content 146')

  #AQAW Educational Resources Word Search - Content 145 cw 2022-05-02
  #   
  #
  try:       
      driver.get(site + 'aqaw/educational-resources-events-activities/');
      # verify title
      # confirm Data returned & displaed 
      xpath="//a[@href='/publications/2022-air-quality-awareness-week/air-quality-awareness-week-2022-word-search']"
      element = driver.find_element_by_xpath(xpath)

      color.write("Pass: ","STRING")   
  except Exception:
      color.write("FAIL: ","COMMENT") 
  print('AQAW Educational Resources Word Search - Content 145')

  #AQAW Home Page - Content 144 cw 2022-04-29
  #   
  #
  try:   
      driver.get(site+'aqaw/')
      xpath="//h1[contains(.,'2022 Air Quality Awareness Week')]"
      element = driver.find_element_by_xpath(xpath)
      
      color.write("Pass: ","STRING")
  except Exception:
      color.write("FAIL: ","COMMENT")
  print('AQAW Home Page - Content 144')

  #AQAW 2022 Content Check - Content 144 cw 2022-04-29
  #   
  #
  try:   
      driver.get(site+'aqaw/around-the-world/')
      xpath="//h1[@class='band-title-light'][contains(.,'World')]"
      element = driver.find_element_by_xpath(xpath)
      
      color.write("Pass: ","STRING")
  except Exception:
      color.write("FAIL: ","COMMENT") 
  print('AQAW 2022 Content Check - Content 144')

  ###########
  # Completed Version 3.0.28 items BELOW here...
  ###########
  print(' ')
  print('         Version 3.0.28')
  ###########

  #Link to Spanish Flag Program Lessons cw 2022-04-19
  #   
  #
  try:   
      driver.get(site+'air-quality-flag-program-classroom-curriculum-publications')
      xpath="//a[contains(.,'Air Quality Flag Program lessons in Spanish')]"
      element = driver.find_element_by_xpath(xpath) 
 
      color.write("Pass: ","STRING")   
  except Exception:
      color.write("FAIL: ","COMMENT") 
  print('Link to Spanish Flag Program Lessons - Content 143')

  #Spanish AQFP Change K2 to K5 cw 2022-04-19
  #   
  #
  try:   
      driver.get(site+'/air-quality-flag-program-in-spanish')
      xpath="//p[contains(.,'(K-5) y')]"
      element = driver.find_element_by_xpath(xpath) 
 
      color.write("Pass: ","STRING")   
  except Exception:
      color.write("FAIL: ","COMMENT") 
  print('Spanish AQFP Change K2 to K5 - Content 143')

  #Spanish AQFP Change K2 to K5 in Band of Cards cw 2022-04-19
  #
  #
  try:   
      driver.get(site+'/air-quality-flag-program-for-schools-in-spanish/for-schools2')
      xpath="//a[@class='links-card-link'][contains(.,'Plan e estudios a vuelo de pájaro (k-5)')]"
      element = driver.find_element_by_xpath(xpath) 
 
      color.write("Pass: ","STRING")   
  except Exception:
      color.write("FAIL: ","COMMENT") 
  print('Spanish AQFP Change K2 to K5 in Band of Cards - Content 143')
  

  #AIR-534 AQFP Lesson Plan Updates cw 2022-04-05
  #   
  #
  try:   
      driver.get(site + 'publications/air-quality-flag-program-classroom-curriculum/ozone-field-testing-lesson-plan');
      # confirm Highcharts
      xpath="//a[contains(.,'Ozone Field Testing Lesson Plan (Grades 6-12)')]"
      element = driver.find_element_by_xpath(xpath)
      value = element.get_attribute("href")
      #print(value)
      assert "2022-04" in value

      driver.get(site + 'publications/air-quality-flag-program-classroom-curriculum/air-strips-lesson-plan');
      # confirm Highcharts
      xpath="//a[contains(.,'Air Strips Lesson Plan (Grades 6-8)')]"
      element = driver.find_element_by_xpath(xpath)
      value = element.get_attribute("href")
      #print(value)
      assert "2022-04" in value

      color.write("Pass: ","STRING")   
  except Exception:
      color.write("FAIL: ","COMMENT") 
  print('#AIR-534 AQFP Lesson Plan Updates - Content 141')
  

  #AIR-530 Updated AirNow API cw 2022-03-25
  #   
  #
  try:   
      # Issue 1: Recent Trends page
      driver.get(site + 'trends/?city=Durham&state=NC&country=USA');
      # verify title
      assert 'Recent AQI Trends' in driver.title
      # confirm Highcharts
      xpath="//div[@class='band-custom-section trends-section'][contains(.,'Created with Highcharts')]"
      element = driver.find_element_by_xpath(xpath)
      #print('1')
      
      # Issue 2: Historic Air Quality page
      driver.get(site + 'state/?name=north-carolina#historicalAQI');
      # verify title
      assert 'State AQI' in driver.title
      # confirm Data returned & displaed 
      xpath="//b[contains(.,'Alexander County')]"
      element = driver.find_element_by_xpath(xpath)
      #print('2')

      color.write("Pass: ","STRING")   
  except Exception:
      color.write("FAIL: ","COMMENT") 
  print('#AIR-530 Updated AirNow API')

  #AIR-530 Dial Page Map Updated Bubble cw 2022-03-25
  #   
  #
  try:       
      # Issue 3: Dial page map Updated bubble
      #   
      driver.get(site + '?city=Durham&state=NC&country=USA');
      # verify title
      assert 'AirNow.gov' in driver.title
      #
      time.sleep(15)
      # confirm Data returned & displaed 
      xpath="//div[@class='time_overlay']"
      element = driver.find_element_by_xpath(xpath)
      value = element.get_attribute("innerHTML")
      #print(value)
      assert 'Updated' in value
      #print('3')

      color.write("Pass: ","STRING")   
  except Exception:
      color.write("FAIL: ","COMMENT") 
  print('#AIR-530 Dial Page Map Updated Bubble')


##  #AIR-529 AQFP Earth Day Page cw 2022-04-05
##  #   
##  #
##  try:   
##      driver.get(site + 'air-quality-flag-program');
##      # confirm Highcharts
##      xpath="//a[contains(.,'Earth Day crossword puzzle and activities')]"
##      element = driver.find_element_by_xpath(xpath)      
##
##      color.write("Pass: ","STRING")   
##  except Exception:
##      color.write("FAIL: ","COMMENT") 
##  print('#AIR-529 AQFP Earth Day Page')


  ###########
  # Completed Version 3.0.27 items BELOW here...
  ###########
  print(' ')
  print('         Version 3.0.27')
  ###########


  #AIR-520 custom-airnow-maps Updated cw 2022-03-22
  #   
  #
  try:   
      driver.get(site+'custom-airnow-maps/map-overview/')
      xpath="(//a[@href='/custom-airnow-maps/keeping-it-simple'])[2]"
      element = driver.find_element_by_xpath(xpath) 
 
      color.write("Pass: ","STRING")   
  except Exception:
      color.write("FAIL: ","COMMENT") 
  print('#AIR-520 custom-airnow-maps Updated - Content 140')

  ###########
  # Completed Version 3.0.26 items BELOW here...
  ###########
  print(' ')
  print('         Version 3.0.26')
  ###########

## ONLY on AQAW Comming Soon Page which has been removed cw 2022-05-12
#
##  #AQAW Toolkit Update cw 2022-03-10
##  #   
##  try:   
##      # on AQAW main URL
##      driver.get(site+'aqaw')
##      xpath="//a[contains(.,'AQAW Toolkit')]"
##      element = driver.find_element_by_xpath(xpath)
##      
##      color.write("Pass: ","STRING") 
##  except Exception:
##      color.write("FAIL: ","COMMENT")
##  except AssertionError:
##      color.write("FAIL: ","COMMENT")
##  print('AQAW Toolkit Update')

  #Spanish Wildfire Factsheets - Content 137 cw 2022-01-28
  #   
  #
  try:
      # Last content change... the date of 02/22
      driver.get(site+'publications/wildfire-guide-factsheets/wildfire-smoke-indoor-air-filtration-factsheet')
      xpath="//p[contains(.,'February 2022')]"
      element = driver.find_element_by_xpath(xpath)
      
      # new publications Group page
      driver.get(site+'wildfire-guide-factsheets-en-espanol')
      # date
      xpath="//p[contains(.,'diciembre 2021')]"
      element = driver.find_element_by_xpath(xpath)
      # blurb
      xpath="//p[contains(.,'Conozca las formas más efectivas de evitar que el humo y las cenizas entren en sus pulmones')]"
      element = driver.find_element_by_xpath(xpath)

##      # Publications group in "all" spanish publications
##      driver.get(site+'all-publications-en-espanol')
##      # date
##      xpath="//p[contains(.,'diciembre 2021')]"
##      element = driver.find_element_by_xpath(xpath)
##      # blurb
##      xpath="//p[contains(.,'Conozca las formas más efectivas de evitar que el humo y las cenizas entren en sus pulmones')]"
##      element = driver.find_element_by_xpath(xpath)    
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('Spanish Wildfire Factsheets - Content 137')




















  ###########
  # Completed Version 3.0.25 items BELOW here...
  ###########
  print(' ')
  print('         Version 3.0.25')
  ###########

  #AIR-523 Archive AQAW 2021 cw 2022-02-22
  #
  try:   
      # 2021 content page
      driver.get(site+'aqaw-2021/wildfires-smoke')
      xpath="//h1[@class='band-title-light'][contains(.,'May 3: Wildfires and Smoke')]"
      element = driver.find_element_by_xpath(xpath)
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  print('#AIR-523 Archive AQAW 2021 - Content 136')

  

  ###########
  # Completed Version 3.0.24 items BELOW here...
  ###########
  print(' ')
  print('         Version 3.0.24')
  ###########

##  #AQAW2022 Coming Soon Page cw 2022-02-15
##  #
##  try:   
##      # Publication Group
##      driver.get(site+'2022-aqaw-coming-soon/')
##      xpath="//h1[@class='band-title-light'][contains(.,'2022 Air Quality Awareness Week Coming Soon')]"
##      element = driver.find_element_by_xpath(xpath)
##      
##      color.write("Pass: ","STRING") 
##  except Exception:
##      color.write("FAIL: ","COMMENT")
##  print('AQAW2022 Coming Soon Page - Content 135')

  #AIR-515 Partners Page Right-Side Navigation cw 2022-02-15
  #
  try:   
      # Where does the link take us?
      driver.get(site)
      xpath="//a[@class='sub-link nav-link'][contains(.,'List of Partners')]"
      element = driver.find_element_by_xpath(xpath)
      value = element.get_attribute("href");
      #print(value)
      assert "/partners/state-and-local-partners" in value
        
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  print('#AIR-515 Partners Page Right-Side Navigation')

  #AIR-516 Gila River Indian Community Move to Arizona Tribal Partner cw 2022-02-15
  #
  try:   
      # Publication Group
      driver.get(site+'/partners/tribal-partners')
      xpath="//a[contains(.,'Gila River Indian Community Department of Environmental Quality - Air Quality Program')]"
      element = driver.find_element_by_xpath(xpath)
                 
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  print('#AIR-516 Gila River Indian Community Move to Arizona Tribal Partner')

  #Add Children's Health Workshop Documents - Content 134 cw 2022-01-25
  #
  try:   
      # Publication Group
      driver.get(site+'publications/children\'s-health/')
      xpath="//span[contains(.,'Disclaimer:')]"
      value = driver.find_element_by_xpath(xpath)
      # First Publication page
      driver.get(site+'publications/children\'s-health/2021-childrens-health-and-wildfire-smoke-workshop-summary')
      xpath="//a[contains(.,'2021 Children’s Health and Wildfire Smoke Workshop: Workshop Summary')]"
      value = driver.find_element_by_xpath(xpath)
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  print('Add Children\'s Health Workshop Documents - Content 134')

  #Remove AQFP Photo Gallery cw 2022-01-25
  #
  try:   
      # the link
      driver.get(site+'air-quality-flag-program/')
      xpath="//a[contains(.,'Photo Gallery')]"
      value = driver.find_element_by_xpath(xpath)
      # the gallery itself
      driver.get(site+'air-quality-flag-program/photo-gallery/')
      xpath="//h1[contains(.,'Flag Program Photo Gallery')]"
      value = driver.find_element_by_xpath(xpath)
      
  # REVIRSED !!!
      color.write("FAIL: ","COMMENT") 
  except Exception:
      color.write("Pass: ","STRING")
  print('Remove AQFP Photo Gallery - Content 134')

  #AIR-441 Five Biggest Documents on "document.airnow.gov" cw 2022-01-19
  #   
  #1 at 68M
  try:   
      driver.get(site+'publications/2018-naq-conference/sacramento-brings-message-masses')
      xpath="//a[@href='https://document.airnow.gov/how-sacramento-brings-the-message-to-the-masses.pdf']"
      value = driver.find_element_by_xpath(xpath)

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#AIR-441 1 of Five Biggest Documents on "document.airnow.gov"')
  
  #2 at 52M
  try:   
      driver.get(site+'publications/2018-naq-conference/integrating-air-quality-data-wearable-technology')
      xpath="//a[@href='https://document.airnow.gov/airfit-mobile-application.pdf']"
      value = driver.find_element_by_xpath(xpath)

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#AIR-441 2 of Five Biggest Documents on "document.airnow.gov"')

  #3 at 29M
  try:   
      driver.get(site+'publications/2018-naq-conference/high-accuracy-satellite-aerosol-products')
      xpath="//a[@href='https://document.airnow.gov/new-nearly-continuous-high-accuracy-satellite-aerosol-products-for-fires.pdf']"
      value = driver.find_element_by_xpath(xpath)

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#AIR-441 3 of Five Biggest Documents on "document.airnow.gov"')

  #4 at 16M
  try:   
      driver.get(site+'publications/2018-naq-conference/mn-air-quality-forecast-alert-collaboration-outreach')
      xpath="//a[@href='https://document.airnow.gov/piecing-it-together-minnesotas-air-quality-forecast-alert-collaboration-and-outreach.pdf']"
      value = driver.find_element_by_xpath(xpath)

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#AIR-441 4 of Five Biggest Documents on "document.airnow.gov"')

  #5 at 14M5
  try:   
      driver.get(site+'/publications/2018-naq-conference/north-calif-wildfires-air-quality-san-fran')
      xpath="//a[@href='https://document.airnow.gov/october-2017-northern-california-wildfires.pdf']"
      value = driver.find_element_by_xpath(xpath)

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#AIR-441 5 of Five Biggest Documents on "document.airnow.gov"')





  

















  ###########
  # Completed Version 3.0.23 items BELOW here...
  ###########
  print(' ')
  print('         Version 3.0.23')
  ###########

    #AIR-512 Correct favicon Used cw 2022-01-04
  #
  # Using the "wire" driver to pull the headers and find the last modified date
  #
  #### restart the Selenium driver
  driver.close()
  driver.quit()
  ## Build a Selenium Wire Driver
  chromeOptions = webdriver.ChromeOptions()
  chromeOptions.add_experimental_option('useAutomationExtension', False)
  capabilities = wiredriver.DesiredCapabilities().CHROME
  capabilities['acceptSslCerts'] = True
  driver2 = wiredriver.Chrome(chrome_options=chromeOptions, desired_capabilities=chromeOptions.to_capabilities())
  driver2.implicitly_wait(30)
  driver2.set_window_position(0, 0)
  driver2.set_window_size(1024, 1024)
      
  timeOut = 0
  value = 0
  try:   
      # Go to the site with Selenium wire driver
      driver2.get(site+'favicon.ico')
      # Access requests via the `requests` attribute
      for request in driver2.requests:
          #print("    here")
          if request.response:
              #print("    there")
              if request.response.headers['Content-Type']:
                # we check the text/html request ONLY
                if (request.response.headers['Content-Type'].find('image/x-icon') == 0):
                  #print("    Hit!")
                  value = request.response.headers['Last-Modified']
                  #print(value)

                  #
                  # Last Modifided Date of correct favicon !
                  # Updated to current date. cw 2022-05-12
                  assert '22 Feb 2022' in value
                  # 
                  
      color.write("Pass: ","STRING")
  except Exception:
      if '.gov' in site:
        color.write("FAIL: ","COMMENT")
      else:
        value = 'n/a'
        color.write("Pass: ","STRING")
  except AssertionError:
      if '.gov' in site:
        color.write("FAIL: ","COMMENT")
      else:
        value = 'n/a'
        color.write("Pass: ","STRING")
  print('#AIR-512 Correct favicon Used; favicon timestamped: '+ value)
  #### shutdown Selenium wire driver
  driver2.close()
  driver2.quit()
  #### rebuild the Selenium driver
  chromeOptions = webdriver.ChromeOptions()
  chromeOptions.add_experimental_option('useAutomationExtension', False)
  capabilities = webdriver.DesiredCapabilities().CHROME
  capabilities['acceptSslCerts'] = True
  driver = webdriver.Chrome(chrome_options=chromeOptions, desired_capabilities=chromeOptions.to_capabilities())
  driver.implicitly_wait(30)
  driver.set_window_position(0, 0)
  driver.set_window_size(1024, 1024)
  #
  ## END of AIR-512


  #AIR-508 Double Link Bug Fix cw 2022-01-06
  #   
  try:       
      # first URL
      driver.get(site+"?city=Sacramento&state=CA&country=USA")
      # reset location; make sure it loads
      driver.get(site+"?city=Sacramento&state=CA&country=USA")
      #
      xpath="//div[contains(@class,'marquee-dataprovider-col')]"
      element = driver.find_element_by_xpath(xpath)
      value = element.get_attribute("outerHTML")
      #print(value)
      #print( value.count("California Air Resources Board") )
      # string should only appear once
      assert value.count("California Air Resources Board") < 2

      # second URL
      driver.get(site+"?city=Phoenix&state=AZ&country=USA")
      # reset location; make sure it loads
      driver.get(site+"?city=Phoenix&state=AZ&country=USA")
      #
      xpath="//div[contains(@class,'marquee-dataprovider-col')]"
      element = driver.find_element_by_xpath(xpath)
      value = element.get_attribute("outerHTML")
      #print(value)
      #print( value.count("Maricopa County Air Quality Department") )
      # string should only appear once
      assert value.count("Maricopa County Air Quality Department") < 2

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#AIR-508 Double Link Bug Fix')

  
  # Fires Menu Highlighting OFF cw 2021-07-27
  #   
  try:   
      driver.get(site);
      # site response
      element = driver.find_element_by_xpath("//div[@class='dropbtn'][contains(.,'Fires')]");
      value = element.get_attribute("outerHTML")
      #print(value)
      assert 'background-color: darkred;' not in value
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('Fires Menu Highlighting OFF')







  








  ###########
  # Completed Version 3.0.22 items BELOW here...
  ###########
  print(' ')
  print('         Version 3.0.22')
  ###########

  #AIR-508 Data Provider URL Fix cw 2021-12-09
  #   
  try:   
      driver.get(site+"?city=Nashville&state=TN&country=USA")
      #
      xpath="(//a[@href='https://www.tn.gov/environment/program-areas/apc-air-pollution-control-home/apc/air-quality-forecasting.html'][contains(.,'Tennessee Air Pollution Control Div.')])[2]" # Look for new link
      value = driver.find_element_by_xpath(xpath)

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#AIR-508 Data Provider URL Fix')

  ###########
  # Completed Version 3.0.21 items BELOW here...
  ###########
  print(' ')
  print('         Version 3.0.21')
  ###########

  #501 Contact Us Link in Footer cw 2021-11-02
  #   
  try:   
      driver.get(site)
      #
      xpath="(//a[@href='/contact-us'][contains(.,'Contact Us')])[3]" # looking for thr 3rd link
      value = driver.find_element_by_xpath(xpath)

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#AIR-501 Contact Us Link in Footer')

  #472 Which Flag Mobile Fix cw 2021-07-15
  #   
  try:   
      # This is the URL from the V 2.0 of the Fire& Smoke Map redirecting to a Document Page
      driver.get(site+'which-flag-do-i-fly/?city=durham&state=Nc&country=USA') # updated to geoloation URL cw 2022-03-07
      xpath="//table[contains(@id,'detail_table')]"
      element = driver.find_element_by_xpath(xpath)
      # This is the PDF itself
      value = element.get_attribute("class")
      assert "table table-border detail" in value
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#472 Which Flag Mobile Fix')
  
  ###########
  # Completed Version 3.0.20 items BELOW here...
  ###########
  print(' ')
  print('         Version 3.0.20')
  ###########
  print('None')

  ###########
  # Completed Version 3.0.19 items BELOW here...
  ###########
  print(' ')
  print('         Version 3.0.19')
  ###########
  
  #AIR-441 Sample Document on "document.airnow.gov" cw 2021-11-01
  #   
  try:   
      driver.get(site+'/publications/2021-air-quality-awareness-week/aqaw-2021-social-media-challenge')
      xpath="//a[@href='https://document.airnow.gov/air-quality-awarness-week-2021-social-media-challenge.pdf'][contains(.,'Air Quality Awareness Week (AQAW) 2021 Social Media Challenge')]"
      value = driver.find_element_by_xpath(xpath)

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#AIR-441 Sample Document on "document.airnow.gov"')

  ###########
  # Completed Version 3.0.18 items BELOW here...
  ###########
  print(' ')
  print('         Version 3.0.18')
  ###########

  #AIR-493 Facebook URL Scraping Authorization cw 2021-10-20
  #   
  try:   
      driver.get(site+'yo5jkr838gvr8dvav6evubwjgzv6rr.html');
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML");
      # should NOT be a 404 page
      assert "Sorry, But This Web Page Does Not Exist" not in value
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#AIR-493 Facebook URL Scraping Authorization')

 #AIR-500 Contact Us Link on Custom AirNow Maps Page cw 2021-10-26
  #   
  try:   
      driver.get(site+'/custom-airnow-maps/troubleshooting-and-fixing-errors')
      #
      xpath="(//a[@href='/contact-us'][contains(.,'Contact Us')])[2]"
      value = driver.find_element_by_xpath(xpath)

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#AIR-500 Contact Us Link on Custom AirNow Maps Page')

  #Flag Progam Community Poster Thumbnail Graphic cw 2021-10-26
  #   
  try:   
      driver.get(site+'/sites/default/files/2021-10/air-quality-flag-program-communities-poster.jpg')
      #
      # Verify NOT a 404 page
      # print(driver.title)
      assert '404' not in driver.title
    
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('Flag Progam Community Poster Thumbnail Graphic')
  

  ###########
  # Completed Version 3.0.17 items BELOW here...
  ###########
  print(' ')
  print('         Version 3.0.17')
  ###########

  #AIR-492 Geolocation JavaScript Alert Removal cw 2021-09-30
  #   
  try:   
      # 
      driver.get(site)
      # JS fix appears in the last JS referenced on the page... let's find that one and look in the Documentation
      # pull out all the HTML source with one line of code!
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      #print(value)
      # find last script tag / hightest index value
      #     cloud.gov changed this directory... made shorter cw 2019-07-29
      index = value.rfind('/js/js_');
      #print (index)
      # find the URL to the target javascript
      #     cloud.gov changed the length; -6 characters... made shorter cw 2019-07-29
      JSpath = value[index:index+53]
      #print(JSpath)
      # This path always now on cloud.gov servers cw 2020-01-21
      sitePathString = "default/files"
      # and here is the complete JS url
      JSurl = site+"sites/"+sitePathString+JSpath
      #print(JSurl)
      # fetch the JS file
      driver.get(JSurl);
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      #print(value)
      
      # Geolocation Tippy is present
      assert '//showGeolocationError(error)' in value

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#AIR-492 Geolocation JavaScript Alert Removal')

  #'Wildfire Guide Information' Page Published cw 2021-09-30
  #   
  try:   
      driver.get(site+'wildfire-guide-information');
      xpath="//h1[@class='band-title-light'][contains(.,'Wildfire Guide Information')]"
      element = driver.find_element_by_xpath(xpath)
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('\'Wildfire Guide Information\' Page Published')

  #'Wildfire Guide Post-Publication Updates' Page Published cw 2021-09-30
  #   
  try:   
      driver.get(site+'wildfire-guide-post-publication-updates/');
      xpath="//h1[@class='band-title-light'][contains(.,'Wildfire Guide Post-Publication Updates')]"
      element = driver.find_element_by_xpath(xpath)
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('\'Wildfire Guide Post-Publication Updates\' Page Published')
  
  
  #Updated 'Wildfire Smoke Guide' PDF cw 2021-09-30
  #   
  try:   
      driver.get(site+'/sites/default/files/2021-09/wildfire-smoke-guide_0.pdf');
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML");
      # should NOT be a 404 page
      assert "Sorry, But This Web Page Does Not Exist" not in value

      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('Updated \'Wildfire Guide Information\' PDF Published')

  ###########
  # Completed Version 3.0.16 items BELOW here...
  ###########
  print(' ')
  print('         Version 3.0.16')
  ###########
  print('None')


  ###########
  # Completed Version 3.0.15 items BELOW here...
  ###########
  print(' ')
  print('         Version 3.0.15')
  ###########

  #AIR-477 Metatag for AQI View Only cw 2021-09-23
  #   
  try:   
      # 
      driver.get(site+'/aqi')
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      assert "The Air Quality Index (AQI) tells you how clean or polluted your outdoor air" in value

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#AIR-477 Metatag for AQI View Only')

  #AIR-281 Gelocation Feedback cw 2021-09-13
  #   
  try: 
    # 
    driver.get(site)
    # JS fix appears in the last JS referenced on the page... let's find that one and look in the Documentation
    # pull out all the HTML source with one line of code!
    value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
    #print(value)
    # find last script tag / hightest index value
    #     cloud.gov changed this directory... made shorter cw 2019-07-29
    index = value.rfind('/js/js_');
    #print (index)
    # find the URL to the target javascript
    #     cloud.gov changed the length; -6 characters... made shorter cw 2019-07-29
    JSpath = value[index:index+53]
    #print(JSpath)
    # This path always now on cloud.gov servers cw 2020-01-21
    sitePathString = "default/files"
    # and here is the complete JS url
    JSurl = site+"sites/"+sitePathString+JSpath
    #print(JSurl)
    # fetch the JS file
    driver.get(JSurl);
    value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
    #print(value)
    
    # Geolocation Tippy is present
    assert '// AIR-281 Add Tippy ONLY if disabled cw 2021-09-02' in value # cw 2021-09-13
      
    color.write("Pass: ","STRING") 
  except Exception:
    color.write("FAIL: ","COMMENT")
  except AssertionError:
    color.write("FAIL: ","COMMENT")
  print('#AIR-281 Gelocation Feedback')

  #AIR-354 Apple Touch Icon cw 2021-09-20
  #   
  try:   
      # 
      driver.get(site+'/apple-touch-icon.png')
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      assert "Sorry, But This Web Page Does Not Exist" not in value

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#AIR-354 Apple Touch Icon (requires post-TOME password free site)')

  #Add PDF of How Smoke Affects Your Health - Content 120 cw 2021-08-10
  #   
  try:   
      # 
      driver.get(site+'/air-quality-and-health/how-smoke-from-fires-can-affect-your-health')
      xpath="//a[contains(.,'Download Printable Brochure version: How Smoke From Fires Can Affect Your Health')]"
      value = driver.find_element_by_xpath(xpath)

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('Add PDF of How Smoke Affects Your Health - Content 120')


  ###########
  # Completed Version 3.0.14 items BELOW here...
  ###########
  print(' ')
  print('         Version 3.0.14')
  ###########
  print('None')

  ###########
  # Completed Version 3.0.13 items BELOW here...
  ###########
  print(' ')
  print('         Version 3.0.13')
  ###########


  #Add PDF of How Smoke Affects Your Health - Content 120 cw 2021-08-10
  #   
  try:   
      # 
      driver.get(site+'/air-quality-and-health/how-smoke-from-fires-can-affect-your-health')
      xpath="//a[contains(.,'Download Printable Brochure version: How Smoke From Fires Can Affect Your Health')]"
      value = driver.find_element_by_xpath(xpath)

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('Add PDF of How Smoke Affects Your Health - Content 120')

  ###########
  # Completed Version 3.0.12 items BELOW here...
  ###########
  print(' ')
  print('         Version 3.0.12')
  ###########

  #AIR-459 Anchors for Fire & Smoke Map FAQs - Updates cw 2021-07-21
  #
  # Disabled... FAQs were moved back to the Faire & SMaoke Map site.
  #
##  try:   
##      # This is the new URL
##      driver.get(site+'fire-smoke-map-faqs/#info')
##      xpath="//a[@id='info']"
##      value = driver.find_element_by_xpath(xpath)
##      # This anchor is a second test
##      driver.get(site+'fire-smoke-map-faqs/#fireinfo')
##      xpath="//a[@id='fireinfo']"
##      value = driver.find_element_by_xpath(xpath)
##      # This anchor is a link on the Fire & Smoke Map 
##      driver.get(site+'fire-smoke-map-faqs/#correction')
##      xpath="//a[@id='correction']"
##      value = driver.find_element_by_xpath(xpath)
##      
##      color.write("Pass: ","STRING") 
##  except Exception:
##      color.write("FAIL: ","COMMENT")
##  except AssertionError:
##      color.write("FAIL: ","COMMENT")
##  print('#AIR-459 Anchors for Fire & Smoke Map FAQs - Updated')

  #AIR-449 Back to Top cw 2021-07-30
  #   
  try:   
      # 
      driver.get(site)
      xpath="//button[contains(.,'Back to top')]"
      value = driver.find_element_by_xpath(xpath)

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#AIR-449 Back to Top')

  #Fire & Smoke Map FAQs as HTML - Content 115 cw 2021-07-21
  #
  # Disabled... FAQs were moved back to the Faire & SMaoke Map site.
  #
##  try:   
##      # This is the URL from the V 2.0.4 of the Fire& Smoke Map redirecting to a Document Page
##      driver.get(site+'fire-smoke-map-faqs/')
##      xpath="//h1[@class='band-title-light'][contains(.,'Fire and Smoke Map Frequently Asked Questions')]"
##      value = driver.find_element_by_xpath(xpath)
##
##      color.write("Pass: ","STRING") 
##  except Exception:
##      color.write("FAIL: ","COMMENT")
##  except AssertionError:
##      color.write("FAIL: ","COMMENT")
##  print('Fire & Smoke Map FAQs as HTML - Content 115')


  ###########
  # AirNow.gov publication links inside the Wildfire Smoke Guide PDF - Content 110
  ###########
  print(' ')
  print('   AirNow.gov publication links inside the Wildfire Smoke Guide PDF - Content 110 & 111')
  ###########

  #Post Publications Updates (Page 1 & 56) cw 2021-06-19
  #   
  try:   
      # The link
      driver.get(site+ 'wildfire-guide-post-publication-updates/')
      # Test for the title
      xpath = "//h1[@class='band-title-light'][contains(.,'Wildfire Guide Post-Publication Updates')]"
      element = driver.find_element_by_xpath(xpath)

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('Post Publications Updates (Page 1 & 56)')

  #Activity Guide Publications (Page 2 & 40 & 46) cw 2021-06-19
  #   
  try:   
      # The link
      driver.get(site+ 'activity-guides-publications/')
      # Test for the title
      xpath = "//h1[contains(.,'Activity Guides Publications')]"
      element = driver.find_element_by_xpath(xpath)

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('Activity Guide Publications (Page 2 & 40 & 46)')

  #Protecting Children from Wildfire Smoke and Ash (Page 8 & 35) cw 2021-06-19
  #   
  try:   
      # The link
      driver.get(site+ 'publications/wildfire-smoke-guide/protecting-children-from-wildfire-smoke-and-ash/')
      # Test for the title
      xpath = "//h1[contains(.,'Protecting Children from Wildfire Smoke and Ash')]"
      element = driver.find_element_by_xpath(xpath)

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('Protecting Children from Wildfire Smoke and Ash (Page 8)')

  #Indoor Air Filtration Factsheet (Page 20 & 48 & A-1) cw 2021-06-19
  #   
  try:   
      # The link
      driver.get(site+ 'publications/wildfire-smoke-guide/wildfire-smoke-indoor-air-filtration-factsheet/')
      # Test for the title
      xpath = "//h1[contains(.,'Indoor Air Filtration')]"
      element = driver.find_element_by_xpath(xpath)

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('Indoor Air Filtration Factsheet (Page 20 & 48 & A-1)')
  
  #Protect Your Lungs from Wildfire Smoke or Ash (Page 26 & A-1) cw 2021-06-19
  #   
  try:   
      # The link
      driver.get(site+ 'publications/wildfire-smoke-guide/protect-your-lungs-from-wildfire-smoke/')
      # Test for the title
      xpath = "//h1[contains(.,'Protect Your Lungs from Wildfire Smoke or Ash')]"
      element = driver.find_element_by_xpath(xpath)

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('Protect Your Lungs from Wildfire Smoke or Ash (Page 26 & A-1)')

  #Protecting Children from Wildfire Smoke and Ash (Page 27 & A-1) cw 2021-06-19
  #   
  try:   
      # The link
      driver.get(site+ 'publications/wildfire-smoke-guide/protecting-children-from-wildfire-smoke-and-ash/')
      # Test for the title
      xpath = "//h1[contains(.,'Protecting Children from Wildfire Smoke and Ash')]"
      element = driver.find_element_by_xpath(xpath)

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('Protecting Children from Wildfire Smoke and Ash (Page 27 A-1)')

  #Activity Sheet for PM (Page 35) cw 2021-06-19
  #   
  try:   
      # The link
      driver.get(site+ 'publications/activity-guides/activity-sheet-for-pm/')
      # Test for the title
      xpath = "//h1[contains(.,'Guide for Particle Pollution')]"
      element = driver.find_element_by_xpath(xpath)

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('Activity Sheet for PM (Page 35)')

  #Protect Your Pets from Wildfire Smoke Factsheet (Page 43 & A-1) cw 2021-06-19
  #   
  try:   
      # The link
      driver.get(site+ 'publications/wildfire-smoke-guide/wildfire-smoke-protect-your-pets/')
      # Test for the title
      xpath = "//h1[contains(.,'Protect Your Pets from Wildfire Smoke')]"
      element = driver.find_element_by_xpath(xpath)

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('Protect Your Pets from Wildfire Smoke Factsheet (Page 43 & A-1)')

  #Protect Your Large Animals and Livestock from Wildfire Smoke Factsheet (Page 43 & A-1) cw 2021-06-19
  #   
  try:   
      # The link
      driver.get(site+ 'publications/wildfire-smoke-guide/wildfire-smoke-protect-your-large-animals-and-livestock/')
      # Test for the title
      xpath = "//h1[contains(.,'Protect Your Large Animals and Livestock from Wildfire Smoke')]"
      element = driver.find_element_by_xpath(xpath)

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('Protect Your Large Animals and Livestock from Wildfire Smoke Factsheet (Page 43 & A-1)')
  
  #Prepare for Fire Season (Page 47 twice & 49) cw 2021-06-19
  #   
  try:   
      # The link
      driver.get(site+ 'publications/wildfire-smoke-guide/wildfire-smoke-prepare-for-fire-season/')
      # Test for the title
      xpath = "//h1[contains(.,'Prepare for Fire Season')]"
      element = driver.find_element_by_xpath(xpath)

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('Prepare for Fire Season (Page 47 twice & 49 & A-1)')

  #Protect Your Lungs from Wildfire Smoke or Ash (Page 48 & A-1) cw 2021-06-19
  #   
  try:   
      # The link
      driver.get(site+ 'publications/wildfire-smoke-guide/protect-your-lungs-from-wildfire-smoke/')
      # Test for the title
      xpath = "//h1[contains(.,'Protect Your Lungs from Wildfire Smoke or Ash')]"
      element = driver.find_element_by_xpath(xpath)

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('Protect Your Lungs from Wildfire Smoke or Ash (Page 48 & A-1)')

  #Air Quality Index - A Guide to Air Quality and Your Health (Page 56) cw 2021-06-19
  #   
  try:   
      # The link
      driver.get(site+ 'publications/air-quality-index/air-quality-index-a-guide-to-air-quality-and-your-health/')
      # Test for the title
      xpath = "//h1[contains(.,'Air Quality Index - A Guide to Air Quality and Your Health')]"
      element = driver.find_element_by_xpath(xpath)

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('Air Quality Index - A Guide to Air Quality and Your Health (Page 56)')

  #Reduce Your Smoke Exposure (Page A-1) cw 2021-06-19
  #   
  try:   
      # The link
      driver.get(site+ 'publications/wildfire-smoke-guide/reduce-your-smoke-exposure/')
      # Test for the title
      xpath = "//h1[contains(.,'Reduce Your Smoke Exposure')]"
      element = driver.find_element_by_xpath(xpath)

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('Reduce Your Smoke Exposure (Page A-1)')

  #Protect Yourself From Ash (Page A-1) cw 2021-06-19
  #   
  try:   
      # The link
      driver.get(site+ 'publications/wildfire-smoke-guide/wildfire-smoke-protect-yourself-from-ash/')
      # Test for the title
      xpath = "//h1[contains(.,'Protect Yourself from Ash')]"
      element = driver.find_element_by_xpath(xpath)

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('Protect Yourself From Ash (Page A-1)')

  #sys.exit()

  ###########
  # Completed Version 3.0.11 items BELOW here...
  ###########
  print(' ')
  print('         Version 3.0.11')
  ###########

  #AIR-460 Remove AcessiBe JavaScript cw 2021-07-07
  #   
  try:   
      driver.get('https://widget.airnow.gov/aq-dial-widget/?city=Durham&state=NC&country=USA')
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      # Has the AcessiBe Script been removed? 
      assert 'https://acsbapp.com/apps/app/dist/js/app.js' not in value
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#AIR-460 Remove AcessiBe JavaScript')


  ###########
  # Completed Version 3.0.10 items BELOW here...
  ###########
  print(' ')
  print('         Version 3.0.10')
  ###########


    #AIR-430 Widget Cleanly Displays No Data - Flag Program Widget cw 2021-06-28
  #   
  try:   
      # An impossible zip code
      driver.get('https://widget.airnow.gov/aq-flag-widget/?zip=30000&transparent=true');
      # NA Imsage Dot
      xpath = "//img[@src='/aq-flag-widget/images/NA-dot.png']"
      element = driver.find_element_by_xpath(xpath)

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#AIR-430 Widget Cleanly Displays No Data - Flag Program Widget')

  #AIR-430 Widget Cleanly Displays No Data - Dial Widget cw 2021-06-28
  #   
  try:   
      # An impossible zip code
      driver.get('https://widget.airnow.gov/aq-dial-widget/?zip=30000&transparent=true');
      # NA Imsage Dot
      xpath = "//p[contains(.,'No Data')]"
      element = driver.find_element_by_xpath(xpath)

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#AIR-430 Widget Cleanly Displays No Data - Dial Widget')

  #AIR-430 Widget Cleanly Displays No Data - Dial Widget Primary Pollutant cw 2021-06-28
  #   
  try:   
      # An impossible zip code
      driver.get('https://widget.airnow.gov/aq-dial-widget-primary-pollutant//?zip=30000&transparent=true');
      # NA Imsage Dot
      xpath = "//p[contains(.,'No Data')]"
      element = driver.find_element_by_xpath(xpath)

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#AIR-430 Widget Cleanly Displays No Data - Dial Widget Primary Pollutant')

  #AIR-430 Widget Cleanly Displays No Data - Dial Widget Digital Sinage cw 2021-06-28
  #   
  try:   
      # An impossible zip code
      driver.get('https://widget.airnow.gov/aq-dial-widget-signage/?zip=30000&transparent=true');
      # NA Imsage Dot
      xpath = "//p[contains(.,'No Data')]"
      element = driver.find_element_by_xpath(xpath)

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#AIR-430 Widget Cleanly Displays No Data - Dial Widget Digital Signage')

  
  ###########
  # Completed Version 3.0.9 items BELOW here...
  ###########
  print(' ')
  print('         Version 3.0.9')
  ###########

  #AIR-357 Deploy GZip Compression cw 2021-06-21
  #
  # A non-Selenium test fo this:
  #  https://www.whatsmyip.org/http-compression-test/?url=d3d3LmFpcm5vdy5nb3Y=
  # 
  # Using the "wire" driver to pull the headers and find the Content-Encoding of gzip
  #
  #### restart the Selenium driver
  driver.close()
  driver.quit()
  ## Build a Selenium Wire Driver
  chromeOptions = webdriver.ChromeOptions()
  chromeOptions.add_experimental_option('useAutomationExtension', False)
  capabilities = wiredriver.DesiredCapabilities().CHROME
  capabilities['acceptSslCerts'] = True
  driver2 = wiredriver.Chrome(chrome_options=chromeOptions, desired_capabilities=chromeOptions.to_capabilities())
  driver2.implicitly_wait(30)
  driver2.set_window_position(0, 0)
  driver2.set_window_size(1024, 1024)
      
  timeOut = 0
  value = 0
  try:   
      # Go to the site with Selenium wire driver
      driver2.get(site)
      # Access requests via the `requests` attribute
      for request in driver2.requests:
          if request.response:
              if request.response.headers['Content-Type']:
                # we check the text/html request ONLY
                if (request.response.headers['Content-Type'].find('text/html') == 0):
                  #print("    Hit!")
                  value = request.response.headers['Content-Encoding']
                  #print(value)
                  if value == 'gzip':
                    break
                  # else value is undefined and throws an exception
                  
      color.write("Pass: ","STRING")
  except Exception:
      if '.gov' in site:
        color.write("FAIL: ","COMMENT")
      else:
        value = 'n/a'
        color.write("Pass: ","STRING")
  except AssertionError:
      if '.gov' in site:
        color.write("FAIL: ","COMMENT")
      else:
        value = 'n/a'
        color.write("Pass: ","STRING")
  print('#AIR-357 Deploy GZip Compression')
  #### shutdown Selenium wire driver
  driver2.close()
  driver2.quit()
  #### rebuild the Selenium driver
  chromeOptions = webdriver.ChromeOptions()
  chromeOptions.add_experimental_option('useAutomationExtension', False)
  capabilities = webdriver.DesiredCapabilities().CHROME
  capabilities['acceptSslCerts'] = True
  driver = webdriver.Chrome(chrome_options=chromeOptions, desired_capabilities=chromeOptions.to_capabilities())
  driver.implicitly_wait(30)
  driver.set_window_position(0, 0)
  driver.set_window_size(1024, 1024)
  ## END of AIR-357

  #AIR-451 State Notifications for Fire Mode cw 2021-06-17
  #   
  try:   
      # Load some data
      driver.get(site+ '?city=Durham&state=NC&country=USA')
      # Test the TG type
      driver.get(site+ '?city=Test&state=TG&country=USA')
      element = driver.find_element_by_xpath("//a[@target='_blank'][contains(.,'Wildfires in TG')]")

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#AIR-451 State Notifications for Fire Mode')

  #AIR-451 Fire Mode URL Test cw 2021-06-21
  #   
  try:   
      # Load the URL
      driver.get(site+ '?city=Durham&state=NC&country=USA&test=TestFireMode')
      #
      element = driver.find_element_by_xpath("//a[@target='_blank'][contains(.,'Wildfires in TF')]")

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#AIR-451 Fire Mode URL Test')

  #AIR-448 Remove Band Container 'airnow' cw 2021-06-21
  #   
  try:   
      # Load the URL
      driver.get(site+ 'airnow/')
      # Should be a 404 page
      xpath = "//h1[@class='band-title-light'][contains(.,'Sorry, But This Web Page Does Not Exist')]"
      element = driver.find_element_by_xpath(xpath)

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#AIR-448 Remove Band Container \'||\\airnow\'')

  #AIR-447 'Beyond the AQI' Standard Phrase cw 2021-06-21
  #   
  try:   
      # Load the URL
      driver.get(site+ 'aqi/aqi-basics/extremely-high-levels-of-pm25/')
      #
      xpath = "//h3[contains(.,'The U.S. AQI does not include recommendations for PM2.5 levels above 500, but levels are sometimes worse (“Beyond the AQI”).')]"
      element = driver.find_element_by_xpath(xpath)

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#AIR-447 \'Beyond the AQI\' Standard Phrase')
  
  ###########
  # Completed Version 3.0.8 items BELOW here...
  ###########
  print(' ')
  print('         Version 3.0.8')
  ###########

  #AIR-444 Protect Your Pets Update cw 2021-06-07
  #   
  try:   
      driver.get(site+ '/publications/wildfire-smoke-guide/wildfire-smoke-protect-your-pets/');
      # the page
      element = driver.find_element_by_xpath("//a[contains(.,'Protect Your Pets from Wildfire Smoke')]");
      # the pdf
      # Revised; Do not refernce PDFs by direct URLs cw 2021-06-28
      #driver.get(site+ '/sites/default/files/2020-10/protect-your-pets-from-wildfire-smoke.pdf');
           
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#AIR-444 Protect Your Pets Update - Content 108')

  ###########
  # Completed Version 3.0.7 items BELOW here...
  ###########
  print(' ')
  print('         Version 3.0.7')
  ###########

  #AIR-439 Whirling Swirling Lesson Plan cw 2021-05-18
  #   
  try:   
      driver.get(site+'publications/air-quality-flag-program-classroom-curriculum/whirling-swirling-air-pollution');
      # New link
      element = driver.find_element_by_xpath("//a[contains(.,'Whirling Swirling Air Pollution (Grades 9- Adult)')]");
      value = element.get_attribute("href")
      #print(value)
      # Updated the URL for an updated PDF cw 2022-01-04
      assert '/2021-12/whirling-swirling-air-pollution.pdf' in value
               
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#AIR-439 Whirling Swirling Lesson Plan')

  #AIR-438 Add Broward County to 2021 AQAW cw 2021-05-18
  #   
  try:   
      driver.get(site+'aqaw-2021/educational-resources-events-activities') #URL updated due to AQAW archiving cw 2022-03-10
      # New link
      element = driver.find_element_by_xpath("//u[contains(.,'Broward County')]")
      # New Page
      driver.get(site+'air-quality-flag-program/ordering-free-flag-program-materials')
      element = driver.find_element_by_xpath("//h1[@class='band-title-light'][contains(.,'Ordering Free Flag Program Materials')]")
          
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#AIR-438 Add Broward County to 2021 AQAW - Content 107')

  #AIR-437 AQFP Ordering Free Flag Program Materials cw 2021-05-18
  #   
  try:   
      driver.get(site+'air-quality-flag-program');
      # New link
      element = driver.find_element_by_xpath("//a[@class='links-card-link'][contains(.,'Ordering Outreach Materials')]");
      # New Page
      driver.get(site+'air-quality-flag-program/ordering-free-flag-program-materials');
      element = driver.find_element_by_xpath("//h1[@class='band-title-light'][contains(.,'Ordering Free Flag Program Materials')]");
          
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#AIR-437 AQFP Ordering Free Flag Program Materials - Content 107')

  #AIR-408 Dial Widget without iframe cw 2021-05-20
  #   
  try:   
      driver.get('https://widget.airnow.gov/aq-dial-widget/JAMstack.html');
      # New link
      element = driver.find_element_by_xpath("//a[contains(.,'Download the widget HTML, JavaScript, CSS, and Images')]");
               
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#AIR-408 Dial Widget without iframe')





  ###########
  # Completed Version 3.0.6 items BELOW here... 2021 Air Quality Awwareness Week... Lots od Content!
  ###########
  print(' ')
  print('         Version 3.0.6')
  ###########

  #AIR-419 Air Quality Awareness Week 2021 & Spanish Version cw 2021-05-18
  #   
  try:   
      driver.get(site+'aqaw-2021/educational-resources-events-activities'); #URL updated due to AQAW archiving cw 2022-03-11
      # Sample New content
      element = driver.find_element_by_xpath("//u[contains(.,'NASA')]");
      # Spanish Site
      driver.get(site+'aqaw-2021-spanish/educational-resources-events-activities'); #URL updated due to AQAW archiving cw 2022-03-11
      # Some sample content
      element = driver.find_element_by_xpath("//h1[@class='band-title-light'][contains(.,'Recursos educacionales de calidad del aire, eventos y actividades')]");
               
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#AIR-419 Air Quality Awareness Week 2021 & Spanish Version - Content 106')

  ###########
  # Completed Version 3.0.5 items BELOW here...
  ###########
  print(' ')
  print('         Version 3.0.5')
  ###########
  print('None')
# Wildfire Smoke Guide was updated again on 2021-09-30
##  #Wildfire Smoke Guide 2021-05 Update cw 2021-05-04
##  #   
##  try:   
##      driver.get(site+'/publications/wildfire-smoke-guide/wildfire-smoke-a-guide-for-public-health-officials/');
##      # Newest link to document
##      element = driver.find_element_by_xpath("//a[@href='https://www.airnow.gov/sites/default/files/2021-05/wildfire-smoke-guide-revised-2019.pdf'][contains(.,'Wildfire Smoke: A Guide for Public Health Officials')]");
##      
##      color.write("Pass: ","STRING") 
##  except Exception:
##      color.write("FAIL: ","COMMENT")
##  except AssertionError:
##      color.write("FAIL: ","COMMENT")
##  print('Wildfire Smoke Guide 2021-05 Update - Content 105')

  

  ###########
  # Completed Version 3.0.4 items BELOW here...
  ###########
  print(' ')
  print('         Version 3.0.4')
  ###########

  #AIR-422 Add Social Media Challenge Spanish cw 2021-04-09
  #   
  try:   
      # Publication Group Title has changed to Spanish cw 2022-06-17
      driver.get(site + 'publications/semana-de-la-concienciación-sobre-la-calidad-del-aire-2021/aqaw-2021-social-media-challenge/');
      # new content
      element = driver.find_element_by_xpath("//h1[contains(.,'Semana de concienciación sobre la calidad del aire (AQAW) 2021 Desafío en las redes sociales')]");
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#AIR-422 Add Social Media Challenge Spanish')

  #AIR-420 Update to Health Professional Page cw 2021-04-09
  #   
  try:   
      driver.get(site + 'publications/health-professionals/promotional-palm-card-for-the-smoke-wildfire-course/');
      # new content
      element = driver.find_element_by_xpath("//li[contains(.,'Click the \"Submit Order\" button.')]");
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#AIR-420 Update to Health Professional Page')

  ###########
  # Completed Version 3.0.3 items BELOW here...
  ###########
  print(' ')
  print('         Version 3.0.3')
  ###########
  
  #Content: AQAW 2021 Scavenger Hunt cw 2021-03-15
  #   
  try:   
      driver.get(site+'publications/2021-air-quality-awareness-week/2021-earth-day-scavenger-hunt');
      # New Publication Link
      element = driver.find_element_by_xpath("//a[contains(.,'2021 Earth Day Scavenger Hunt')]");
      # New Publ;ication URL
      driver.get(site+'sites/default/files/2021-03/aqfp-earth-day-scavenger-hunt-2021.pdf');
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('Content: AQAW 2021 Scavenger Hunt')
  
  #Content: AQAW 2021 Social Media Challenge cw 2021-03-15
  #   
  try:   
      driver.get(site+'publications/2021-air-quality-awareness-week/aqaw-2021-social-media-challenge');
      # New Publication Link
      element = driver.find_element_by_xpath("//a[contains(.,'Air Quality Awareness Week (AQAW) 2021 Social Media Challenge')]");
      # New Publ;ication URL
      driver.get(site+'sites/default/files/2021-03/aqaw-2021-sm-challenge.pdf');
      # Is it on the Publication List page?
      driver.get(site+'publications/2021-air-quality-awareness-week');
      element = driver.find_element_by_xpath("//a[contains(.,'Air Quality Awareness Week (AQAW) 2021 Social Media Challenge')]");
   
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('Content: AQAW 2021 Social Media Challenge')

  #Content: Verify Activity Guides cw 2021-03-29
  #   
  try:   
      # As "Air Quality Index" Documents
      driver.get(site+'all-publications');
      # 3 listings
      element = driver.find_element_by_xpath("//a[@href='/publications/air-quality-index/air-quality-guide-for-no2']");
      element = driver.find_element_by_xpath("//a[@href='/publications/air-quality-index/air-quality-guide-for-ozone']");
      element = driver.find_element_by_xpath("//a[@href='/publications/air-quality-index/air-quality-guide-for-particle-pollution']");
      # 3 pages
      driver.get(site+'publications/air-quality-index/air-quality-guide-for-no2');
      driver.get(site+'publications/air-quality-index/air-quality-guide-for-ozone');
      driver.get(site+'publications/air-quality-index/air-quality-guide-for-particle-pollution');

      # As "Activity Guides" Documents
      driver.get(site+'publications/activity-guides-publications');
      # 3 listings
      element = driver.find_element_by_xpath("//a[@href='/publications/activity-guides/air-quality-guide-for-ozone']");
      element = driver.find_element_by_xpath("//a[@href='/publications/activity-guides/air-quality-guide-for-particle-pollution']");
      element = driver.find_element_by_xpath("//a[@href='/publications/activity-guides/air-quality-and-outdoor-activity-guidance-for-schools']");
      # 3 pages
      driver.get(site+'publications/air-quality-index/air-quality-guide-for-no2');
      driver.get(site+'publications/air-quality-index/air-quality-guide-for-ozone');
      driver.get(site+'publications/air-quality-index/air-quality-guide-for-particle-pollution');

      # new Nav Bar link
      driver.get(site+'all-publications');
      element = driver.find_element_by_xpath("//h1[contains(.,'Activity Guides Publications')]")
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('Content: Verify Activity Guides')

  #AIR-418 Add Wildfire Leadership Council Doc cw 2021-03-29
  #   
  try:   
      driver.get(site+'fires');
      # New Link
      element = driver.find_element_by_xpath("//a[@href='/publications/wildland-fire-leadership-council/statement-by-the-wflc-and-partners']");
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#AIR-418 Add Wildfire Leadership Council Doc')

  #AIR-309 Better State Page Printing cw 2021-03-29
  # 
  driver.get(site+'state/?name=alabama');
  try:
      # CSS fix appears in the FIRST CSS referenced on the page... let's find that one and look in the Documentation
      # pull out all the HTML source with one line of code!
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      #print(value)
      # find First script tag / lowest index value
      index = value.find('/css/css_');
      #print (index)
      # find the URL to the target javascript
      #     cloud.gov changed the length; -6 characters... made shorter cw 2019-07-29
      CSSpath = value[index:index+56]
      #print(CSSpath)
      # This path always now on cloud.gov servers cw 2020-01-21
      sitePathString = "default/files"
      # and here is the complete CSS url
      CSSurl = site+"sites/"+sitePathString+CSSpath
      #print(CSSurl)
      # fetch the JS file
      driver.get(CSSurl);
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      #print(value)
      # Latest Update to the CSS
      assert 'zoom:50%' in value
      
      color.write("Pass: ","STRING") 
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  except Exception:
      color.write("FAIL: ","COMMENT")
  print('#AIR-309 Better State page Printing')

  ###########
  # Completed Version 3.0.2 items BELOW here...
  ###########
  print(' ')
  print('         Version 3.0.2')
  ###########

# Revised. AQFP Photo Gallery was removed on 2022-01-27
#
##  #417 Flag Program Updates cw 2021-03-15
##  #   
##  try:   
##      driver.get(site+'air-quality-flag-program');
##      # New Link; Revised by AIR-437 cw 2021-05-20
##      #element = driver.find_element_by_xpath("//a[contains(.,'2021 Earth Day Scavenger Hunt')]");
##      # move Photo Gallery link to card
##      element = driver.find_element_by_xpath("//a[@class='links-card-link'][contains(.,'Photo Gallery')]");
##      
##      color.write("Pass: ","STRING") 
##  except Exception:
##      color.write("FAIL: ","COMMENT")
##  except AssertionError:
##      color.write("FAIL: ","COMMENT")
##  print('#AIR-417 Flag Program Updates')

  #Content: Remove old 2015 Air Quality Guides cw 2021-03-15
  #   
  try:   
      # 2015 Ozone
      driver.get(site+'sites/default/files/2020-09/air-quality-guide-ozone-2015.pdf');
      # Should be 404
      element = driver.find_element_by_xpath("//h1[@class='band-title-light'][contains(.,'Sorry, But This Web Page Does Not Exist')]")

      # 2015 pm
      driver.get(site+'sites/default/files/2018-04/air-quality-guide_pm_2015_0.pdf');
      # Should be 404
      element = driver.find_element_by_xpath("//h1[@class='band-title-light'][contains(.,'Sorry, But This Web Page Does Not Exist')]")
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('Content: Remove old 2015 Air Quality Guides')
  
  ###########
  # Completed Version 2.24.0 items BELOW here...
  ###########
  print(' ')
  print('         Version 3.0.0')
  ###########

  #402 Remove Weathercaster Content cw 2021-02-16
  #   
  try:   
      driver.get(site);
      # Link should be missing
      element = driver.find_element_by_xpath("//div[@class='navigation-holder']");
      value = element.get_attribute("innerHTML")
      #print(value)
      assert "Weathercasters" not in value
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#AIR-402 Remove Weathercaster Content')

  #381 HTML Landmark Issues cw 2021-02-16
  #   
  try:   
      driver.get(site);
      # New links
      element = driver.find_element_by_xpath("//div[@role='navigation']");
            
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#AIR-381 HTML Landmark Issues')

  ###########
  # Completed Version 2.24.0 items BELOW here...
  ###########
  print(' ')
  print('         Version 2.24.0')
  ###########

  #AIR-401 Remove Link to Fire Map from Splash Page cw 2021-01-21
  #   
  try:   
      driver.get(site);
      # Get the element that HAD the link
      element = driver.find_element_by_xpath("//h1[contains(@class,'location-label standard-location-label splash-main-message')]");
      value = element.get_attribute("innerHTML")
      #print(value)
      # verify the link is now gone
      assert 'Fire' not in value
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#AIR-401 Remove Link to Fire Map from Splash Page')

  #AIR-382 Site Improve: Remove "i" tags cw 2021-01-22
  #   
  try:   
      driver.get(site+ '/fires/using-airnow-during-wildfires')
      # Drupal Content change
      element = driver.find_element_by_xpath("//div[@id='ftn1']")
      value = element.get_attribute("innerHTML")
      #print(value)
      assert '<i>' not in value

      driver.get(site+ 'international/us-embassies-and-consulates')
      ## Tantus Tech controls this iframe content
      element = driver.find_element_by_xpath("//div[@class='aboutWrapper']")
      value = element.get_attribute("innerHTML")
      #print(value)
      assert '</i>' not in value
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#AIR-382 Site Improve: Remove \"i\" tags')

  #Flag Program Updates -- Content 96 cw 2021-01-28
  #   
  try:   
      driver.get(site+ '/how-ozone-is-formed-animation')
      # Drupal Content item
      element = driver.find_element_by_xpath("//h1[@class='band-title-light'][contains(.,'How Ozone is Formed Animation')]")

      driver.get(site+ '/publications/air-quality-flag-program-classroom-curriculum/virtual-flag-display')
      # Drupal Content item
      element = driver.find_element_by_xpath("//a[contains(.,'Virtual Flag Display')]")
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('Flag Program Updates -- Content 96')

  #AIRN-105 & AIRN-118 Recent Trends -- Team Tantus Update cw 2021-01-25
  # 
  driver.get(site+'trends/?city=Durham&state=NC&country=USA');
  try:
      # JS fix appears in the last JS referenced on the page... let's find that one and look in the Documentation
      # pull out all the HTML source with one line of code!
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      #print(value)
      # find last script tag / hightest index value
      #     cloud.gov changed this directory... made shorter cw 2019-07-29
      index = value.rfind('/js/js_');
      #print (index)
      # find the URL to the target javascript
      #     cloud.gov changed the length; -6 characters... made shorter cw 2019-07-29
      JSpath = value[index:index+53]
      #print(JSpath)
      # This path always now on cloud.gov servers cw 2020-01-21
      sitePathString = "default/files"
      # and here is the complete JS url
      JSurl = site+"sites/"+sitePathString+JSpath
      #print(JSurl)
      # fetch the JS file
      driver.get(JSurl);
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      #print(value)
      # 2021-01-27 Update
      assert '// AIRN-105 UTC Offset is only present in a "Day" JSON cw 2021-01-27' in value # cw 2021-01-27
      
      color.write("Pass: ","STRING") 
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  except Exception:
      color.write("FAIL: ","COMMENT")
  print('#AIRN-105 & #AIRN-118 Recent Trends -- Team Tantus Update')

  # ColdFusion aqibasics.index#underaqi Redirect from MyAir cw 2021-01-07
  #   
  try:   
      driver.get('https://airnow.gov/index.cfm?action=aqibasics.index#underaqi');
      #
      value = driver.find_element_by_xpath("//h3[contains(.,'What is the U.S. Air Quality Index (AQI)?')]");

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('ColdFusion aqibasics.index#underaqi Redirect from MyAir')

        
##  #   fire.airnow.gov available cw 2020-08-12
##  try:   
##      driver.get('https://fire.airnow.gov');
##      # Wait for the National Maps page to load cw 2020-03-11
##      delay = 30 # seconds
##      try:
##        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//img[contains(@alt,'Air Now Logo')]")))
##      except TimeoutException:
##        print ("Loading fire.airnow.gov took too long!")
##
##      color.write("Pass: ","STRING") 
##  except Exception:
##      color.write("FAIL: ","COMMENT")
##  except AssertionError:
##      color.write("FAIL: ","COMMENT")
##  print('fire.airnow.gov Available')
##

  

##  #325 Timestamp on Dial cw 2020-06-23
##  #   
##  try:   
##      driver.get(site + '?city=Durham&state=NC&country=USA');
##      # JS fix appears in the last JS referenced on the page... let's find that one and look in the Documentation
##        # pull out all the HTML source with one line of code!
##      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
##      # find last script tag / hightest index value
##      #     cloud.gov changed this directory... made shorter cw 2019-07-29
##      index = value.rfind('/js/js_');
##      #print (index)
##      # find the URL to the target javascript
##      #     cloud.gov changed the length; -6 characters... made shorter cw 2019-07-29
##      JSpath = value[index:index+53]
##      #print(JSpath)
##      # This path always now on cloud.gov servers cw 2020-01-21
##      sitePathString = "default/files"
##      # and here is the complete JS url
##      JSurl = site+"sites/"+sitePathString+JSpath
##      # fetch the JS file
##      #print(JSurl);
##      driver.get(JSurl);
##      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
##      #print(value)
##      # assert the string in the fix ...
##      assert "// [AirNowDrupal-325] Time should no longer include minutes." in value 
##
##      color.write("Pass: ","STRING") 
##  except Exception:
##      color.write("FAIL: ","COMMENT")
##  except AssertionError:
##      color.write("FAIL: ","COMMENT")
##  print('#325 Timestamp on Dial')
##  


  ###########
  # Completed Version 2.23.0 items BELOW here...
  ###########
  print(' ')
  print('         Version 2.23.0')
  ###########

  #396 Widgets: Add Primary Pollutant cw 2021-01-14
  #   
  try:   
      driver.get('https://widget.airnow.gov/aq-dial-widget-primary-pollutant/?city=Tulsa&state=OK&country=USA')
      # Wait for the page to load cw 2022-03-11
      delay = 30 # seconds
      try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//span[@class='city'][contains(.,'Tulsa')]")))
      except TimeoutException:
        print ("Loading widget took too long!")
        
      driver.find_element_by_xpath("//span[@class='city'][contains(.,'Tulsa')]")

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#396 Widgets: Add Primary Pollutant')

  #395 Widgets: Digital Signage cw 2021-01-14
  #   
  try:   
      driver.get('https://widget.airnow.gov/aq-dial-widget-signage/?city=Sacramento&state=CA&country=USA&transparent=true')
      # Wait for the page to load cw 2022-03-11
      delay = 30 # seconds
      try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//span[@class='city'][contains(.,'Sacramento')]")))
      except TimeoutException:
        print ("Loading widget took too long!")
      #
      driver.find_element_by_xpath("//span[@class='city'][contains(.,'Sacramento')]")

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#395 Widgets: Digital Signage')

  #Widgets: Widget Page Instructions Update cw 2021-01-14
  #   
  try:   
      driver.get(site+ '/aqi-widgets/')
      # 
      driver.find_element_by_xpath("//h2[@class='band-title-grey'][contains(.,'Air Quality Index Widget with Primary Pollutant')]")

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('Widgets: Widget Page Instructions Update')







  ###########
  # Completed Version 2.22.0 items BELOW here...
  ###########
  print(' ')
  print('         Version 2.22.0')
  ###########

  #392 Remove Flash Content cw 2021-01-04
  #   
  try:   
      driver.get(site+'/air-quality-videos');
      # pull out all the HTML source with one line of code!
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      assert '- Flash' not in value

      driver.get(site+'/education/students/clean-and-dirty-air-part-two')
      # pull out all the HTML source with one line of code!
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      assert 'Flash plug-in required,' not in value
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#392 Remove Flash Content')

  #389 Widgets: 508 for Spokane Regional Clean Air Agency  cw 2021-01-04
  #   
  try:   
      driver.get('https://widget.airnow.gov/aq-dial-widget/css/style.css')
      # pull out all the HTML source with one line of code!
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      # the new style is there
      assert '.aq-dial-widget.good' in value
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#389 Widgets: 508 for Spokane Regional Clean Air Agency')

  #382 Hightlight on Focus - Site Improve cw 2020-12-18
  # Updated cw 2021-01-15
  #   
  try:   
      driver.get(site);
      # Nav Bar Links
      element = driver.find_element_by_xpath("//a[@class='main-link dropbtn-nav-link'][contains(.,'AirNow')]");
      value = element.get_attribute("tabindex")
      #print(value)
      assert '0' in value
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#382 Hightlight on Focus - Site Improve')




  ###########
  # Completed Version 2.21.0 items BELOW here...
  ###########
  print(' ')
  print('         Version 2.21.0')
  ###########

  #380 Timestamp Update after No Data cw 2020-12-02
  #   
  try:   
      delay = 30 # seconds
      # First Load -- No Data
      driver.get(site+'?city=Rio Grande City&state=TX&country=USA');
      try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//a[@href='/state/?name=texas'][contains(.,'Texas state page')]")))
      except TimeoutException:
        print ("Loading dial took too long!")
      # Second Load 
      driver.get(site+'?city=Durham&state=NC&country=USA');
      try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//span[@class='reporting-location-name'][contains(.,'Durham County Reporting Area')]")))
      except TimeoutException:
        print ("Loading dial took too long!")
      # Is the timestamp there?
      element = driver.find_element_by_xpath("//span[@class='aq-updated-time']");
      value = element.get_attribute("style")
      #print(value)
      assert 'none;' not in value
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#380 Timestamp Update after No Data cw 2020-12-02')




  ###########
  # Completed Version 2.20.0 items BELOW here...
  ###########
  print(' ')
  print('         Version 2.20.0')
  ###########

  #375 Monitors Near Me Zoom cw 2020-11-30
  #   
  try:   
      driver.set_window_size(1024, 1024)
      driver.get(site+'?city=Durham&state=NC&country=USA')
      # Seattle NEW site response
      element = driver.find_element_by_xpath("//a[@id='air-quality-monitors-near-me']");
      element.click()
      # Switch to new tab
      driver.switch_to.window(driver.window_handles[1])
      # get url of the Interactive Map Tab
      value = driver.current_url
      #print(value)
      assert 'gispub.epa.gov/airnow/' in value
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#375 Monitors Near Me Zoom')
  
  ###########
  # Completed Version 2.19.0 items BELOW here...
  ###########
  print(' ')
  print('         Version 2.19.0')
  ###########
  

  #AIR-379 ServiceNow Links cw 2020-10-09
  # Updated on 2021-11-01 for updated links on Contact Us page
  #   
  try:   
      driver.get(site+'/contact-us');
      # New links
      element = driver.find_element_by_xpath("//a[contains(.,'frequently asked questions')]");
      # 
      element = driver.find_element_by_xpath("(//a[@href='https://usepa.servicenowservices.com/airnow'])[1]");
      #
      driver.get(site+'/aqi/aqi-basics/using-air-quality-index/');
      element = driver.find_element_by_xpath("(//a[@href='https://usepa.servicenowservices.com/airnow?id=kb_article_view&sys_id=fed0037b1b62545040a1a7dbe54bcbd4'])");
      # the PDF, Too
      driver.get(site+'/publications/wildfire-smoke-guide/using-airnow-during-wildfires/');
      # The PDF from 2020-11-05
      element = driver.find_element_by_xpath("(//a[contains(@href,'2020-11-05_Using_AirNow_During_Wildfires')])[2]");
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#AIR-379 ServiceNow Links - Content')

  #328 RSS.XML Feed Available cw 2020-11-16
  #   
  try:   
      driver.get(site+'airnow.gov/rss.xml');

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#328 RSS.XML Feed Available')

  ###########
  # Completed Version 2.18.0 items BELOW here...
  ###########
  print(' ')
  print('         Version 2.18.0')
  ###########
  
  #378 Using AirNow During Wildfires cw 2020-10-28
  #   
  try:   
      driver.get(site+'/fires/using-airnow-during-wildfires');
      # Two New Menu Options
      element = driver.find_element_by_xpath("(//a[@class='main-link nav-link'][contains(.,'Using AirNow During Wildfires')])[1]");
      element = driver.find_element_by_xpath("(//a[@class='main-link nav-link'][contains(.,'Using AirNow During Wildfires')])[2]");
      # The New Page
      element = driver.find_element_by_xpath("//h1[@class='band-title-light'][contains(.,'Using AirNow During Wildfires')]");
      element = driver.find_element_by_xpath("//span[contains(.,'AirNow and Air Quality Information During Wildfires')]");
      # The Publication Page
      driver.get(site+'/publications/wildfire-smoke-guide/using-airnow-during-wildfires');
      element = driver.find_element_by_xpath("(//a[contains(.,'Using AirNow During Wildfires')])[3]");

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#378 Using AirNow During Wildfires')

  #377 Action Days Update for Dayton, OH -- Content cw 2020-10-26
  #   
  try:   
      driver.get(site + 'aqi/action-days');
      # site response
      value = driver.find_element_by_xpath("//a[@href='http://www.MiamiValleyAir.org'][contains(.,'Air Quality Alert')]");

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#377 Action Days Update for Dayton, OH -- Content')

#### REMOVED by cw 2021-01-25 ####
##  #373 Link to Fire Map from Splash Page cw 2020-10-22
##  #   
##  try:   
##      driver.get(site);
##      # site response third link...
##      element = driver.find_element_by_xpath("(//a[@href='https://fire.airnow.gov'][contains(.,'Fire and Smoke Map')])[3]");
##
##      color.write("Pass: ","STRING") 
##  except Exception:
##      color.write("FAIL: ","COMMENT")
##  except AssertionError:
##      color.write("FAIL: ","COMMENT")
##  print('#373 Link to Fire Map from Splash Page')

  #371 Chrome Widgets cw 2020-10-15
  #   
  try:
      driver.get(site+'aqi-widgets');
      element = driver.find_element_by_xpath("//p[contains(.,'NOTE: For the widgets to work in Chrome, users must allow third-party cookies. The widgets will not work at all on some centrally-managed systems where third-party cookies are blocked entirely.')]")
      # check the widgets themselves
      driver.get('https://widget.airnow.gov/aq-dial-widget/?city=Durham&state=NC&country=USA');
      element = driver.find_element_by_xpath("//span[@class='city'][contains(.,'Durham')]");
      driver.get('https://widget.airnow.gov/aq-flag-widget/?z=27713&n=Durham,%20NC');
      element = driver.find_element_by_xpath("//strong[contains(.,'Durham, NC')]");
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#371 Chrome Widgets')

  #363 Teachers and Students Pages Updates cw 2020-10-15
  #   
  try:   
      # Presentations added
      driver.get(site+'workshop-for-educators-publications');
      value = driver.find_element_by_xpath("//h1[contains(.,'Workshop for Educators Presentations')]");
      # Workshop item added
      driver.get(site+'education/teachers/worskhop-for-educators');
      value = driver.find_element_by_xpath("//h2[@class='strip-margin '][contains(.,'Workshops for Educators')]");  

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#363 Teachers and Students Pages Updates - Content')
  

  ###########
  # Completed Version 2.17.0 items BELOW here...
  ###########
  print(' ')
  print('         Version 2.17.0')
  ###########

# There is no longer a Monitor at Eureka, CA cw 2022-03-11
##  #366 Eureka on CA State Page cw 2020-09-29
##  #   
##  try:   
##      driver.get(site+'state/?name=california');
##      # Wait for the CA state page page to load AND look for Eureka
##      delay = 30 # seconds
##      try:
##        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "(//p[contains(.,'AirNow.gov - Home of the U.S. Air Quality Index')])[1]")))
##      except TimeoutException:
##        print ("Loading CA State Page took too long!")
##
##      driver.find_element_by_xpath("//b[contains(.,'Eureka')]")
##      
##      color.write("Pass: ","STRING") 
##  except Exception:
##      color.write("FAIL: ","COMMENT")
##  except AssertionError:
##      color.write("FAIL: ","COMMENT")
##  print('#366 Eureka on CA State Page')

  #365 Remove Village Green Link from Site Map cw 2020-10-05
  #   
  try:   
      driver.get(site+'site-map');
      # Wait for a page to load AND look for Eureka
      delay = 30 # seconds
      try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "(//p[contains(.,'AirNow.gov - Home of the U.S. Air Quality Index')])[1]")))
      except TimeoutException:
        print ("Loading the page took too long!")

      # pull out all the HTML source with one line of code!
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      #print(value)
      assert "Village Green Project" not in value
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#365 Remove Village Green Link from Site Map - Content')
  
  #350 Highest NowCast AQI Update Link cw 2020-09-04
  #   
  try:
      driver.get(site+'national-maps');
      element = driver.find_element_by_xpath("//h1[@class='band-title-light'][contains(.,'Highest NowCast AQI Locations')]");
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#350 Highest NowCast AQI Update - Content 80')

  #349 Mules, not Horses  cw 2020-09-08
  #   
  try:
      driver.get(site+'fires');
      element = driver.find_element_by_xpath("(//div[contains(@class,'carousel-inner')])");
      value = element.get_attribute("innerHTML")
      #print(value)
      assert "wildfire-animals.png" in value
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#349 Mules, not Horses - Content 80')



  ###########
  # Completed Version 2.16.0 items BELOW here...
  ###########
  print(' ')
  print('         Version 2.16.0')
  ###########
  

  #356 Remove February and April Announcements cw 2020-09-01
  #   
  try:   
      driver.get(site);
      # find element
      element = driver.find_element_by_xpath("//a[@class='link'][contains(.,'https://www.airnow.gov/announcement/3336')]")
      element = driver.find_element_by_xpath("//a[@class='link'][contains(.,'https://www.airnow.gov/announcement/3321')]")

      #####  ####
      ## Exception is reversed !!! ###
      color.write("FAIL: ","COMMENT")
  except Exception:
      color.write("Pass: ","STRING")
      ## Exception is reversed !!! ###
  print('#356 Remove February and April Announcements - Content 79')

  #354 CDN Cache Timeout cw 2020-09-01
  # Using the "wire" driver to pull the headers and find the cache time
  #
  #### restart the Selenium driver
  driver.close()
  driver.quit()
  ## Build a Selenium Wire Driver
  chromeOptions = webdriver.ChromeOptions()
  chromeOptions.add_experimental_option('useAutomationExtension', False)
  capabilities = wiredriver.DesiredCapabilities().CHROME
  capabilities['acceptSslCerts'] = True
  driver2 = wiredriver.Chrome(chrome_options=chromeOptions, desired_capabilities=chromeOptions.to_capabilities())
  driver2.implicitly_wait(30)
  driver2.set_window_position(0, 0)
  driver2.set_window_size(1024, 1024)
      
  timeOut = 0
  value = 0
  try:   
      # Go to the site with Selenium wire driver
      driver2.get(site)
      # Access requests via the `requests` attribute
      for request in driver2.requests:
          if request.response:
              if request.response.headers['Content-Type']:
                #print(request.response.headers['Content-Type'])
                #print(request.response.headers['Cache-control'])
                #print("....")
                if 'text/html' in request.response.headers['Content-Type']:
                  if 'max-age=' in request.response.headers['Cache-control']:
  ##                print(
  ##                  request.response.status_code,
  ##                  request.response.headers['Content-Type'],
  ##                  request.response.headers['Cache-control'],
  ##                  request.response.headers['Content-Type']
  ##                )
                    value = request.response.headers['Cache-control']
                    #print(value)
                    #print(' ')
                    #print(value.find('='))
                    #print(value[value.find('='):len(value)])
                    timeOut = int(value[value.find('=')+1:len(value)])
                    #print(str(timeOut))               
                    assert timeOut == 600 # 600 = 10 minutes.
                    # Revised cw 2021-01-15
                    break

      color.write("Pass: ","STRING")
  except Exception:
      if '.gov' in site:
        color.write("FAIL: ","COMMENT")
      else:
        value = 'n/a'
        color.write("Pass: ","STRING")
  except AssertionError:
      if '.gov' in site:
        color.write("FAIL: ","COMMENT")
      else:
        value = 'n/a'
        color.write("Pass: ","STRING")
  print('#354 cloud.gov CDN Cache Timeout is '+str(value) )
  #### shutdown Selenium wire driver
  driver2.close()
  driver2.quit()
  #### rebuild the Selenium driver
  chromeOptions = webdriver.ChromeOptions()
  chromeOptions.add_experimental_option('useAutomationExtension', False)
  capabilities = webdriver.DesiredCapabilities().CHROME
  capabilities['acceptSslCerts'] = True
  driver = webdriver.Chrome(chrome_options=chromeOptions, desired_capabilities=chromeOptions.to_capabilities())
  driver.implicitly_wait(30)
  driver.set_window_position(0, 0)
  driver.set_window_size(1024, 1024)

  #352 CDC’s “Wildfire Smoke and COVID-19” Link cw 2020-08-17
  #   
  try:
      driver.get(site+'wildfire-guide-post-publication-updates');
      element = driver.find_element_by_xpath("//a[@href='https://www.cdc.gov/disasters/covid-19/wildfire_smoke_covid-19.html'][contains(.,'Wildfire Smoke and COVID-19')]")
         
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#352 CDCs Wildfire Smoke and COVID-19 Link - Content 78')

  
  #348 San Francisco Bay Area Subgroup on CA Page cw 2020-08-24
  #   
  try:
      driver.get(site+'state/?name=california');
      time.sleep(5)
      element = driver.find_element_by_xpath("//b[contains(.,'San Francisco Bay Area')]")
            
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#348 San Francisco Bay Area Subgroup on CA Page')

  #342 AQI Widget Explanation Page cw 2020-08-27
  #   
  try:
      driver.get(site+'aqi-widgets');
      element = driver.find_element_by_xpath("//h1[@class='band-title-light'][contains(.,'Widgets')]")
      # nav Menu Item
      element = driver.find_element_by_xpath("//a[@class='sub-link nav-link'][contains(.,'Widgets')]")
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#342 AQI Widget Explanation Page - Content 78')


  ###########
  # Completed Version 2.15.0 items BELOW here...
  ###########
  print(' ')
  print('         Version 2.15.0')
  ###########

  #345 Highest AQI Mobile cw 2020-08-11
  #   
  try:   
      driver.get(site + 'national-maps');
      value = driver.find_element_by_xpath("//h1[@class='band-title-light'][contains(.,'Highest NowCast AQI Locations')]");

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#345 Highest AQI Mobile')

  #341 Air Quality Videos and Flash Links Page cw 2020-08-13
  #   
  try:   
      driver.get(site + 'air-quality-videos');
      value = driver.find_element_by_xpath("//h1[@class='band-title-light'][contains(.,'Air Quality Videos')]");

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#341 Air Quality Videos and Flash Links Page')

  #340 Coco Video, Content Updates, and Alias  cw 2020-08-24
  #   
  try:   
      driver.get(site + 'coco');
      value = driver.find_element_by_xpath("//p[contains(.,'Coco has a problem.')]");

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#340 Coco Video, Content Updates, and Alias')

  #339 Custom AirNow Maps Overview cw 2020-08-17
  #   
  try:
      driver.get(site+'custom-airnow-maps/map-overview');
      element = driver.find_element_by_xpath("//h1[@class='band-title-light'][contains(.,'Custom AirNow Maps - Map Overview')]")

      # Updated map graphic    Updated: cw 2021-05-10
      driver.get(site+'sites/default/files/inline-images/custom-map-page-1.PNG');
      #value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      #print(value)
      #assert "Sorry, But This Web Page Does Not Exist" not in value

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#339 Custom AirNow Maps Overview')

  #Fast Flag Alias  cw 2020-08-13
  #   
  try:   
      driver.get(site + 'flag');
      value = driver.find_element_by_xpath("//h1[contains(.,'Air Quality Flag Program')]");

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('Fast Flag Alias')


  ###########
  # Completed Version 2.14.0 items BELOW here...
  ###########
  print(' ')
  print('         Version 2.14.0')
  ###########

  #289 Highest AQI cw 2020-08-11
  #   
  try:   
      # First
      driver.get(site + 'national-maps');
      value = driver.find_element_by_xpath("//h1[@class='band-title-light'][contains(.,'Highest NowCast AQI Locations')]");

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#289 Highest AQI')

  ###########
  # Completed Version 2.13.0 items BELOW here...
  ###########
  print(' ')
  print('         Version 2.13.0')
  ###########
  #334 Add Mexican Organizations to Partners Page cw 2020-08-13
  #   
  try:   
      driver.get(site+'partners');
      element = driver.find_element_by_xpath("//h1[contains(.,'Mexican Partners')]")
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#334 Add Mexican Organizations to Partners Page')
  
  ###########
  # Completed Version 2.12.0 items BELOW here...
  ###########
  print(' ')
  print('         Version 2.12.0')
  ###########
  #313 Which Flag do I Fly widget cw 2020-08-13
  #   
  try:
      driver.get(site+'which-flag-do-i-fly/?city=Durham&state=NC&country=USA');
      element = driver.find_element_by_xpath("//h2[contains(.,'Which Flag Do I Fly?')]") # styale name changed; made xpath simpler cw 2022-01-04
      # Spanish
      #driver.get(site+'which-flag-do-i-fly/?lang=es&city=Durham&state=NC&country=USA');
      #element = driver.find_element_by_xpath("//strong[contains(.,'¿Qué banderín ondeo?')]")
            
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#313 Which Flag do I Fly widgets')

  ###########
  # Completed Version 2.11.0 items BELOW here...
  ###########
  print(' ')
  print('         Version 2.11.0')
  ###########
  
  #325 Timestamp on Dial cw 2020-06-23
  #   
  try:   
      driver.get(site + '?city=Durham&state=NC&country=USA');
      # JS fix appears in the last JS referenced on the page... let's find that one and look in the Documentation
        # pull out all the HTML source with one line of code!
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      # find last script tag / hightest index value
      #     cloud.gov changed this directory... made shorter cw 2019-07-29
      index = value.rfind('/js/js_');
      #print (index)
      # find the URL to the target javascript
      #     cloud.gov changed the length; -6 characters... made shorter cw 2019-07-29
      JSpath = value[index:index+53]
      #print(JSpath)
      # This path always now on cloud.gov servers cw 2020-01-21
      sitePathString = "default/files"
      # and here is the complete JS url
      JSurl = site+"sites/"+sitePathString+JSpath
      # fetch the JS file
      #print(JSurl);
      driver.get(JSurl);
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      #print(value)
      # assert the string in the fix ...
      assert "// [AirNowDrupal-325] Time should no longer include minutes." in value 

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#325 Add Date to Timestamp on Dial')

  








  ###########
  # Completed Version 2.10.0 items BELOW here...
  ###########
  print(' ')
  print('         Version 2.10.0')
  ###########

  #300 Spanish AQI Basics cw 2020-05-29
  #   
  try:   
      driver.get(site + '/aqi/aqi-basics-in-spanish');
      value = driver.find_element_by_xpath("//h3[contains(.,'¿Cómo funciona el AQI?')]");
  
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#300 Spanish AQI Basics - Content ')
  
  #309 Updates to California Regions cw 2020-06-02
  #   
  try:   
      driver.get(site + 'state/?name=california');
      value = driver.find_element_by_xpath("//b[contains(.,'Central Orange')]");
  
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#309 Updates to California Regions')

  #317 Recent Trends New Month Update
  #
  try:
      driver.get(site + '?city=Durham&state=NC&country=USA');
      driver.get(site + 'trends/?cityName&stateName&countryCode');
      # JS fix appears in the last JS referenced on the page... let's find that one and look in the Documentation
        # pull out all the HTML source with one line of code!
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      # find last script tag / hightest index value
      #     cloud.gov changed this directory... made shorter cw 2019-07-29
      index = value.rfind('/js/js_');
      #print (index)
      # find the URL to the target javascript
      #     cloud.gov changed the length; -6 characters... made shorter cw 2019-07-29
      JSpath = value[index:index+53]
      #print(JSpath)
      # This path always now on cloud.gov servers cw 2020-01-21
      sitePathString = "default/files"
      # and here is the complete JS url
      JSurl = site+"sites/"+sitePathString+JSpath
      # fetch the JS file
      #print(JSurl);
      driver.get(JSurl);
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      #print(value)
      # assert the string in the fix ...
      assert "endDateTime = moment().year(endDateTime.year()).month(endDateTime.month()).date(endDateTime.date()).startOf(\"day\");" in value 

      color.write("Pass: ","STRING")
  except Exception:
      color.write("FAIL: ","COMMENT")
  print('#317 Recent Trends New Month Update - Code - STI')






  ###########
  # Completed Version 2.9.0 items BELOW here...
  ###########
  print(' ')
  print('         Version 2.9.0')
  ###########

  #40 Use NCC Search Engine cw 2020-04-22
  #   Updated cw 2020-08-13
  try:   
    # open the search box
    driver.get(site);
    # verify it
    value = driver.find_element_by_xpath("//div[contains(@id,'search-content')]").get_attribute("innerHTML");
    #print(value)
    assert '<input type="hidden" name="areaname" value="AirNow">' in value
    assert '<input type="hidden" name="inmeta" value="URL~www.airnow.gov">' in value

    color.write("Pass: ","STRING") 
  except Exception:
    color.write("FAIL: ","COMMENT")
  except AssertionError:
    color.write("FAIL: ","COMMENT")
  print('#40 Use NCC Search Engine')

  #40 Verify About Metatags are Present cw 2020-04-22
  #   
  try:   
    # pull About page
    driver.get(site + 'about-airnow');
    value = driver.find_element_by_xpath("//head").get_attribute("innerHTML");
    #print(value)
    assert '<meta name="dcterms.title"' in value
    assert '<meta name="dcterms.description"' in value

    color.write("Pass: ","STRING") 
  except Exception:
    color.write("FAIL: ","COMMENT")
  except AssertionError:
    color.write("FAIL: ","COMMENT")
  print('#40 Verify About Metatags are Present')

  #44 Create Air Quality Flag Program Widget page cw 2020-05-29
  #   Udated. Not longer using ColdFusion sire. cw 2020-08-13
  #   
  try:   
      driver.get(site + '/air-quality-flag-program-widget/');
      value = driver.find_element_by_xpath("//h2[@class='strip-margin '][contains(.,'The Air Quality Flag Widget')]");
            
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#44 Create Air Quality Flag Program Widget page')

  #210 Shareable Trends Page URLs cw 2020-06-01
  #   
  try:   
      driver.get(site + '?city=Durham&state=NC&country=USA');
      element = driver.find_element_by_xpath("//a[@id='trends']");
      element.click()
      time.sleep(5)

      # Check for new URL format
      assert '?city=Durham&state=NC&country=USA' in driver.current_url
           
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#210 Shareable Trends Page URLs')

  #304 Publications Metadata cw 2020-05-29
  #   
  try:   
      driver.get(site + '/publications/air-quality-flag-program-newsletters');
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML");
      #print(value)
      assert '<meta name="dcterms.description"' in value
      
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#304 Publications Metadata - First one working')
  
  

  ###########
  # Completed Version 2.8.0 items BELOW here...
  ###########
  print(' ')
  print('         Version 2.8.0')
  ###########

  #293 Update Links to fire.airnow.gov cw 2020-05-11
  #   
  try:   
      # Fires page
      driver.get(site + 'fires/');
      # Card Link
      value = driver.find_element_by_xpath("(//a[@href='https://fire.airnow.gov'])[3]");
      # Featured Item Link
      value = driver.find_element_by_xpath("//a[@href='https://fire.airnow.gov/'][contains(.,'Fire and Smoke Map')]");
      #print("Here");
      # Navbar Link
      value = driver.find_element_by_xpath("(//a[@href='https://fire.airnow.gov'])[1]");
     
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#293 Update Links to fire.airnow.gov - Content 58')

  #287 Fire Map Warning for Old Browsers cw 2020-05-11
  #   
  try:   
      # First
      driver.get('https://fire.airnow.gov');
      value = driver.find_element_by_xpath("//div[@id='unsupportedBrowser']");

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#287 Fire Map Warning for Old Browsers')

  #182 Fix Data Provider for Denver, CO cw 2020-05-05
  #   
  try:   
      # Only one provider
      driver.get(site + '?city=Denver&state=CO&country=USA');
      value = driver.find_element_by_xpath("(//a[@href='https://www.colorado.gov/airquality/'][contains(.,'Colorado Department of Public Health and Environment')])[2]");

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#182 Fix Data Provider for Denver, CO ')

  ###########
  # Completed Version 2.7.0 items BELOW here...
  ###########
  print(' ')
  print('         Version 2.7.0')
  ###########

  #296 Mobile Band titles larger than Card titles cw 2020-05-01
  #
  # Mobile test
  driver.set_window_size(375, 667) # iPhone 6
  try:
    driver.get(site + 'aqaw/');
    value = driver.find_element_by_xpath("//h1[contains(@class,'band-title-light')]").value_of_css_property("font-size");
    #print(value)
    assert '28px' in value
    
    color.write("Pass: ","STRING")
  except Exception:
    color.write("FAIL: ","COMMENT")
  except AssertionError:
    color.write("FAIL: ","COMMENT")
  print('#296 Mobile Band titles larger than Card titles')
  driver.set_window_size(1024, 1024)
  
  #290 Add OAP CASTNET to Partners cw 2020-04-29
  #   
  try:   
      driver.get(site + 'partners/federal-partners');
      # new item added
      value = driver.find_element_by_xpath("//a[@href='https://www.epa.gov/castnet']");
      # "'s" removed
      value = driver.find_element_by_xpath("//a[contains(.,'EPA Office of Atmospheric Programs (OAP) CASTNET')]");
      
      # alphabetical Test
      value = driver.find_element_by_xpath("//td[@class='partner-info']").get_attribute("innerHTML");
      # pull values for 3 strings
      #print(value)
      x = value.find("CDC")
      #print(x)
      y = value.find("CASTNET")
      #print(y)
      z = value.find("Wyoming")
      #print(z)
      assert x < y < z
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#290 Add OAP CASTNET to Partners - Content 54')

  #285 Flag Program Earth Day page cw 2020-04-22
  #   
  try:   
    # check the page
    driver.get(site + 'air-quality-flag-program/earth-day/');
    value = driver.find_element_by_xpath("//h1[@class='band-title-light'][contains(.,'Earth Day 2020')]");

    color.write("Pass: ","STRING") 
  except Exception:
    color.write("FAIL: ","COMMENT")
  except AssertionError:
    color.write("FAIL: ","COMMENT")
  print('#285 Flag Program Earth Day page')

  #277 Automatic Rotating Banner cw 2020-04-21 
  #   
  try:   
    # First
    driver.get(site + 'fires/');
    value = driver.find_element_by_xpath("//div[@id='carousel-example-generic']").get_attribute("data-interval");
    #print(value)
    assert '5000' in value
    value = driver.find_element_by_xpath("//div[@id='carousel-example-generic']").get_attribute("data-wrap");
    #print(value)
    assert 'false' in value

    color.write("Pass: ","STRING") 
  except Exception:
    color.write("FAIL: ","COMMENT")
  except AssertionError:
    color.write("FAIL: ","COMMENT")
  print('#277 Automatic Rotating Banner - Content 53')

  #183 AQAW 2020 cw 2020-04-02
  #  Updated: Now uses "strong" cw 2020-08-14
  #  Updated: 2021 AQAW changes many links cw 2021-05-10
  #   
  try:   
    # airaware page - Content 52
    #driver.get(site + 'airaware/');
    #value = driver.find_element_by_xpath("//h1[contains(.,'2020 Air Quality Awareness Week')]");
    # 2020-04-28 Changes to Friday's Title
    #driver.get(site + 'aqaw/');
    #value = driver.find_element_by_xpath("//h2[contains(.,'Friday – Air Quality Educational Resources')]");
    # AQAW is "live"
    #driver.get(site + 'aqaw/');
    #value = driver.find_element_by_xpath("//h1[contains(.,'2020 Air Quality Awareness Week')]");
    # Friday page
    driver.get(site + 'friday-resources/');
    value = driver.find_element_by_xpath("//h1[contains(.,'Air Quality Educational Resources')]");
    # Thursday page
    driver.get(site + 'thursday-world/');
    value = driver.find_element_by_xpath("//h1[contains(.,'Air Quality Around the World')]");
    # Wednesday page
    driver.get(site + 'wednesday-aqi/');
    value = driver.find_element_by_xpath("//h1[contains(.,'s your AQI coming from')]"); 
    # Tuesday page
    driver.get(site + 'tuesday-asthma/');
    value = driver.find_element_by_xpath("//h1[contains(.,'Asthma & Your Health')]");
    # Monday page - Content 52 
    driver.get(site + 'monday-wildfires/');
    value = driver.find_element_by_xpath("//h1[contains(.,'Wildfires & Smoke')]");
    # Spanish Translation -- Content 55
    driver.get(site + 'thursday-world-spanish');
    value = driver.find_element_by_xpath("//h1[contains(.,'Calidad del aire alrededor del mundo')]");
    # Spanish page link back to English -- Content 55
    driver.get(site + 'wednesday-aqi-spanish');
    value = driver.find_element_by_xpath("//strong[contains(.,'English Version')]");
    # Spanish AQAW page -- Content 55
    #driver.get(site + 'aqaw-spanish/');
    #value = driver.find_element_by_xpath("//h1[contains(.,'Semana de concienciación sobre la calidad del aire 2020')]");
    
    color.write("Pass: ","STRING") 
  except Exception:
    color.write("FAIL: ","COMMENT")
  except AssertionError:
    color.write("FAIL: ","COMMENT")
  print('#183 2020 Air Quality Awareness Week - Content 55')

  #90 404 page after Tome cw 2020-02-19
  #   
  try:   
      driver.get(site + 'junk42');
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML");
      assert "Sorry, But This Web Page Does Not Exist" in value
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#90 404 page after Tome')










  


  ###########
  # Completed Version 2.6.1 items BELOW here...
  ###########
  print(' ')
  print('         Version 2.6.1')
  ###########

  #283 AQAW Already Published URLs redirection cw 2020-04-13
  #   
  try:   
      #URLs from the email from Lori
      driver.get(site + 'publications/2020-air-quality-awareness-week/aqaw-template-with-instructions/');
      time.sleep(10);
      value = driver.find_element_by_xpath("//h1[contains(.,'AQAW Template with Instructions')]");
      #
      driver.get(site + 'publications/why-is-coco-orange/why-is-coco-orange-picture-book/');
      time.sleep(10);
      value = driver.find_element_by_xpath("//h1[contains(.,'Why is Coco Orange? Picture Book')]");
      #
      driver.get(site + 'publications/wildfire-smoke-guide/wildfire-smoke-prepare-for-fire-season/');
      time.sleep(10);
      value = driver.find_element_by_xpath("//h1[contains(.,'Prepare for Fire Season')]");

      #URL from the 4/8/20 Communications Plan
      # publications/2020-air-quality-awareness-week/aqaw-poster-with-instructions/
      driver.get(site + 'publications/2020-air-quality-awareness-week/aqaw-poster-with-instructions/');
      time.sleep(10);
      value = driver.find_element_by_xpath("//h1[contains(.,'AQAW Template with Instructions')]");

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#283 AQAW Already Published URLs redirection')  
  
  #282 AQAW Template Publications cw 2020-03-31
  #   
  try:   
      # 1st document
      driver.get(site + 'publications/2020-air-quality-awareness-week/aqaw-template-with-instructions/');
      value = driver.find_element_by_xpath("//h1[contains(.,'AQAW Template with Instructions')]");
      # 2nd document
      driver.get(site + 'publications/2020-air-quality-awareness-week/aqaw-template/');
      value = driver.find_element_by_xpath("//h1[contains(.,'AQAW Template')]");
      # 3rd document
      driver.get(site + 'publications/2020-air-quality-awareness-week/aqaw-template-instructions/');
      value = driver.find_element_by_xpath("//h1[contains(.,'AQAW Template Instructions')]");
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#282 AQAW Template Publications - Content 48')
 
  #280 Redirect Aliases in the cloud cw 2020-04-14
  #   
  try:   
      value = "#280 Should PASS after airnow.gov domain move";
      # https://airnow.gov/flag
      driver.get(site + 'flag');
      time.sleep(2);
      value = driver.find_element_by_xpath("//h1[contains(.,'Air Quality Flag Program')]");
      value = "#280 Should PASS after airnow.gov domain move - 1";
      # https://airnow.gov/flag-program-widget 
      driver.get(site + 'flag-program-widget');
      time.sleep(2);
      value = driver.find_element_by_xpath("//h2[@class='strip-margin '][contains(.,'The Air Quality Flag Widget')]");
      value = "#280 Should PASS after airnow.gov domain move - 2";
      # https://airnow.gov/kids
      driver.get(site + 'kids');
      time.sleep(2);
      value = driver.find_element_by_xpath("//img[@src='graphics/blue_title.gif']");
      value = "#280 Should PASS after airnow.gov domain move - 3";
      # https://airnow.gov/picturebook 
      driver.get(site + 'picturebook');
      time.sleep(5);
      value = driver.find_element_by_xpath("//h1[contains(.,'Why is Coco Orange?')]");
      value = "#280 Should PASS after airnow.gov domain move - 4";
      # https://airnow.gov/students
      driver.get(site + 'students');
      time.sleep(2);
      value = driver.find_element_by_xpath("//h1[@class='band-title-light'][contains(.,'For Students')]");
      value = "#280 Should PASS after airnow.gov domain move - 5";
      # https://airnow.gov/teachers 
      driver.get(site + 'teachers');
      time.sleep(2);
      value = driver.find_element_by_xpath("//h1[@class='band-title-light'][contains(.,'For Teachers')]");
      value = "#280 Should PASS after airnow.gov domain move - 6";
      # https://airnow.gov/wildfire-guide
      driver.get(site + 'wildfire-guide');
      time.sleep(10);
      value = driver.find_element_by_xpath("//h1[contains(.,'Wildfire Smoke: A Guide for Public Health Officials')]");
      value = "#280 Should PASS after airnow.gov domain move -7";
      # /wildfires/ now used for "Fires Landing Page" cw 2022-03-11
##      # https://airnow.gov/wildfires 
##      driver.get(site + 'wildfires');
##      time.sleep(2);
##      value = driver.find_element_by_xpath("//h1[contains(.,'Fires')]");      
      # https://airnow.gov/whichflag
      # Updated to support geosearch cw 2021-05-18
      value = site + "whichflag?lang=en&city=Durham&state=NC&country=USA";
      driver.get(site + 'whichflag?lang=en&city=Durham&state=NC&country=USA');
      time.sleep(5);
      value = driver.find_element_by_xpath("//h2[contains(.,'Which Flag Do I Fly?')]");
        
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("      "+value,"COMMENT")
      print("");
      color.write("FAIL: ","COMMENT")
  print('#280 Redirect Aliases in the cloud - Content 50');

  #274 Fires Page Updates cw 2020-04-08
  #   
  try:   
      driver.get(site + 'fires/');
      # second banner image is San Francisco
      element = driver.find_element_by_xpath("//li[@data-target='#carousel-example-generic'][contains(.,'2')]");
      element.click();
      driver.find_element_by_xpath("//h2[contains(.,'San Francisco')]");
      # correct name for the "guide"
      driver.find_element_by_xpath("//a[@class='links-card-link'][contains(.,'Wildfire Smoke: A Guide for Public Health Officials')]");
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#274 Fires Page Updates - Content 47')

  #271 Enable Automation Redirection of the Top ColdFusion URLs cw 2020-03-20
  #   
  try:   
      value = "#271 Should PASS after airnow.gov domain move";
      # first redirect -- flag_program.index
      driver.get('https://airnow.gov/index.cfm?action=flag_program.index');
      time.sleep(2);
      value = driver.find_element_by_xpath("//h1[contains(.,'Air Quality Flag Program')]");
      # AQI Basics redirect -- aqibasics.aqi
      driver.get('https://airnow.gov/index.cfm?action=aqibasics.aqi');
      time.sleep(2);
      value = driver.find_element_by_xpath("//h1[contains(.,'Air Quality Index (AQI) Basics')]");
      # topics.smoke_wildfires
      driver.get('https://airnow.gov/index.cfm?action=topics.smoke_wildfires');
      time.sleep(2);
      value = driver.find_element_by_xpath("//h1[contains(.,'Fires')]");
      # airnow.local_state&stateid=5&mapcenter=0&tabs=0
      driver.get('https://airnow.gov/index.cfm?action=airnow.local_state&stateid=5&mapcenter=0&tabs=0');
      time.sleep(5);
      value = driver.find_element_by_xpath("//h2[contains(.,'California')]");
      # airnow.local_state&stateid=12&mapcenter=0&tabs=0
      driver.get('https://airnow.gov/index.cfm?action=airnow.local_state&stateid=12&mapcenter=0&tabs=0');
      time.sleep(2);
      value = driver.find_element_by_xpath("//h2[contains(.,'Hawaii')]");
      # airnow.calculator
      driver.get('https://airnow.gov/index.cfm?action=airnow.calculator');
      time.sleep(2);
      value = driver.find_element_by_xpath("//h1[contains(.,'AQI Calculator')]");
      # aqi_brochure.index
      driver.get('https://airnow.gov/index.cfm?action=aqi_brochure.index');
      time.sleep(2);
      value = driver.find_element_by_xpath("//h1[contains(.,'Air Quality Index Publications')]");
      # airnow.mapcenter&mapcenter=1
      driver.get('https://airnow.gov/index.cfm?action=airnow.mapcenter&mapcenter=1');
      time.sleep(2);
      value = driver.find_element_by_xpath("//h1[contains(.,'Interactive Map of Air Quality')]");
      # airnow.global_summary
      driver.get('https://airnow.gov/index.cfm?action=airnow.global_summary');
      time.sleep(2);
      value = driver.find_element_by_xpath("//h2[contains(.,'AirNow Department of State')]");      
      # last redirect -- airnow.actiondays
      driver.get('https://airnow.gov/index.cfm?action=airnow.actiondays');
      time.sleep(2);
      value = driver.find_element_by_xpath("//h1[contains(.,'Action Days')]");
      # Tweeted 2020-03-26
      driver.get('https://airnow.gov/index.cfm?action=resources.aqi_toolkit');
      time.sleep(2);
      value = driver.find_element_by_xpath("//h1[contains(.,'Teachers Toolkit')]");
      # Requested 2020-04-07
      driver.get('https://airnow.gov/index.cfm?action=learning.forteachers');
      time.sleep(2);
      value = driver.find_element_by_xpath("//h1[contains(.,'For Teachers')]");
      # Requested 2020-04-07
      driver.get('https://airnow.gov/index.cfm?action=flag_program.outdoorguid');
      time.sleep(2);
      value = driver.find_element_by_xpath("//h1[contains(.,'Asthma and Heart Disease')]");
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("      "+value,"COMMENT")
      print("");
      color.write("FAIL: ","COMMENT")
  print('#271 Automation Redirection of ColdFusion URLs - post-TOME Production URLs ONLY')

  #187 Shining Rock Webcam cw 2020-04-07
  #   
  try:   
      driver.get(site + 'resources/web-cams/');
      value = driver.find_element_by_xpath("//a[@href='https://www.resortcams.com/webcams/shining-rock/'][contains(.,'Shining Rock')]");
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#187 Shining Rock Webcam - Content')

  #181 NY Cities have Data courtsey links cw 2020-04-07
  #   
  try:   
      # Albany
      driver.get(site + '?city=Albany&state=NY&country=USA');
      value = driver.find_element_by_xpath("(//a[@href='http://www.dec.ny.gov/'][contains(.,'New York Dept. of Environmental Conservation')])[2]");

      # Poughkeepsie
      driver.get(site + '?city=Poughkeepsie&state=NY&country=USA');
      value = driver.find_element_by_xpath("(//a[@href='http://www.dec.ny.gov/'][contains(.,'New York Dept. of Environmental Conservation')])[2]");
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#181 NY Cities have Data courtsey links')
  
  #178 Verify Robots.txt cw 2020-04-08
  #   
  try:   
      driver.get(site + 'robots.txt');
      # pull out all the HTML source with one line of code!
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      #print(value)
      assert 'robots.txt' in value
      
      # Verfity NOT the standard Acquia robots.txt
      #print('acquia-sites.com' not in site);
      if 'acquia-sites.com' not in site and '.dev.dd' not in site:
        assert 'acquia-sites.com' not in value
        # Verify spider delay IS set to something
        assert 'Crawl-delay:' in value
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#178 Verify robots.txt on cloud.gov - Tomed Code')




  ###########
  # Completed Version 2.6 items BELOW here...
  ###########
  print(' ')
  print('         Version 2.6.0')
  ###########

  #276 Air Quality Awarenes Week Publications cw 2020-03-31
  #   
  try:   
      driver.get(site + 'airaware-publications');
      value = driver.find_element_by_xpath("//h1[contains(.,'2020 Air Quality Awareness Week')]");
      # 3rd document
      value = driver.find_element_by_xpath("//a[contains(.,'AQAW Template Instructions')]");
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#276 Air Quality Awarenes Week Publications')

  #275 Flag Program Tribal Updates cw 2020-03-31
  #    Updates for Title change cw 2020-08-15
  #   
  try:   
      driver.get(site + 'air-quality-flag-program-and-tribes-publications/');
      value = driver.find_element_by_xpath("//h1[contains(.,'Air Quality Flag Program for Tribes Publications')]");
      value.click();

      # verify we made it to the Publication page
      driver.find_element_by_xpath("//a[contains(.,'Tribal Air Quality Flag Program Packet')]");
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#275 Flag Program Tribal Updates - Content 45')

  #273 Upgrade Data Providers request
  #
  try:
      driver.get(site + '?city=Durham&state=NC&country=USA');
      # JS fix appears in the last JS referenced on the page... let's find that one and look in the Documentation
        # pull out all the HTML source with one line of code!
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      # find last script tag / hightest index value
      #     cloud.gov changed this directory... made shorter cw 2019-07-29
      index = value.rfind('/js/js_');
      #print (index)
      # find the URL to the target javascript
      #     cloud.gov changed the length; -6 characters... made shorter cw 2019-07-29
      JSpath = value[index:index+53]
      #print(JSpath)
      # This path always now on cloud.gov servers cw 2020-01-21
      sitePathString = "default/files"
      # and here is the complete JS url
      JSurl = site+"sites/"+sitePathString+JSpath
      # fetch the JS file
      #print(JSurl);
      driver.get(JSurl);
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      #print(value)
      # assert the string in the fix ...
      assert "if (radps.name !== reportingAreaName || radps.stateCode !== stateCode) {" in value 

      color.write("Pass: ","STRING")
  except Exception:
      color.write("FAIL: ","COMMENT")
  print('#273 Upgrade Data Providers request - Code - STI')

  #272 State Page URL in No Data dialog cw 2020-03-23
  #   
  try:   
      # delay for page load
      delay = 30
      # Load city without data to make the No Data dialog appear
      driver.get(site + '?city=Rio Grande City&state=TX&country=USA');
      # Wait for the No Data dialog to load
      try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//h3[contains(.,'No Data Available')]")))
      except TimeoutException:
        print ("Loading the No Data dialog took too long!")
      time.sleep(4);
      # using this? //a[@href='/state/?name=texas'][contains(.,'Texas state page')]
      element = driver.find_element_by_xpath("//a[@href='/state/?name=texas'][contains(.,'Texas state page')]");
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#272 State Page URL in No Data dialog - Code')


# The timestamp has been turned back "on" cw 2020-08-14
##  #270 Disable Leaflet Timestamp
##  #
##  driver.get(site + '?city=Durham&state=NC&country=USA');
##  try:  
##      # JS fix appears in the last JS referenced on the page... let's find that one and look in the Documentation
##        # pull out all the HTML source with one line of code!
##      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
##      # find last script tag / hightest index value
##      #     cloud.gov changed this directory... made shorter cw 2019-07-29
##      index = value.rfind('/js/js_');
##      #print (index)
##      # find the URL to the target javascript
##      #     cloud.gov changed the length; -6 characters... made shorter cw 2019-07-29
##      JSpath = value[index:index+53]
##      #print(JSpath)
##      # This path always now on cloud.gov servers cw 2020-01-21
##      sitePathString = "default/files"
##      # and here is the complete JS url
##      JSurl = site+"sites/"+sitePathString+JSpath
##      # fetch the JS file
##      #print(JSurl);
##      driver.get(JSurl);
##      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
##      #print(value)
##      # assert the string in the fix ...
##      assert "#270 - Disabling map timestamp" in value 
##
##      color.write("Pass: ","STRING")
##  except Exception:
##      color.write("FAIL: ","COMMENT")
##  print('#270 Disable Leaflet Timestamp- Code - STI')
  
  #269 Remove Media Partners cw 2020-03-16
  #
  try:   
      # delay for page load
      delay = 30;
      driver.get(site + 'partners/');
      # Wait for page to load
      myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//img[contains(@alt,'Air Now Logo')]")))
      #
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML");
      assert "Media Partners" not in value

      # REMOVING Media Partners, so you need to delete this subdirectory... tricky
      # /partners/media-partners/
      driver.get(site + 'partners/media-partners/');
      # Wait for page to load
      myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//img[contains(@alt,'Air Now Logo')]")))
      #
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML");
      assert "Media Partners" not in value
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#269 Remove Media Partners - Content 44')

  #256 Remove AirNow International & Teacher Workshop cw 2020-02-26
  #
  driver.get(site + 'airnow-international/');
  try:   
      element = driver.find_element_by_xpath("//h2[contains(.,'We want to help you find what you are looking for.')]");
      # remove teacher workshop page, too
      #driver.get(site + 'education/teachers/workshop-for-teachers/');
      #element = driver.find_element_by_xpath("//h1[@class='band-title-light'][contains(.,'Sorry, But This Web Page Is Not Available')]");
     
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#256 Remove AirNow International & Teacher Workshop')

  #259 Trends Page AQI Updates cw 2020-03-04
  #
  driver.get(site + '?city=Durham&state=NC&country=USA');
  # Wait for the fire map to load 2020-02-26
  delay = 30 # seconds
  try:
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//h1[contains(.,'Durham, NC')]")))
  except TimeoutException:
    print ("Loading the Dial Page took too long!")
        
  driver.get(site + 'trends');
  # Wait for the fire map to load 2020-02-26
  delay = 30 # seconds
  try:
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//div[@class='chartHeader'][contains(.,'Today')]")))
  except TimeoutException:
    print ("Loading the Trends Page took too long!")
 
  try:   
      driver.find_element_by_xpath("//a[@href='/aqi/aqi-basics/extremely-high-levels-of-pm25'][contains(.,'beyond')]");
      #print('beyond link is ok');
      # check for side legend broken icon cw 2020-03-31
      driver.find_element_by_xpath("//img[@src='/themes/anblue/images/Legend_Color_block.svg']");
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#259 Trends Page AQI Updates - STI/KMEA')

  #257 Remove Old Views cw 2020-02-26
  #
  try:   
      driver.get(site + 'taxonomy/term/1');
      value = driver.find_element_by_xpath("//div[@class='region region-content']").get_attribute("innerHTML");
      #print(value)
      assert "Subscribe to Home" not in value

      driver.get(site + 'data-providers/');
      value = driver.find_element_by_xpath("//div[@class='region region-content']").get_attribute("innerHTML");
      #print(value)
      assert "Data Providers " not in value

      driver.get(site + 'test-page/');
      value = driver.find_element_by_xpath("//div[@class='region region-content']").get_attribute("innerHTML");
      #print(value)
      assert "Test Band" not in value
      
      driver.get(site + 'teacher-view/');
      value = driver.find_element_by_xpath("//div[@class='region region-content']").get_attribute("innerHTML");
      #print(value)
      assert "Older Adults En Espanol Publications" not in value

      driver.get(site + 'older-adults-test/');
      value = driver.find_element_by_xpath("//div[@class='region region-content']").get_attribute("innerHTML");
      #print(value)
      assert "Older Adults En Espanol Publications" not in value

      driver.get(site + 'older-adults-test/');
      value = driver.find_element_by_xpath("//div[@class='region region-content']").get_attribute("innerHTML");
      #print(value)
      assert "Older Adults En Espanol Publications" not in value

      driver.get(site + 'older-adults-test/');
      value = driver.find_element_by_xpath("//div[@class='region region-content']").get_attribute("innerHTML");
      #print(value)
      assert "Older Adults En Espanol Publications" not in value

      driver.get(site + 'alert/');
      value = driver.find_element_by_xpath("//div[@class='region region-content']").get_attribute("innerHTML");
      #print(value)
      assert "class=\"container inner-card-style" not in value
      
      driver.get(site + 'beta-test-view/');
      value = driver.find_element_by_xpath("//div[@class='region region-content']").get_attribute("innerHTML");
      #print(value)
      assert "AirNow.gov Beta Test" not in value

      #What-is-Asthma (Content)
      driver.get(site + 'What-is-Asthma/');
      value = driver.find_element_by_xpath("//div[@class='region region-content']").get_attribute("innerHTML");
      #print(value)
      assert "What is Asthma" not in value

      #beta-test (Content)
      driver.get(site + 'beta-test/');
      value = driver.find_element_by_xpath("//div[@class='region region-content']").get_attribute("innerHTML");
      #print(value)
      assert "AirNow.gov Beta Test" not in value

      #beta-test (Content)
      driver.get(site + 'beta-test-known-issues/');
      value = driver.find_element_by_xpath("//div[@class='region region-content']").get_attribute("innerHTML");
      #print(value)
      assert "Beta Test Known Issues" not in value
      
      color.write("Pass: ","STRING") 
  except Exception:
      print(driver.current_url)
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      print(driver.current_url)
      color.write("FAIL: ","COMMENT")
  print('#257 Remove Old Views - Content')

  #258 Banner text not showing up in subpage headers cw 2020-03-05
  #   
  driver.get(site + 'fires/');
  try:   
      driver.find_element_by_xpath("//h2[contains(.,'Salmon River Fire')]");
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#258 Banner text not showing up in subpage headers')



  #253 Mobile Smoke Advisories cw 2020-03-27
  #   
  try:   
      driver.get(site + 'air-quality-and-health/fires/smoke-advisories/');
      # Updated: Not correct anymore cw 2021-05-10
      #value = driver.find_element_by_xpath("//div[@class='container-fluid']");
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#253 Mobile Smoke Advisories - Content 44')
  
  #252 Partners Right-side topic list cw 2020-03-27
  #   
  try:   
      driver.get(site + 'partners/tribal-partners');
      value = driver.find_element_by_xpath("//a[@href='/partners/tribal-partners']");
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#252 Partners Right-side topic list')

  #251 Create Fire Mask/Respirator Palm Cards Publications Section cw 2020-03-30
  #   
  try:   
      driver.get(site + 'all-publications/');
      value = driver.find_element_by_xpath("//h1[contains(.,'Fire Mask/Respirator Palm Cards')]");
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#251 Create Fire Mask/Respirator Palm Cards Publications Section - Content 44')

  #244 Esri Search Reporting Area Names Showing cw 2019-04-03
  # 
  driver.get(site + '?city=Durham&state=NC&country=USA');
  try:
      # Wait for the dial page to load cw 2019-08-08
      delay = 30 # seconds
      try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "(//h1[contains(.,'Durham, NC')])")))
      except TimeoutException:
        print ("Loading the dial took too long!")
      # END Wait for the dial page to load cw 2019-08-08
      
      # Type Reporting Area name works
      # Scroll the page down to make the Location box appear in the nav bar
      driver.execute_script("window.scrollTo(0, 800)")
      # verify metatags on About the Data page
      element = driver.find_element_by_xpath("//input[@id='location-input-nav_input']")
      element.send_keys('western new york reg')
      #Verify the Reporting Area name Still shows in the Esri search list
      delay = 20 # seconds
      try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "(//li[@data-index='0'][contains(.,'Western New York Region, NY')])[1]")))
      except TimeoutException:
        print ("Loading the Esri search list took too long!")
      # END Wait for the Town of Western New York
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#244 Esri Search Reporting Area Names Showing - STI - Code')

  
  ###########
  # cloud.gov & Dial w/forecast changes items BELOW here...
  ###########
  print(' ')
  print('         cloud.gov & Dial w/forecast changes')
  ###########

  # 163
  # Mobile Friendly Cards on Dial Page cw 2019-05-30
  # Updated xpath for Post Dial w/Forecast changes cw 2020-03-10
  driver.set_window_size(375, 667) # iPhone 6
  driver.get(site);
  try:
      # verify element are present
      element = driver.find_element_by_xpath("//h2[@class='text-center card-name'][contains(.,'Air Quality Flag Program')]")
      element = driver.find_element_by_xpath("//h2[@class='text-center card-name'][contains(.,'Email Notifications')]")
      
      color.write("Pass: ","STRING")
  except Exception:    
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#163 Mobile Friendly Cards on Dial Page - Content 44')
  driver.set_window_size(1024, 1024)

  #161
  # No Text Jump on Splash Screen cw 2019-09-25
  # Modified to work with Dial w/Forecast; now using DIV tag cw 2020-03-10
  #
  # It's a Mobile Test
  driver.set_window_size(375, 667);
  driver.get(site + '?city=Durham&state=NC&country=USA');
  try:
      # Wait for the dial page to load cw 2019-08-08
      delay = 30 # seconds
      try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "(//h1[contains(.,'Durham, NC')])")))
      except TimeoutException:
        print ("Loading the dial took too long!")
      # END Wait for the dial page to load cw 2019-08-08

      # find the City Name label
      element = driver.find_element_by_xpath("(//div[contains(@id,'location-input-mobile-gps')])");
      # check new Style value
      value = element.value_of_css_property('margin-bottom')
      #print(value)
      assert "-7px" in value
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#161 No Text Jump on Splash Screen - Code')
  driver.set_window_size(1024, 1024)
  
  # 136
  # Center Location Search on Mobile cw 2019-05-15
  # Rewrite to stop & restart browser in NCC to get back to No Location remembered cw 2019-06-05
  # updated cw 2020-03-10
  #
  #### restart the Selenium driver
  driver.close()
  driver.quit()
  #### rebuild the Selenium driver
  driver = webdriver.Chrome(chrome_options=chromeOptions, desired_capabilities=chromeOptions.to_capabilities())
  driver.implicitly_wait(30)
  driver.set_window_position(0, 0)
  driver.set_window_size(1024, 1024)

  # Try now
  driver.set_window_size(375, 667) # iPhone 6
  driver.get(site+'?city=Durham&state=NC&country=USA');
  
  # Wait for the Dial page to load cw 2019-08-08
  delay = 30 # seconds
  try:
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//img[@alt='Air Now Logo']")))
  except TimeoutException:
    print ("Loading the Dial page took too long!")
        
  try:
      # verify the element CSS value
      #print('here')
      element = driver.find_element_by_css_selector('.location-holder.splash-screen') # moded css selector; still working cw 2022-03-11
      #print('here')
      #print(element)
      value = element.value_of_css_property('top')
      #print(value)
      assert '140px' in value # revised; still working... new value... cw 2021-11-02
   
      color.write("Pass: ","STRING")
  except Exception:    
      color.write("FAIL: ","COMMENT")
  print('#136 Center Location Search on Mobile - Code')
  driver.set_window_size(1024,1024)

  #125
  # Change Leafet Button to National Maps cw 2019-04-02
  # Modified xpath to make lookup easier cw 2020-03-10
  #
  driver.get(site + '?city=Durham&state=NC&country=USA');
  try:
      assert 'AirNow.gov' in driver.title # Simple Page title cw 2021-01-25
      # verify National Maps Button item
      driver.find_element_by_xpath("//button[contains(.,'National Maps')]").click()

      # verify forwarded to the new Alias
      assert '/national-map' in driver.current_url
      
      color.write("Pass: ","STRING") 
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  except Exception:
      color.write("FAIL: ","COMMENT")
  print('#125 Change Leafet Button to National Maps - Code')

  #120
  # Monitors Near Me should display Monitors 
  driver.get(site + '?city=Durham&state=NC&country=USA');
  try:
      assert 'AirNow.gov' in driver.title # Simple Page title cw 2021-01-25
      # Click on Monitors Near Me button
      driver.find_element_by_xpath("//a[@id='air-quality-monitors-near-me']").click()
      #print('here')
      # Swicth to new tab
      driver.switch_to.window(driver.window_handles[1])
      # get url of the Interactive Map Tab
      element = driver.current_url
      # assert correct URL parameters
      assert '&clayer=none&mlayer=ozonepm' in element

      # close extra tab Method cw 2019-09-20
      driver.close();
      # Switch back to original Tab
      driver.switch_to.window(driver.window_handles[0]);

      color.write("Pass: ","STRING") 
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  except Exception:
      color.write("FAIL: ","COMMENT")
  print('#120 Monitors Near Me show Monitors')

  #119
  # Streamline the Maps and Data Band cw 2019-04-04
  # Updated xpath for 'Fires' cw 2020-03-10
  driver.get(site+'?city=Durham&state=NC&country=USA');
  try:
      assert 'AirNow.gov' in driver.title # Simple Page title cw 2021-01-25
      # verify Interactive Map Menu items
      driver.find_element_by_xpath("//img[contains(@alt,'US Department of State Seal')]")
      driver.find_element_by_xpath("//h2[@class='text-center card-name'][contains(.,'Fire')]")
      driver.find_element_by_xpath("//img[contains(@alt,'Archived Dates')]")
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  print('#119 Streamline the Maps and Data Band -- Content')
    
  # 66 
  # Update Links on For Partners page cw 2019-06-28
  # Updated URL cw 2020-03-10
  #
  driver.get(site + 'partners/for-partners');
  try:
      # verify element is NOT present. The link for Oklahoma city
      element = driver.find_element_by_xpath("//a[@href='/download-images'][contains(.,'Download Images')]")
       
      color.write("Pass: ","STRING")
  except Exception:    
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#66 Update Links on For Partners page - Content')




  ###########
  # Completed Version 2.5.1 items BELOW here...
  ###########
  print(' ')
  print('         Version 2.5.1')
  ###########

  # Links to Fire and Smoke Map cw 2020-02-26
  #   Replaced by #293 Update Links to fire.airnow.gov - Content 58 cw 2020-05-13
  #
##  driver.get(site);
##  try:   
##      element = driver.find_element_by_xpath("(//a[@class='main-link nav-link'][contains(.,'Fire and Smoke Map')])[2]")
##      #
##      driver.get(site + 'air-quality-and-health/fires-and-your-health');
##      element = driver.find_element_by_xpath("(//a[@href='https://airnowfire.app.cloud.gov'][contains(.,'Fire and Smoke Map')])[2]")
##        
##      color.write("Pass: ","STRING") 
##  except Exception:
##      color.write("FAIL: ","COMMENT")
##  except AssertionError:
##      color.write("FAIL: ","COMMENT")
##  print('Links to Fire and Smoke Map')
                                   
  # Fire and Smoke Map Available cw 2020-02-26
  #   
  try:
      # Updated to Custom Domain URL cw 2022-01-04
      driver.get('https://fire.airnow.gov/?lat=35.995420000000024&lng=-78.89643999999998&zoom=12');
      # Wait for the fire map to load 2020-02-26
      delay = 30 # seconds
      try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "(//span[@class='hidden-xs'][contains(.,'Fire and Smoke Map')])")))
      except TimeoutException:
        print ("Loading the Fire Map took too long!")
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  # Updated to Custom Domain URL cw 2022-01-04
  print('Fire and Smoke Map Available at fire.airnow.gov')

  # 211
  # Hover tooltip in IE11 cw 2020-02-24
  driver.get(site +'trends');
  try:
      # JS fix appears in the last JS referenced on the page... let's find that one and look in the Documentation
        # pull out all the HTML source with one line of code!
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      # find last script tag / hightest index value
      #     cloud.gov changed this directory... made shorter cw 2019-07-29
      index = value.rfind('/js/js_');
      #print (index)
      # find the URL to the target javascript
      #     cloud.gov changed the length; -6 characters... made shorter cw 2019-07-29
      JSpath = value[index:index+53]
      #print(JSpath)
      # This path always now on cloud.gov servers cw 2020-01-21
      sitePathString = "default/files"
      # and here is the complete JS url
      JSurl = site+"sites/"+sitePathString+JSpath
      # fetch the JS file
      #print(JSurl);
      driver.get(JSurl);
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      #print(value)
      # assert the string in the fix ...
      assert "const pointData = chartSeriesData[chartIdx].filter(function(row){" in value 

      color.write("Pass: ","STRING")
  except AssertionError:
      color.write("FAIL: ","COMMENT")    
  print('#211 Hover tooltip in IE11 - STI - Code')

  # 213
  # State page issues in IE11 cw 2020-02-24
  driver.get(site +'state/?name=utah');
  try:
      # JS fix appears in the last JS referenced on the page... let's find that one and look in the Documentation
        # pull out all the HTML source with one line of code!
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      # find last script tag / hightest index value
      #     cloud.gov changed this directory... made shorter cw 2019-07-29
      index = value.rfind('/js/js_');
      #print (index)
      # find the URL to the target javascript
      #     cloud.gov changed the length; -6 characters... made shorter cw 2019-07-29
      JSpath = value[index:index+53]
      #print(JSpath)
      # This path always now on cloud.gov servers cw 2020-01-21
      sitePathString = "default/files"
      # and here is the complete JS url
      JSurl = site+"sites/"+sitePathString+JSpath
      # fetch the JS file
      #print(JSurl);
      driver.get(JSurl);
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      #print(value)
      # assert the string in the fix ... 
      assert "#todayForecastDate\").append" in value 

      color.write("Pass: ","STRING")
  except AssertionError:
      color.write("FAIL: ","COMMENT")    
  print('#213 State page issues in IE11 - STI - Code')

  # 240
  # Data Courtesy of in IE11 cw 2020-02-24
  driver.get(site +'?city=Durham&state=NC&country=USA');
  try:
      # JS fix appears in the last JS referenced on the page... let's find that one and look in the Documentation
        # pull out all the HTML source with one line of code!
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      # find last script tag / hightest index value
      #     cloud.gov changed this directory... made shorter cw 2019-07-29
      index = value.rfind('/js/js_');
      #print (index)
      # find the URL to the target javascript
      #     cloud.gov changed the length; -6 characters... made shorter cw 2019-07-29
      JSpath = value[index:index+53]
      #print(JSpath)
      # This path always now on cloud.gov servers cw 2020-01-21
      sitePathString = "default/files"
      # and here is the complete JS url
      JSurl = site+"sites/"+sitePathString+JSpath
      # fetch the JS file
      #print(JSurl);
      driver.get(JSurl);
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      #print(value)
      # assert the string NOT in the fix ... 
      assert "dataProviders.includes(forecastProvider)" not in value

      color.write("Pass: ","STRING")
  except AssertionError:
      color.write("FAIL: ","COMMENT")    
  print('#240 Data Courtesy of in IE11 - STI - Code')

  # 242
  # Monitors and Trends buttons on mobile cw 2020-02-24
  #
  # It's a Mobile Test
  driver.set_window_size(375, 667);
  driver.get(site + '?city=Durham&state=NC&country=USA');
  try:
      # Wait for the dial page to load cw 2019-08-08
      delay = 30 # seconds
      try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "(//h1[contains(.,'Durham, NC')])")))
      except TimeoutException:
        print ("Loading the dial took too long!")
      # END Wait for the dial page to load cw 2019-08-08

      # Verify button present
      element = driver.find_element_by_xpath("//a[@id='mobile-air-quality-monitors-near-me']");

      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#242 Monitors and Trends buttons on mobile - STI - Code')
  #Desktop size
  driver.set_window_size(1024, 1024);  


  # Historic State JSON Data Available cw 2020-02-19
  #   
  month = str(int(datetime.datetime.fromtimestamp(ts).strftime('%m')));
  yesterday = str(int(datetime.datetime.fromtimestamp(ts).strftime('%d'))-1);
  # testing edge case   yesterday = 0;
  # only if first day of month; special date cw 2020-03-31
  if (yesterday == "0"):
    month = str(int(month) - 1);
    yesterday = "28";
  #print('http://airnowgovapi.com/andata/States/West_Virginia/2020/'+month+'/'+yesterday+'.json')
  try:
      driver.get('http://airnowgovapi.com/andata/States/West_Virginia/2020/'+month+'/'+yesterday+'.json');
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML");
      assert "error" not in value
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#250 Historic State JSON Data Available - STI Infrastrucure')

  #254 older-adults Link cw 2020-02-26
  #
  driver.get(site + 'air-quality-and-health/older-adults/');
  try:   
      element = driver.find_element_by_xpath("//h1[@class='band-title-light'][contains(.,'Older Adults and Air Quality')]")

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#254 older-adults Link')
  
  #255 ESRI Lookup after Reporting Area selection cw 2020-02-27
  #   
  driver.get(site + '?city=Durham&state=NC&country=USA');
  try:   
      element = driver.find_element_by_xpath("//input[@id='location-input_input']");
      element.send_keys('d');
      time.sleep(2);
      # select Dallas-Ft. Worh Reporting Area
      element = driver.find_element_by_xpath("//li[contains(.,'Dallas-Fort Worth, TX')]");
      element.click();
      time.sleep(2);
      # selcet "Dur"
      element = driver.find_element_by_xpath("//input[@id='location-input_input']");
      element.send_keys('dur');
      time.sleep(2);
      # verifiy the "Durham" is an option and click it
      element = driver.find_element_by_xpath("//li[contains(.,'Durham, NC, USA')]");
      element.click();
      time.sleep(2);
      # back to the Durham Dial... PASS
      element = driver.find_element_by_xpath("//h1[contains(.,'Durham, NC')]");
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#255 ESRI Lookup after Reporting Area selection - STI')

  ###########
  # Completed Version 2.5 items BELOW here...
  ###########
  print(' ')
  print('         Version 2.5')
  ###########

  #133 FAQ Link NOT Zendesk cw 2020-01-14
  #
  driver.get(site + '?city=Durham&state=NC&country=USA');
  try:
      element = driver.find_element_by_xpath("//a[@class='main-link nav-link'][contains(.,'FAQs')]")
      value = element.get_attribute("href");
      #print(value)
      assert "airnow.zendesk.com"  not in value

      # Check here too.
      driver.get(site + 'a-z-links');
      element = driver.find_element_by_xpath("//a[contains(.,'FAQs')]")
      value = element.get_attribute("href");
      #print(value)
      assert "airnow.zendesk.com"  not in value
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#133 FAQ Link NOT Zendesk - Content')

  # 185 Air Quality Flag Program Tome Issues
  #  two Band Contianer and four images are causing the issue
  driver.get(site+'?city=Durham&state=NC&country=USA');
  try:
      # The four broken images... in their NEW location with thier NEW files names
      # Image 1
      driver.get(site + 'sites/default/files/2019-08/pagina-para-colorear-small.jpg');
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML");
      assert "Not Found" not in value
      
      # Image 2
      driver.get(site + 'sites/default/files/2019-08/guia-a-de-la-calidad-small.jpg');
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML");
      assert "Not Found" not in value
      
      # Image 3
      driver.get(site + 'sites/default/files/2019-08/guia-para-el-inicio-rapido-small.jpg');
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML");
      assert "Not Found" not in value

      # Image 4
      driver.get(site + 'sites/default/files/2019-08/high_school_female_soccer_players_small.jpg');
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML");
      assert "Not Found" not in value

      # the Spanish Quick Start Guide
      driver.get(site + 'publications/air-quality-flag-program-en-espanol/quick-start-guide-spanish');
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML");
      #assert "Not Found" not in value
      # one more check for actual content on this one
      #assert "para el inicio" in value

      # Older Adults in Spanish broken link URL Redirect
      driver.get(site + 'publications/air-quality-flag-program-publications-en-espanol/adultos-mayores');
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML");
      #assert "Not Found" not in value
      
      # verify new link on the Spanish Four Steps page
      driver.get(site + 'four-steps-in-spanish');
      element = driver.find_element_by_xpath("//a[@href='/publications/air-quality-flag-program-en-espanol/quick-start-guide-spanish']")
      
      # verify new link on the Spanish Coordinators handbook
      driver.get(site + 'publications/air-quality-flag-program-en-espanol/coordinator-handbook-spanish');
      element = driver.find_element_by_xpath("//a[contains(.,'Manual para el coordinador del Programa de banderines')]")

      # verify the LAST created new URL Redirection link for tome cw 2019-09-05
      driver.get(site + 'publications/air-quality-flag-program-en-espanol/school-poster-in-spanish');
      element = driver.find_element_by_xpath("//a[contains(.,'Cartel para las escuelas')]")
      
      # Coloring book document
      driver.get(site + 'sites/default/files/2019-08/coloring_page-SPA.pdf');
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML");
      assert "Not Found" not in value
  
      # Older Adults document
      driver.get(site + 'sites/default/files/2019-08/older-adults_spa.pdf');
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML");
      assert "Not Found" not in value
      
      color.write("Pass: ","STRING")    
  except AssertionError:
      # Check for Drupal 404 page, else display the HTML of the missing value
      if driver.find_element_by_xpath("//h2[contains(.,'We want to help you find what you are looking for.')]"):
        print(' ')
        print('       ' + 'This Web Page Does Not Exist')
        print(driver.current_url )        
        print(' ')
      else:
        print(' ')
        print('       ' + value)
        print(' ')
      color.write("FAIL: ","COMMENT")
  except Exception:
      color.write("FAIL: ","COMMENT")
  print('#185 Air Quality Flag Program Tome Issues - Content')
  
  #188 Wildfire Publication Updates cw 2020-01-27
  # Modified Removing "Fires and your health" publication section cw 2020-02-25
  driver.get(site + 'wildland-fire-mask-respirator-palm-cards-publications/');
  try:
      # verity new document
      driver.get(site + 'publications/fire-mask-respirator-and-palm-cards-in-seven-languages/palm-card-english');
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#188 Wildfire Publication Updates - Content')

  #201 Alerts & Announcements cw 2020-01-16
  #
  try:
      #check for the existance of the Alerts page
      driver.get(site + 'alerts');
      #element = driver.find_element_by_xpath("//h1[contains(.,'Current Alerts')]")
     
      #check for the existance of the Announcments page
      driver.get(site + 'announcements');
      element = driver.find_element_by_xpath("//h1[contains(.,'Current Announcements')]")
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#201 Alerts & Announcements - Content')

  #226 Wildfire Smoke Course Promo Flyers cw 2020-01-14
  #
  driver.get(site + 'air-quality-and-health/online-training-for-health-professionals');
  try:
      # Two new links
      element = driver.find_element_by_xpath("//a[@href='/publications/health-professionals/promotional-post-card-for-the-particle-pollution-and-your-patients-health-on-line-training-course'][contains(.,'Promotional Palm Card for the Course')]")
      element = driver.find_element_by_xpath("//a[@href='/publications/health-professionals/promotional-flyer-for-the-particle-pollution-and-your-patients-health-on-line-training-course'][contains(.,'Promotional flyer for the course')]")

      #value = element.get_attribute("href");
      #print(value)
      #assert "" in value
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#226 Wildfire Smoke Course Promo Flyers - Code/Content')
  
  #227 "Why is Coco Orange?" Publications cw 2020-01-29
  # 
  driver.get(site + 'all-publications');
  try:
      # verify link is removed
      element = driver.find_element_by_xpath("//h1[contains(.,'Why is Coco Orange? Publications')]")
      #value = element.get_attribute("outerHTML");
      #print(value)
      #assert 'data-providers' not in value
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#227 \"Why is Coco Orange?\" Publications - Content')
  
  #231 Health Messages on Dial with Forecast cw 2020-01-16
  #
  driver.get(site + '?city=Durham&state=NC&country=USA');
  try:   
      # look for new div tagelement = driver.find_element_by_xpath("//div[@class='aqi']")      
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#231 Health Messages on Dial with Forecast - Code')

  #232 Repalce "Bird’s Eye View Lesson Plan" cw 2020-01-27
  #
  driver.get(site + 'publications/air-quality-flag-program-classroom-curriculum/birds-eye-view-lesson-plan');
  try:
      element = driver.find_element_by_xpath("//h2[@class='publication-title publication-download-link']")
      value = element.get_attribute("innerHTML");
      #print(value)
      assert "birds-eye-lesson-nov-2019.pdf" in value
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#232 Replace \"Bird’s Eye View Lesson Plan\" - Content')

  # 233
  # Remove Forecast Rollovers on Dial w/Forecast cw 2020-02-05
  driver.get(site+'?city=Durham&state=NC&country=USA');
  try:
      # JS fix appears in the last JS referenced on the page... let's find that one and look in the Documentation
        # pull out all the HTML source with one line of code!
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      # find last script tag / hightest index value
      #     cloud.gov changed this directory... made shorter cw 2019-07-29
      index = value.rfind('/js/js_');
      #print (index)
      # find the URL to the target javascript
      #     cloud.gov changed the length; -6 characters... made shorter cw 2019-07-29
      JSpath = value[index:index+53]
      #print(JSpath)
      # special string varies on localhost; otherwise it's "deafult"
      sitePathString = "default/files"
      if site == 'http://preview:Welcome1@airnowgov.dev.dd:8083/':
        sitePathString = "airnowgov.dev.dd/files"
      # and here is the complete JS url
      JSurl = site+"sites/"+sitePathString+JSpath
      # fetch the JS file
      driver.get(JSurl);
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      #print(value)
      # assert the string in the fix ... Line 64 of pageloader.js
      assert "Tooltips.createTip(\".aq-dial .bottom-half .forecast-aq-container .today-aq-data" not in value 

      color.write("Pass: ","STRING")
  except AssertionError:
      color.write("FAIL: ","COMMENT")    
  print('#233 Remove Forecast Rollovers on Dial w/Forecast - STI - Code')

  #234 Restore Data Courtesy of Feature cw 2019-09-09
  # 
  driver.get(site + '?city=Durham&state=NC&country=USA');
  try:
      # Wait for the dial page to load cw 2019-08-08
      delay = 30 # seconds
      try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "(//h1[contains(.,'Durham, NC')])")))
      except TimeoutException:
        print ("Loading the dial took too long!")
      # END Wait for the dial page to load cw 2019-08-08

      # verify link is removed
      element = driver.find_element_by_xpath("//b[contains(.,'Data courtesy of')]")
      #value = element.get_attribute("outerHTML");
      #print(value)
      #assert 'data-providers' not in value
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#234 Restore \"Data Courtesy of\" Feature--Testing Durham, NC')

  #
  # No Longer works due to new New GeoLocation Dialog box cw 2021-09-24
  #
##  #235 Splash Page Update and EPA Logo cw 2020-01-30
##  #
##  try:
##      # Reset the driver to clear the session variables and get to the Splash screen
##      driver.close();
##      driver = webdriver.Chrome(chrome_options=chromeOptions, desired_capabilities=chromeOptions.to_capabilities())
##      driver.implicitly_wait(30)
##      driver.set_window_position(0, 0)
##      driver.set_window_size(1024, 1024)
##      driver.get(site);
##     
##      #Splash text
##      element = driver.find_element_by_xpath("(//h1[contains(.,'Get air quality data where you live')])")
##      # EPA Logo at lower left
##      element = driver.find_element_by_xpath("//img[@alt='EPA']")
##
##      color.write("Pass: ","STRING") 
##  except Exception:
##      color.write("FAIL: ","COMMENT")
##  except AssertionError:
##      color.write("FAIL: ","COMMENT")
##  print('#235 Splash Page Update and EPA Logo - STI - Code')
 
  ###########
  # Completed Version 2.4 items BELOW here...
  ###########
  print(' ')
  print('         Version 2.4')
  ###########


  # Dial with Forecast cw 2019-11-26
  #
  driver.get(site + '?city=Durham&state=NC&country=USA');
  try:
      element = driver.find_element_by_xpath("(//img[contains(@class,'aq-dial-background')])[2]")
      value = element.get_attribute("src");
      #print(value)
      assert "/dial2/" in value
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('Dial with Forecast - STI - Code')

  # 205
  # Improve display when forecasts are missing cw 2019-11-26
  # .current-aq-band-row .pollutant-card.primary-pollutant-card
  # 
  driver.get(site + '?city=Alexandria&state=LA&country=USA');
  try:
      # Wait for the dial page to load cw 2019-08-08
      delay = 20 # seconds
      try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "(//h1[contains(.,'Alexandria, LA')])")))
      except TimeoutException:
        print ("Loading the dial took too long!")
      # END Wait for the dial page to load cw 2019-08-08

      # find the City Name label
      element = driver.find_element_by_xpath("//div[@class='pollutant-card primary-pollutant-card show-none-text']");
      # check new Style value
      value = element.value_of_css_property('border')
      #print(value)
      assert "5px" in value
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#205 Improve display when forecasts are missing - STI - Code')

  # 206
  # State page no data item click cw 2019-11-26
  driver.get(site+'?city=Durham&state=NC&country=USA');
  try:
      # JS fix appears in the last JS referenced on the page... let's find that one and look in the Documentation
        # pull out all the HTML source with one line of code!
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      # find last script tag / hightest index value
      #     cloud.gov changed this directory... made shorter cw 2019-07-29
      index = value.rfind('/js/js_');
      #print (index)
      # find the URL to the target javascript
      #     cloud.gov changed the length; -6 characters... made shorter cw 2019-07-29
      JSpath = value[index:index+53]
      #print(JSpath)
      # special string varies on localhost; otherwise it's "deafult"
      sitePathString = "default/files"
      if site == 'http://preview:Welcome1@airnowgov.dev.dd:8083/':
        sitePathString = "airnowgov.dev.dd/files"
      # and here is the complete JS url
      JSurl = site+"sites/"+sitePathString+JSpath
      # fetch the JS file
      driver.get(JSurl);
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      #print(value)
      # assert the string in the fix ... Line 64 of pageloader.js
      assert "if (!reportingAreaData || reportingAreaData !== AirNowGov.GLOBALS.getUrlVar(\"reportingArea\")) {" in value 

      color.write("Pass: ","STRING")
  except AssertionError:
      color.write("FAIL: ","COMMENT")    
  print('#206 State page no data item click - STI - Code')

  # 207
  # Multiple tabs loss of reporting area name cw 2019-11-26
  driver.get(site+'?city=Durham&state=NC&country=USA');
  try:
      # JS fix appears in the last JS referenced on the page... let's find that one and look in the Documentation
        # pull out all the HTML source with one line of code!
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      # find last script tag / hightest index value
      #     cloud.gov changed this directory... made shorter cw 2019-07-29
      index = value.rfind('/js/js_');
      #print (index)
      # find the URL to the target javascript
      #     cloud.gov changed the length; -6 characters... made shorter cw 2019-07-29
      JSpath = value[index:index+53]
      #print(JSpath)
      # special string varies on localhost; otherwise it's "deafult"
      sitePathString = "default/files"
      if site == 'http://preview:Welcome1@airnowgov.dev.dd:8083/':
        sitePathString = "airnowgov.dev.dd/files"
      # and here is the complete JS url
      JSurl = site+"sites/"+sitePathString+JSpath
      # fetch the JS file
      driver.get(JSurl);
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      #print(value)
      # assert the string in the fix ... Line 550 0f reportingarea.js
      assert "else if (forecastData.length" in value 

      color.write("Pass: ","STRING")
  except AssertionError:
      color.write("FAIL: ","COMMENT")    
  print('#207 Multiple tabs loss of reporting area name - STI - Code')
  
  # 219
  # AQI Colors Consistant cw 2019-11-26
  #
  driver.get(site + 'themes/anblue/images/Legend_Color_block.svg');
  try:
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      #print(value)
      # assert the string in the fix ... Line 64 of pageloader.js
      assert "xmlns:inkscape=" in value 
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#219 AQI Colors Consistant - STI - Code')

  # 224
  # Remove Spaces in Health Messages cw 2019-12-02
  driver.get(site);
  try:
      # JS fix appears in the last JS referenced on the page... let's find that one and look in the Documentation
        # pull out all the HTML source with one line of code!
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      # find last script tag / hightest index value
      #     cloud.gov changed this directory... made shorter cw 2019-07-29
      index = value.rfind('/js/js_');
      #print (index)
      # find the URL to the target javascript
      #     cloud.gov changed the length; -6 characters... made shorter cw 2019-07-29
      JSpath = value[index:index+53]
      #print(JSpath)
      # This path always now on cloud.gov servers cw 2020-01-21
      sitePathString = "default/files"
      # and here is the complete JS url
      JSurl = site+"sites/"+sitePathString+JSpath
      # fetch the JS file
      driver.get(JSurl);
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      #print(value)
      # assert the string in the fix ... Line 64 of pageloader.js
      assert "AirNowDrupal#224" in value 

      color.write("Pass: ","STRING")
  except AssertionError:
      color.write("FAIL: ","COMMENT")    
  print('#224 Remove Spaces in Health Messages - KMEA - Code/Content')
  
  #sys.exit()
  
  ###########
  # Completed Version 2.3 items BELOW here...
  ###########
  print(' ')
  print('         Version 2.3')
  ###########

  # 202 
  #  AirNow Messaging Updates - Code cw 2019-10-09
  # 
  driver.get(site+'?city=Durham&state=NC&country=USA');
  try:
      # JS fix appears in the last JS referenced on the page... let's find that one and look in the Documentation
      # pull out all the HTML source with one line of code!
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      #print(value)
      # find last script tag / hightest index value
      index = value.rfind('/files/js/js_');
      # find last script tag / hightest index value
      #     cloud.gov changed this directory... made shorter cw 2019-07-29
      index = value.rfind('/js/js_');
      #print (index)
      # find the URL to the target javascript
      #     cloud.gov changed the length; -6 characters... made shorter cw 2019-07-29
      JSpath = value[index:index+53]
      #print(JSpath)
      # This path always now on cloud.gov servers cw 2020-01-21
      sitePathString = "default/files"
      # and here is the complete JS url
      JSurl = site+"sites/"+sitePathString+JSpath
      #print(JSurl)
      # fetch the JS file
      driver.get(JSurl);
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      #print(value)
      # assert the string that was fixed 
      assert 'Current Air Quality is the most recent air quality in your area. ' in value # cw 2019-10-09

      color.write("Pass: ","STRING") 
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  except Exception:
      color.write("FAIL: ","COMMENT")
  print('#202 AirNow Messaging Updates - Code ')
  
  #196
  # GeoLocate for Parameter based State URLs - STI/KMEA cw 2019-09-20
  # 
  driver.get(site + '?city=Durham&state=NC&country=USA');
  try:
      # Wait for the dial page to load cw 2019-08-08
      delay = 30 # seconds
      try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "(//h1[contains(.,'Durham, NC')])")))
      except TimeoutException:
        print ("Loading the dial for the city took too long!")
      # END Wait for the dial page to load cw 2019-08-08

      # a STATE NAME works
      element = driver.find_element_by_xpath("//input[@id='location-input_input']");
      element.send_keys('Utah');
      element.send_keys(Keys.ENTER);
      #Verity the Utah page
      delay = 30 # seconds
      try:
        # updated to Salt Lake City cw 2022-01-04
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//b[contains(.,'Salt Lake City')]")))
      except TimeoutException:
        print ("Loading the dial for the state took too long!")
      # END Wait for the Utah page to load cw 2020-01-16
      
      # a STATE TWO LETTER works
      # Scroll the page down to make the Location box appear in the nav bar
      driver.execute_script("window.scrollTo(0, 800)")
      # verify metatags on About the Data page
      element = driver.find_element_by_xpath("//input[@id='location-input-nav_input']")
      element.send_keys('NC')
      element.send_keys(Keys.ENTER)
      #Verify the North Carolina page
      delay = 30 # seconds
      try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//b[contains(.,'Alexander County')]")))
      except TimeoutException:
        print ("Loading the dial took too long!")
      # END Wait for the North Carolina page to load cw 2020-01-16
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#196 GeoLocate for Parameter based State URLs - STI/KMEA - Code')

  #193
  # Disable Breadcrumbs Block - Content cw 2019-09-17
  # 
  driver.get(site + 'aqi/aqi-basics');
  try:
      # verify links are updated
      element = driver.find_element_by_xpath("//div[@class='region region-froze-nav']")
      value = element.get_attribute("innerHTML");
      #print(value)
      assert '<ol class="breadcrumb">' not in value
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#193 Disable Breadcrumbs Block - KMEA - Content')


  #192 Links in pop-ups on Mobile - Code cw 2019-09-19; mods cw 2022-03-11
  #   Changes at
  #       1) Code in "base.js" Line 78
  #       2) Code in "current_aq_data_helper.js" line 178 & 182
  #       3) Content in "Home Current AQ Band"/ Copy Entire HTML Source in Field "Home Map Icon Tooltip"
  # 
  # It's a Mobile Test
  driver.set_window_size(375, 667);
  driver.get(site + '?city=Durham&state=NC&country=USA');
  try:
      # Wait for the dial page to load cw 2019-08-08
      delay = 30 # seconds
      try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//div[contains(.,'Durham, NC')]")))
      except TimeoutException:
        print ("Loading the dial page took too long!")
      # END Wait for the dial page to load cw 2019-08-08
      
      # Scroll the page down to make room for the pop-up
      driver.execute_script("window.scrollTo(0, 800)")
      time.sleep(5)  # Added cw 2022-03-11
      # Open the tippy with links
      element = driver.find_element_by_xpath("//img[contains(@alt,'Map Info Icon')]");
      # click the pop-up
      element.click();
  
      # Wait for the NowCast AQI page to load cw 2019-08-08
      delay = 30 # seconds
      try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "//a[contains(.,'NowCast AQI')]")))
      except TimeoutException:
        print ("Loading the NowCast AQI page took too long!")

      # Find & Click the Link
      element = driver.find_element_by_xpath("//a[contains(.,'NowCast AQI')]");
      element.click()
      # a little extra time cw 2022-03-11
      time.sleep(10)
      # Swicth to new tab
      driver.switch_to.window(driver.window_handles[1]);
      #verify the correct URL opened
      value = driver.current_url
      #print(value)
      assert 'nowcast' in value

      # close extra tab Method cw 2019-09-20
      driver.close();
      # Switch back to original Tab
      driver.switch_to.window(driver.window_handles[0]);

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#192 Links in pop-ups on Mobile - KMEA - Code/Content')
  #Desktop size
  driver.set_window_size(1024, 1024)

  
  # 191
  # Two word state URL parameter as "-" cw 2019-09-11
  # 
  driver.get(site + 'state/?name=north-carolina');
  try:
      # verify it loaded Noth Carolina's Page
      element = driver.find_element_by_xpath("//b[contains(.,'Alexander County')]") # Using new Reporting areas cw 2020-01-21
      
      color.write("Pass: ","STRING") 
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  except Exception:
      color.write("FAIL: ","COMMENT")
  print('#191 Two word state URL parameter as \'-\' - STI/KMEA - Code')
  
  #190
  # Remove "Data Courtesy of" Link cw 2019-09-09
  # Now using Petaluma, CA since "Courtesy of" sytem is under repair cw 2020-01-21
  # 
  driver.get(site + '?city=Petaluma&state=CA&country=USA');
  try:
      # Wait for the dial page to load cw 2019-08-08
      delay = 20 # seconds
      try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "(//h1[contains(.,'Petaluma, CA')])")))
      except TimeoutException:
        print ("Loading the dial took too long!")
      # END Wait for the dial page to load cw 2019-08-08

      # verify link is removed
      element = driver.find_element_by_xpath("//b[contains(.,'Data courtesy of')]")
      value = element.get_attribute("outerHTML");
      #print(value)
      assert 'data-providers' not in value
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#190 Remove \'Data Courtesy of\' Link')
  
  #186
  # Edits to Beyond Index page - Content cw 2019-09-16
  # 
  driver.get(site + 'aqi/aqi-basics/extremely-high-levels-of-pm25');
  try:
      # verify "Beijing Text" was updated
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML");
      assert "or your local air agency website for the most recent hourly air quality conditions." in value

      # verify Wildfire Publiction link was updated
      element = driver.find_element_by_xpath("//a[@href='/wildfire-smoke-guide-publications'][contains(.,'Wildfire Smoke, A Guide for Public Health Officials, 2019')]")

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#186 Edits to Beyond Index page - Content')

  # 185 Air Quality Flag Program Tome Issues
  #  two Band Contianer and four images are causing the issue
  driver.get(site);
  try:
      # The four broken images... I their NEW location with thier NEW files names
      # Image 1
      driver.get(site + 'sites/default/files/2019-08/pagina-para-colorear-small.jpg');
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML");
      assert "Not Found" not in value
      
      # Image 2
      driver.get(site + 'sites/default/files/2019-08/guia-a-de-la-calidad-small.jpg');
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML");
      assert "Not Found" not in value
      
      # Image 3
      driver.get(site + 'sites/default/files/2019-08/guia-para-el-inicio-rapido-small.jpg');
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML");
      assert "Not Found" not in value

      # Image 4
      driver.get(site + 'sites/default/files/2019-08/high_school_female_soccer_players_small.jpg');
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML");
      assert "Not Found" not in value

      # the Spanish Quick Start Guide
      driver.get(site + 'publications/air-quality-flag-program-en-espanol/quick-start-guide-spanish');
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML");
      #assert "Not Found" not in value
      # one more check for actual content on this one
      #assert "para el inicio" in value

      # Older Adults in Spanish broken link URL Redirect
      driver.get(site + 'publications/air-quality-flag-program-publications-en-espanol/adultos-mayores');
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML");
      #assert "Not Found" not in value
      
      # verify new link on the Spanish Four Steps page
      driver.get(site + 'four-steps-in-spanish');
      element = driver.find_element_by_xpath("//a[@href='/publications/air-quality-flag-program-en-espanol/quick-start-guide-spanish']")
      
      # verify new link on the Spanish Coordinators handbook
      driver.get(site + 'publications/air-quality-flag-program-en-espanol/coordinator-handbook-spanish');
      element = driver.find_element_by_xpath("//a[contains(.,'Manual para el coordinador del Programa de banderines')]")

      # verify the LAST created new URL Redirection link for tome cw 2019-09-05
      driver.get(site + 'publications/air-quality-flag-program-en-espanol/school-poster-in-spanish');
      element = driver.find_element_by_xpath("//a[contains(.,'Cartel para las escuelas')]")
      
      # Coloring book document
      driver.get(site + 'sites/default/files/2019-08/coloring_page-SPA.pdf');
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML");
      assert "Not Found" not in value
  
      # Older Adults document
      driver.get(site + 'sites/default/files/2019-08/older-adults_spa.pdf');
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML");
      assert "Not Found" not in value
      
      color.write("Pass: ","STRING")    
  except AssertionError:
      # Check for Drupal 404 page, else display the HTML of the missing value
      if driver.find_element_by_xpath("//h2[contains(.,'We want to help you find what you are looking for.')]"):
        print(' ')
        print('       ' + 'This Web Page Does Not Exist')
        print(driver.current_url )        
        print(' ')
      else:
        print(' ')
        print('       ' + value)
        print(' ')
      color.write("FAIL: ","COMMENT")
  except Exception:
      color.write("FAIL: ","COMMENT")
  print('#185 Air Quality Flag Program Tome Issues - Content')

  # 184
  # Four Steps to Starting a Flag Program fixes - Content cw 2019-10-02
  # 
  driver.get(site + 'four-steps-to-starting-an-air-quality-flag-program');
  try:
      ## As of Content Version 51 we now link back to the Coldfusion website cw 2020-04-21
      # verify correct link to registration page
      #element = driver.find_element_by_xpath("//a[@href='https://geopub.epa.gov/flagregistration/'][contains(.,'online registration form')]")

      # verify correct link to flag ordeing page
      #//a[contains(.,'Flag Ordering Tips')]
      element = driver.find_element_by_xpath("//a[contains(.,'Flag Ordering Tips')]")
      value = element.get_attribute("href")
      #print(value)
      assert "/node/1171" not in value

      # Also check the Spanish Page
      #  Pointed BACK to ColdFusion with Version 2.7.0
      ##      driver.get(site + 'four-steps-in-spanish/');
      ##      # verify correct link to registration page
      ##      element = driver.find_element_by_xpath("//a[@href='https://geopub.epa.gov/flagregistration/'][contains(.,'ormulario de inscripción en internet')]")
      
      color.write("Pass: ","STRING") 
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  except Exception:
      color.write("FAIL: ","COMMENT")
  print('#184 Four Steps to Starting a Flag Program fixes - Content')
  
  #172
  # Clean up extraneous charactors in the AQI Basics page - Content cw 2019-09-16
  # 
  driver.get(site + 'aqi/aqi-basics');
  try:
      # Verify cleaned up code
      element = driver.find_element_by_xpath("//tr[contains(.,'Moderate')]");
      value = element.get_attribute("outerHTML");
      #print(value)
      assert "color:black; font-family: &quot;Arial&quot;" not in value
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#172 Clean up extraneous characters in the AQI Basics page -  Content')

  # 171 
  #  Beyond AQI Modifications - Code/Content cw 2019-10-10
  # 
  driver.get(site);
  try:
      # JS fix appears in the last JS referenced on the page... let's find that one and look in the Documentation
      # pull out all the HTML source with one line of code!
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      #print(value)
      # find last script tag / hightest index value
      index = value.rfind('/files/js/js_');
      # find last script tag / hightest index value
      #     cloud.gov changed this directory... made shorter cw 2019-07-29
      index = value.rfind('/js/js_');
      #print (index)
      # find the URL to the target javascript
      #     cloud.gov changed the length; -6 characters... made shorter cw 2019-07-29
      JSpath = value[index:index+53]
      #print(JSpath)
      # This path always now on cloud.gov servers cw 2020-01-21
      sitePathString = "default/files"
      # and here is the complete JS url
      JSurl = site+"sites/"+sitePathString+JSpath
      #print(JSurl)
      # fetch the JS file
      driver.get(JSurl);
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      #print(value)
      # assert the string that was fixed 
      assert '// Added Beyond AQI cw 2019-10-10' in value # cw 2019-10-10

      color.write("Pass: ","STRING") 
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  except Exception:
      color.write("FAIL: ","COMMENT")
  print('#171 Beyond AQI Modifications - Code/Content')
  
  #170
  #  Remove extra spaces in Health Messages - Code
  driver.get(site);
  try:
      # JS fix appears in the last JS referenced on the page... let's find that one and look in the Documentation
      # pull out all the HTML source with one line of code!
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      #print(value)
      # find last script tag / hightest index value
      index = value.rfind('/files/js/js_');
      # find last script tag / hightest index value
      #     cloud.gov changed this directory... made shorter cw 2019-07-29
      index = value.rfind('/js/js_');
      #print (index)
      # find the URL to the target javascript
      #     cloud.gov changed the length; -6 characters... made shorter cw 2019-07-29
      JSpath = value[index:index+53]
      #print(JSpath)
      # This path always now on cloud.gov servers cw 2020-01-21
      sitePathString = "default/files"
      # and here is the complete JS url
      JSurl = site+"sites/"+sitePathString+JSpath
    
      # fetch the JS file
      driver.get(JSurl);
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      #print(value)
      # assert the string that was fixed cw 2019-09-09
      assert '&lt;b&gt;Everyone&lt;/b&gt; should stay indoors and reduce activity levels.' in value

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#170 Remove extra spaces in Health Messages - Code/Content')

  #151
  # Fix for Maine reporting areas - STI cw 2019-09-12
  # 
  driver.get(site + 'state/?name=maine');
  try:
      # verify link is removed
      element = driver.find_element_by_xpath("//b[contains(.,'Downeast Coast')]")
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#151 Fix for Maine reporting areas - STI')

  # 141 Mobile i icon on Air Quality Forecast title cw 2019-09-12
  # It's a Mobile Test
  driver.set_window_size(375, 667)
  driver.get(site);
  try:
      # JS fix appears in the last JS referenced on the page... let's find that one and look in the Documentation
      # pull out all the HTML source with one line of code!
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      #print(value)
      # find last script tag / hightest index value
      index = value.rfind('/files/js/js_');
      # find last script tag / hightest index value
      #     cloud.gov changed this directory... made shorter cw 2019-07-29
      index = value.rfind('/js/js_');
      #print (index)
      # find the URL to the target javascript
      #     cloud.gov changed the length; -6 characters... made shorter cw 2019-07-29
      JSpath = value[index:index+53]
      #print(JSpath)
      # This path always now on cloud.gov servers cw 2020-01-21
      sitePathString = "default/files"
      # and here is the complete JS url
      JSurl = site+"sites/"+sitePathString+JSpath
      
      # fetch the JS file
      driver.get(JSurl);
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      #print(value)
      # assert the string that was fixed cw 2019-09-09
      assert 'Mobile i icon on Air Quality Forecast title cw 2019-09-12' in value
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#141 Mobile i icon on Air Quality Forecast title - Code')
  driver.set_window_size(1024, 1024)

  #140
  # Updated How to Use this Site cw 2019-09-17
  # 
  driver.get(site + 'how-to-use-this-site');
  try:
      # verify page Current Air Quality graphic is updated
      element = driver.find_element_by_xpath("//li[contains(.,'The primary pollutant and steps you can take to minimize your exposure to air pollution.')]")
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#140 Updated How to Use this Site - Content')

## As of Content Version 51 we now link back to the Coldfusion website cw 2020-04-21
##  #135
##  # Link to new Flag Program registration page & participate list - Content cw 2019-08-12
##  # 
##  driver.get(site + 'air-quality-flag-program');
##  try:
##      # verify links are updated
##      element = driver.find_element_by_xpath("//a[@href='https://geopub.epa.gov/flagregistration/participants/'][contains(.,'Participating Organizations')]")
##      element = driver.find_element_by_xpath("//a[@href='https://geopub.epa.gov/flagregistration/'][contains(.,'Register Your Organization')]");
##
##      # Spainsh page, too
##      driver.get(site + 'air-quality-flag-program-in-spanish');
##      element = driver.find_element_by_xpath("//a[@href='https://geopub.epa.gov/flagregistration/participants/'][contains(.,'Organizaciones participantes')]")
##      element = driver.find_element_by_xpath("//a[@href='https://geopub.epa.gov/flagregistration/'][contains(.,'Inscriba a su organización')]");
##
##      color.write("Pass: ","STRING") 
##  except Exception:
##      color.write("FAIL: ","COMMENT")
##  except AssertionError:
##      color.write("FAIL: ","COMMENT")
##  print('#135 Link to new Flag Program registration page - Content')
 
   
##  #122 Editable location box in black bar - STI cw 2019-07-02
##  #     This item is NOT completed!
##  # 
##  driver.get(site + '/?city=Durham&state=NC&country=USA');
##  try:
##      # Scroll the page down to make the Location box appear in the nav bar
##      driver.execute_script("window.scrollTo(0, 555)")
##      # verify metatags on About the Data page
##      element = driver.find_element_by_xpath("//input[contains(@id,'location-input-nav_input')]")
##      element.send_keys('Charlotte, NC')
##      element.send_keys(Keys.ENTER)
##      # should now change to Charlottee, NC  
##      element = driver.find_element_by_xpath("//a[@href='/'][contains(.,'Charlotte, NC')]")
##      
##      color.write("Pass: ","STRING") 
##  except Exception:
##      color.write("FAIL: ","COMMENT")
##  except AssertionError:
##      color.write("FAIL: ","COMMENT")
##  print('#122 Editable location box in black bar - STI - code')
      




##
##  # 141
##  # Mobile close boxes on Pop-ups cw 2019-06-20
##  driver.set_window_size(375, 667) # iPhone 6
##  driver.get(site + '/?city=Durham&state=NC&country=USA');
##  try:
##      # Open the Tippy for Current Air Quality
##      element = driver.find_element_by_xpath("//h1[@class='band-title-white'][contains(.,'Air Quality Forecast')]")
##      value = element
##      print(value)
##      #assert 'x-placement="bottom"' in value
##      
##      color.write("Pass: ","STRING")
##  except Exception:    
##      color.write("FAIL: ","COMMENT")
##  except AssertionError:
##      color.write("FAIL: ","COMMENT")
##  print('#141 Mobile close boxes on Pop-ups - Content? Code?')
##  driver.set_window_size(1024, 1024)






  
  
  
  #40 Metatag
  # Metatag Module using dcterms cw 2019-04-22
  #driver.get(site + '/about-the-data');
  #try:
      # verify metatags on About the Data page
      #assert 'About the Data | AirNow.gov' in driver.title
      #element = driver.find_element_by_xpath("//meta[@name='dcterms.title' and @content='About the Data | AirNow.gov']")
      #element = driver.find_element_by_xpath("//meta[@name='dcterms.description' and @content='Measurements are collected by state, local or tribal monitoring agencies using federal reference or equivalent monitoring methods approved by EPA.']")
      
      #color.write("Pass: ","STRING") 
  #except Exception:
      #color.write("FAIL: ","COMMENT")
  #except AssertionError:
      #color.write("FAIL: ","COMMENT")
  #print('v2.?.? #94 R23.8 Metatag Module using dcterms - Content')


  
  #
  # Use these to short cut and stop testing when testing new tests
  #driver.close()
  #driver.quit()
  #sys.exit()
  #
  ###########
  # Completed Version 2.3.0 items BELOW here...
  ###########
  #print(' ')
  #print('         Version 2.3.0')
  ###########
  #print(' ')
  #print('None yet.')





  print(' ')
  print('         Misc. Cloud Tests');
  # Misc cloud.gov tests cw 2019-07-22
  # 
  driver.get(site + '/?city=Durham&state=NC&country=USA');
  try:
      # Sample Profile picture -- Public Path
      driver.get('https://cg-f4d7e578-4b57-4941-95f8-331b8b5881c6.s3.us-gov-west-1.amazonaws.com/s3fs-public/styles/thumbnail/public/pictures/2019-07/VelociraptorNoText.jpg?itok=chuw1_lX');
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML");
      #print (value)
      assert "Not Found" in value
      # teachers workshop picture
      driver.get('https://cg-f4d7e578-4b57-4941-95f8-331b8b5881c6.s3.us-gov-west-1.amazonaws.com/s3fs-public/2019-07/workshop-280-150.jpg');
      element = driver.find_element_by_xpath("//img[@alt='https://cg-f4d7e578-4b57-4941-95f8-331b8b5881c6.s3.us-gov-west-1.amazonaws.com/s3fs-public/2019-07/workshop-280-150.jpg']");
      # Important JS file
      driver.get(site + '/themes/custom/anblue/js/navigation/navigation_helper.js');
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML");
      assert "/* AirnowDrupal # 122 Nav Bar redirects to Dial page from Content pages cw 2019-05-17 */" in value
		  
      ## Exception is reversed !!! ###
      color.write("FAIL: ","COMMENT")
  except Exception:
      color.write("Pass: ","STRING")
      ## Exception is reversed !!! ###
  print('Misc cloud.gov tests - Cloud.gov')

  # 158
  # Broken links on Dev and Stage cw 2019-06-26
  # ALIAS must be all lower case for TOME; added addtional Page to this test cw 2019-09-09
  driver.get(site + 'air-quality-and-health/fires-and-your-health');
  try:
      # verify link is correct
      element = driver.find_element_by_xpath("//a[contains(.,'Wildfire Smoke, A Guide for Public Health Officials')]")
      value = element.get_attribute("href")
      #print(value)
      assert '/wildfire-smoke-guide-publications' in value

      # verify addtional link is correct cw 2019-09-09
      driver.get(site + 'air-quality-and-health/your-health');
      element = driver.find_element_by_xpath("//img[contains(@alt,'Girl Inhaler Bus')]")
      
      color.write("Pass: ","STRING")
  except Exception:    
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#158 Broken links on Dev and Stage - Content')
  
  # 154
  # Dial page and interactive map bug - STI cw 2019-06-06
  #  Inproved Test to be independant of screen size; use a litle cooordindate "closeness" cw 2020-04-08
  #
  driver.get(site + '?city=Detroit&state=MI&country=USA');
  driver.get(site + '?city=Kansas City&state=KS&country=USA');
  driver.get(site + '?city=Detroit&state=MI&country=USA');

  # Wait for the dial page to load cw 2019-08-08
  delay = 20 # seconds
  try:
    myElem0 = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "(//h1[contains(.,'Detroit, MI')])")))
  except TimeoutException:
    print ("Loading the dial took too long!")
  # END Wait for the dial page to load cw 2019-08-08
  
  try:
      # go to a different city ... far East... Boston, MA
      driver.get(site + '?city=Boston&state=MA&country=USA');
      # Wait for the dial page to load cw 2019-08-08
      delay = 20 # seconds
      try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "(//h1[contains(.,'Boston, MA')])")))
        time.sleep(5)
      except TimeoutException:
        print ("Loading the dial took too long!")
      # END Wait for the dial page to load cw 2019-08-08
      # Click the Moniotrs near me button
      element = driver.find_element_by_xpath("//a[@id='air-quality-monitors-near-me']");
      value = element.get_attribute("outerHTML")
      #print(value)
      # get everthing after xmin=
      xminValue = value.split("xmin=")[1]
      #print(xminValue)
      # get stuff before the .; just the Int
      xminValue = xminValue.split(".")[0]
      #print(xminValue)
      # Is it "close" to Raleigh at -9,000,000?
      #print(int(xminValue))
      # to be Greater Than is closer to the Prime Merdian
      assert int(xminValue) > -9000000    
      
      color.write("Pass: ","STRING")    
  except AssertionError:
      #print('       ' + value)
      color.write("FAIL: ","COMMENT")
  except Exception:
      color.write("FAIL: ","COMMENT")
  print('#154 Dial page and interactive map bug - STI - Code')

  #129 
  # Calendar Selector for Mobile cw 2019-04-05
  # Modified for new State Pages "name" parameter based method cw 209-09-09 
  driver.set_window_size(375, 667)
  driver.get(site + 'state/?name=north-carolina');
  try:
      # verify calendar pop-up selector 
      element = driver.find_element_by_xpath("//a[@data-toggle='tab'][contains(.,'Historical Air Quality')]").click()
      element = driver.find_element_by_xpath("//input[@id='historicalDatePicker']")
      value = element.get_attribute('placeholder')
      # in NEW code placeholder does not have the ".." at the end.
      #   Therefore, this is an exact comparison
      assert value == "Select Date"

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#129 Calendar Selector for Mobile - STI - Code')
  driver.set_window_size(1024, 1024)
  
  #109
  # Data Provider for Toledo cw 2019-03-28
  # 
  #
  #Data Provider Links removed by AirNowDrupal #190 cw 2019-09-11
  #
  
  #108
  # State Page to reportingArea format - STI cw 2019-04-10
  # Modified URL for new URL parameter "name" for Tome and a Delay for the dial page cw 2019-09-12
  # 
  driver.get(site + 'state/?name=north+carolina');
  try:
      # title
      assert 'State AQI | AirNow.gov' in driver.title;

      # verify new links
      element = driver.find_element_by_xpath("//b[contains(.,'Alexander County')]").click();
      # Wait for the dial page to load cw 2019-08-08
      delay = 20 # seconds
      try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "(//h1[contains(.,'Taylorsville, NC')])")))
      except TimeoutException:
        print ("Loading the dial took too long!")
        
      assert 'reportingArea' in driver.current_url
      
      color.write("Pass: ","STRING") 
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  except Exception:
      color.write("FAIL: ","COMMENT")
  print('#108 State Page to reportingArea format - STI - Code')
  
  # 107
  # v2.1.0 Updated JS for MS browsers cw 2019-05-24
  driver.get(site);
  try:
      # JS fix appears in the last JS referenced on the page... let's find that one and look in the Documentation
        # pull out all the HTML source with one line of code!
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      #print(value)
      # find last script tag / hightest index value
      index = value.rfind('/files/js/js_');
      # find last script tag / hightest index value
      #     cloud.gov changed this directory... made shorter cw 2019-07-29
      index = value.rfind('/js/js_');
      #print (index)
      # find the URL to the target javascript
      #     cloud.gov changed the length; -6 characters... made shorter cw 2019-07-29
      JSpath = value[index:index+53]
      #print(JSpath)
      # special string varies on localhost; otherwise it's "deafult"
      sitePathString = "default/files"
      if site == 'http://preview:Welcome1@airnowgov.dev.dd:8083/':
        sitePathString = "airnowgov.dev.dd/files"
      # and here is the complete JS url
      JSurl = site+"sites/"+sitePathString+JSpath
      #     cloud.gov changed the path cw 2019-07-29
      if site == 'https://preview:Welcome1@airnow.app.cloud.gov/':
        JSurl = "https://cg-f4d7e578-4b57-4941-95f8-331b8b5881c6.s3.us-gov-west-1.amazonaws.com/s3fs-public"+JSpath
      # print(JSurl)
      # fetch the JS file
      driver.get(JSurl);
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      #print(value)
      # assert the string in the fix
      assert '// IE11 fix - ES6 introduced defaulted function parameters, but sadly ES6 is not supported in IE11.' in value 

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#107 Updated JS for MS browsers - STI- Code')

  #61 R23.5
  # AQI Calculator cw 2019-04-22
  driver.get(site + 'aqi/aqi-calculator');
  try:
      assert 'AQI Calculator' in driver.title
      # verify O3 calulation feature
      select = Select(driver.find_element_by_name('pollutant')) 
      select.select_by_visible_text("O3 - Ozone (1hr avg)")
      element = driver.find_element_by_xpath("//input[contains(@name,'inputbox')]")
      element.send_keys("124")
      driver.find_element_by_name("Calculate").click()
      element = driver.find_element_by_xpath("//input[contains(@name,'outputbox2')]")
      value = element.get_attribute("value")
      assert "Unhealthy for Sensitive Groups" in value
      element = driver.find_element_by_xpath("//textarea[contains(@name,'Cautionary')]")
      value = element.get_attribute("value")
      assert "Active children and adults, and people with respiratory disease, such as asthma, should limit heavy outdoor exertion." in value

      # verify PM10 calulation feature
      select = Select(driver.find_element_by_name('pollutant')) 
      select.select_by_visible_text("PM10 - Particulate <10 microns (24hr avg)")
      element = driver.find_element_by_xpath("//input[contains(@name,'inputbox')]")
      element.send_keys("124")
      driver.find_element_by_name("Calculate").click()
      element = driver.find_element_by_xpath("//input[contains(@name,'outputbox2')]")
      value = element.get_attribute("value")
      assert "Unhealthy for Sensitive Groups" in value
      element = driver.find_element_by_xpath("//textarea[contains(@name,'Cautionary')]")
      value = element.get_attribute("value")
      assert "People with respiratory disease, such as asthma, should limit outdoor exertion." in value

      # verify PM10 calulation feature
      select = Select(driver.find_element_by_name('pollutant')) 
      select.select_by_visible_text("O3 - Ozone (1hr avg)")
      element = driver.find_element_by_xpath("//input[contains(@name,'inputbox')]")
      element.send_keys("144")
      driver.find_element_by_name("Calculate").click()
      element = driver.find_element_by_xpath("//input[contains(@name,'outputbox2')]")
      value = element.get_attribute("value")
      assert "Unhealthy for Sensitive Groups" in value
      element = driver.find_element_by_xpath("//textarea[contains(@name,'Cautionary')]")
      value = element.get_attribute("value")
      assert "Active children and adults, and people with respiratory disease, such as asthma, should limit heavy outdoor exertion." in value
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#61 R23.5 AQI Calculator')

  # CSS & JS Aggregation
  #  look for the /themes/anblue/css/base.css as MISSING; it has been aggregated.
  #
  driver.get(site + '?city=Durham&state=NC&country=USA');
  try:
      # pull out all the HTML source with one line of code!
      #  https://stackoverflow.com/questions/7861775/python-selenium-accessing-html-source
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      #print(value)
      # If this string exists then the site is NOT using Agregation
      #  cloud.gov needs this stings to be shorter; it has "custom" directory cw 2019-08-08
      assert '/anblue/css/base.css' in value
      
      #### Looking for Missing string ###
      ## Exception is reversed !!! ###
      color.write("FAIL: ","COMMENT")
  except Exception:
      color.write("Pass: ","STRING")
      ## Exception is reversed !!! ###
  print('CSS & JS Aggregation')





  ###########
  # Completed Version 2.2.4 items BELOW here...
  ###########
  print(' ')
  print('         Version 2.2.4')
  ###########

  # V2.2.4 XSS Shield Custom Module font-family
  # Fix escaped characters Issues cw 2019-08-22
  color.write("Pass: ","STRING")
  print('v2.2.4 XSS Shield Custom Module Update v1.3 - No Public Test')

    
  ###########
  # Completed Version 2.2.1 items BELOW here...
  ###########
  print(' ')
  print('         Version 2.2.1')
  ###########

  # v2.2.1 Bug Fix: URL Redirection on content pages cw 2019-07-15
  #   a bug caused by the v2.1.0 code; the failed attemept at #122
  driver.get(site + '?city=Durham&state=NC&country=USA');
  try:
      # go to a content page
      driver.get(site + 'how-to-use-this-site');
      # Scroll the page down to make the Location box appear in the nav bar
      driver.execute_script("window.scrollTo(0, 555)")
      # verify metatags on About the Data page
      element = driver.find_element_by_xpath("//input[contains(@id,'location-input-nav_input')]")
      element.send_keys('Charlotte, NC')
      element.send_keys(Keys.ENTER)
      # should NOT change to Charlottee, NC; should stay on the content page
      driver.refresh();
      element = driver.find_element_by_xpath("//h1[@class='band-title-light'][contains(.,'How to Use the AirNow Website')]")
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT") 
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('v2.2.1 Bug Fix: URL Redirection on content pages - code')

  ###########
  # Completed Version 2.2.0 items BELOW here...
  ###########
  print(' ')
  print('         Version 2.2.0')
  ###########
 
  # 164
  # AppScan flagged non-existant domain cw 2019-06-11
  driver.get(site + 'aqi/action-days');
  try:
      # verify element is NOT present. The link for Oklahoma city
      element = driver.find_element_by_xpath("//a[@href='http://bettertogetherok.org/air-quality/ozone-alerts/']")
       
      ## Exception is reversed !!! ###
      color.write("FAIL: ","COMMENT")
  except Exception:
      color.write("Pass: ","STRING")
      ## Exception is reversed !!! ###
  print('#164 AppScan flagged non-existent domain - Content')

  # 164
  # AppScan flagged two external URLs cw 2019-06-17
  driver.get(site + 'resources/web-cams');
  try:
      # verify element is NOT present. The link for Oklahoma city
      element = driver.find_element_by_xpath("//a[@href='http://www.co.mendocino.ca.us/aqmd/webcam/camera0.jpg']")

      driver.get(site + '/partners');
      # verify element is NOT present. The link for Oklahoma city
      element = driver.find_element_by_xpath("//a[@href='http://www.co.mendocino.ca.us/aqmd/']")
       
      color.write("Pass: ","STRING")
  except Exception:    
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#164 AppScan flagged two external URLs - Content')

  # 160
  # Remove Empty Alert bar on Mobile cw 2019-06-21
  driver.set_window_size(375, 667) # iPhone 6
  driver.get(site + '/?city=Durham&state=NC&country=USA')
  try:
      assert 'AirNow.gov' in driver.title # Simple Page title cw 2021-01-25
      ## currently NO alerts are "on"
      # verify that bar is not present... hidden in the TWIG
      driver.find_element_by_xpath("(//div[@id='bb-mobile-status-bar'])")

      ## Exception is reversed !!! ###
      color.write("FAIL: ","COMMENT")
  except Exception:
      color.write("Pass: ","STRING")
      ## Exception is reversed !!! ###
  # Reset Window size
  driver.set_window_size(1024, 1024)
  print('#160 Remove Empty Alert bar on Mobile - Code')
  
  # 159
  # Update Announcements on Dial Page cw 2019-06-06
  ### Make the 9/12/19 "Welcome" NOT be there
  driver.get(site);
  try:
      # verify element is NOT present
      element = driver.find_element_by_xpath("//b[contains(.,'2018-09-12')]")
       
      ## Exception is reversed !!! ###
      color.write("FAIL: ","COMMENT")
  except Exception:
      color.write("Pass: ","STRING")
      ## Exception is reversed !!! ###
  print('#159 Update Announcements on Dial Page - Content')

  # 158
  # Broken links on Dev and Stage cw 2019-06-26
  driver.get(site + 'air-quality-and-health/fires-and-your-health');
  try:
      # verify link is correct
      element = driver.find_element_by_xpath("//a[contains(.,'Wildfire Smoke, A Guide for Public Health Officials')]")
      value = element.get_attribute("href")
      #print(value)
      assert '/wildfire-smoke-guide-publications' in value
      
      color.write("Pass: ","STRING")
  except Exception:    
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#158 Broken links on Dev and Stage - Content')
  
  # 157
  # Vertical Center Mobile Dial Page Titles cw 2019-06-10
  driver.set_window_size(375, 667) # iPhone 6
  #   on cloud.gov a slash in the site added string escapes the ?... maybe?
  driver.get(site + '?city=Durham&state=NC&country=USA');
  driver.set_page_load_timeout(30)
  try:
      # titles should be same size
      element = driver.find_element_by_xpath("//h1[@class='band-title-white']")
      value = element.value_of_css_property('padding-bottom')
      #print(value)
      assert "12px" in value

      # Borders on boxes
      element = driver.find_element_by_xpath("//h1[@class='band-title-light']")
      value = element.value_of_css_property('padding-bottom')
      #print(value)
      assert "12px" in value

      color.write("Pass: ","STRING")
  except Exception:    
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#157 Vertical Center Mobile Dial Page Titles - Code')
  driver.set_window_size(1024, 1024)

  # #155
  # Double Pollutant Values cw 2019-05-29
  driver.get('https://api-airnowgov.sonomatech.com/reportingarea/get/?latitude=35.878&longitude=-78.787');    
  try:
      # pull out all the HTML source with one line of code!
      json_string = json.dumps( driver.find_element_by_xpath("//*").get_attribute("outerHTML") )
      # print(json_data)
      # Get the number of rows of data; count of "issueDate"
      value = json_string.count("issueDate")
      ##### Theory: #####
      # If more than a month of data is in the JSON response, then the application displays Double Pollutant Values!
      # There are up to 6 Pollutants per day, so looking for more than 3 weeks of built up cache = 6 * 3 * 7 = 126
      if value > ( 6 * 3 * 7 ):
        assert 1 == 2
      
      color.write("Pass: ","STRING")
  except Exception:    
      color.write("DANGER: Try this URL to reset:","COMMENT")
      print(" ")
      color.write("https://api-airnowgov.sonomatech.com/reportingarea/set?resetCache=true ","COMMENT")
      print(" ")
      color.write("FAIL: ","COMMENT")
  print('#155 Double Pollutant Values (JSON at:',value,'rows) - STI - JSON Issue')
  
  # 154
  # Dial page and interactive map bug - STI cw 2019-06-06
  #  Inproved Test to be independant of screen size; use a litle cooordindate "closeness" cw 2020-04-08
  #
  driver.get(site + '?city=Detroit&state=MI&country=USA');
  driver.get(site + '?city=Kansas City&state=KS&country=USA');
  driver.get(site + '?city=Detroit&state=MI&country=USA');

  # Wait for the dial page to load cw 2019-08-08
  delay = 20 # seconds
  try:
    myElem0 = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "(//h1[contains(.,'Detroit, MI')])")))
  except TimeoutException:
    print ("Loading the dial took too long!")
  # END Wait for the dial page to load cw 2019-08-08
  
  try:
      # go to a different city ... far East... Boston, MA
      driver.get(site + '?city=Boston&state=MA&country=USA');
      # Wait for the dial page to load cw 2019-08-08
      delay = 20 # seconds
      try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "(//h1[contains(.,'Boston, MA')])")))
        time.sleep(5)
      except TimeoutException:
        print ("Loading the dial took too long!")
      # END Wait for the dial page to load cw 2019-08-08
      # Click the Moniotrs near me button
      element = driver.find_element_by_xpath("//a[@id='air-quality-monitors-near-me']");
      value = element.get_attribute("outerHTML")
      #print(value)
      # get everthing after xmin=
      xminValue = value.split("xmin=")[1]
      #print(xminValue)
      # get stuff before the .; just the Int
      xminValue = xminValue.split(".")[0]
      #print(xminValue)
      # Is it "close" to Raleigh at -9,000,000?
      #print(int(xminValue))
      # to be Greater Than is closer to the Prime Merdian
      assert int(xminValue) > -9000000    
      
      color.write("Pass: ","STRING")    
  except AssertionError:
      #print('       ' + value)
      color.write("FAIL: ","COMMENT")
  except Exception:
      color.write("FAIL: ","COMMENT")
  print('#154 Dial page and interactive map bug - STI - Code')

  # 153
  # IE11 bug fix cw 2019-06-19
  driver.get(site);
  try:
      # JS fix appears in the last JS referenced on the page... let's find that one and look in the Documentation
        # pull out all the HTML source with one line of code!
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      # find last script tag / hightest index value
      #     cloud.gov changed this directory... made shorter cw 2019-07-29
      index = value.rfind('/js/js_');
      #print (index)
      # find the URL to the target javascript
      #     cloud.gov changed the length; -6 characters... made shorter cw 2019-07-29
      JSpath = value[index:index+53]
      #print(JSpath)
      # special string varies on localhost; otherwise it's "deafult"
      sitePathString = "default/files"
      if site == 'http://preview:Welcome1@airnowgov.dev.dd:8083/':
        sitePathString = "airnowgov.dev.dd/files"
      # and here is the complete JS url
      JSurl = site+"sites/"+sitePathString+JSpath
      #     cloud.gov changed the path cw 2019-07-29
      if site == 'https://preview:Welcome1@airnow.app.cloud.gov/':
        JSurl = "https://cg-f4d7e578-4b57-4941-95f8-331b8b5881c6.s3.us-gov-west-1.amazonaws.com/s3fs-public"+JSpath
      #print(JSurl)
      # fetch the JS file
      driver.get(JSurl);
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      #print(value)
      # assert the string in the fix
      assert "window.addEventListener('scroll', () =&gt; {" in value 

      ## Exception is reversed !!! ###
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("Pass: ","STRING")
      ## Exception is reversed !!! ###
  print('#153 IE11 bug fix - KMEA/STI - Code')

  # 146
  # Mobile Forecast courtesy of cw 2019-06-13
  driver.set_window_size(375, 667) # iPhone 6
  driver.get(site + '?city=Durham&state=NC&country=USA');
  try:
      # If this element is present, then "Forecast courtesy of is showing in Mobile
      driver.find_element_by_xpath("//div[@class='visible-xs col-xs-12 forecastProvider']")
      
      color.write("Pass: ","STRING")
  except Exception:    
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#146 Mobile Forecast courtesy of - STI - Code')
  driver.set_window_size(1024, 1024)

  #139 Initial Version of Recent Trends - STI cw 2019-07-08
  try:
      # verify the Inital Trends page is present
      driver.get(site + 'trends');
      # verify title
      assert 'Recent AQI Trends' in driver.title

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#139 Initial Version of Recent Trends - STI - code')

  # 124
  # Mobile close boxes on Pop-ups cw 2020-01-23
  driver.set_window_size(375, 667) # iPhone 6
  driver.get(site + '?city=Durham&state=NC&country=USA');
  try:
      # Open the Tippy for Current Air Quality
      element = driver.find_element_by_xpath("(//div[@class='header'])[3]").click()
      element = driver.find_element_by_xpath("//div[@id='tippy-5']")
      value = element.get_attribute('outerHTML')
      #print(value)
      assert 'x-placement="bottom"' in value
      
      color.write("Pass: ","STRING")
  except Exception:    
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#124 Mobile close boxes on Pop-ups - Code')
  driver.set_window_size(1024, 1024)
  
  ###########
  # Completed Version 2.1.0 items BELOW here...
  ###########
  print(' ')
  print('         Version 2.1.0')
  ###########
  
    # 145
  # Mobile Fixes cw 2019-05-30
  driver.set_window_size(375, 667) # iPhone 6
  driver.get(site + '?city=Durham&state=NC&country=USA');
  try:
      # titles should be same size
      element = driver.find_element_by_xpath("//h1[@class='band-title-white'][contains(.,'Air Quality Forecast')]")
      value = element.value_of_css_property('font-size')
      #print(value)
      assert "28px" in value
      
      # make Explore Icons smaller
      element = driver.find_element_by_xpath("//img[contains(@alt,'Archived Dates')]")
      value = element.value_of_css_property('padding')
      #print(value)
      assert "35px" in value
      

      # make Explore Cards smaller
      element = driver.find_element_by_xpath("//div[@class='inner-card-style inner-card-style-basic']")
      value = element.value_of_css_property('height')
      #print(value)
      assert "120px" in value

      # Remove gap in forecast pollutant cards
      ### Can't figure out a Xpath to unique element

      # Border around Forecast section
      element = driver.find_element_by_xpath("//div[@class='row forecast-aq-days has-data']")
      value = element.value_of_css_property('margin')
      #print(value)
      assert "0px" in value

      # New size for announcements titles
      element = driver.find_element_by_xpath("//div[@class='inner-card-style inner-card-style-announcement']")
      value = element.value_of_css_property('font-size')
      #print(value)
      assert "12px" in value
      
      color.write("Pass: ","STRING")
  except Exception:    
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#145 Mobile Fixes - Code/Content')
  driver.set_window_size(1024, 1024)
  

  # 143
  # Changes to Pollutant Boxes cw 2019-05-31
  driver.get(site + '?city=Durham&state=NC&country=USA');
  try:
      # 2 px border on both Other Pollutant boxes
      element = driver.find_element_by_xpath("//div[@class='pollutant-card other-pollutants-card']")
      value = element.value_of_css_property('border')
      #print(value)
      assert "2px" in value

      # Forecast Primary Pollutant health message should be open
      element = driver.find_element_by_xpath("(//div[@class='col-xs-12 pollutant-info-sub '])[2]")

      color.write("Pass: ","STRING")    
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  except Exception:
      color.write("FAIL: ","COMMENT")
  print('#143 Changes to Pollutant Boxes - Code')
  
  # 142
  # Rearrange bottom Band on Dial Page cw 2019-05-30
  #  changed for current status cw 2019-10-17
  driver.get(site);
  try:
      # New title is "Explore"
      element = driver.find_element_by_xpath("//h1[@class='band-title-white'][contains(.,'Explore')]")
      value = element.get_attribute('outerHTML')
      #print(value)
      assert ">Explore</h1>" in value
      
      color.write("Pass: ","STRING")
  except Exception:    
      color.write("FAIL: ","COMMENT")
  print('#142 Rearrange bottom Band on Dial Page - Content')

  # 142
  # Remove Back to Top and old Bands from Dial Page cw 2019-05-30
  #  changed to a "positive" test cw 2019-10-17
  driver.get(site);
  try:
      # verify "Explore Maps & Data title is gone
      element = driver.find_element_by_xpath("//h1[@class='band-title-light'][contains(.,'Announcements')]")

      # verify "Featured Resources is gone
      element = driver.find_element_by_xpath("//h1[@class='band-title-white'][contains(.,'Explore')]")
      
      color.write("Pass: ","STRING")
  except Exception:    
      color.write("FAIL: ","COMMENT")
  print('#142 Remove Back to Top and old Bands from Dial Page - Content')
  
  # 134
  # Update Web Cam Links cw 2019-04-29
  driver.get(site + 'resources/web-cams');
  try:
      # verify NO links to "fsvisimages.com"
       # pull out all the HTML source with one line of code!
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      assert 'fsvisimages.com' in value
   
      ## Exception is reversed !!! ###
      color.write("FAIL: ","COMMENT")
  except Exception:
      color.write("Pass: ","STRING")
      ## Exception is reversed !!! ###
  print('#134 Update Web Cam Links - Content')
  
  # 130
  # No Pollutant Available Flashing Message cw 2019-04-29
  driver.get(site + '?city=Santa Clara&state=CA&country=USA');
  try:
      # verify Old message appears ... Reversed Exception
      element = driver.find_element_by_xpath("//div[@class='col-xs-12 pollutants-list'][contains(.,'No Pollutant Available')]")

      ## Exception is reversed !!! ###
      color.write("FAIL: ","COMMENT")
  except Exception:
      color.write("Pass: ","STRING")
      ## Exception is reversed !!! ###
  print('#130 No Pollutant Available Flashing Message - Code')
  
  #129 
  # Calendar Selector for Mobile cw 2019-04-05
  # Modified for new State Pages "name" parameter based method cw 209-09-09 
  driver.set_window_size(375, 667)
  driver.get(site + 'state/?name=north-carolina');
  try:
      # verify calendar pop-up selector 
      element = driver.find_element_by_xpath("//a[@data-toggle='tab'][contains(.,'Historical Air Quality')]").click()
      element = driver.find_element_by_xpath("//input[@id='historicalDatePicker']")
      value = element.get_attribute('placeholder')
      # in NEW code placeholder does not have the ".." at the end.
      #   Therefore, this is an exact comparison
      assert value == "Select Date"

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#129 Calendar Selector for Mobile - STI - Code')
  driver.set_window_size(1024, 1024)

  # 115
  # Candy Stripe Dial Page cw 2019-04-29
  #  changed for new location of band cw 2019-10-17
  driver.get(site + '?city=Durham&state=NC&country=USA');
  try:
      # verify Accouncements band is White, the newest style created
      element = driver.find_element_by_xpath("//h1[@class='band-title-light'][contains(.,'Announcements')]")    
      
      color.write("Pass: ","STRING")
  except Exception: 
      color.write("FAIL: ","COMMENT")
  print('#115 Candy Stripe Dial Page - Code')

  # 107
  # v2.1.0 Updated JS for MS browsers cw 2019-05-24
  driver.get(site);
  try:
      # JS fix appears in the last JS referenced on the page... let's find that one and look in the Documentation
        # pull out all the HTML source with one line of code!
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      #print(value)
      # find last script tag / hightest index value
      index = value.rfind('/files/js/js_');
      # find last script tag / hightest index value
      #     cloud.gov changed this directory... made shorter cw 2019-07-29
      index = value.rfind('/js/js_');
      #print (index)
      # find the URL to the target javascript
      #     cloud.gov changed the length; -6 characters... made shorter cw 2019-07-29
      JSpath = value[index:index+53]
      #print(JSpath)
      # special string varies on localhost; otherwise it's "deafult"
      sitePathString = "default/files"
      if site == 'http://preview:Welcome1@airnowgov.dev.dd:8083/':
        sitePathString = "airnowgov.dev.dd/files"
      # and here is the complete JS url
      JSurl = site+"sites/"+sitePathString+JSpath
      #     cloud.gov changed the path cw 2019-07-29
      if site == 'https://preview:Welcome1@airnow.app.cloud.gov/':
        JSurl = "https://cg-f4d7e578-4b57-4941-95f8-331b8b5881c6.s3.us-gov-west-1.amazonaws.com/s3fs-public"+JSpath
      #print(JSurl)
      # fetch the JS file
      driver.get(JSurl);
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      #print(value)
      # assert the string in the fix
      assert '// IE11 fix - ES6 introduced defaulted function parameters, but sadly ES6 is not supported in IE11.' in value 

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#107 Updated JS for MS browsers - STI- Code')
  
  #101
  # National Maps V 2.1.0 cw 2019-05-14
  #
  driver.get(site + 'national-maps');
  try:
      # title
      assert 'National Maps | AirNow.gov' in driver.title
      
      # Must follow Heading Hierarchy for 508 compliance
      element = driver.find_element_by_xpath("//h1[@class='band-title-light'][contains(.,'National Maps')]").text
      assert element == 'National Maps'
        
      color.write("Pass: ","STRING") 
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  except NoSuchElementException:
      color.write("FAIL: ","COMMENT")
  print('#101 National Maps Update - Code')
  
  # V2.1.0 XSS Shield Custom Module
  # Systematically fixes XSS Issues cw 2019-05-28
  color.write("Pass: ","STRING")
  print('v2.1.0 XSS Shield Custom Module - No Public Test')

  ###########
  # Completed Version 2.0.0 items BELOW here...
  ###########
  print(' ')
  print('         Version 2.0.0')
  ###########
  
  #v2.0.0 Bug#2
  # Map Info Icon on airnow2.epa.gov cw 2019-04-26
  driver.get(site);
  try:
      # get the Air Now Logo src
      value = driver.find_element_by_xpath("//img[contains(@alt,'Air Now Logo')]").get_attribute("src")
      # should NOT have airnow2 in path
      assert 'airnow2.epa.gov' in value
   
      ## Exception is reversed !!! ###
      color.write("FAIL: ","COMMENT")
  except Exception:
      color.write("Pass: ","STRING")
      ## Exception is reversed !!! ###
  print('Bug#2 - NOT Using airnow2 in Paths - Server')
  

  
  #127
  # Using ESRI Location lookup cw 2019-04-05
  driver.get(site);
  try:
      assert 'AirNow.gov' in driver.title # Simple Page title cw 2021-01-25
      # verify ESRI lookup feature
      driver.find_element_by_xpath("//span[@class = 'searchIcon esri-icon-loading-indicator searchSpinner']")

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  print('#127 Using ESRI Location lookup - Code')
  
  #121
  # Add Interactive Map to Maps & Data Menu cw 2019-04-02
  driver.get(site + 'maps-and-data');
  try:
      assert 'Maps and Data | AirNow.gov' in driver.title
      # verify Interactive Map Menu item
      driver.find_element_by_xpath("//a[@class='main-link nav-link'][contains(.,'Interactive Map')]")
      driver.find_element_by_xpath("//a[@class='main-link nav-link'][contains(.,'National Map')]")
      
      # follow the Nation Map link
      driver.find_element_by_xpath("//a[@href='https://gispub.epa.gov/airnow/']")
      driver.find_element_by_xpath("//a[@href='/national-maps']")
 
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  print('#121 Interactive Map in Maps & Data Menu')
  
  #118
  # Remove More Cities button cw 2019-04-01
  driver.get(site + '/?city=Durham&state=NC&country=USA');
  try:
      assert 'AirNow.gov' in driver.title # Simple Page title cw 2021-01-25
      # find the button
      element = driver.find_element_by_xpath("//a[@class='state-air-quality btn btn-custom-blue-state']")

      ##### Deleting this element ####
      ## Exception is reversed !!! ###
      color.write("FAIL: ","COMMENT")
  except Exception:
      color.write("Pass: ","STRING")
      ## Exception is reversed !!! ###
  print('#118 Remove More Cities button - Code')
  
  #116
  # Remove Highcharts cw 2019-04-04
  driver.get(site + '?city=Durham&state=NC&country=USA');
  try:    
      # pull out all the HTML source with one line of code!
      #  https://stackoverflow.com/questions/7861775/python-selenium-accessing-html-source
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")

      # If this string exists then the site is loding highcharts.js when it is not needed!
      #   This assertion should throw an Exception
      assert '/highcharts.css' in value
      
      ##### Deleting this element ####
      ## Exception is reversed !!! ###
      color.write("FAIL: ","COMMENT")
  except Exception:
      color.write("Pass: ","STRING")
      ## Exception is reversed !!! ###
  print('#116 Remove Highcharts - Code')
  
  #114
  # New Wildfire Factsheets cw 2019-04-03
  #   Updated for New Factsheet title method... Don't include the word "Factsheet"  cw 2021-11-01
  try:
      # verify two newDocument Pages exist
      driver.get(site + 'publications/wildfire-smoke-guide/wildfire-smoke-protect-your-pets');
      driver.find_element_by_xpath("//h1[contains(.,'Protect Your Pets from Wildfire Smoke')]");
      #
      driver.get(site + 'publications/wildfire-smoke-guide/wildfire-smoke-protect-your-large-animals-and-livestock');
      driver.find_element_by_xpath("//h1[contains(.,'Protect Your Large Animals and Livestock from Wildfire Smoke')]");

      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  print('#114 New Wildfire Factsheets - Content') 

  #113 Add WY Data Providers
  # Links come from a call to JSON?
  try:
      # Casper, WY
      driver.get(site + '?city=Casper&state=WY&country=USA')
      element = driver.find_elements_by_xpath("//a[contains(.,'Data courtesy of')]")
        
      # Cheyenne, WY
      driver.get(site + '?city=Cheyenne&state=WY&country=USA')
      element = driver.find_elements_by_xpath("//a[contains(.,'Data courtesy of')]")
 
      # Boulder, WY
      driver.get(site + '?city=Boulder&state=WY&country=USA')
      element = driver.find_elements_by_xpath("//a[contains(.,'Data courtesy of')]")
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: STI: Link Missing on Dial Page ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#113 Add WY Data Provider - Cloud')
  
##  #112
##  # X-ing Out Alerts cw 2019-04-10
##  driver.get(site)
##  try:
##      assert 'Home Page | AirNow.gov' in driver.title  
##      # find the new close button & and the clicked change
##      driver.find_element_by_xpath("(//i[contains(@class,'fa fa-times')])[2]").click()
##      driver.find_element_by_xpath("(//div[@class='col-xs-4 strip-padding status-message-container hidden-xs hidden'])")
##
##      # find the new close button on Mobile & and the clicked change
##      driver.get(site)
##      driver.set_window_size(375, 667)
##      driver.find_element_by_xpath("(//i[contains(@class,'fa fa-times')])[4]").click()
##      driver.find_element_by_xpath("(//div[@class='bb-mobile-status-bar hidden'])")
##
##      color.write("Pass: ","STRING") 
##  except Exception:
##      color.write("FAIL: ","COMMENT")
##  except AssertionError:
##      color.write("FAIL: ","COMMENT")
##  # Reset Window size
##  driver.set_window_size(1024, 1024)
##  print('#112 X-ing Out Alerts - Code')
  
  #111
  # Add More Maps to Maps & Data Menu
  # Changed to "National Maps" bt # 118 cw 2019-04-02
  driver.get(site);
  try:
      assert 'AirNow.gov' in driver.title # Simple Page title cw 2021-01-25
      # verify More Maps Menu item
      driver.find_element_by_xpath("//a[@class='main-link nav-link'][contains(.,'National Maps')]")

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  print('#111 More Maps in Maps & Data Menu')
  
  #110 
  # Not Using Randomized backgrounds cw 2019-04-09
  driver.get(site + '?city=Durham&state=NC&country=USA');
  try:
      # pull out all the HTML source with one line of code!
      #  https://stackoverflow.com/questions/7861775/python-selenium-accessing-html-source
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")

      # If this string exists then the site is using the set of old Randomized backgrounds
      #   This assertion should be a FAIL
      assert 'AirNow_Marquee_sky' in value
      
      ##### Removing this element ####
      ## Exception is reversed !!! ###
      color.write("FAIL: ","COMMENT")
  except Exception:
      color.write("Pass: ","STRING")
      ## Exception is reversed !!! ###
  print('#110 Not Using Randomized backgrounds - Code')
  
  #110 Addtional Test
  #  Sun beam Background Image  cw 2019-04-01
  #  Rewritten to be simpler cw 2019-04-09
  driver.get(site);
  try:
      assert 'AirNow.gov' in driver.title # Simple Page title cw 2021-01-25
      # Verify Background image on the Welcome page is the "SunBeam"
      element = driver.find_element_by_xpath("//div[@class='marquee']")
      value = element.get_attribute('style')
      #print(value)
      assert "AirNow_Marquee_Sunbeam" in value

      # Verify Background image on one of two different Dial Pages 
      driver.get(site + '?city=Durham&state=NC&country=USA'); # Durham
      element = driver.find_element_by_xpath("//div[@class='marquee']")
      value = element.get_attribute('style')
      #print(value)
      assert "AirNow_Marquee_Sunbeam" in value
   
      # Verify Background image on two of two different Dial Pages 
      driver.get(site + '?city=San%20Francisco&state=CA&country=USA'); #San Franciso
      element = driver.find_element_by_xpath("//div[@class='marquee']")
      value = element.get_attribute('style')
      #print(value)
      assert "AirNow_Marquee_Sunbeam" in value
             
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("Pass: ","STRING") 
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#110 Sunbeam Background Image')
  
  #110 
  # NOT Missing Explore Maps & Data images cw 2019-04-22
  driver.get(site);
  try:
      # find Current Fires image
      element = driver.find_element_by_xpath("//img[contains(@alt,'Fire Icon')]")
      value = element.get_attribute('src')
      # visit the image
      driver.get(value)
      # pull out all the HTML source with one line of code!
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      assert 'Not Found' in value
      # reset driver
      driver.get(site)

      # Look for updated DoS Seal
      element = driver.find_element_by_xpath("//img[contains(@alt,'US Department of State Seal')]")
      value = element.get_attribute('src')
      # visit the image
      driver.get(value)
      # pull out all the HTML source with one line of code!
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      assert 'Not Found' in value
      # reset driver
      driver.get(site) 

      # Look for updated DoS Seal
      element = driver.find_element_by_xpath("//img[contains(@alt,'Archived Dates')]")
      value = element.get_attribute('src')
      # visit the image
      driver.get(value)
      # pull out all the HTML source with one line of code!
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      assert 'Not Found' in value
      # reset driver
      driver.get(site)
   
      ## Exception is reversed !!! ###
      color.write("FAIL: ","COMMENT")
  except Exception:
      color.write("Pass: ","STRING")
      ## Exception is reversed !!! ###
  print('#110 NOT Missing Explore Maps & Data images - Content')
  
  #109
  # Data Provider for Toledo cw 2019-03-28
  #
  #Data Provider Links removed by AirNowDrupal #190 cw 2019-09-11
  #

  #108
  # State Page to reportingArea format - STI cw 2019-04-10
  # Modified URL for new URL parameter "name" for Tome and a Delay for the dial page cw 2020-01-23
  # 
  driver.get(site + 'state/?name=north+carolina');
  try:
      # title
      assert 'State AQI | AirNow.gov' in driver.title;

      # verify new links
      element = driver.find_element_by_xpath("//b[contains(.,'Alexander County')]").click();
      # Wait for the dial page to load cw 2019-08-08
      delay = 20 # seconds
      try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "(//h1[contains(.,'Taylorsville, NC')])")))
      except TimeoutException:
        print ("Loading the dial took too long!")
        
      assert 'reportingArea' in driver.current_url
      
      color.write("Pass: ","STRING") 
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  except Exception:
      color.write("FAIL: ","COMMENT")
  print('#108 State Page to reportingArea format - STI - Code')
  
  #105
  # Activity Guides cw 2019-03-22
  # 
  driver.get(site+'/activity-guides-publications');
  try:
      # title
      assert 'Activity Guides Publications | AirNow.gov' in driver.title
      
      # xpath - title; must get to the HTML element and pull the text
      #               Then can Assert the element, to catch the error as AssertionError:
      element = driver.find_element_by_xpath('//h1').text
      assert element == 'Activity Guides'

      # verify Graphic
      element = driver.find_element_by_xpath('//a/img')
      value = element.get_attribute('src')
      assert 'aqguideozonesm.jpg' in value

      # verify new menu item
      element = driver.find_element_by_xpath("//a[@class='sub-link nav-link'][contains(.,'Activity Guides')]")
      
      color.write("Pass: ","STRING") 
  except AssertionError:
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  print('#105 Activity Guides')

  #102
  # Illinois Data Provider link cw 2019-04-01
  #
  #Data Provider Links removed by AirNowDrupal #190 cw 2019-09-11
  #

  #101 - AQI Legend on National Maps
  # More Maps - AQI Legend cw 2019-03-21
  #   Simplified cw 2020-09-24
  #
  driver.get(site + 'national-maps');
  try:
      # title
      assert 'National Maps | AirNow.gov' in driver.title
      
      # Test AQI Legend
      value = driver.find_element_by_xpath("//button[@class='po-scale-item po-aqi-scale-btn'][contains(.,'AQI Legend')]").text
      assert value == 'AQI Legend'
      #print(value)

      color.write("Pass: ","STRING") 
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  except Exception:
      color.write("FAIL: ","COMMENT")
  print('#101 More Maps - AQI Legend on National Maps')

  #101
  # National Maps cw 2019-03-21
  #
  driver.get(site + 'national-maps');
  try:
      # title
      assert 'National Maps | AirNow.gov' in driver.title
      
      # Must follow Heading Hierarchy for 508 compliance
      # changed by version 2.1.0
      #element = driver.find_element_by_xpath("//h1[@class='band-title'][contains(.,'National Maps')]").text
      #assert element == 'National Maps'
      element = driver.find_element_by_xpath("//h2[@class='text-center'][contains(.,'Current Air Quality')]").text
      assert element == 'Current Air Quality'
      element = driver.find_element_by_xpath("//h3[contains(.,'More Current Map Options:')]").text
      assert element == 'More Current Map Options:'

      # xpath - list item as of 2019-03-27
      element = driver.find_element_by_xpath("//a[contains(@href, 'https://gispub.epa.gov/airnow/?mlayer=ozonepm&clayer=none&panel=0')]").text
      #assert element == 'Current - by monitor'

      # xpath - Current Time Stamp Exists on page; Byran Chastain change on 2019-03-27
      #value = driver.find_element_by_xpath("//span[@id='currenttimestamp']").text

      # card icon under SSL; ONLY NCC servers force to SSL
      if '.gov' in site:
        element = driver.find_element_by_xpath("//img[@alt='Fire Icon']")
        value = element.get_attribute("src")
        #assert 'https:' in value
        
      color.write("Pass: ","STRING") 
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  except NoSuchElementException:
      color.write("FAIL: Timestamp missing ","COMMENT")
  print('#101 National Maps') 

  #
  # Mobile State Pages - STI cw 2019-04-16
  # Modified URL for new URL parameter "name" fot Tome cw 2019-09-09
  driver.get(site + 'state/?name=north-carolina');
  try:
      # look for new elements
      driver.find_element_by_xpath("(//th[contains(.,'Reporting Area')])[1]")
      driver.find_element_by_xpath("(//span[@class='city-time-cell'])[1]")

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('Mobile State Pages - STI - Code')
  
  #
  # AirNowLatestContoursCombined ESRI Service cw 2019-03-28
  #
  driver.get('https://services.arcgis.com/cJ9YHowT8TU7DUyn/ArcGIS/rest/services/AirNowLatestContoursCombined/FeatureServer');
  try:
      # title
      assert 'AirNowLatestContoursCombined' in driver.title
      
      # xpath - title; must get to the HTML element and pull the text
      #               Then can Assert the element, to catch the error as AssertionError:
      element = driver.find_element_by_xpath("//h2[contains(.,'AirNowLatestContoursCombined (FeatureServer)')]")
        
      color.write("Pass: ","STRING") 
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  except NoSuchElementException:
      color.write("FAIL: ","COMMENT")
  print('AirNowLatestContoursCombined ESRI Service')

  #
  # State Page label Reporting Area - STI  cw 2019-04-12
  # Modified URL for new URL parameter "name" for Tome cw 2019-09-09
  driver.get(site + 'state/?name=north-carolina');
  try:
      assert 'State AQI | AirNow.gov' in driver.title
      # verify ESRI lookup feature
      driver.find_element_by_xpath("(//th[contains(.,'Reporting Area')])[1]")

      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('State Page label Reporting Area - STI - Code')

  
  #
  # Data Courtesy of links for WY cw 2019-04-03
  # look for missing "Data Courtesy of" links
  #
  #
  #Data Provider Links removed by AirNowDrupal #190 cw 2019-09-11
  #


  # CSS & JS Aggregation
  #  look for the /themes/anblue/css/base.css as MISSING; it has been aggregated.
  #
  driver.get(site + '?city=Durham&state=NC&country=USA');
  try:
      # pull out all the HTML source with one line of code!
      #  https://stackoverflow.com/questions/7861775/python-selenium-accessing-html-source
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
      #print(value)
      # If this string exists then the site is NOT using Agregation
      #  cloud.gov needs this stings to be shorter; it has "custom" directory cw 2019-08-08
      assert '/anblue/css/base.css' in value
      
      #### Looking for Missing string ###
      ## Exception is reversed !!! ###
      color.write("FAIL: ","COMMENT")
  except Exception:
      color.write("Pass: ","STRING")
      ## Exception is reversed !!! ###
  print('CSS & JS Aggregation')

  #
  # Theme Debuging OFF cw 2019-04-04
  driver.get(site);
  try:
      # verify Theme Debugging is off

      # pull out all the HTML source with one line of code!
      #  https://stackoverflow.com/questions/7861775/python-selenium-accessing-html-source
      value = driver.find_element_by_xpath("//*").get_attribute("outerHTML")

      # If this string exists then the site is using Theme Debuging and not running at full speed
      #   This assertion should throw an Exception
      assert '<!-- FILE NAME SUGGESTIONS:' in value
      
      ##### Deleting this element ####
      ## Exception is reversed !!! ###
      color.write("FAIL: ","COMMENT")
  except Exception:
      color.write("Pass: ","STRING")
      ## Exception is reversed !!! ###
  print('Theme Debuging OFF - Code')

  print(' ')
  ###########
   ## Pre wildfire tests below here
  ###########
  print('         Previous Releases')
  ###########


  #100 R23.8
  # Download Images cw 2019-04-22
  #     cloud.gov changed the path cw 2019-07-29
  if site == 'https://preview:Welcome1@airnow.app.cloud.gov/':
    driver.get('https://cg-f4d7e578-4b57-4941-95f8-331b8b5881c6.s3.us-gov-west-1.amazonaws.com/s3fs-public/download-images/aqi-logos/aqi_ex1.jpg');
  else:
    driver.get(site + '/sites/default/files/download-images/aqi-logos/aqi_ex1.jpg');
  try:
      #assert '' in driver.title
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#100 R23.8 Download Images')
  
  #81 R23.7
  # Public File NOT airnowtest cw 2019-04-22
  driver.get(site + '/publications/air-quality-and-your-health/smog-who-does-it-hurt');
  try:
      #assert 'Publications Page' in driver.title
      # Publications pages now have the title of their Prolications for SEO cw 2020-08-14
      # Look for Reference to airnowtest
      element = driver.find_element_by_xpath("///a[contains(@href, 'https://airnowtest.epa.gov/sites/default/files/2018-03/smog.pdf')])[2]")

  except AssertionError:
      color.write("FAIL: ","COMMENT")
      
  ## Exception is reversed !!! ###
      color.write("FAIL: ","COMMENT")
  except Exception:
      color.write("Pass: ","STRING")
  ## Exception is reversed !!! ###
  print('#81 R23.7 Public File NOT airnowtest')
  
  #69 R23.6
  # Data Providers cw 2019-04-22
  #
  #Data Provider Links removed by AirNowDrupal #190 cw 2019-09-11
  #
  
  #61 R23.5
  # AQI Calculator cw 2019-04-22
  driver.get(site + 'aqi/aqi-calculator');
  try:
      assert 'AQI Calculator' in driver.title
      # verify O3 calulation feature
      select = Select(driver.find_element_by_name('pollutant')) 
      select.select_by_visible_text("O3 - Ozone (1hr avg)")
      element = driver.find_element_by_xpath("//input[contains(@name,'inputbox')]")
      element.send_keys("124")
      driver.find_element_by_name("Calculate").click()
      element = driver.find_element_by_xpath("//input[contains(@name,'outputbox2')]")
      value = element.get_attribute("value")
      assert "Unhealthy for Sensitive Groups" in value
      element = driver.find_element_by_xpath("//textarea[contains(@name,'Cautionary')]")
      value = element.get_attribute("value")
      assert "Active children and adults, and people with respiratory disease, such as asthma, should limit heavy outdoor exertion." in value

      # verify PM10 calulation feature
      select = Select(driver.find_element_by_name('pollutant')) 
      select.select_by_visible_text("PM10 - Particulate <10 microns (24hr avg)")
      element = driver.find_element_by_xpath("//input[contains(@name,'inputbox')]")
      element.send_keys("124")
      driver.find_element_by_name("Calculate").click()
      element = driver.find_element_by_xpath("//input[contains(@name,'outputbox2')]")
      value = element.get_attribute("value")
      assert "Unhealthy for Sensitive Groups" in value
      element = driver.find_element_by_xpath("//textarea[contains(@name,'Cautionary')]")
      value = element.get_attribute("value")
      assert "People with respiratory disease, such as asthma, should limit outdoor exertion." in value

      # verify PM10 calulation feature
      select = Select(driver.find_element_by_name('pollutant')) 
      select.select_by_visible_text("O3 - Ozone (1hr avg)")
      element = driver.find_element_by_xpath("//input[contains(@name,'inputbox')]")
      element.send_keys("144")
      driver.find_element_by_name("Calculate").click()
      element = driver.find_element_by_xpath("//input[contains(@name,'outputbox2')]")
      value = element.get_attribute("value")
      assert "Unhealthy for Sensitive Groups" in value
      element = driver.find_element_by_xpath("//textarea[contains(@name,'Cautionary')]")
      value = element.get_attribute("value")
      assert "Active children and adults, and people with respiratory disease, such as asthma, should limit heavy outdoor exertion." in value
      
      color.write("Pass: ","STRING") 
  except Exception:
      color.write("FAIL: ","COMMENT")
  except AssertionError:
      color.write("FAIL: ","COMMENT")
  print('#61 R23.5 AQI Calculator')






  
  #
  # Put tests above here...
  #################################
  # Clean-up & User Feed Back
  print(' ')
  print ('Done. ')
  print ('Finished testing ' + site)
  ts = time.time()
  now = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
  print (now)
  print ('Closing the browser.')
  print(' ')
  driver.close()
  driver.quit()

  

