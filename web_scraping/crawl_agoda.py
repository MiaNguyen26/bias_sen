import time
import numpy as np
import pandas as pd
import requests
import json
import math
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


CHROME_DRIVER_PATH = '/home/user/Downloads/chromedriver/chromedriver'
start_urls = [
                'https://www.agoda.com/vi-vn/search?city=16079',
                # 'https://www.agoda.com/vi-vn/city/c-n-tho-vn.html'
]

def parse():
    
    #loop over each url 
    for url in start_urls:
        driver_path = CHROME_DRIVER_PATH
        driver = webdriver.Chrome(driver_path)
        driver.get(start_urls[0])
        time.sleep(5)
