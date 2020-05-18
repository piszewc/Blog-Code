# -*- coding: utf-8 -*-
"""
Created on Thu May 14 11:21:42 2020

@author: piotr

Script is part of the post from my blog.
If you want to learn more go to www.pszewc.pl

--------------
Following scrip will do two things:
    1) Scape page.
    2) Input Scraped data into form.

By learning thouse 2 things we will be able to read forms and automate inputing data into the forms. 
Thanks to this you should be able to create your own scripts to automate your daily tasks.
    
"""

from selenium import webdriver #import webdriver - launch browser
from selenium.webdriver.common.by import By # search using specific parameters.
from selenium.webdriver.support.ui import WebDriverWait #wait for a page to load. 
from selenium.webdriver.support import expected_conditions as EC #wait for specific element to be loaded.
from selenium.common.exceptions import TimeoutException # timeout errors
import pandas as pd

options = webdriver.ChromeOptions()

driver = webdriver.Chrome("./chromedriver.exe",options=options)
driver.get("https://www.amazon.com/") # only works with https or http

# Wait 20 seconds for page to load
timeout = 20

try:
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a[class='nav-logo-link']")))
except TimeoutException:
    print("Timed out waiting for page to load") 
    driver.quit()

# find search button and type searched item
    
search_bar = driver.find_element_by_css_selector("input[id='twotabsearchtextbox']")
search_bar.click()

search_bar.send_keys("Logitech C930e")
#click on search button
driver.find_element_by_css_selector("input[class='nav-input']").click()

items_prices = pd.DataFrame(columns=["Title","Price"])

# find all titles from page
items_titles = driver.find_elements_by_css_selector("div[class='a-section a-spacing-medium']")


for i in items_titles:
    title = i.find_elements_by_css_selector("span[class='a-size-medium a-color-base a-text-normal']")[0].text
    
    try:
        price = i.find_elements_by_css_selector("span[class='a-price-whole']")[0].text
    except:
        price = "NaN"
        
    items_prices = items_prices.append(pd.DataFrame({"Title":title,"Price":price}, index=[0]))


'''

BONUS CODE - Load all pages

'''

from selenium import webdriver #import webdriver - launch browser
from selenium.webdriver.common.by import By # search using specific parameters.
from selenium.webdriver.support.ui import WebDriverWait #wait for a page to load. 
from selenium.webdriver.support import expected_conditions as EC #wait for specific element to be loaded.
from selenium.common.exceptions import TimeoutException # timeout errors
import pandas as pd

options = webdriver.ChromeOptions()

driver = webdriver.Chrome("./chromedriver.exe",options=options)
driver.get("https://www.amazon.com/") # only works with https or http

# Wait 20 seconds for page to load
timeout = 20

try:
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a[class='nav-logo-link']")))
except TimeoutException:
    print("Timed out waiting for page to load") 
    driver.quit()

# find search button and type searched item
    
search_bar = driver.find_element_by_css_selector("input[id='twotabsearchtextbox']")
search_bar.click()

search_bar.send_keys("Logitech C930e")
#click on search button
driver.find_element_by_css_selector("input[class='nav-input']").click()


def getPagesUrl():
    list_of_pages = driver.find_elements_by_css_selector("div[class='a-section a-spacing-none a-padding-base']")[0].find_elements_by_css_selector("li")
    last_page = list_of_pages[-2].text
    
    next_page_link = list_of_pages[2].find_element_by_css_selector("a").get_attribute("href")
    next_page_link = next_page_link.split("page=")[0]+str("page=")
    
    return int(last_page), next_page_link

def getPageItems():
    local_items_prices = pd.DataFrame(columns=["Title","Price"])

    items_titles = driver.find_elements_by_css_selector("div[class='a-section a-spacing-medium']")

    for i in items_titles:
        title = i.find_elements_by_css_selector("span[class='a-size-medium a-color-base a-text-normal']")[0].text
        
        try:
            price = i.find_elements_by_css_selector("span[class='a-price-whole']")[0].text
        except:
            price = "NaN"
            
        local_items_prices = local_items_prices.append(pd.DataFrame({"Title":title,"Price":price}, index=[0]))
    return local_items_prices


items_prices = pd.DataFrame(columns=["Title","Price"])

max_page,create_links = getPagesUrl()

for i in range(1,max_page):
    driver.get(create_links+str(i))
    items_prices = items_prices.append(getPageItems(),ignore_index=True)
    
    

    