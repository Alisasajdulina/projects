# test_browser.py - тест видимости браузера
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

print("="*60)
print("ТЕСТ ВИДИМОСТИ БРАУЗЕРА")
print("="*60)

# НАСТРОЙКИ ДЛЯ ВИДИМОГО БРАУЗЕРА:
chrome_options = Options()

# ВАЖНО: НЕ добавлять --headless
# chrome_options.add_argument('--headless')  # ← ЗАКОММЕНТИРОВАТЬ!

# Дополнительные настройки
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument('--start-maximized')  # ← Максимизировать окно

# Отключаем уведомления
chrome_options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 2
})

# Скрываем автоматизацию
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

print("1. Устанавливаем ChromeDriver...")
service = Service(ChromeDriverManager().install())

print("2. Запускаем Chrome...")
driver = webdriver.Chrome(service=service, options=chrome_options)

# Скрываем webdriver
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

print("3. Открываем ВКонтакте...")
driver.get("https://vk.com")

print("4. Открываем поиск...")
driver.get("https://vk.com/search?c[q]=программирование&c[section]=news")

print(f"\n✅ Браузер запущен!")
print(f"   Заголовок: {driver.title}")
print(f"   URL: {driver.current_url}")

print("\n⏳ Браузер будет открыт 30 секунд...")
print("   Вы должны увидеть окно Chrome с ВКонтакте")

# Ждем и делаем скриншот
time.sleep(5)
driver.save_screenshot('browser_test.png')
print(f"   Скриншот сохранен: browser_test.png")

# Прокручиваем
print("   Прокручиваем страницу...")
driver.execute_script("window.scrollTo(0, 500)")
time.sleep(2)

# Получаем HTML
html = driver.page_source[:500]
print(f"   Первые 500 символов HTML: {html}")

print("\n⏳ Ждем еще 20 секунд...")
time.sleep(20)

print("\n5. Закрываем браузер...")
driver.quit()

print("\n" + "="*60)
print("✅ ТЕСТ ЗАВЕРШЕН!")
print("="*60)
input("Нажмите Enter...")
