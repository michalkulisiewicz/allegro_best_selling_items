from webdriver import init_selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config
import json
import re

class AllegroAuctionScraper:
    def __init__(self):
        self.driver = init_selenium()

    def _get_product_price(self):
        '''
        Selector returns price as: '18,98 zł'. Method extracts price swaps ',' with '.'
        return the price as a float in order to use it for further calculation
        :return: product price (float)
        '''
        product_price = self.driver.find_element(By.XPATH, config.product_price_selector).text
        match = re.match('.\d+[,].\d', product_price)
        if match != None:
            match = match.group(0)
            product_price = match.replace(',', '.')
            return float(product_price)
        else:
            print('Couldn\'t extract product price')

    def _get_shipping_price(self):
        '''
        Selector returns price as: 'Dostawa od 6,70 zł'. Method extracts price swaps ',' with '.'
        return the price as a float in order to use it for further calculation
        :return: shipping price (float)
        '''
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

    def run_auction_scraper(self, url=None):
        self.driver.get(url)
        test = self._get_number_of_sold_items()
        print(test)
        # product_price = self._get_product_price()
        # print(product_price)
        # shipping_price = self._get_shipping_price()
        # print(shipping_price)

        self.driver.close()

        # containers = [
        #     "section#top-card div.content",  # product_image
        #     "div.job-salary-container",  # product_price
        #     "ul.company-growth-stats.stats-list",  # product_shipping_cost
        #     "div.insights-card.applicants-skills"  # number_of_sold_items
        # ]
        # for container in containers:
        #     try:
        #         WebDriverWait(self.driver, .25).until(
        #             EC.presence_of_element_located(
        #                 (By.XPATH, container)
        #             )
        #         )
        #     except Exception as e:
        #         print("timeout error waiting for container to load or element" \
        #               " not found: {}".format(container))
        #         print(e)


allegro_auction_scraper = AllegroAuctionScraper()
allegro_auction_scraper.run_auction_scraper('https://allegro.pl/oferta/biustonosz-samonosny-push-up-bez-ramiaczek-oslonki-10852424622')