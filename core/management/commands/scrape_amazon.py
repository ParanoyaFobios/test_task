from django.core.management.base import BaseCommand, CommandError
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webapp.models import Product
import time
import random
from decimal import Decimal
from core.management.user_agents import user_agents

class Command(BaseCommand):
    help = 'Scrape Amazon laptops data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--category',
            type=str,
            default='laptops',
            help='Category to search on Amazon'
        )

    def handle(self, *args, **options):
        category = options['category']
        search_query = category.replace(' ', '+')
        chrome_options = Options()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # chrome_options.add_argument("--headless")
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_argument(f"user-agent={random.choice(user_agents)}")
        chrome_options.add_argument("accept-language=en-US,en;q=0.9")
        chrome_options.add_argument("referer=https://www.google.com/")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-gpu")
        
        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.get("https://www.google.com")
            time.sleep(random.uniform(1, 3))
            driver.get(f"https://www.amazon.com/s?k={search_query}")
            time.sleep(random.uniform(2, 4))
            
            driver.execute_script("window.scrollBy(0, 1000);")
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-asin]:not([data-asin=''])")))
            
            products = driver.find_elements(By.CSS_SELECTOR, "div.s-result-item[data-component-type='s-search-result']")[:16]
            
            for product in products:
                product_data = {
                    'title': 'N/A',
                    'current_price': Decimal('0'),
                    'rating': None,
                    'reviews': None,
                    'product_url': None
                }
                
                # Название товара
                try:
                    title_element = product.find_element(By.CSS_SELECTOR, "h2.a-size-medium.a-spacing-none.a-color-base.a-text-normal span")
                    product_data['title'] = title_element.text.strip()
                    self.stdout.write(f"Found title: {product_data['title']}")
                except Exception as e:
                    self.stdout.write(f"Error getting title: {str(e)}")
                # Цена
                try:
                    price_element = product.find_element(By.CSS_SELECTOR, "span.a-price-whole")
                    price_fraction = product.find_element(By.CSS_SELECTOR, "span.a-price-fraction").text
                    price_text = f"{price_element.text}.{price_fraction}"
                    product_data['current_price'] = Decimal(price_text)
                except:
                    try:
                        price_text = product.find_element(By.CSS_SELECTOR, "span.a-offscreen").get_attribute("textContent")
                        product_data['current_price'] = Decimal(price_text.replace('$', '').strip())
                    except Exception as e:
                        self.stdout.write(f"Error getting price: {str(e)}")
                
                # Рейтинг
                try:
                    rating_element = product.find_element(By.CSS_SELECTOR, "span.a-icon-alt")
                    rating_text = rating_element.get_attribute("textContent")
                    product_data['rating'] = float(rating_text.split()[0])
                except Exception as e:
                    self.stdout.write(f"Error getting rating: {str(e)}")
                
                # Количество отзывов
                try:
                    reviews_element = product.find_element(By.CSS_SELECTOR, "span.a-size-base.s-underline-text")
                    reviews_text = reviews_element.text.replace(',', '')
                    if reviews_text.isdigit():
                        product_data['reviews'] = int(reviews_text)
                except Exception as e:
                    self.stdout.write(f"Error getting reviews: {str(e)}")
                
                # Ссылка на товар из блока выбора цвета (swatch)
                try:
                    url_element = product.find_element(By.CSS_SELECTOR, "h2 > a.a-link-normal")
                    product_url = url_element.get_attribute("href")
                    if product_url:
                        if not product_url.startswith('http'):
                            product_url = f"https://www.amazon.com{product_url}"
                        product_data['product_url'] = product_url
                        self.stdout.write(f"Found URL: {product_url}")
                except Exception as e:
                    self.stdout.write(f"Error getting URL from swatch link: {str(e)}")

                
                # Сохранение в БД
                if product_data['product_url']:  # Проверяем на наличие любого URL
                    try:
                        Product.objects.update_or_create(
                            product_url=product_data['product_url'],
                            defaults={
                                'title': product_data['title'],
                                'current_price': product_data['current_price'],
                                'rating': product_data['rating'],
                                'reviews': product_data['reviews']
                            }
                        )
                        self.stdout.write(self.style.SUCCESS(f'Successfully saved: {product_data["title"]}'))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Error saving to DB: {str(e)}'))
                else:
                    self.stdout.write(self.style.WARNING('Skipped product - no URL found'))
            
            self.stdout.write(self.style.SUCCESS('Scraping completed successfully'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error during scraping: {str(e)}'))
            
        finally:
            driver.quit()
            self.stdout.write(self.style.SUCCESS('Scraping process finished.'))