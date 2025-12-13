from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
import allure
from typing import Dict, List, Optional, Tuple


class FormPage:
    """
    Page Object для страницы с формой заполнения данных.

    Методы для работы с формой, заполнения полей и проверки валидации.
    """

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализация страницы с формой.

        Args:
            driver: WebDriver для управления браузером
        Returns:
            None
        """
        self.driver: WebDriver = driver
        self.wait: WebDriverWait = WebDriverWait(driver, 10)

        # Данные для заполнения формы
        self.fields: Dict[str, str] = {
            'first-name': "Иван",
            'last-name': "Петров",
            'address': "Ленина, 55-3",
            'zip-code': "",  # Пустое поле для проверки ошибки
            'city': "Москва",
            'country': "Россия",
            'e-mail': "test@skypro.com",
            'phone': "+7985899998787",
            'job-position': "QA",
            'company': "SkyPro"
        }

    @allure.step("Открыть страницу с формой")
    def open(self) -> 'FormPage':
        """
        Открывает страницу с формой для заполнения данных.

        Returns:
            FormPage: Текущий экземпляр страницы (для цепочки вызовов)
        """
        self.driver.get(
            "https://bonigarcia.dev/selenium-webdriver-java/data-types.html"
        )
        return self

    @allure.step("Заполнить все поля формы")
    def fill_form(self) -> 'FormPage':
        """
        Заполняет все поля формы тестовыми данными.

        Returns:
            FormPage: Текущий экземпляр страницы (для цепочки вызовов)
        """
        for field, value in self.fields.items():
            self._fill_field(field, value)
        return self

    @allure.step("Заполнить поле '{field_name}' значением '{value}'")
    def _fill_field(self, field_name: str, value: str) -> None:
        """
        Заполняет конкретное поле формы.

        Args:
            field_name: Имя поля (атрибут name)
            value: Значение для заполнения
        Returns:
            None
        """
        element: WebElement = self.wait.until(
            EC.presence_of_element_located((By.NAME, field_name))
        )
        element.clear()
        element.send_keys(value)

    @allure.step("Отправить форму")
    def submit_form(self) -> 'FormPage':
        """
        Отправляет форму на сервер.
        Использует JavaScript для надежного клика.

        Returns:
            FormPage: Текущий экземпляр страницы (для цепочки вызовов)
        """
        submit_button: WebElement = self.wait.until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, '[type="submit"]'
            ))
        )

        # Надежный клик через JavaScript
        self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        self.driver.execute_script("arguments[0].click();", submit_button)

        # Ждем применения валидации
        self.wait.until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, '.alert-danger'
            ))
        )
        return self

    @allure.step("Получить CSS класс поля '{field_id}'")
    def get_field_class(self, field_id: str) -> str:
        """
        Получает CSS класс элемента поля формы.

        Args:
            field_id: ID поля формы
        Returns:
            str: Значение атрибута class
        """
        element: WebElement = self.wait.until(
            EC.presence_of_element_located((By.ID, field_id))
        )
        return element.get_attribute("class")

    @allure.step("Проверить, что поле zip-code имеет ошибку")
    def is_zip_code_has_error(self) -> bool:
        """
        Проверяет, содержит ли поле zip-code класс ошибки.

        Returns:
            bool: True если поле содержит alert-danger, иначе False
        """
        field_class: str = self.get_field_class("zip-code")
        return "alert-danger" in field_class

    @allure.step("Проверить, что все остальные поля успешно заполнены")
    def are_other_fields_have_success(self) -> bool:
        """
        Проверяет, что все поля кроме zip-code имеют класс успеха.

        Returns:
            bool: True если все поля содержат alert-success, иначе False
        """
        fields: List[str] = [
            'first-name', 'last-name', 'address', 'e-mail', 'phone',
            'city', 'country', 'job-position', 'company'
        ]

        for field in fields:
            field_class: str = self.get_field_class(field)
            if "alert-success" not in field_class:
                allure.attach(
                    f"Поле '{field}' не имеет класса success. Класс: {field_class}",
                    name=f"field_{field}_error",
                    attachment_type=allure.attachment_type.TEXT
                )
                return False
        return True

    @allure.step("Получить состояния всех полей формы")
    def get_field_states(self) -> Dict[str, str]:
        """
        Возвращает словарь с классами всех полей формы.

        Returns:
            Dict[str, str]: Словарь {field_id: css_class}
        """
        fields: List[str] = [
            'first-name', 'last-name', 'address', 'e-mail', 'phone',
            'city', 'country', 'job-position', 'company', 'zip-code'
        ]

        states: Dict[str, str] = {}
        for field in fields:
            states[field] = self.get_field_class(field)

        return states
