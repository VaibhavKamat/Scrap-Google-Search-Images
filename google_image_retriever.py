# -*- coding: utf-8 -*-
import os
import urllib
import urllib.request
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException


def check_exists_by_xpath(xpath):
    try:
        webdriver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

def retrieve_images(search_term,count=200,thumbnail=True):
    """Retrieve images from google search using Selenium-Python. The search_term is the search keyword to be used.
       Count is the number of images to be downloaded, with a default value of 200.
       The function will try downloading thumbnails if it is set to True or will first try to download
       full images if it is False."""
    
    if (thumbnail==True): # Wait times will be less if the user wants the thumbnails.
        iw = 2
        panel_wait = 2
    else: # or else wait for more time for proper images to be extracted.
        iw = 100
        panel_wait = 2000
    
    folder_name = search_term # The search term will also be the name of the folder.
    if not os.path.exists(folder_name): # Make a folder in that name if it doesn't exist.
        os.mkdir(folder_name)
    
    search_term = '+'.join(search_term.split())
    url = "https://www.google.co.in/search?q="+search_term+"&source=lnms&tbm=isch" # Create the search query
    driver = webdriver.Chrome() # choosing Chrome browser. Make sure the Chrome driver is in the same directory.
    driver.maximize_window()
    driver.get(url)


    for _ in range(260): # Scroll to the bottom of the search, displying all the search images.
        driver.execute_script("window.scrollBy(0,10000)")
        element = driver.find_element_by_xpath('//*[@id="islmp"]/div/div/div/div/div[5]/input') # Click "Show more results"
        if element.is_displayed():
            element.click()

    divs = driver.find_elements_by_xpath("//*[@id='islrg']/div[1]/div/a[1]/div[1]/img") # The xpath for all searched images.
    if count>len(divs): # If count is more than the number of images, download the max number of images.
        count = len(divs)

    wait = WebDriverWait(driver,10) # Set explicit wait.
    actions = ActionChains(driver) # Set action chain variable.
    
    # Move to each of the images and wait for sometime.
    actions.move_to_element(driver.find_element_by_xpath(r"//*[@id='islrg']/div[1]/div[1]/a[1]/div[1]/img")).perform()
    driver.implicitly_wait(iw)
    for i in range(1,count+1):
        try: # Find image elements.
            search_image = wait.until(EC.element_to_be_clickable((By.XPATH,r"//*[@id='islrg']/div[1]/div["+str(i)+"]/a[1]/div[1]/img")))
            driver.implicitly_wait(iw)
            driver.execute_script("arguments[0].click();",search_image) # Click on each of the images.
        except:
            continue
         
            
        try: # Extract images from the black image panel (div).
            panel = wait.until(EC.element_to_be_clickable((By.XPATH,r'//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div[1]/div[1]/div/div[2]/a/img')))
            time.sleep(iw/50) # Wait for the panel to load.
            img = urllib.request.urlopen(urllib.request.Request(panel.get_attribute('src'))).read() # Extract the image.
        except:
            try: # or extract thumbnails if the above fails.
                search_image = driver.find_element_by_xpath(r"//*[@id='islrg']/div[1]/div["+str(i)+"]/a[1]/div[1]/img")
                #print(i,search_image.get_attribute("src"))
                if search_image.get_attribute("src") != None:
                    img = urllib.request.urlopen(urllib.request.Request(search_image.get_attribute('src'))).read()
                else:
                    img = urllib.request.urlopen(urllib.request.Request(search_image.get_attribute('data-src'))).read()
            except:
                continue
            
        f = open(os.getcwd()+'\\'+folder_name+'\\'+folder_name+str(i)+'.jpg',"wb") # Save the image as jpeg.
        f.write(img)
        f.close()
    
    driver.close()



if __name__ == "__main__":
    import sys
    retrieve_images(sys.argv[1],int(sys.argv[2]),bool(int(sys.argv[3])))
