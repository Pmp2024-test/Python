from time import sleep
from selenium import webdriver


browser = webdriver.Firefox()
browser.get("https://ya.ru/")

sleep(50)
