from django.core.management.base import BaseCommand
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webapp.models import Product
import time
import random
from decimal import Decimal

class Command(BaseCommand):
    help = 'Scrape Amazon laptops data'

    def handle(self, *args, **options):
        # Ваш текущий код парсера с изменениями:
        chrome_options = Options()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # chrome_options.add_argument("--headless")  # Фоновый режим (без открытия окна)
        chrome_options.add_experimental_option("useAutomationExtension", False)
        user_agents = [
            # Chrome (Windows)
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            
            # Chrome (macOS)
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            
            # Firefox (Windows)
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
            
            # Safari (Mac)
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",
            
            # Edge (Windows)
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
            
            # Chrome (Linux)
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            
            # Firefox (Mac)
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0",
            
            # Opera (Windows)
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
        chrome_options.add_argument(f"user-agent={random.choice(user_agents)}")
        # Дополнительные заголовки
        chrome_options.add_argument("accept-language=en-US,en;q=0.9")
        chrome_options.add_argument("referer=https://www.google.com/")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-gpu")
        
        driver = webdriver.Chrome(options=chrome_options)
        
        try:
            driver = webdriver.Chrome(options=chrome_options)
            # Имитируем поведение человека
            driver.get("https://www.google.com")
            time.sleep(random.uniform(1, 3))
            driver.get("https://www.amazon.com/s?k=laptops")
            time.sleep(random.uniform(2, 4))
            # Поиск товаров
            search_box = driver.find_element(By.ID, "twotabsearchtextbox")
            # search_box.send_keys("laptops")
            search_box.submit()
            time.sleep(random.uniform(3, 5))
                # Прокрутка и парсинг
            driver.execute_script("window.scrollBy(0, 1000);")
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-asin]:not([data-asin=''])")))
            
            products = driver.find_elements(By.CSS_SELECTOR, "div[data-asin]:not([data-asin=''])")[:5]
            
            for product in products:
                try:
                    # Парсинг данных
                    title = product.find_element(By.CSS_SELECTOR, "h2.a-size-medium span").text
                    price_text = product.find_element(By.CSS_SELECTOR, ".a-price .a-offscreen").get_attribute("textContent")
                    price = Decimal(price_text.replace('$', '').replace(',', ''))
                    rating_text = product.find_element(By.CSS_SELECTOR, "i.a-icon-star-small .a-icon-alt").get_attribute("textContent")
                    rating = float(rating_text.split()[0])
                    reviews_text = product.find_element(By.CSS_SELECTOR, "span.a-size-base.s-underline-text").text
                    reviews = int(reviews_text.replace(',', ''))
                    url = product.find_element(By.CSS_SELECTOR, "h2 a").get_attribute("href")
                    
                    # Создаем или обновляем запись в БД
                    Product.objects.update_or_create(
                        product_url=url,
                        defaults={
                            'title': title,
                            'current_price': price,
                            'rating': rating,
                            'reviews': reviews
                        }
                    )
                    
                    self.stdout.write(self.style.SUCCESS(f'Successfully saved: {title}'))
                    
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error parsing product: {e}'))
                    continue
                    
        finally:
            driver.quit()