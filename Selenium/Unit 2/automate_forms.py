# -*- coding: utf-8 -*-
"""
Created on Wed May 27 21:16:59 2020

@author: piotr
"""

from selenium import webdriver #import webdriver - launch browser
from selenium.webdriver.common.by import By # search using specific parameters.
from selenium.webdriver.support.ui import WebDriverWait #wait for a page to load. 
from selenium.webdriver.support import expected_conditions as EC #wait for specific element to be loaded.
from selenium.common.exceptions import TimeoutException # timeout errors

import pandas as pd
 
cars_data = pd.read_excel("input_items.xlsx")


options = webdriver.ChromeOptions()
#options.add_argument("--incognito")
driver = webdriver.Chrome("./chromedriver.exe",options=options)
driver.get("https://forms.office.com/Pages/ResponsePage.aspx?id=DQSIkWdsW0yxEjajBLZtrQAAAAAAAAAAAAN__tPvGS1URFNTU0RQNjdaRThJSVowWDdUMkZTS1dOSy4u") # only works with https or http

# Wait 20 seconds for page to load
timeout = 20

try:
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='office-form-title heading-1']")))
except TimeoutException:
    print("Timed out waiting for page to load") 
    driver.quit()
    
for i in range(len(cars_data)):
    
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='office-form-title heading-1']")))

    manufacturer = driver.find_element_by_css_selector("div[class='select-placeholder']")
    manufacturer.click()
    
    manufacturer_list = driver.find_element_by_css_selector("ul[class='select-option-menu-container']")
    manufacturer_list.find_element_by_xpath(u'//span[text()="'+str(cars_data.at[i,"manufacturer"])+'"]').click()
    
    #if website is using Select you can use:
    #manufacturer_list = Select(driver.find_element_by_css_selector("ul[class='select-option-menu-container']"))
    #manufacturer_list.select_by_value("bmw")
    
    model = driver.find_element_by_css_selector("input[aria-labelledby='question3-title question3-questiontype']")
    model.click()
    model.send_keys(str(cars_data.at[i,"model"]))
    
    fuel = driver.find_element_by_css_selector("input[aria-labelledby='question5-title question5-questiontype']")
    fuel.find_element_by_xpath(u'//span[text()="'+cars_data.at[i,"fuel"]+'"]').click()
    
    price = driver.find_element_by_css_selector("input[aria-labelledby='question5-title question5-questiontype']")
    price.click()
    price.send_keys(int(cars_data.at[i,"price"]))
    
    description = driver.find_element_by_css_selector("textarea[aria-labelledby='question6-title question6-questiontype']")
    description.click()
    description.send_keys(cars_data.at[i,"description"])
    
#    driver.execute_script('document.querySelector("[aria-labelledby="question6-title question6-questiontype"]").value="My Dummy Text";')

    submit_button = driver.find_element_by_css_selector("button[class='__submit-button__ office-form-bottom-button office-form-theme-button button-control light-background-button']")
    submit_button.click()
        
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span[class='thank-you-page-comfirm-text']")))
    driver.get("https://forms.office.com/Pages/ResponsePage.aspx?id=DQSIkWdsW0yxEjajBLZtrQAAAAAAAAAAAAN__tPvGS1URFNTU0RQNjdaRThJSVowWDdUMkZTS1dOSy4u")

    