from selenium import webdriver
 
# The place we will direct our WebDriver to
url = 'http://www.srcmake.com/'

# Creating the WebDriver object using the ChromeDriver
driver = webdriver.Chrome()

# Directing the driver to the defined url
driver.get(url)

# https://www.srcmake.com/home/selenium-python-chromedriver-ubuntu
# https://dzone.com/articles/python-getting-started  => this is not