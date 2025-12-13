import pytest
import allure
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.firefox import GeckoDriverManager
from pages.login_page_allure import LoginPage
from pages.main_page_allure import MainPage
from pages.cart_page_allure import CartPage
from pages.checkout_page_allure import CheckoutPage
from typing import List


@allure.feature("Полный поток покупки")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("e2e", "purchase", "firefox")
class TestSauceDemo:
    """
    End-to-end тест полного потока покупки в интернет-магазине.
    """

    @pytest.fixture
    def driver(self) -> WebDriver:
        """
        Фикстура для создания и настройки Firefox WebDriver.
        """
        with allure.step("Инициализация Firefox драйвера"):
            service = Service(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service)
            driver.maximize_window()

        yield driver

        with allure.step("Завершение работы драйвера"):
            driver.quit()

    @allure.title("Полный поток покупки в интернет-магазине")
    @allure.description("""
    End-to-end тест полного цикла покупки:
    1. Авторизация в системе
    2. Добавление товаров в корзину
    3. Переход в корзину и проверка содержимого
    4. Оформление заказа с заполнением информации о доставке
    5. Проверка итоговой суммы заказа
    """)
    def test_complete_purchase_flow(self, driver: WebDriver) -> None:
        """
        Тестирование полного потока покупки в интернет-магазине.
        """
        # Тестовые данные
        USERNAME: str = "standard_user"
        PASSWORD: str = "secret_sauce"
        PRODUCTS_TO_ADD: List[str] = [
            "Sauce Labs Backpack",
            "Sauce Labs Bolt T-Shirt",
            "Sauce Labs Onesie"
        ]
        FIRST_NAME: str = "Марина"
        LAST_NAME: str = "Панова"
        POSTAL_CODE: str = "249360"
        EXPECTED_TOTAL: float = 58.29

        with allure.step("Шаг 1: Авторизация в системе"):
            login_page = LoginPage(driver)

            with allure.step("Открыть страницу авторизации"):
                login_page.open()

            with allure.step(f"Войти под пользователем {USERNAME}"):
                login_page.login(USERNAME, PASSWORD)

                allure.attach(
                    f"Успешная авторизация пользователя: {USERNAME}",
                    name="login_successful",
                    attachment_type=allure.attachment_type.TEXT
                )

        with allure.step("Шаг 2: Добавление товаров в корзину"):
            main_page = MainPage(driver)

            with allure.step(f"Добавить {len(PRODUCTS_TO_ADD)} товаров в корзину"):
                for product in PRODUCTS_TO_ADD:
                    with allure.step(f"Добавить товар: {product}"):
                        main_page.add_product_to_cart(product)

            with allure.step("Проверить количество товаров в корзине"):
                cart_count = main_page.get_cart_count()
                allure.attach(
                    f"Товаров в корзине: {cart_count} (ожидалось: {len(PRODUCTS_TO_ADD)})",
                    name="cart_count_check",
                    attachment_type=allure.attachment_type.TEXT
                )

                assert cart_count == len(PRODUCTS_TO_ADD), \
                    f"Ожидалось {len(PRODUCTS_TO_ADD)} товаров, но в корзине {cart_count}"

        with allure.step("Шаг 3: Переход в корзину"):
            main_page.go_to_cart()

            current_url = driver.current_url
            allure.attach(
                f"Перешли в корзину. URL: {current_url}",
                name="cart_navigation",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Шаг 4: Проверка содержимого корзины"):
            cart_page = CartPage(driver)

            with allure.step("Получить количество товаров в корзине"):
                cart_items_count = cart_page.get_cart_items()
                allure.attach(
                    f"Товаров в корзине: {cart_items_count}",
                    name="cart_items_count",
                    attachment_type=allure.attachment_type.TEXT
                )

                assert cart_items_count == len(PRODUCTS_TO_ADD), \
                    f"В корзине {cart_items_count} товаров вместо {len(PRODUCTS_TO_ADD)}"

            with allure.step("Начать оформление заказа"):
                cart_page.click_checkout()

                current_url = driver.current_url
                allure.attach(
                    f"Перешли к оформлению. URL: {current_url}",
                    name="checkout_navigation",
                    attachment_type=allure.attachment_type.TEXT
                )

        with allure.step("Шаг 5: Заполнение информации о доставке"):
            checkout_page = CheckoutPage(driver)

            with allure.step(f"Заполнить информацию: {FIRST_NAME} {LAST_NAME}, {POSTAL_CODE}"):
                checkout_page.fill_shipping_info(FIRST_NAME, LAST_NAME, POSTAL_CODE)

            with allure.step("Перейти к подтверждению заказа"):
                checkout_page.click_continue()

        with allure.step("Шаг 6: Проверка итоговой суммы заказа"):
            with allure.step("Получить общую сумму заказа"):
                total_price = checkout_page.get_total_price()
                allure.attach(
                    f"Общая сумма заказа: ${total_price:.2f} (ожидалось: ${EXPECTED_TOTAL:.2f})",
                    name="total_price_comparison",
                    attachment_type=allure.attachment_type.TEXT
                )

            with allure.step("Проверить соответствие ожидаемой сумме"):
                assert abs(total_price - EXPECTED_TOTAL) < 0.01, \
                    f"Ожидаемая сумма: ${EXPECTED_TOTAL:.2f}, Фактическая: ${total_price:.2f}"

                allure.attach(
                    f"✅ Тест пройден! Итоговая сумма: ${total_price:.2f}",
                    name="test_passed",
                    attachment_type=allure.attachment_type.TEXT
                )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
