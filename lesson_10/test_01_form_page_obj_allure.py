import pytest
import allure
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from pages.form_page_allure import FormPage


@pytest.fixture
def driver() -> WebDriver:
    """
    Фикстура для создания и настройки WebDriver Edge.

    Returns:
        WebDriver: Настроенный экземпляр драйвера Edge
    """
    driver = webdriver.Edge()
    driver.implicitly_wait(3)
    driver.maximize_window()
    yield driver
    driver.quit()


@allure.feature("Форма заполнения данных")
@allure.severity(allure.severity_level.CRITICAL)
class TestFormPage:
    """Тесты для страницы с формой заполнения данных."""

    @allure.title("Отправка формы с пустым полем индекса")
    @allure.description("""
    Проверка валидации формы при отправке с пустым полем zip-code.

    Тестовые данные:
    - Все поля заполнены корректно
    - Поле zip-code оставлено пустым

    Ожидаемый результат:
    - Поле zip-code подсвечено красным (ошибка)
    - Все остальные поля подсвечены зеленым (успех)
    """)
    def test_form_submission_flow(self, driver: WebDriver) -> None:
        """
        Тестирование полного потока заполнения и отправки формы.

        Args:
            driver: WebDriver для управления браузером
        Returns:
            None
        """
        form_page = FormPage(driver)

        with allure.step("1. Открыть страницу с формой"):
            form_page.open()
            allure.attach(
                driver.current_url,
                name="page_url",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("2. Заполнить все поля формы (кроме zip-code)"):
            form_page.fill_form()

        with allure.step("3. Отправить форму"):
            form_page.submit_form()

        with allure.step("4. Проверить валидацию поля zip-code"):
            is_zip_error = form_page.is_zip_code_has_error()
            allure.attach(
                str(is_zip_error),
                name="zip_code_has_error",
                attachment_type=allure.attachment_type.TEXT
            )
            assert is_zip_error, "Поле индекса должно содержать ошибку"

        with allure.step("5. Проверить успешное заполнение остальных полей"):
            are_other_success = form_page.are_other_fields_have_success()
            allure.attach(
                str(are_other_success),
                name="other_fields_success",
                attachment_type=allure.attachment_type.TEXT
            )
            assert are_other_success, "Все остальные поля должны быть успешно заполнены"

    @allure.title("Проверка состояний всех полей формы")
    @allure.description("""
    Детальная проверка CSS классов всех полей после отправки формы.
    """)
    @allure.severity(allure.severity_level.NORMAL)
    def test_all_fields_states(self, driver: WebDriver) -> None:
        """
        Тестирование состояний всех полей формы.

        Args:
            driver: WebDriver для управления браузером
        Returns:
            None
        """
        form_page = FormPage(driver)

        with allure.step("Открыть страницу с формой"):
            form_page.open()

        with allure.step("Заполнить форму тестовыми данными"):
            form_page.fill_form()

        with allure.step("Отправить форму"):
            form_page.submit_form()

        with allure.step("Получить состояния всех полей"):
            field_states = form_page.get_field_states()

            # Прикрепляем информацию о состояниях
            states_report = "\n".join([f"{field}: {state}" for field, state in field_states.items()])
            allure.attach(
                states_report,
                name="all_field_states",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Проверить поле с ошибкой (zip-code)"):
            assert "alert-danger" in field_states["zip-code"], \
                "Поле zip-code должно содержать класс alert-danger"

        with allure.step("Проверить все остальные поля на успех"):
            success_fields = [
                'first-name', 'last-name', 'address', 'e-mail', 'phone',
                'city', 'country', 'job-position', 'company'
            ]

            failed_fields = []
            for field_name in success_fields:
                if "alert-success" not in field_states[field_name]:
                    failed_fields.append(field_name)

            assert len(failed_fields) == 0, \
                f"Поля {failed_fields} должны быть успешно заполнены"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
