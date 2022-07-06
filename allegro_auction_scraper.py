from selenium.webdriver import Keys
from webdriver import init_selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
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


    def _scroll_down_page(self):
        try:
                WebDriverWait(self.driver, .25).until(
                    ec.presence_of_element_located(
                        (By.TAG_NAME, 'html')
                    )
                )
        except Exception as e:
            print('timeout error waiting to located element by TAG_NAME: "html"')
            print(e)
        page = self.driver.find_element(By.TAG_NAME, 'html')
        page.send_keys(Keys.PAGE_DOWN)
        page.send_keys(Keys.PAGE_DOWN)


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


    def run_auction_scraper(self, url=None):
        self.driver.get(url)
        self._scroll_down_page()
        print(self._get_product_img_url())
        # self._get_name_of_the_seller()
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
allegro_auction_scraper.run_auction_scraper('https://allegro.pl/oferta/bandana-bandamka-chusta-oddychajaca-czarna-meska-10182306603?bi_s=ads&bi_m=listing:desktop:category&bi_c=N2FlYTIxM2MtMjQ5MC00MGNiLTgzM2QtYWI3ZTM3ZjBlOTJlAA&bi_t=ape&referrer=proxy&emission_unit_id=32a9d685-2f25-49b5-8626-aea235895459')