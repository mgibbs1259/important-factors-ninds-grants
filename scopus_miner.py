import time

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

# Get driver
driver = webdriver.Chrome()
driver.get("https://www.scopus.com/freelookup/form/author.uri?zone=&origin=NO%20ORIGIN%20DEFINED")

# Wait
time.sleep(2)

# Input author
driver.find_element_by_css_selector(".formControls > .inputTextLabel").click()
time.sleep(1)
driver.find_element_by_css_selector(".formControls > .inputTextLabel").send_keys("Han")

driver.quit()