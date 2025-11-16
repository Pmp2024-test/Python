import pytest
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver():
    service = EdgeService(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service)
    driver.maximize_window()
    
    yield driver
    
    driver.quit()

def test_open_page(driver):
    driver.get("https://bonigarcia.dev/selenium-webdriver-java/data-types.html")
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    # Заполнение формы
    driver.find_element(By.NAME, "first-name").send_keys("Иван")
    driver.find_element(By.NAME, "last-name").send_keys("Петров")
    driver.find_element(By.NAME, "address").send_keys("Ленина, 55-3")
    driver.find_element(By.NAME, "e-mail").send_keys("test@skypro.com")
    driver.find_element(By.NAME, "phone").send_keys("+7985899998787")
    driver.find_element(By.NAME, "zip").send_keys("")  # Оставляем пустым
    driver.find_element(By.NAME, "city").send_keys("Москва")
    driver.find_element(By.NAME, "country").send_keys("Россия")
    driver.find_element(By.NAME, "job-position").send_keys("QA")
    driver.find_element(By.NAME, "company").send_keys("SkyPro")
    
    # Нажимаем кнопку Submit
    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    submit_button.click()
    
    # Проверка, что поле Zip code подсвечено красным
    zip_code_field = driver.find_element(By.NAME, "zip-code")
    zip_code_class = zip_code_field.get_attribute("class")
    assert "is-invalid" in zip_code_class, "Поле Zip code не подсвечено красным"
    
    # Проверка, что остальные поля подсвечены зеленым
    fields_to_check = [
        "first-name", "last-name", "address", "e-mail", "phone", 
        "city", "country", "job-position", "company"
    ]
    
    for field_name in fields_to_check:
        field = driver.find_element(By.NAME, field_name)
        field_class = field.get_attribute("class")
        assert "is-valid" in field_class, f"Field {field_name} должны иметь зеленую подсветку"
    print("Все проверки пройдены успешно!")

    driver.quit()


