import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_form_validation():
    driver = webdriver.Firefox()
    driver.get("https://www.saucedemo.com")

try:
    # Авторизация
    username = driver.find_element(By.ID, "user-name")
    password = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")

    username.send_keys("standard_user")
    password.send_keys("secret_sauce")
    login_button.click()

    # Ожидание загрузки страницы с товарами
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "inventory_item")))

    # Добавление товаров в корзину
    add_button = driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack")
    add_button.click()

    add_button = driver.find_element(By.ID, "add-to-cart-sauce-labs-bolt-t-shirt")
    add_button.click()

    add_button = driver.find_element(By.ID, "add-to-cart-sauce-labs-onesie")
    add_button.click()

    cart_badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
    assert cart_badge.text == "3", "В корзине должно быть 3 товара"

    # Переход в корзину
    cart_button = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
    cart_button.click()

    # Ожидание загрузки страницы корзины
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "cart_item")))

    # Нажатие Checkout
    checkout_button = driver.find_element(By.ID, "checkout")
    checkout_button.click()

    # Ожидание загрузки формы checkout
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "first-name")))

    # Заполнение формы checkout
    first_name_field = driver.find_element(By.ID, "first-name")
    last_name_field = driver.find_element(By.ID, "last-name")
    postal_code_field = driver.find_element(By.ID, "postal-code")
    continue_button = driver.find_element(By.ID, "continue")

    first_name_field.send_keys("Marina")
    last_name_field.send_keys("Panova")
    postal_code_field.send_keys("249360")
    continue_button.click()

    # Ожидание загрузки страницы Overview
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "summary_info")))

    # Чтение итоговой стоимости
    total_element = driver.find_element(By.CLASS_NAME, "summary_total_label")
    total_text = total_element.text
    total_value = float(total_text.split("$")[1])

    # Проверка итоговой суммы
    expected_total = 58.29
    assert total_value == expected_total, (
        f"Итоговая сумма составляет ${total_value:.2f}, "
        f"ожидалось ${expected_total:.2f}")

finally:
    driver.quit()
