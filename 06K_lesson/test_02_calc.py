import pytest
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
import time

@pytest.fixture
def driver():
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    
    yield driver
    driver.quit()
def test_slow_calculator(driver):
    driver.get("https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html")
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "delay"))
    )
    
    delay_field = driver.find_element(By.ID, "delay")
    delay_field.clear()
    delay_field.send_keys("45")
    
    # Нажимаем кнопки: 7 + 8 =
    driver.find_element(By.XPATH, "//span[text()='7']").click()
    driver.find_element(By.XPATH, "//span[text()='+']").click()
    driver.find_element(By.XPATH, "//span[text()='8']").click()
    driver.find_element(By.XPATH, "//span[text()='=']").click()
    
    # Явное ожидание 46 секунд
    result_element = driver.find_element(By.CLASS_NAME, "screen")
    
    # Ждем пока результат не станет 15 с тайм-аутом
    WebDriverWait(driver, 46).until(
        EC.text_to_be_present_in_element((By.CLASS_NAME, "screen"), "15")
    )
    
    # Проверка результата
    final_result = result_element.text
    assert final_result == "15", f"Ожидался результат '15', но получили '{final_result}'"
    
    print("Тест пройден! Резульаь 15 появился через 45 секунд")
