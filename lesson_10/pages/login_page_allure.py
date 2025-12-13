from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
import allure


class LoginPage:
    """
    Page Object для страницы авторизации.

    Методы для входа в систему, заполнения учетных данных
    и управления процессом аутентификации.
    """

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализация страницы авторизации.

        Args:
            driver: WebDriver для управления браузером
        Returns:
            None
        """
        self.driver: WebDriver = driver
        self.wait: WebDriverWait = WebDriverWait(driver, 10)

    @allure.step("Открыть страницу авторизации")
    def open(self) -> 'LoginPage':
        """
        Открывает страницу входа в систему.

        Returns:
            LoginPage: Текущий экземпляр страницы (для цепочки вызовов)
        """
        self.driver.get("https://www.saucedemo.com/")

        allure.attach(
            "Страница авторизации открыта: https://www.saucedemo.com/",
            name="login_page_opened",
            attachment_type=allure.attachment_type.TEXT
        )

        return self

    @allure.step("Ввести имя пользователя: {username}")
    def enter_username(self, username: str) -> 'LoginPage':
        """
        Вводит имя пользователя в соответствующее поле.

        Args:
            username: Имя пользователя для авторизации
        Returns:
            LoginPage: Текущий экземпляр страницы (для цепочки вызовов)
        """
        username_field: WebElement = self.wait.until(
            EC.presence_of_element_located((By.ID, "user-name"))
        )
        username_field.clear()
        username_field.send_keys(username)

        allure.attach(
            f"Введено имя пользователя: {username}",
            name="username_entered",
            attachment_type=allure.attachment_type.TEXT
        )

        return self

    @allure.step("Ввести пароль")
    def enter_password(self, password: str) -> 'LoginPage':
        """
        Вводит пароль в соответствующее поле.

        Args:
            password: Пароль для авторизации
        Returns:
            LoginPage: Текущий экземпляр страницы (для цепочки вызовов)
        """
        password_field: WebElement = self.driver.find_element(By.ID, "password")
        password_field.clear()
        password_field.send_keys(password)

        allure.attach(
            "Пароль введен (скрыт для безопасности)",
            name="password_entered",
            attachment_type=allure.attachment_type.TEXT
        )

        return self

    @allure.step("Нажать кнопку 'Login'")
    def click_login(self) -> 'LoginPage':
        """
        Нажимает кнопку входа в систему.

        Returns:
            LoginPage: Текущий экземпляр страницы (для цепочки вызовов)
        """
        login_button: WebElement = self.driver.find_element(By.ID, "login-button")
        login_button.click()

        allure.attach(
            "Нажата кнопка 'Login'",
            name="login_button_clicked",
            attachment_type=allure.attachment_type.TEXT
        )

        return self

    @allure.step("Выполнить вход с данными: {username}")
    def login(self, username: str, password: str) -> 'LoginPage':
        """
        Выполняет полный процесс авторизации.

        Args:
            username: Имя пользователя
            password: Пароль пользователя
        Returns:
            LoginPage: Текущий экземпляр страницы (для цепочки вызовов)
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

        allure.attach(
            f"Выполнена попытка входа пользователем: {username}",
            name="login_attempt",
            attachment_type=allure.attachment_type.TEXT
        )

        return self

    @allure.step("Проверить загрузку страницы авторизации")
    def is_login_page_loaded(self) -> bool:
        """
        Проверяет, корректно ли загружена страница авторизации.

        Returns:
            bool: True если страница загружена, иначе False
        """
        try:
            # Проверяем наличие ключевых элементов страницы логина
            username_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "user-name"))
            )
            password_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "password"))
            )
            login_button = self.wait.until(
                EC.presence_of_element_located((By.ID, "login-button"))
            )

            # Проверяем видимость элементов
            is_loaded = (
                username_field.is_displayed() and
                password_field.is_displayed() and
                login_button.is_displayed()
            )

            # Добавляем информацию в Allure-отчёт
            if is_loaded:
                allure.attach(
                    "Страница авторизации успешно загружена",
                    name="login_page_loaded",
                    attachment_type=allure.attachment_type.TEXT
                )
            else:
                allure.attach(
                    "Страница авторизации не полностью загружена",
                    name="login_page_not_loaded",
                    attachment_type=allure.attachment_type.TEXT
                )

            return is_loaded

        except Exception as e:
            # Если произошла ошибка при проверке
            allure.attach(
                f"Ошибка при проверке загрузки страницы: {str(e)}",
                name="login_page_load_error",
                attachment_type=allure.attachment_type.TEXT
            )
            return False
