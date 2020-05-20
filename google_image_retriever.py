# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import os
import urllib
import urllib.request

def retrieve_images(search_term,count=200):
    """Retrieve images from google search using Selenium-Python. The search_term is the search keyword to be used.
       Count is the number of images to be downloaded, with a default value of 200."""
    
    folder_name = search_term # The search term will also be the name of the folder.

    if not os.path.exists(folder_name): # Make a folder in that name if it doesn't exist.
        os.mkdir(folder_name)
    
    search_term = '+'.join(search_term.split())
    url = "https://www.google.co.in/search?q="+search_term+"&source=lnms&tbm=isch" # Create the search query
    driver = webdriver.Firefox() #Make sure the Geckodriver file is there in the same folder as the script.
    driver.get(url)

    for _ in range(260): # Scroll to the bottom of the search, displying all the search images.
        driver.execute_script("window.scrollBy(0,10000)")
        element = driver.find_element_by_xpath('//*[@id="islmp"]/div/div/div/div/div[5]/input') # Click "Show more results"
        if element.is_displayed():
            element.click()

    divs = driver.find_elements_by_xpath("//*[@id='islrg']/div[1]/div/a[1]/div[1]/img") # The xpath for all searched images.
    if count>len(divs): # If count is more than the number of images, download the max number of images.
        count = len(divs)

    for i in range(1,count+1):
        try: # Find image elements.
            image = driver.find_element_by_xpath(r"//*[@id='islrg']/div[1]/div["+str(i)+"]/a[1]//img") # The xpath for all searched images.
        except:
            continue
        
        try: # Extract images.
            img = urllib.request.urlopen(urllib.request.Request(image.get_attribute('src'))).read()
        except:
            img = urllib.request.urlopen(urllib.request.Request(image.get_attribute('data-src'))).read()
    
        f = open(os.getcwd()+'\\'+folder_name+'\\'+folder_name+str(i)+'.jpg',"wb") # Save as jpeg.
        f.write(img)
        f.close()
    
    driver.close()



if __name__ == "__main__":
    import sys
    retrieve_images(sys.argv[1],int(sys.argv[2]))
    
