from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CalculatorPage:
    def __init__(self):
        self.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()))
        self.driver.get(
            "https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html")
        self.driver.implicitly_wait(4)
        self.driver.maximize_window()

    def set_delay(self, seconds=45):
        text_input = self.driver.find_element(By.CSS_SELECTOR, "#delay")
        text_input.clear()
        text_input.send_keys(str(seconds))

    def enter_digits(self):
        self.driver.find_element(By.XPATH, '//span[text()="7"]').click()
        self.driver.find_element(By.XPATH, '//span[text()="+"]').click()
        self.driver.find_element(By.XPATH, '//span[text()="8"]').click()
        self.driver.find_element(By.XPATH, '//span[text()="="]').click()

    def wait_for_result(self):
        WebDriverWait(self.driver, 50).until(
            EC.text_to_be_present_in_element(
                ((By.CSS_SELECTOR, ".screen"), "15"))
            )

    def check_result(self):
        result = self.driver.find_element(By.CSS_SELECTOR, ".screen").text
        assert result == "15", f"Ожидался результат 15, но получен {result}"
        print("✅ Тест пройден! Результат 15 отобразился через 45 секунд")

    def close(self):
        self.driver.quit()
