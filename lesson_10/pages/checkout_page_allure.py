from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
import allure
from typing import Optional


class CheckoutPage:
    """
    Page Object для страницы оформления заказа.

    Методы для заполнения информации о доставке,
    подтверждения заказа и завершения покупки.
    """

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализация страницы оформления заказа.

        Args:
            driver: WebDriver для управления браузером
        Returns:
            None
        """
        self.driver: WebDriver = driver
        self.wait: WebDriverWait = WebDriverWait(driver, 10)

    @allure.step("Заполнить информацию о доставке: {first_name} {last_name}, {postal_code}")
    def fill_shipping_info(self, first_name: str, last_name: str, postal_code: str) -> 'CheckoutPage':
        """
        Заполняет форму с информацией о доставке.

        Args:
            first_name: Имя покупателя
            last_name: Фамилия покупателя
            postal_code: Почтовый индекс
        Returns:
            CheckoutPage: Текущий экземпляр страницы (для цепочки вызовов)
        """
        # Заполнение поля имени
        first_name_field: WebElement = self.wait.until(
            EC.presence_of_element_located((By.ID, "first-name"))
        )
        first_name_field.clear()
        first_name_field.send_keys(first_name)

        # Заполнение поля фамилии
        last_name_field: WebElement = self.driver.find_element(By.ID, "last-name")
        last_name_field.clear()
        last_name_field.send_keys(last_name)

        # Заполнение поля почтового индекса
        postal_code_field: WebElement = self.driver.find_element(By.ID, "postal-code")
        postal_code_field.clear()
        postal_code_field.send_keys(postal_code)

        allure.attach(
            f"Заполнена информация о доставке:\n"
            f"Имя: {first_name}\n"
            f"Фамилия: {last_name}\n"
            f"Индекс: {postal_code}",
            name="shipping_info",
            attachment_type=allure.attachment_type.TEXT
        )

        return self

    @allure.step("Нажать кнопку 'Continue'")
    def click_continue(self) -> 'CheckoutPage':
        """
        Нажимает кнопку для продолжения оформления заказа.

        Returns:
            CheckoutPage: Текущий экземпляр страницы (для цепочки вызовов)
        """
        continue_button: WebElement = self.driver.find_element(By.ID, "continue")
        continue_button.click()
        return self

    @allure.step("Получить общую сумму заказа")
    def get_total_price(self) -> float:
        """
        Получает общую сумму заказа из итоговой секции.

        Returns:
            float: Общая сумма заказа в числовом формате
        """
        total_element: WebElement = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "summary_total_label"))
        )
        total_text: str = total_element.text

        # Извлекаем число из строки вида "Total: $58.29"
        try:
            total_price_str: str = total_text.split('$')[-1]
            total_price: float = float(total_price_str)

            allure.attach(
                f"Общая сумма заказа: ${total_price:.2f}",
                name="order_total",
                attachment_type=allure.attachment_type.TEXT
            )

            return total_price
        except (ValueError, IndexError) as e:
            allure.attach(
                f"Ошибка извлечения суммы из текста '{total_text}': {str(e)}",
                name="total_price_error",
                attachment_type=allure.attachment_type.TEXT
            )
            raise ValueError(f"Не удалось извлечь сумму из текста: {total_text}")

    @allure.step("Нажать кнопку 'Finish'")
    def click_finish(self) -> 'CheckoutPage':
        """
        Нажимает кнопку для завершения оформления заказа.

        Returns:
            CheckoutPage: Текущий экземпляр страницы (для цепочки вызовов)
        """
        finish_button: WebElement = self.driver.find_element(By.ID, "finish")
        finish_button.click()
        return self

    @allure.step("Получить сообщение об успешном оформлении заказа")
    def get_complete_message(self) -> str:
        """
        Получает текст сообщения об успешном завершении заказа.

        Returns:
            str: Текст сообщения о завершении заказа
        """
        complete_message: WebElement = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "complete-header"))
        )
        message_text: str = complete_message.text

        allure.attach(
            f"Сообщение об оформлении заказа: '{message_text}'",
            name="order_complete_message",
            attachment_type=allure.attachment_type.TEXT
        )

        return message_text
