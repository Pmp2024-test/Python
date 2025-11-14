import pytest
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.support import expected_conditions as EC


def driver():
    edge_driver_path = r"c:\edgedriver_win64\msedgedriver.exe"
    driver = webdriver.Edge(service=EdgeService(edge_driver_path))

    driver.maximize_window()

    yield driver

    driver.quit()
def test_open_page(driver):
    driver.get("https://bonigarcia.dev/selenium-webdriver-java/data-types.html")



   

  


