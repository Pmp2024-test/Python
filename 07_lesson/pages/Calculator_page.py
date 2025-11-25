from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CalculatorPage:
    def __init__(self, driver):
        self.driver = driver

    def set_delay(self, seconds):
        delay_input = self.driver.find_element(By.CSS_SELECTOR, "#delay")
        delay_input.clear()
        delay_input.send_keys(str(seconds))

    def click_7(self):
        self.driver.find_element(By.XPATH, '//span[text()="7"]').click()

    def click_plus(self):
        self.driver.find_element(By.XPATH, '//span[text()="+"]').click()

    def click_8(self):
        self.driver.find_element(By.XPATH, '//span[text()="8"]').click()

    def click_equals(self):
        self.driver.find_element(By.XPATH, '//span[text()="="]').click()

    def get_result(self):
        return self.driver.find_element(By.CSS_SELECTOR, ".screen").text

    def wait_for_result(self, expected_result, timeout=50):
        WebDriverWait(self.driver, timeout).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".screen"), expected_result)
        )
