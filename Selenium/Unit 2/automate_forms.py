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

