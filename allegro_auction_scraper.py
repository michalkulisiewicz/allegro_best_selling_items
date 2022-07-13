from selenium.common import TimeoutException
from selenium.webdriver import Keys
from webdriver import init_selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import config
import json
import re
from pathlib import Path

class AllegroAuctionScraper:
    def __init__(self):
        self.driver = init_selenium()

    def _extract_digits_from_string(self, string):
        return [int(s) for s in string.split() if s.isdigit()][0]

    def _extract_cat_num_from_filename(self, filename):
        category_num = filename.split('.')[0]
        return int(category_num)

    def _save_to_json_file(self, filename, input):
        with open(filename, 'w') as f:
            json.dump(input, f, indent=4, ensure_ascii=False)

    def _read_auctions_from_json(self):
        file_list = list(Path('category_scraper_output').glob("*.json"))
        auctions = {}
        for file in file_list:
            cat_num = self._extract_cat_num_from_filename(file.name)
            with open(file, 'r') as f:
                json_file = json.load(f)
                auctions[cat_num] = json_file
        return auctions


    def _scroll_down_page(self):
        """
        Method used to scroll into view of description in order to load product image needed for further scraping.
        """
        try:
            wait = WebDriverWait(self.driver, 20)
            description = wait.until(ec.presence_of_element_located((By.XPATH, config.description_selector)))
            #Execute javascript to scroll page in order to load nedded elements
            self.driver.execute_script("arguments[0].scrollIntoView();", description)
        except TimeoutException as e:
            print('Timeout error, could not to scroll down a page')
            print(e)

    def _get_product_price(self):
        """
        Selector returns price as: '18,98 zł'. Method extracts price swaps ',' with '.'
        return the price as a float in order to use it for further calculation
        :return: product price (float)
        """
        try:
            wait = WebDriverWait(self.driver, 20)
            product_price = wait.until(ec.visibility_of_element_located((By.XPATH, config.product_price_selector))).text
            match = re.match('.\d+[,].\d', product_price)
            if match != None:
                match = match.group(0)
                product_price = match.replace(',', '.')
                return float(product_price)
            else:
                print('Couldn\'t extract product price')
        except TimeoutException as e:
            print('timeout error waiting to located element by XPATH: {}'.format(config.product_price_selector))
            print(e)

    def _get_shipping_price(self):
        """
        Selector returns price as: 'Dostawa od 6,70 zł'. Method extracts price swaps ',' with '.'
        return the price as a float in order to use it for further calculation
        :return: shipping price (float)
        """
        try:
            wait = WebDriverWait(self.driver, 20)
            shipping_price = wait.until(ec.visibility_of_element_located((By.XPATH, config.shipping_price_selector))).text
            match = re.search('.\d+[,].\d', shipping_price)
            if match != None:
                match = match.group(0)
                shipping_price = match.replace(',', '.')
                return float(shipping_price)
            else:
                print('Couldn\'t extract shipping price')
        except TimeoutException as e:
            print('timeout error waiting to located element by XPATH: {}'.format(config.product_price_selector))
            print(e)

    def _get_number_of_sold_items(self):
        '''
        Selector returns number of sold items as: '607 osób kupiło'. Method extracts number swaps ',' with '.'
        return the price as int in order to use it for further calculation
        :return: number of sold items (int)
        '''
        try:
            wait = WebDriverWait(self.driver, 20)
            number_of_sold_items = wait.until(ec.visibility_of_element_located((By.XPATH, config.number_of_sold_items_selector))).text
            match = re.match('.\d+', number_of_sold_items)
            if match != None:
                match.group(0)
                number_of_sold_items = match[0].replace(',', '.')
                return int(number_of_sold_items)
            else:
                print('Couldn\'t extract shipping price')
        except TimeoutException as e:
            print('timeout error waiting to located element by XPATH: {}'.format(config.number_of_sold_items_selector))
            print(e)


    def _get_name_of_the_seller(self):
        """
        Selector returns seller name as: 'od name_of_the_seller'. Method splits string to extract
        just the name of the seller
        :return: name_of_the_seller (str)
        """
        try:
            wait = WebDriverWait(self.driver, 20)
            name_of_the_seller = wait.until(ec.visibility_of_element_located((By.XPATH, config.name_of_the_seller_selector))).text
            name_of_the_seller = name_of_the_seller.split(' ')
            return name_of_the_seller[-1]
        except TimeoutException as e:
            print('timeout error waiting to located element by XPATH: {}'.format(config.name_of_the_seller_selector))
            print(e)


    def _get_product_img_url(self):
        """
        Method obtains url for first image that is available in auction description
        :return: product_img_url (str)
        """
        try:
            wait = WebDriverWait(self.driver, 20)
            image = wait.until(ec.visibility_of_element_located((By.XPATH, config.product_img_selector))).get_attribute('src')
            return image
        except TimeoutException as e:
            print('timeout error waiting to located element by XPATH: {}'.format(config.product_img_selector))
            print(e)

    def _get_auction_number(self):
        """
        Selector returns auction number as: 'Numer oferty: 10182306603'. Method get digits from the string
        and returns as an integer
        :return: auction number (int)
        """
        try:
            wait = WebDriverWait(self.driver, 20)
            auction_number = wait.until(ec.visibility_of_element_located((By.XPATH, config.auction_number_selector))).text
            auction_number = self._extract_digits_from_string(auction_number)
            return auction_number
        except TimeoutException as e:
            print('timeout error waiting to located element by XPATH: {}'.format(config.auction_number_selector))
            print(e)

    def run_auction_scraper(self):
        auctions_from_json = self._read_auctions_from_json()
        scraped_auctions = []
        for cat_num, auction_dict in auctions_from_json.items():
            for auction_name, auction_url in auction_dict.items():
                auction = {}
                self.driver.get(auction_url)
                print('Scraping auction from url: {}'.format(auction_url))
                self._scroll_down_page()
                auction['url'] = auction_url
                auction['name_of_the_seller'] = self._get_name_of_the_seller()
                auction['product_price'] = self._get_product_price()
                auction['shipping_price'] = self._get_shipping_price()
                auction['number_of_sold_items'] = self._get_number_of_sold_items()
                auction['product_img_url'] = self._get_product_img_url()
                auction['auction_number'] = self._get_auction_number()
                scraped_auctions.append(auction)
        self._save_to_json_file('test.json', scraped_auctions)
        self.driver.close()