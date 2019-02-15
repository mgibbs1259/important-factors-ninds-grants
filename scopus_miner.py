from selenium import webdriver
from bs4 import BeautifulSoup
import time

# Get driver
driver = webdriver.Chrome()
driver.get("https://www.scopus.com/freelookup/form/author.uri?zone=&origin=NO%20ORIGIN%20DEFINED")

# Wait
time.sleep(2)

# Input author
driver.find_element_by_css_selector(".formControls > .inputTextLabel").click()
drive.find_element_by_css_selector("#lastname").send_keys("Han")

driver.quit()