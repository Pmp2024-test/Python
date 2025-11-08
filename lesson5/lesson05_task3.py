from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()

driver.get("http://the-internet.herokuapp.com/inputs")

search_field = driver.find_element(By.CSS_SELECTOR, "input")

search_field.send_keys("12345") 

search_field.clear()

search_field.send_keys("54321")

driver.quit()
sleep(15)
