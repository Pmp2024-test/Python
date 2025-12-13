from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
import allure
from typing import List


class CartPage:
    """
    Page Object для страницы корзины покупок.

    Методы для взаимодействия с элементами корзины:
    - переход к оформлению заказа
    - получение списка товаров
    - удаление товаров из корзины
    """

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализация страницы корзины.

        Args:
            driver: WebDriver для управления браузером
        Returns:
            None
        """
        self.driver: WebDriver = driver
        self.wait: WebDriverWait = WebDriverWait(driver, 10)

    @allure.step("Нажать кнопку 'Checkout'")
    def click_checkout(self) -> 'CartPage':
        """
        Нажимает кнопку для перехода к оформлению заказа.

        Returns:
            CartPage: Текущий экземпляр страницы (для цепочки вызовов)
        """
        checkout_button: WebElement = self.wait.until(
            EC.element_to_be_clickable((By.ID, "checkout"))
        )
        checkout_button.click()
        return self

    @allure.step("Получить количество товаров в корзине")
    def get_cart_items(self) -> int:
        """
        Подсчитывает количество товаров в корзине.

        Returns:
            int: Количество товаров в корзине
        """
        items: List[WebElement] = self.driver.find_elements(By.CLASS_NAME, "cart_item")
        item_count: int = len(items)

        allure.attach(
            f"Количество товаров в корзине: {item_count}",
            name="cart_items_count",
            attachment_type=allure.attachment_type.TEXT
        )

        return item_count

    @allure.step("Удалить товар '{product_name}' из корзины")
    def remove_product(self, product_name: str) -> 'CartPage':
        """
        Удаляет указанный товар из корзины.

        Args:
            product_name: Название товара для удаления
        Returns:
            CartPage: Текущий экземпляр страницы (для цепочки вызовов)
        """
        remove_xpath: str = f"//div[text()='{product_name}']/ancestor::div[@class='cart_item']//button"

        try:
            remove_button: WebElement = self.driver.find_element(By.XPATH, remove_xpath)
            remove_button.click()

            allure.attach(
                f"Товар '{product_name}' удален из корзины",
                name="product_removed",
                attachment_type=allure.attachment_type.TEXT
            )

        except Exception as e:
            allure.attach(
                f"Не удалось удалить товар '{product_name}': {str(e)}",
                name="remove_product_error",
                attachment_type=allure.attachment_type.TEXT
            )
            raise

        return self
