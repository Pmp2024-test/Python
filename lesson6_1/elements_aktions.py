from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get("https://ya.ru/")

element = driver.find_element(By.CSS_SELECTOR, '#text')
element.clear() #очищаем элемент
element.send_keys("test skypro") #вводим текст в поле

driver.find_element(By.CSS_SELECTOR, "button[type=submit]").click() #вводим данные
# кнопки уникальные и нажимаем на нее

sleep(15)

driver.quit()
