from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_form_validation():
    # Инициализация драйвера Edge
    driver = webdriver.Edge()
    driver.get("https://bonigarcia.dev/selenium-webdriver-java/data-types.html")
    
    try:
        # Заполняем форму значениями
        driver.find_element(By.CSS_SELECTOR, 'input[name="first-name"]').send_keys("Иван")
        driver.find_element(By.CSS_SELECTOR, 'input[name="last-name"]').send_keys("Петров")
        driver.find_element(By.CSS_SELECTOR, 'input[name="address"]').send_keys("Ленина, 55-3")
        driver.find_element(By.CSS_SELECTOR, 'input[name="e-mail"]').send_keys("test@skypro.com")
        driver.find_element(By.CSS_SELECTOR, 'input[name="phone"]').send_keys("+7985899998787")
        # Zip code оставляем пустым
        driver.find_element(By.CSS_SELECTOR, 'input[name="city"]').send_keys("Москва")
        driver.find_element(By.CSS_SELECTOR, 'input[name="country"]').send_keys("Россия")
        driver.find_element(By.CSS_SELECTOR, 'input[name="job-position"]').send_keys("QA")
        driver.find_element(By.CSS_SELECTOR, 'input[name="company"]').send_keys("SkyPro")
        
        # Нажимаем кнопку Submit
        submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit_button.click()
        
        # Ждем применения стилей валидации
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-danger"))
        )
        # Проверяем, что поле Zip code подсвечено красным
        zip_code_field = driver.find_element(By.ID, 'zip-code')
        zip_code_class = zip_code_field.get_attribute("class")
        assert "alert py-2 alert-danger" in zip_code_class, "Поле Zip code не подсвечено красным"
        
        # Проверяем, что остальные поля подсвечены зеленым
        fields_to_check = [
            'first-name', 'last-name', 'address', 'e-mail', 'phone',
            'city', 'country', 'job-position', 'company'
        ]
        
        for field_name in fields_to_check:
            field = driver.find_element(By.ID, f"{field_name}")
            field_class = field.get_attribute("class")
            assert "alert py-2 alert-success" in field_class, f"Поле {field_name} не подсвечено зеленым"
            
    finally:
        # Закрываем браузер
        driver.quit()
