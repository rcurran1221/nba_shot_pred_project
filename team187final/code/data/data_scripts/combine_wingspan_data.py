#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 11:37:03 2020

@author: adam
"""

import os 
import pandas as pd 
import urllib

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.support.ui import Select 

from bs4 import BeautifulSoup 
import re 
import numpy as np 

os.chdir("/Users/adam/Documents/GT Masters/CSE 6242/project")
headers = { 'User-Agent' : 'Mozilla/5.0' }

base_url = "https://stats.nba.com/draft/combine-anthro/?SeasonYear=2000-01"

req = urllib.request.Request(base_url, None, headers)
r = urllib.request.urlopen(req).read()
soup = BeautifulSoup(r)



class get_combine_data():
    
    def __init__(self):
    
        self.driver = webdriver.Chrome("/Users/adam/Documents/GT Masters/CSE 6242/project/chromedriver")
        
    def launch_nba_website(self):
        
        self.driver.get('https://stats.nba.com/draft/combine-anthro/?SeasonYear=2000-01')
    
    


ye = get_combine_data()
ye.launch_nba_website()
