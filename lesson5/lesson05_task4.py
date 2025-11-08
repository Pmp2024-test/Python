from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()

driver.get("http://the-internet.herokuapp.com/login")

element_login = driver.find_element(By.CSS_SELECTOR, '#username')

element_login.send_keys("tomsmith")

element_parol = driver.find_element(By.CSS_SELECTOR, '#password')

element_parol.send_keys("SuperSecretPassword!")

check_input = driver.find_element(By.CLASS_NAME, 'radius').click()

# "#flash"

driver.quit()
sleep(15)
