from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def click_checkout(self):
        checkout_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, "checkout"))
        )
        checkout_button.click()
        return self

    def get_cart_items(self):
        items = self.driver.find_elements(By.CLASS_NAME, "cart_item")
        return len(items)

    def remove_product(self, product_name):
        remove_xpath = \
            f"//div[text()='{product_name}']/ancestor::div[@class='cart_item']//button"
        remove_button = self.driver.find_element(By.XPATH, remove_xpath)
        remove_button.click()
        return self
