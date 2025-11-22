from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MainPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def add_product_to_cart(self, product_name):
        # Находим продукт по имени и добавляем в корзину
        product_xpath = f"//div[text()='{product_name}' \
            ]/ancestor::div[@class='inventory_item']//button"
        add_to_cart_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, product_xpath))
        )
        add_to_cart_button.click()
        return self

    def go_to_cart(self):
        cart_button = self.driver.find_element(
            By.CLASS_NAME, "shopping_cart_link")
        cart_button.click()
        return self

    def get_cart_count(self):
        cart_badge = self.driver.find_elements(
            By.CLASS_NAME, "shopping_cart_badge"
            )
        if cart_badge:
            return int(cart_badge[0].text)
        return 0
