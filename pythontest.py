from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from parse import *

dcid='voxindochim'
dcpw='dochim1212!'
# file = open("./data/history.txt")


options = webdriver.ChromeOptions() 
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("start-maximized")
chrome_driver = webdriver.Chrome(options=options, executable_path='D:/chromedriver/chromedriver.exe')
chrome_driver.implicitly_wait(5)

 
# enter keyword to search
keyword = "geeksforgeeks"
 
# get geeksforgeeks.org
chrome_driver.get("https://www.geeksforgeeks.org/")
 
# get element
element = chrome_driver.find_element(By.LINK_TEXT,"Courses").get_attribute('href')
 
# get href attribute
print(element)
print(type(element))