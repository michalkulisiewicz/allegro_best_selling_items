from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import config
from fake_useragent import UserAgent
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
            #Temporary version 102.0.5005.61 of chrome is used as the latest version does not work properly
            service = ChromeService(executable_path=ChromeDriverManager(version='102.0.5005.61').install())
            # service = ChromeService(executable_path='/home/donnie/PycharmProjects/allegro_best_selling_items/chromedriver')
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

    def scrape_cat_page(self):
        """
            scrapes urls and product names from single page.
            Returns data as a dictionary
        """
        try:
            elems = self.driver.find_elements(By.XPATH, config.cat_product_selector)
            products = {}
            for elem in elems:
                products[elem.text] = elem.get_attribute('href')
            return products

        except Exception as e:
            print('Error acquiring urls and product names from category')
            print(e)
            return {}

    def _get_maximum_page_num_from_cat(self):
        '''
        Function used to find maximum number of available pages to scrape
        :return: int
        '''

        try:
            WebDriverWait(self.driver, .25).until(
                EC.presence_of_element_located(
                    (By.XPATH, config.cat_max_page_selector)
                )
            )
        except Exception as e:
            print('timeout error element not found: {}'.format(config.cat_max_page_selector))
            print(e)
        max_page = self.driver.find_element(By.XPATH, config.cat_max_page_selector).text
        return int(max_page)


    def category_scraper(self, cat_url, num_of_pages=5):
        page_number = 1
        #filter used to sort auctions by number of sold items
        sort_filter = '?order=qd'
        self.driver.get(cat_url)
        maximum_page_number = self._get_maximum_page_num_from_cat()
        print(maximum_page_number)
        for page in range(num_of_pages):
            page_filter = '&p={}'.format(str(page_number))
            url = cat_url + sort_filter + page_filter
            self.driver.get(url)
            try:
                WebDriverWait(self.driver, .25).until(
                    EC.presence_of_element_located(
                        (By.XPATH, config.cat_product_selector)
                    )
                    )
            except Exception as e:
                print('timeout error element not found: {}'.format(config.cat_product_selector))
                print(e)

            print(self.scrape_cat_page())
            page_number += 1

        self.driver.close()


allegro_scraper = AllegroScraper()
allegro_scraper.category_scraper('https://allegro.pl/kategoria/bielizna-damska-ponczochy-76003')

