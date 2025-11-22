from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def fill_shipping_info(self, first_name, last_name, postal_code):
        first_name_field = self.wait.until(
            EC.presence_of_element_located((By.ID, "first-name"))
        )
        first_name_field.clear()
        first_name_field.send_keys(first_name)

        last_name_field = self.driver.find_element(By.ID, "last-name")
        last_name_field.clear()
        last_name_field.send_keys(last_name)

        postal_code_field = self.driver.find_element(By.ID, "postal-code")
        postal_code_field.clear()
        postal_code_field.send_keys(postal_code)

        return self

    def click_continue(self):
        continue_button = self.driver.find_element(By.ID, "continue")
        continue_button.click()
        return self

    def get_total_price(self):
        total_element = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "summary_total_label"))
        )
        total_text = total_element.text
        # Извлекаем число из строки вида "Total: $58.29"
        total_price = total_text.split('$')[-1]
        return float(total_price)

    def click_finish(self):
        finish_button = self.driver.find_element(By.ID, "finish")
        finish_button.click()
        return self

    def get_complete_message(self):
        complete_message = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "complete-header"))
        )
        return complete_message.text
