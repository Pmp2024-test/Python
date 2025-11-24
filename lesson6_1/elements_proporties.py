from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get("https://ya.ru/")

txt = driver.find_element(By.CSS_SELECTOR, "a[title=USD MDEX']").text
print(txt)

tag = driver.find_element(By.CSS_SELECTOR, "a[title=USD MDEX']").text_name
print(tag)

id = driver.find_element(By.CSS_SELECTOR, "a[title=USD MDEX']").id
print(id)

href = driver.find_element(By.CSS_SELECTOR, "a[title=USD MDEX']").get_attribute("href")
print(href)

ff = driver.find_element(By.CSS_SELECTOR, "a[title=USD MDEX']").value_of_css_property("fent-family")
color = driver.find_element(By.CSS_SELECTOR, "a[title=USD MDEX']").value_of_css_property("color")
print(ff)
print(color)

sleep(50)

driver.quit()
