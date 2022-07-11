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
        try:
            wait = WebDriverWait(self.driver, 20)
            page = wait.until(ec.visibility_of_element_located((By.TAG_NAME, 'html')))
            page.send_keys(Keys.PAGE_DOWN)
            page.send_keys(Keys.PAGE_DOWN)
        except TimeoutException as e:
            print('timeout error waiting to located element by TAG_NAME: "html", could not to scroll down a page')
            print(e)

    def _get_product_price(self):
        '''
        Selector returns price as: '18,98 zł'. Method extracts price swaps ',' with '.'
        return the price as a float in order to use it for further calculation
        :return: product price (float)
        '''
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
        shipping_price = self.driver.find_element(By.XPATH, config.shipping_price_selector).text
        match = re.search('.\d+[,].\d', shipping_price)
        if match != None:
            match = match.group(0)
            shipping_price = match.replace(',', '.')
            return float(shipping_price)
        else:
            print('Couldn\'t extract shipping price')

    def _get_number_of_sold_items(self):
        '''
        Selector returns number of sold items as: '607 osób kupiło'. Method extracts number swaps ',' with '.'
        return the price as int in order to use it for further calculation
        :return: number of sold items (int)
        '''
        number_of_sold_items = self.driver.find_element(By.XPATH, config.number_of_sold_items_selector).text
        match = re.match('.\d+', number_of_sold_items)
        if match != None:
            match.group(0)
            number_of_sold_items = match[0].replace(',', '.')
            return int(number_of_sold_items)
        else:
            print('Couldn\'t extract shipping price')


    def _get_name_of_the_seller(self):
        """
        Selector returns seller name as: 'od name_of_the_seller'. Method splits string to extract
        just the name of the seller
        :return: name_of_the_seller (str)
        """
        name_of_the_seller = self.driver.find_element(By.XPATH, config.name_of_the_seller_selector).text
        name_of_the_seller = name_of_the_seller.split(' ')
        return name_of_the_seller[-1]


    def _get_product_img_url(self):
        """
        Method obtains url for first image that is available in auction description
        :return: product_img_url (str)
        """
        wait = WebDriverWait(self.driver, 20)
        image = wait.until(ec.visibility_of_element_located((By.XPATH, config.product_img_selector))).get_attribute('src')
        return image

    def _get_auction_number(self):
        """
        Selector returns auction number as: 'Numer oferty: 10182306603'. Method get digits from the string
        and returns as an integer
        :return: auction number (int)
        """
        auction_number_output = self.driver.find_element(By.XPATH, config.auction_number_selector).text
        auction_number = self._extract_digits_from_string(auction_number_output)
        return auction_number

    def run_auction_scraper(self, url=None):
        auctions_from_json = self._read_auctions_from_json()
        scraped_auctions = []
        for cat_num, auction_dict in auctions_from_json.items():
            for auction_name, auction_url in auction_dict.items():
                auction = {}
                self.driver.get(auction_url)
                print('Scraping auction from url: {}'.format(auction_url))
                self._scroll_down_page()
                auction['url'] = auction_url
                auction['product_price'] = self._get_product_price()
                auction['shipping_price'] = self._get_shipping_price()
                auction['name_of_the_seller'] = self._get_name_of_the_seller()
                auction['number_of_sold_items'] = self._get_number_of_sold_items()
                auction['product_img_url'] = self._get_product_img_url()
                auction['auction_number'] = self._get_auction_number()
                scraped_auctions.append(auction)
        self._save_to_json_file('test.json', scraped_auctions)
        self.driver.close()

        # self.driver.get(url)
        # self._scroll_down_page()
        #
        # self.driver.close()




allegro_auction_scraper = AllegroAuctionScraper()
allegro_auction_scraper.run_auction_scraper('https://allegro.pl/oferta/bandana-bandamka-chusta-oddychajaca-czarna-meska-10182306603?bi_s=ads&bi_m=listing:desktop:category&bi_c=N2FlYTIxM2MtMjQ5MC00MGNiLTgzM2QtYWI3ZTM3ZjBlOTJlAA&bi_t=ape&referrer=proxy&emission_unit_id=32a9d685-2f25-49b5-8626-aea235895459')