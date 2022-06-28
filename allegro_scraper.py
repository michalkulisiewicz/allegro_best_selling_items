from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from fake_useragent import UserAgent
from fp.fp import FreeProxy

from time import sleep

class AllegroScraper:
    def __init__(self):
        self.driver = self.init_selenium()


    def wait_and_click(self, path):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, path))).click()

    #initialize webdriver set settings that allows to hide browser automation
    def init_selenium(self):
        try:
            service = ChromeService(executable_path=ChromeDriverManager(version="103.0.5060.53").install())
            options = Options()
            options.add_argument('user-data-dir=session')
            # For ChromeDriver version 79.0.3945.16 or over
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument("--disable-blink-features")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--start-maximized")
            # options.add_argument('--headless')
            driver = webdriver.Chrome(service=service, options=options)
            # disable automation flag
            # self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return driver
        except Exception as e:
            print('Error while initializing webdriver')
            print(e)

    def scrape_items_from_category(self, cat_url):
        self.driver.get(cat_url)
        sleep(15)

allegro_scraper = AllegroScraper()
allegro_scraper.scrape_items_from_category('https://allegro.pl/kategoria/bielizna-damska-ponczochy-76003?order=qd')
