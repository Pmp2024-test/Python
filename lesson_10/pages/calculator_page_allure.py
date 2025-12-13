from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
import allure


class CalculatorPage:
    """
    Page Object для страницы калькулятора.
    """

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализирует страницу калькулятора.

        Args:
            driver: WebDriver для управления браузером
        Returns:
            None
        """
        self.driver = driver

    @allure.step("Установить задержку: {seconds} секунд")
    def set_delay(self, seconds: int) -> None:
        """
        Устанавливает задержку вычислений.

        Args:
            seconds: Задержка в секундах
        Returns:
            None
        """
        delay_input = self.driver.find_element(By.CSS_SELECTOR, "#delay")
        delay_input.clear()
        delay_input.send_keys(str(seconds))

    @allure.step("Нажать кнопку 7")
    def click_7(self) -> None:
        """
        Нажимает кнопку с цифрой 7.

        Returns:
            None
        """
        self.driver.find_element(By.XPATH, '//span[text()="7"]').click()

    @allure.step("Нажать кнопку +")
    def click_plus(self) -> None:
        """
        Нажимает кнопку сложения.

        Returns:
            None
        """
        self.driver.find_element(By.XPATH, '//span[text()="+"]').click()

    @allure.step("Нажать кнопку 8")
    def click_8(self) -> None:
        """
        Нажимает кнопку с цифрой 8.

        Returns:
            None
        """
        self.driver.find_element(By.XPATH, '//span[text()="8"]').click()

    @allure.step("Нажать кнопку =")
    def click_equals(self) -> None:
        """
        Нажимает кнопку равно.

        Returns:
            None
        """
        self.driver.find_element(By.XPATH, '//span[text()="="]').click()

    @allure.step("Получить результат")
    def get_result(self) -> str:
        """
        Получает текст с экрана калькулятора.

        Returns:
            str: Результат вычисления
        """
        return self.driver.find_element(By.CSS_SELECTOR, ".screen").text

    @allure.step("Ожидать результат: {expected_result}")
    def wait_for_result(self, expected_result: str, timeout: int = 50) -> None:
        """
        Ожидает появления результата на экране.

        Args:
            expected_result: Ожидаемый результат
            timeout: Максимальное время ожидания в секундах
        Returns:
            None
        """
        WebDriverWait(self.driver, timeout).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".screen"), expected_result)
        )
