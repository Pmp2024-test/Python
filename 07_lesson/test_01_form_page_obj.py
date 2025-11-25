import pytest
from selenium import webdriver
from pages.form_page import FormPage


@pytest.fixture
def driver():
    driver = webdriver.Edge()
    driver.implicitly_wait(3)
    driver.maximize_window()
    yield driver
    driver.quit()


def test_form_submission_flow(driver):
    form_page = FormPage(driver)
    form_page.open()
    form_page.fill_form()
    form_page.submit_form()
    assert form_page.is_zip_code_has_error(), "Поле индекса должно содержать ошибку"
    assert form_page.are_other_fields_have_success(), "Все остальные поля должны быть заполнены"


def test_all_fields_states(driver):
    form_page = FormPage(driver)
    form_page.open()
    form_page.fill_form()
    form_page.submit_form()

    # Проверка всех полей через один метод
    field_states = form_page.get_field_states()

    # Проверяем поле с ошибкой
    assert "alert-danger" in field_states["zip-code"]

    # Проверяем все остальные поля на успех
    success_fields = ['first-name', 'last-name', 'address', 'e-mail', 'phone',
    'city', 'country', 'job-position', 'company']

    for field_name in success_fields:
        assert "alert-success" in field_states[field_name], f"Field {field_name} должны быть успешно заполнены"
