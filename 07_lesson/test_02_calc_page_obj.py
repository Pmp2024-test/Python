import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from pages.calculator_page import CalculatorPage


@pytest.fixture
def driver():
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()))
    driver.get(
        "https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html"
    )
    driver.implicitly_wait(4)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def calculator(driver):
    return CalculatorPage(driver)


def test_calculator_45_seconds_delay(driver, calculator):
    calculator.set_delay(45)

    # Выполнение вычисления 7 + 8 
    calculator.click_7()
    calculator.click_plus()
    calculator.click_8()
    calculator.click_equals()

    # Ожидание результата 
    calculator.wait_for_result("15", 50)

    # Проверка результата 
    result = calculator.get_result()
    assert result == "15"
