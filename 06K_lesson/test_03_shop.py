import pytest
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    service = FirefoxService(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)
    driver.maximize_window()
    
    yield driver
    driver.quit()

def test_saucedemo(driver):
    driver.get("https://www.saucedemo.com/")
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "user-name"))
    )
    
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
    )
    
    # Добавляем товары в корзину
    items_to_add = [
        "Sauce Labs Backpack",
        "Sauce Labs Bolt T-Shirt", 
        "Sauce Labs Onesie"
    ]
    
    for item_name in items_to_add:
        # Найти кнопку для добавления в корзину
        add_to_cart_button = driver.find_element(
            By.XPATH, f"//div[text()='{item_name}']/ancestor::div[@class='inventory_item']//button"
        )
        add_to_cart_button.click()
        print(f"Добавлено {item_name} в корзину")
    
    # Переходим в корзину
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    
    # Ждем загрузку страницы
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "cart_list"))
    )
    
    # Нажать "Оформить заказ"
    driver.find_element(By.ID, "checkout").click()
    
    # Дожидаемся формы страницы "Оформить товар"
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "first-name"))
    )
    
    # Заполняем формц с личными данными
    driver.find_element(By.ID, "first-name").send_keys("Марина")
    driver.find_element(By.ID, "last-name").send_keys("Панова")
    driver.find_element(By.ID, "postal-code").send_keys("249360")
    
    # Нажать Продолжить
    driver.find_element(By.ID, "continue").click()
    
    # Ожидаем страницу с информацией о сумме
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "summary_total_label"))
    )
    
    # Читать общую сумму
    total_element = driver.find_element(By.CLASS_NAME, "summary_total_label")
    total_text = total_element.text
    total_amount = total_text.replace("Total: $", "")
    
    print(f"Total amount: {total_text}")
    
    # Подтверждение, что общая сумма $58.29
    assert total_amount == "58.29", f"Ожидается общая сумма $58.29, но получили ${total_amount}"
    
    print("Тест пройден! Общая сумма $58.29")
    
    driver.quit()
