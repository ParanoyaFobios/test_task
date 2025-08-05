from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import random

def get_driver():
    options = Options()
    
    # Основные настройки для обхода защиты
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    
    # Рандомный User-Agent
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0"
    ]
    options.add_argument(f"user-agent={random.choice(user_agents)}")
    
    # Дополнительные заголовки
    options.add_argument("accept-language=en-US,en;q=0.9")
    options.add_argument("referer=https://www.google.com/")
    
    driver = webdriver.Chrome(options=options)
    
    # Изменяем свойства браузера
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """
    })
    
    return driver

def scrape_amazon():
    driver = None
    try:
        driver = get_driver()
        
        # Имитация поведения человека
        driver.get("https://www.google.com/search?q=amazon+laptops")
        time.sleep(random.uniform(2, 4))
        
        # Основной запрос
        search_url = "https://www.amazon.com/s?k=laptops&ref=nb_sb_noss_2"
        driver.get(search_url)
        time.sleep(random.uniform(3, 5))
        
        # Проверка на капчу
        if "captcha" in driver.page_source.lower():
            print("Обнаружена CAPTCHA! Попробуйте позже или используйте прокси.")
            return
        
        # Ожидание загрузки
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-asin]:not([data-asin=''])"))
        )
        
        # Прокрутка
        for _ in range(3):
            driver.execute_script("window.scrollBy(0, 800);")
            time.sleep(random.uniform(1, 2))
        
        # Парсинг
        products = driver.find_elements(By.CSS_SELECTOR, "div[data-asin]:not([data-asin=''])")[:3]
        
        for product in products:
            try:
                data = {
                    'title': 'N/A',
                    'price': 'N/A',
                    'rating': 'N/A',
                    'reviews': 'N/A',
                    'url': 'N/A'
                }
                
                # Название
                try:
                    title_elem = product.find_element(By.CSS_SELECTOR, "h2 a span")
                    data['title'] = title_elem.text.strip()
                except NoSuchElementException:
                    pass
                
                # Цена
                try:
                    price_elem = product.find_element(By.CSS_SELECTOR, ".a-price .a-offscreen")
                    data['price'] = price_elem.get_attribute("textContent").strip()
                except NoSuchElementException:
                    pass
                
                # Рейтинг
                try:
                    rating_elem = product.find_element(By.CSS_SELECTOR, "i.a-icon-star-small .a-icon-alt")
                    data['rating'] = rating_elem.get_attribute("textContent").strip()
                except NoSuchElementException:
                    pass
                
                # Отзывы
                try:
                    reviews_elem = product.find_element(By.CSS_SELECTOR, "span.a-size-base.s-underline-text")
                    data['reviews'] = reviews_elem.text.strip()
                except NoSuchElementException:
                    pass
                
                # URL
                try:
                    url_elem = product.find_element(By.CSS_SELECTOR, "h2 a")
                    data['url'] = url_elem.get_attribute("href")
                except NoSuchElementException:
                    pass
                
                print(f"Данные: {data}")
                
            except Exception as e:
                print(f"Ошибка при парсинге товара: {str(e)}")
                continue
                
    except Exception as e:
        print(f"Критическая ошибка: {str(e)}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    scrape_amazon()