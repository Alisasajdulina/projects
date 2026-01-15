import time
import re
import pandas as pd
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DynamicWebParser:
    """Базовый класс парсера динамических веб-сайтов с использованием Selenium"""
    
    def __init__(self, headless: bool = True):
        """
        Инициализация парсера
        
        Args:
            headless: Запуск браузера в фоновом режиме
        """
        self.headless = headless
        self.driver = None
        self.setup_driver()
    
    def setup_driver(self):
        """Настройка драйвера браузера"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument('--headless')
        
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        service = Service(ChromeDriverManager().install())
        
        self.driver = webdriver.Chrome(
            service=service,
            options=chrome_options
        )
        
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
        
        logger.info("Браузер успешно запущен")
    
    def wait_for_element(self, by: By, selector: str, timeout: int = 10):
        """Ожидание появления элемента"""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, selector))
        )
    
    def scroll_to_bottom(self, pause_time: float = 1.0):
        """Прокрутка до конца страницы"""
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(pause_time)
            
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    
    def get_page_source(self) -> str:
        """Получение HTML кода страницы"""
        return self.driver.page_source
    
    def close(self):
        """Закрытие браузера"""
        if self.driver:
            self.driver.quit()
            logger.info("Браузер закрыт")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class HabrParser(DynamicWebParser):
    """Парсер статей с Habr.com"""
    
    def __init__(self, headless: bool = True):
        super().__init__(headless)
        self.base_url = "https://habr.com"
    
    def parse_articles(self, page_count: int = 3) -> List[Dict]:
        """
        Парсинг статей с Habr
        
        Args:
            page_count: Количество страниц для парсинга
            
        Returns:
            Список словарей с данными статей
        """
        all_articles = []
        
        logger.info("Начинаем парсинг статей с Habr...")
        
        for page_num in range(1, page_count + 1):
            logger.info(f" Страница {page_num}/{page_count}...")
            
            url = f"{self.base_url}/ru/all/page{page_num}/"
            self.driver.get(url)
            
            self.wait_for_element(By.CLASS_NAME, "tm-articles-list")
            
            self.scroll_to_bottom(pause_time=0.5)
            
            html = self.get_page_source()
            articles = self._extract_articles_from_html(html)
            
            all_articles.extend(articles)
            
            logger.info(f" Найдено {len(articles)} статей")
            
            if page_num < page_count:
                time.sleep(2)
        
        logger.info(f"\nВсего собрано {len(all_articles)} статей")
        return all_articles
    
    def _extract_articles_from_html(self, html: str) -> List[Dict]:
        """Извлечение данных статей из HTML"""
        soup = BeautifulSoup(html, 'html.parser')
        articles = []
        
        article_elements = soup.find_all('article', class_='tm-articles-list_item')
        
        for article in article_elements:
            try:
                title_elem = article.find('h2', class_='tm-title')
                title = title_elem.text.strip() if title_elem else "Без заголовка"
                
                link_elem = article.find('a', class_='tm-title_link')
                link = f"{self.base_url}{link_elem['href']}" if link_elem else ""
                
                author_elem = article.find('a', class_='tm-user-info_username')
                author = author_elem.text.strip() if author_elem else "Неизвестный"
                
                time_elem = article.find('time')
                pub_time = time_elem['datetime'] if time_elem else ""
                
                hubs = []
                hub_elements = article.find_all('a', class_='tm-publication-hub_link')
                for hub in hub_elements:
                    hubs.append(hub.text.strip())
                rating_elem = article.find('span', class_='tm-votes-meter_value')
                rating = rating_elem.text.strip() if rating_elem else "0"
                
                preview_elem = article.find('div', class_='article-formatted-body')
                preview = preview_elem.text.strip() if preview_elem else ""
                
                article_data = {
                    'title': title,
                    'link': link,
                    'author': author,
                    'publication_time': pub_time,
                    'hubs': ', '.join(hubs[:3]),  # Первые 3 хаба
                    'rating': rating,
                    'preview': preview[:200] + '...' if len(preview) > 200 else preview,
                    'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
                }
                
                articles.append(article_data)
                
            except Exception as e:
                logger.error(f"Ошибка при парсинге статьи: {e}")
                continue
        
        return articles

class VKParser(DynamicWebParser):
    """Парсер публичных постов с ВКонтакте (vk.com)"""
    
    def __init__(self, headless: bool = True, login_required: bool = False):
        """
        Инициализация парсера ВКонтакте
        
        Args:
            headless: Запуск браузера в фоновом режиме
            login_required: Требуется ли вход в аккаунт
        """
        super().__init__(headless)
        self.base_url = "https://vk.com"
        self.login_required = login_required
        self.is_logged_in = False
        
        # Дополнительные настройки для VK
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
    
    def login(self, username: str, password: str) -> bool:
        """
        Вход в аккаунт ВКонтакте
        
        Args:
            username: Логин или телефон
            password: Пароль
            
        Returns:
            bool: Успешность входа
        """
        if not self.login_required:
            logger.info("Вход не требуется, используем публичный доступ")
            return True
            
        try:
            logger.info("Начинаем процесс входа в ВКонтакте...")
            
            self.driver.get(self.base_url)
            time.sleep(3)
            email_input = self.wait_for_element(By.NAME, 'email', timeout=10)
            email_input.clear()
            email_input.send_keys(username)
            password_input = self.driver.find_element(By.NAME, 'pass')
            password_input.clear()
            password_input.send_keys(password)
            login_button = self.driver.find_element(By.XPATH, 
                "//button[@type='submit' and contains(@class, 'FlatButton')]")
            login_button.click()
            time.sleep(5)
            
            if "feed" in self.driver.current_url or "id" in self.driver.current_url:
                self.is_logged_in = True
                logger.info("Успешный вход в ВКонтакте!")
                return True
            else:
                logger.warning("Не удалось подтвердить успешный вход")
                return False
                
        except Exception as e:
            logger.error(f"Ошибка при входе: {e}")
            return False
    
    def search_public_posts(self, search_query: str, max_posts: int = 50) -> List[Dict]:
        """
        Поиск публичных постов по запросу
        
        Args:
            search_query: Поисковый запрос
            max_posts: Максимальное количество постов для сбора
            
        Returns:
            List[Dict]: Список постов
        """
        try:
            logger.info(f"Начинаем поиск постов по запросу: '{search_query}'")
            
            from urllib.parse import quote
            encoded_query = quote(search_query)
        
            search_url = f"{self.base_url}/search?c[q]={encoded_query}&c[section]=all"
            self.driver.get(search_url)
            time.sleep(3)
            try:
                posts_tab = self.wait_for_element(
                    By.XPATH, 
                    "//a[contains(@href, 'c[section]=news')]",
                    timeout=5
                )
                posts_tab.click()
                time.sleep(2)
            except:
                logger.info("Не найдена вкладка новостей, используем текущий вид")
            
            posts = []
            last_post_count = 0
            scroll_attempts = 0
            max_scroll_attempts = 20
            
            while len(posts) < max_posts and scroll_attempts < max_scroll_attempts:
    
                self.scroll_to_bottom(pause_time=1.5)
                scroll_attempts += 1
                html = self.get_page_source()
                new_posts = self._extract_posts_from_html(html, search_query)
                
                unique_new_posts = []
                for post in new_posts:
                    if post['post_id'] not in [p['post_id'] for p in posts]:
                        unique_new_posts.append(post)
                
                posts.extend(unique_new_posts)
                if len(posts) > last_post_count:
                    logger.info(f"Собрано постов: {len(posts)}/{max_posts}")
                    last_post_count = len(posts)
                
                if len(unique_new_posts) == 0 and scroll_attempts % 5 == 0:
        
                    try:
                        more_button = self.driver.find_element(
                            By.XPATH, 
                            "//div[contains(@class, 'show_more')]//a"
                        )
                        more_button.click()
                        time.sleep(2)
                    except:
                        pass
                
                time.sleep(1)
            
            logger.info(f"Завершено. Всего собрано {len(posts)} постов")
            return posts[:max_posts]
            
        except Exception as e:
            logger.error(f"Ошибка при поиске постов: {e}")
            return []
    
    def get_public_page_posts(self, page_id: str, max_posts: int = 30) -> List[Dict]:
        """
        Получение постов с публичной страницы или группы
        
        Args:
            page_id: ID или короткое имя страницы/группы
            max_posts: Максимальное количество постов
            
        Returns:
            List[Dict]: Список постов
        """
        try:
            logger.info(f"Получаем посты с публичной страницы: {page_id}")
            
            page_url = f"{self.base_url}/{page_id}"
            
            self.driver.get(page_url)
            time.sleep(3)
            try:
                self.wait_for_element(
                    By.CLASS_NAME, 
                    "wall_post_text",
                    timeout=10
                )
            except:
                logger.warning("Не найдены посты с классом wall_post_text")
            
            posts = []
            scroll_attempts = 0
            max_scroll_attempts = 15
            
            while len(posts) < max_posts and scroll_attempts < max_scroll_attempts:
              
                self.scroll_to_bottom(pause_time=2)
                scroll_attempts += 1
                html = self.get_page_source()
                new_posts = self._extract_page_posts_from_html(html, page_id)
                
                unique_new_posts = []
                for post in new_posts:
                    if post['post_id'] not in [p['post_id'] for p in posts]:
                        unique_new_posts.append(post)
                
                posts.extend(unique_new_posts)
                if len(posts) > 0 and (len(posts) % 10 == 0 or len(unique_new_posts) == 0):
                    logger.info(f"Собрано постов: {len(posts)}/{max_posts}")
                
                time.sleep(1.5)
            
            logger.info(f"Завершено. Собрано {len(posts)} постов с {page_id}")
            return posts[:max_posts]
            
        except Exception as e:
            logger.error(f"Ошибка при получении постов с страницы: {e}")
            return []
    
    def _extract_posts_from_html(self, html: str, search_query: str) -> List[Dict]:
        """Извлечение постов из HTML страницы поиска"""
        soup = BeautifulSoup(html, 'html.parser')
        posts = []
        result_blocks = soup.find_all('div', class_=re.compile(r'result.*wrapper'))
        
        for block in result_blocks:
            try:
                post_data = self._parse_post_block(block)
                if post_data:
                    post_data['search_query'] = search_query
                    post_data['source_type'] = 'search'
                    posts.append(post_data)
                    
            except Exception as e:
                logger.debug(f"Ошибка при парсинге блока: {e}")
                continue
        if not posts:
            wall_items = soup.find_all('div', class_='wall_item')
            for item in wall_items:
                try:
                    post_data = self._parse_wall_item(item)
                    if post_data:
                        post_data['search_query'] = search_query
                        post_data['source_type'] = 'search'
                        posts.append(post_data)
                except Exception as e:
                    logger.debug(f"Ошибка при парсинге wall_item: {e}")
                    continue
        
        return posts
    
    def _extract_page_posts_from_html(self, html: str, page_id: str) -> List[Dict]:
        """Извлечение постов со страницы сообщества"""
        soup = BeautifulSoup(html, 'html.parser')
        posts = []
        
        wall_items = soup.find_all('div', class_='wall_item')
        
        for item in wall_items:
            try:
                post_data = self._parse_wall_item(item)
                if post_data:
                    post_data['page_id'] = page_id
                    post_data['source_type'] = 'page'
                    posts.append(post_data)
            except Exception as e:
                logger.debug(f"Ошибка при парсинге поста со страницы: {e}")
                continue
        
        return posts
    
    def _parse_post_block(self, block) -> Optional[Dict]:
        """Парсинг блока поста из результатов поиска"""
        try:
            post_id_elem = block.get('id', '')
            if not post_id_elem:
                post_id_elem = block.get('data-post-id', '')
            
            text_elem = block.find('div', class_=re.compile(r'wall_post_text'))
            text = text_elem.get_text(strip=True, separator=' ') if text_elem else ""
            
            author_elem = block.find('a', class_=re.compile(r'author|user'))
            author = author_elem.get_text(strip=True) if author_elem else "Неизвестный"
            author_link = author_elem.get('href', '') if author_elem else ""
            
            time_elem = block.find('span', class_=re.compile(r'time|rel_date'))
            post_time = time_elem.get_text(strip=True) if time_elem else ""
            
            likes_elem = block.find('span', class_=re.compile(r'like.*count'))
            likes = likes_elem.get_text(strip=True) if likes_elem else "0"
            
            reposts_elem = block.find('span', class_=re.compile(r'share.*count'))
            reposts = reposts_elem.get_text(strip=True) if reposts_elem else "0"
            
            views_elem = block.find('span', class_=re.compile(r'view.*count'))
            views = views_elem.get_text(strip=True) if views_elem else "0"
            
            link_elem = block.find('a', class_=re.compile(r'post_link'))
            post_link = link_elem.get('href', '') if link_elem else ""
            if post_link and not post_link.startswith('http'):
                post_link = f"{self.base_url}{post_link}"
            
            media_count = len(block.find_all('div', class_=re.compile(r'media|photo')))
            
            post_data = {
                'post_id': post_id_elem or f"post_{int(time.time())}_{hash(text[:50])}",
                'text': text[:500] + '...' if len(text) > 500 else text,
                'author': author,
                'author_link': author_link,
                'time': post_time,
                'likes': self._parse_count(likes),
                'reposts': self._parse_count(reposts),
                'views': self._parse_count(views),
                'link': post_link,
                'media_count': media_count,
                'has_photo': 'photo' in str(block).lower(),
                'has_video': 'video' in str(block).lower(),
                'has_link': 'link' in str(block).lower(),
                'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return post_data
            
        except Exception as e:
            logger.debug(f"Ошибка в _parse_post_block: {e}")
            return None
    
    def _parse_wall_item(self, item) -> Optional[Dict]:
        """Парсинг элемента стены (wall_item)"""
        try:
            post_id = item.get('id', '')
            if not post_id:
                post_id = f"wall_item_{hash(str(item)[:100])}"
            
            text_div = item.find('div', class_='wall_post_text')
            text = text_div.get_text(strip=True, separator=' ') if text_div else ""
            
            author_div = item.find('div', class_='author')
            author = author_div.get_text(strip=True) if author_div else ""
            
            time_span = item.find('span', class_='rel_date')
            post_time = time_span.get_text(strip=True) if time_span else ""
            
            likes = self._extract_stat(item, 'like')
            reposts = self._extract_stat(item, 'share')
            comments = self._extract_stat(item, 'comment')
            views = self._extract_stat(item, 'view')
            photos = item.find_all('div', class_='photo')
            photo_count = len(photos)
            
            videos = item.find_all('div', class_='video')
            video_count = len(videos)
        
            post_link = ""
            link_elem = item.find('a', class_='post_link')
            if link_elem:
                post_link = link_elem.get('href', '')
                if not post_link.startswith('http'):
                    post_link = f"{self.base_url}{post_link}"
            
            return {
                'post_id': post_id,
                'text': text[:1000] + '...' if len(text) > 1000 else text,
                'author': author,
                'time': post_time,
                'likes': likes,
                'reposts': reposts,
                'comments': comments,
                'views': views,
                'photo_count': photo_count,
                'video_count': video_count,
                'link': post_link,
                'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except Exception as e:
            logger.debug(f"Ошибка в _parse_wall_item: {e}")
            return None
    
    def _extract_stat(self, item, stat_type: str) -> str:
        """Извлечение статистики (лайки, репосты и т.д.)"""
        try:
            stat_elem = item.find('span', class_=re.compile(f'{stat_type}.*count'))
            if stat_elem:
                return stat_elem.get_text(strip=True)
            divs = item.find_all('div', class_=re.compile(f'{stat_type}s?.*count'))
            for div in divs:
                text = div.get_text(strip=True)
                if text and any(char.isdigit() for char in text):
                    return text
            
            return "0"
        except:
            return "0"
    
    def _parse_count(self, count_str: str) -> str:
        """Парсинг числовых значений (например, '2.5K' -> '2500')"""
        try:
            count_str = count_str.strip().upper()
            
            if not count_str or count_str == '0':
                return '0'
            
            count_str = re.sub(r'[^\d.KMБ,]', '', count_str)
            
            if 'K' in count_str or 'К' in count_str:
                num = float(count_str.replace('K', '').replace('К', ''))
                return str(int(num * 1000))
            elif 'M' in count_str or 'М' in count_str:
                num = float(count_str.replace('M', '').replace('М', ''))
                return str(int(num * 1000000))
            else:
                return count_str.replace(',', '')
        except:
            return count_str
    
    def get_trending_posts(self, category: str = "all", max_posts: int = 20) -> List[Dict]:
        """
        Получение популярных постов (если доступно)
        
        Args:
            category: Категория (all, news, funny, etc.)
            max_posts: Максимальное количество постов
            
        Returns:
            List[Dict]: Список популярных постов
        """
        logger.info(f"Получение популярных постов из категории: {category}")
        
        try:
            discover_url = f"{self.base_url}/discover"
            if category != "all":
                discover_url += f"?c[section]={category}"
            
            self.driver.get(discover_url)
            time.sleep(3)
            
            self.scroll_to_bottom(pause_time=1.5)
            html = self.get_page_source()
            soup = BeautifulSoup(html, 'html.parser')
            
            posts = []
            post_elements = soup.find_all('div', class_=re.compile(r'feed_row|post_item'))
            
            for i, element in enumerate(post_elements[:max_posts]):
                try:
                    text_elem = element.find('div', class_=re.compile(r'wall_post_text'))
                    text = text_elem.get_text(strip=True, separator=' ') if text_elem else ""
                    
                    like_elem = element.find('span', class_=re.compile(r'like.*count'))
                    likes = like_elem.get_text(strip=True) if like_elem else "0"
                    
                    posts.append({
                        'post_id': f"trend_{i}_{hash(text[:50])}",
                        'text': text[:300] + '...' if len(text) > 300 else text,
                        'likes': self._parse_count(likes),
                        'category': category,
                        'source': 'discover',
                        'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
                except:
                    continue
            
            logger.info(f"Найдено {len(posts)} популярных постов")
            return posts
            
        except Exception as e:
            logger.error(f"Ошибка при получении популярных постов: {e}")
            return []