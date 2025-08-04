from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Настройки Chrome
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")  # Отключаем песочницу
chrome_options.add_argument("--disable-dev-shm-usage")  # Для ограниченных ресурсов

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.amazon.com")
print(driver.title)
driver.quit()