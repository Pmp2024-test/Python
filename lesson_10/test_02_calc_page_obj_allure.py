import pytest
import allure
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from pages.calculator_page_allure import CalculatorPage


@pytest.fixture
def driver() -> WebDriver:
    """Создает и настраивает драйвер Chrome."""
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install())
    )
    driver.get(
        "https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html"
    )
    driver.implicitly_wait(4)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def calculator(driver: WebDriver) -> CalculatorPage:
    """Создает экземпляр CalculatorPage."""
    return CalculatorPage(driver)


@allure.feature("Калькулятор")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Тест калькулятора с задержкой 45 секунд")
@allure.description("Проверка работы медленного калькулятора")
def test_calculator_45_seconds_delay(driver: WebDriver, calculator: CalculatorPage) -> None:
    """
    Тест сложения с задержкой 45 секунд.

    Args:
        driver: WebDriver для управления браузером
        calculator: Страница калькулятора
    Returns:
        None
    """
    with allure.step("Установить задержку 45 секунд"):
        calculator.set_delay(45)

    with allure.step("Выполнить вычисление 7 + 8"):
        calculator.click_7()
        calculator.click_plus()
        calculator.click_8()
        calculator.click_equals()

    with allure.step("Ожидать результат вычисления"):
        calculator.wait_for_result("15", 50)

    with allure.step("Проверить результат"):
        result = calculator.get_result()
        assert result == "15", f"Ожидался результат 15, получен {result}"
