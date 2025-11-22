import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from pages.Login_page import LoginPage
from pages.Main_page import MainPage
from pages.Cart_page import CartPage
from pages.Checkout_page import CheckoutPage


class TestSauceDemo:
    @pytest.fixture
    def driver(self):
        # Настройка Firefox драйвера
        service = Service(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service)
        driver.maximize_window()
        yield driver
        driver.quit()

    def test_complete_purchase_flow(self, driver):
        # Тестовые данные
        USERNAME = "standard_user"
        PASSWORD = "secret_sauce"
        PRODUCTS_TO_ADD = [
            "Sauce Labs Backpack",
            "Sauce Labs Bolt T-Shirt",
            "Sauce Labs Onesie"
        ]
        FIRST_NAME = "Марина"
        LAST_NAME = "Панова"
        POSTAL_CODE = "249360"
        EXPECTED_TOTAL = 58.29

        # Шаг 1: Авторизация
        login_page = LoginPage(driver)
        login_page.open().login(USERNAME, PASSWORD)

        # Шаг 2: Добавление товаров в корзину
        main_page = MainPage(driver)
        for product in PRODUCTS_TO_ADD:
            main_page.add_product_to_cart(product)

        # Проверяем, что все товары добавлены
        cart_count = main_page.get_cart_count()
        assert cart_count == len(PRODUCTS_TO_ADD), (
            f"Ожидалось {len(PRODUCTS_TO_ADD)} товаров, но в корзине {cart_count}"
        )

        # Шаг 3: Переход в корзину
        main_page.go_to_cart()

        # Шаг 4: Нaчало оформления заказа
        cart_page = CartPage(driver)
        cart_items_count = cart_page.get_cart_items()
        assert cart_items_count == len(PRODUCTS_TO_ADD), (
            f"В корзине {cart_items_count} товаров вместо {len(PRODUCTS_TO_ADD)}"
        )
        cart_page.click_checkout()

        # Шаг 5: Заполнение информации о доставке
        checkout_page = CheckoutPage(driver)
        checkout_page.fill_shipping_info(FIRST_NAME, LAST_NAME, POSTAL_CODE)
        checkout_page.click_continue()

        # Шаг 6: Проверка итоговой суммы
        total_price = checkout_page.get_total_price()

        # Проверка утверждения
        assert total_price == EXPECTED_TOTAL, (
            f"Ожидаемая сумма: ${EXPECTED_TOTAL}, Фактическая: ${total_price}"
        )
        print(f"Тест пройден! Итоговая сумма: ${total_price}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
