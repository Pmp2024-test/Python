from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException


class FormPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)  # Увеличим время ожидания
        self.fields = {
            'first-name': "Иван",
            'last-name': "Петров",
            'address': "Ленина, 55-3",
            'zip-code': "",
            'city': "Москва",
            'country': "Россия",
            'e-mail': "test@skypro.com",
            'phone': "+7985899998787",
            'job-position': "QA",
            'company': "SkyPro"
        }

    def open(self):
        self.driver.get(
            "https://bonigarcia.dev/selenium-webdriver-java/data-types.html"
            )
        return self

    def fill_form(self):
        for field, value in self.fields.items():
            element = self.wait.until(
                EC.presence_of_element_located((By.NAME, field)))
            element.clear()
            element.send_keys(value)
        return self

    def submit_form(self):
        submit_button = self.wait.until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, '[type="submit"]')))
        
        # Надежный клик через JavaScript
        self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        self.driver.execute_script("arguments[0].click();", submit_button)
        
        # Ждем применения валидации
        self.wait.until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, '.alert-danger')))
        return self

    def get_field_class(self, field_id):
        element = self.wait.until(
            EC.presence_of_element_located((
                By.ID, field_id)))
        return element.get_attribute("class")

    def is_zip_code_has_error(self):
        return "alert-danger" in self.get_field_class("zip-code")

    def are_other_fields_have_success(self):
        fields = ['first-name', 'last-name', 'address', 'e-mail', 'phone',
                  'city', 'country', 'job-position', 'company']
        for field in fields:
            if "alert-success" not in self.get_field_class(field):
                return False
        return True

    def get_field_states(self):
        """Возвращает словарь с состояниями всех полей"""
        fields = ['first-name', 'last-name', 'address', 'e-mail', 'phone',
                  'city', 'country', 'job-position', 'company', 'zip-code']
        states = {}
        for field in fields:
            states[field] = self.get_field_class(field)
        return states
