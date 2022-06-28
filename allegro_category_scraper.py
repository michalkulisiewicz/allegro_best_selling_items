from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import config
import json
from fake_useragent import UserAgent
from time import sleep


class AllegroCategoryScraper:
    def __init__(self):
        self.driver = self._init_selenium()

    def _save_dict_to_json_file(self, filename, dict):
        with open(filename, 'w') as f:
            json.dump(dict, f, indent=4, ensure_ascii=False)

    def wait_and_click(self, path):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, path))).click()

    #initialize webdriver set settings that allows to hide browser automation
    def _init_selenium(self):
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

    def _scrape_cat_page(self):
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

    def _get_maximum_num_of_pages_from_cat(self):
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

    def _check_num_of_pages(self, num_of_pages, maximum_page_number):
        '''
        Method checks if user didn't put more pages than it's available to scrape if so scraper will scrape
        all pages that are available in category.
        :return: number of pages to be scraped (int)
        '''
        if num_of_pages == 'max':
            return maximum_page_number
        elif num_of_pages > maximum_page_number:
            return maximum_page_number
        else:
            return num_of_pages

    def run_cat_scraper(self, cat_url, num_of_pages=5):
        '''
        Method used to run category scraper and save output to file.
        :param cat_url: (required)
        :param num_of_pages: (optional)
        :return: None. Creates json file with name of the auction as key and url of the auction as value
        '''
        products = {}
        page_number = 1
        #filter used to sort auctions by number of sold items
        sort_filter = '?order=qd'
        self.driver.get(cat_url)
        maximum_page_number = self._get_maximum_num_of_pages_from_cat()
        print('maximum page number to be scraped: {}'.format(maximum_page_number))
        num_of_pages = self._check_num_of_pages(num_of_pages, maximum_page_number)
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

            products.update(self._scrape_cat_page())
            page_number += 1

        self.driver.close()
        self._save_dict_to_json_file('cat_scaper_output.json', products)


allegro_scraper = AllegroCategoryScraper()
products = allegro_scraper.run_cat_scraper('https://allegro.pl/kategoria/bielizna-damska-ponczochy-76003', 2)
allegro_scraper.save_dict_to_json_file('cat_scraper_output.json', products)
