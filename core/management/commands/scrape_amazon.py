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
from core.management.user_agents import user_agents  # Импортируем список user_agents

class Command(BaseCommand):
    help = 'Scrape Amazon laptops data'

    def handle(self, *args, **options):
        # Ваш текущий код парсера с изменениями:
        chrome_options = Options()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # chrome_options.add_argument("--headless")  # Фоновый режим (без открытия окна)
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_argument(f"user-agent={random.choice(user_agents)}")
        # Дополнительные заголовки
        chrome_options.add_argument("accept-language=en-US,en;q=0.9")
        chrome_options.add_argument("referer=https://www.google.com/")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-gpu")
        
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
                    price = Decimal(price_text.replace('$', '').replace('.', ''))
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