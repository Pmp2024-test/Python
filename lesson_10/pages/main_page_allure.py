from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
import allure
from typing import List, Optional


class MainPage:
    """
    Page Object для главной страницы интернет-магазина.

    Методы для взаимодействия с товарами, корзиной
    и навигацией по главной странице.
    """

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализация главной страницы.

        Args:
            driver: WebDriver для управления браузером
        Returns:
            None
        """
        self.driver: WebDriver = driver
        self.wait: WebDriverWait = WebDriverWait(driver, 10)

    @allure.step("Добавить товар '{product_name}' в корзину")
    def add_product_to_cart(self, product_name: str) -> 'MainPage':
        """
        Добавляет указанный товар в корзину покупок.

        Args:
            product_name: Название товара для добавления в корзину
        Returns:
            MainPage: Текущий экземпляр страницы (для цепочки вызовов)
        """
        product_xpath: str = f"//div[text()='{product_name}']/ancestor::div[@class='inventory_item']//button"

        try:
            add_to_cart_button: WebElement = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, product_xpath))
            )
            add_to_cart_button.click()

            allure.attach(
                f"Товар '{product_name}' добавлен в корзину",
                name="product_added_to_cart",
                attachment_type=allure.attachment_type.TEXT
            )

        except Exception as e:
            allure.attach(
                f"Не удалось добавить товар '{product_name}' в корзину: {str(e)}",
                name="add_product_error",
                attachment_type=allure.attachment_type.TEXT
            )
            raise

        return self

    @allure.step("Перейти в корзину")
    def go_to_cart(self) -> 'MainPage':
        """
        Переходит на страницу корзины покупок.

        Returns:
            MainPage: Текущий экземпляр страницы (для цепочки вызовов)
        """
        cart_button: WebElement = self.driver.find_element(
            By.CLASS_NAME, "shopping_cart_link"
        )
        cart_button.click()

        allure.attach(
            "Переход в корзину выполнен",
            name="navigated_to_cart",
            attachment_type=allure.attachment_type.TEXT
        )

        return self

    @allure.step("Получить количество товаров в корзине")
    def get_cart_count(self) -> int:
        """
        Получает текущее количество товаров в корзине из бейджа.

        Returns:
            int: Количество товаров в корзине (0 если корзина пуста)
        """
        cart_badge_elements: List[WebElement] = self.driver.find_elements(
            By.CLASS_NAME, "shopping_cart_badge"
        )

        if cart_badge_elements:
            cart_count_text: str = cart_badge_elements[0].text
            try:
                cart_count: int = int(cart_count_text)

                allure.attach(
                    f"Количество товаров в корзине: {cart_count}",
                    name="cart_count",
                    attachment_type=allure.attachment_type.TEXT
                )

                return cart_count
            except ValueError:
                allure.attach(
                    f"Не удалось преобразовать '{cart_count_text}' в число",
                    name="cart_count_error",
                    attachment_type=allure.attachment_type.TEXT
                )
                return 0
        else:
            allure.attach(
                "Корзина пуста (бейдж не отображается)",
                name="cart_empty",
                attachment_type=allure.attachment_type.TEXT
            )
            return 0
