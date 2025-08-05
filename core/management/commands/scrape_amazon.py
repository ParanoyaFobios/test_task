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
            
            # Прокрутка и парсинг
            driver.execute_script("window.scrollBy(0, 1000);")
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-asin]:not([data-asin=''])")))
            
            # собираем первые 3 товара
            products = driver.find_elements(By.CSS_SELECTOR, "div.s-result-item[data-component-type='s-search-result']")[:16]
            
            for product in products:
                # Инициализация данных
                product_data = {
                    'title': 'N/A',
                    'price': 'N/A',
                    'rating': 'N/A',
                    'reviews': 'N/A',
                    'url': 'N/A'
                }
                
                # Название товара
                try:
                    title_element = product.find_element(By.CSS_SELECTOR, "h2 a.a-link-normal.a-text-normal")
                    product_data['title'] = title_element.text.strip()
                except:
                    pass
                
                # Цена
                try:
                    price_text = product.find_element(By.CSS_SELECTOR, "span.a-price span.a-offscreen").get_attribute("textContent")
                    product_data['price'] = Decimal(price_text.replace('$', '').strip())
                except:
                    product_data['price'] = Decimal('0') # Если цена не найдена, устанавливаем 0
                
                # Рейтинг
                try:
                    rating_element = product.find_element(By.CSS_SELECTOR, "span.a-icon-alt")
                    product_data['rating'] = rating_element.get_attribute("textContent").strip()
                except:
                    pass
                
                # Количество отзывов
                try:
                    reviews_element = product.find_element(By.CSS_SELECTOR, "span.a-size-base.s-underline-text")
                    product_data['reviews'] = reviews_element.text.strip()
                except:
                    pass
                
                # Ссылка на товар
                try:
                    url_element = product.find_element(By.CSS_SELECTOR, "h2 a.a-link-normal.a-text-normal")
                    product_data['url'] = url_element.get_attribute("href")
                except:
                    pass
                
                # Создаем или обновляем запись в БД
                if product_data['url'] != 'N/A':
                    Product.objects.update_or_create(
                        product_url=product_data['url'],
                        defaults={
                            'title': product_data['title'],
                            'current_price': product_data['price'],
                            'rating': product_data['rating'],
                            'reviews': product_data['reviews']
                        }
                    )
                    
                    self.stdout.write(self.style.SUCCESS(f'Successfully saved: {product_data["title"]}'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error during scraping: {e}'))
            
        finally:
            driver.quit()
            # В management командах нельзя использовать redirect, так как это не HTTP-запрос
            self.stdout.write(self.style.SUCCESS('Scraping completed'))