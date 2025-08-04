from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# Настройки Chrome для обхода блокировки
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)
# Актуальный User-Agent (проверьте свою версию Chrome в chrome://settings/help)
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# Дополнительные заголовки
chrome_options.add_argument("accept-language=en-US,en;q=0.9")
chrome_options.add_argument("referer=https://www.google.com/")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=chrome_options)

try:
    # Имитируем поведение человека
    driver.get("https://www.google.com")
    time.sleep(random.uniform(1, 3))
    driver.get("https://www.amazon.com/s?k=laptops")
    time.sleep(random.uniform(2, 4))

    # Поиск товаров
    search_box = driver.find_element(By.ID, "twotabsearchtextbox")
    search_box.send_keys("laptops")
    search_box.submit()
    time.sleep(random.uniform(3, 5))

    # Прокрутка и парсинг (селекторы из предыдущего ответа)
    driver.execute_script("window.scrollBy(0, 1000);")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-asin]:not([data-asin=''])"))
    )

    # Парсим первые 5 товаров
    products = driver.find_elements(By.CSS_SELECTOR, "div[data-asin]:not([data-asin=''])")[:2]
    
    for product in products:
        try:
            # Название
            title = product.find_element(By.CSS_SELECTOR, "h2.a-size-medium span").text
        except:
            title = "N/A"

        try:
            # Цена ($148.98 -> 148.98)
            price = product.find_element(By.CSS_SELECTOR, ".a-price .a-offscreen").get_attribute("textContent").replace("$", "")
        except:
            price = "N/A"

        try:
            # Рейтинг (извлекаем текст "4.1 out of 5 stars")
            rating = product.find_element(By.CSS_SELECTOR, "i.a-icon-star-small .a-icon-alt").get_attribute("textContent")
        except:
            rating = "N/A"

        try:
            # Количество отзывов
            reviews = product.find_element(By.CSS_SELECTOR, "span.a-size-base.s-underline-text").text
        except:
            reviews = "N/A"

        print(f"Title: {title}")
        print(f"Price: ${price}")
        print(f"Rating: {rating}")
        print(f"Reviews: {reviews}")
        print("-" * 50)

finally:
    driver.quit()