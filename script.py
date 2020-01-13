#!/usr/bin/env python

from selenium import webdriver

# Creating the WebDriver object using the ChromeDriver
driver = webdriver.Chrome()

driver.get('http://www.ubuntu.com/')

# https://dzone.com/articles/python-getting-started