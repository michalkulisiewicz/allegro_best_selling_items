from webdriver import init_selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.common import TimeoutException
import config
import utils
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import re


class AllegroCategoryScraper:
    def __init__(self):
        self.first_run = self._check_if_first_run()
        self.driver = init_selenium()
        self.wait = WebDriverWait(self.driver, 30)
        self.scraped_auctions = []

    def _check_if_first_run(self):
        """
        Method checks for existence of user-data-dir
        in order to tell if script is ran for the first time.
        :return: Bool
        """
        return utils.check_if_directory_exists('./session')

    def _first_run(self):
        """
        Method used to check if script is ran for the first time.
        If it's first execution it will handle cookie prompt
        and toggle view of the auctions for easier scraping.
        """
        if not self.first_run:
            try:
                self.wait.until(ec.element_to_be_clickable((By.XPATH, config.accept_cookies_selector))).click()
            except TimeoutException:
                pass
            self._toggle_view()

    def _scroll_down_page(self):
        """
        Method used to scroll down to the bottom of the page
        in order to load all images that are needed to scrape
        """
        y = self.driver.find_element(By.XPATH, config.scroll_down_selector).location['y']
        for x in range(0, y, 50):
            self.driver.execute_script("window.scrollTo(0, " + str(x) + ");")

    def _toggle_view(self):
        """
        Method used to toggle view of a list of auctions in category.
        Default view makes it harder to scrape images from auction.
        """
        try:
            self.wait.until(ec.presence_of_element_located((By.XPATH, config.toggle_view_selector))).click()
        except TimeoutException:
            pass

    def _scrape_cat_page(self):
        """
        Method used to scrape auctions from a single page.
        BeautifulSoup is used to parse data
        """
        self._scroll_down_page()
        page_source = self.driver.page_source

        soup = BeautifulSoup(page_source, 'lxml')
        products = self._get_products(soup)
        for product in products:
            auction = {}

            product_url = self._get_product_url(product)
            # Omits promoted auctions
            if 'clicks?emission_unit' not in product_url:
                product_price = self._get_product_price(product)
                auction['product_url'] = product_url
                auction['product_name'] = self._get_product_name(product)
                auction['product_price'] = product_price
                auction['shipping_price'] = self._get_product_shipping_price(product, product_price)
                auction['number_of_sold_items'] = self._get_product_num_of_sold_items(product)
                auction['product_image_url'] = self._get_product_image_url(product)

                self.scraped_auctions.append(auction)

    def _get_product_image_url(self, product):
        return product.find('img')['src']

    def _parse_product_num_of_sold_items(self, num_of_sold_items):
        """
        Selector returns number of sold items as: "15 osób kupiło"
        Method extract number from string and returns it as int
        :param num_of_sold_items (str)
        :return num_of_sold_items (int)
        """
        num_of_sold_items = num_of_sold_items.split()
        num_of_sold_items = num_of_sold_items[0]
        return int(num_of_sold_items)

    def _get_product_num_of_sold_items(self, product):
        try:
            num_of_sold_items = product.find('span', class_='msa3_z4 mgn2_12').get_text()
        except AttributeError:
            num_of_sold_items = product.find('span', class_='msa3_z4 mgn2_12 munh_4').get_text()
        num_of_sold_items = self._parse_product_num_of_sold_items(num_of_sold_items)
        return num_of_sold_items

    def _parse_price(self, product_price):
        """
        Selector returns price as: '18,98 zł'. Method extracts price swaps ',' with '.'
        return the price as a float in order to use it for further calculation
        :param product_price (str)
        :return product price (float)
        """
        match = re.match('\d+[,].\d', product_price)
        if match != None:
            match = match.group(0)
            product_price = match.replace(',', '.')
            return float(product_price)
        else:
            print('Couldn\'t extract product price')

    def _get_product_price(self, product):
        raw_product_price = product.find('span',
                            class_='mli8_k4 msa3_z4 mqu1_1 mgmw_qw mp0t_ji m9qz_yo mgn2_27 mgn2_30_s').get_text()
        product_price = self._parse_price(raw_product_price)
        return product_price


    def _get_product_shipping_price(self, product, product_price):
        raw_product_price_with_shipping = product.find('div', class_='mqu1_g3 mgn2_12').get_text()
        if raw_product_price_with_shipping != 'darmowa dostawa':
            product_price_with_shipping = self._parse_price(raw_product_price_with_shipping)
            shipping_price = product_price_with_shipping - product_price
            return round(shipping_price, 2)
        else:
            return 0

    def _get_product_name(self, product):
        return product.find('h2',
                            class_='mgn2_14 m9qz_yp meqh_en mpof_z0 mqu1_16 m6ax_n4 mp4t_0 m3h2_0 mryx_0 munh_0 mj7a_4').find(
            'a').get_text()

    def _get_product_url(self, product):
        return product.find('h2',
                            class_='mgn2_14 m9qz_yp meqh_en mpof_z0 mqu1_16 m6ax_n4 mp4t_0 m3h2_0 mryx_0 munh_0 mj7a_4').find(
            'a')['href']

    def _get_products(self, soup):
        products = soup.find_all('article', class_='mx7m_1 mnyp_co mlkp_ag _6a66d_YapB2')
        return products

    def _get_maximum_num_of_pages_from_cat(self):
        """
        Method used to find maximum number of pages available to scrape
        :return max_page (int)
        """
        max_page = self.driver.find_element(By.XPATH, config.max_page_selector).text
        return int(max_page)

    def _check_num_of_pages(self, num_of_pages, maximum_page_number):
        """
        Method checks if user didn't put more pages than it's available to scrape if so scraper will scrape
        all pages that are available in category.
        :param num_of_pages (int)
        :param maximum_page_number (int)
        :return num_of_pages (int)
        """
        if num_of_pages == 'max':
            return maximum_page_number
        elif num_of_pages > maximum_page_number:
            return maximum_page_number
        else:
            return num_of_pages

    def _get_category_id_form_url(self, url):
        """
        Method used to get id of category being scraped in order to
        use the id as the name of the output file
        :param url (str)
        :return url (int)
        """
        category_id = [int(s) for s in url.split('-') if s.isdigit()]
        if len(category_id) == 1:
            return category_id[0]
        else:
            raise ValueError('Incorrect url for category')

    def run_cat_scraper(self, cat_url, num_of_pages=1):
        """
        Method used to run category scraper and save output to file.
        :param cat_url (str)
        :param num_of_pages (int) (optional)
        :return None: Creates json file with a list of scraped auctions
        """
        page_number = 1
        # filter used to sort auctions by number of sold items
        sort_filter = '?order=qd'
        category_id = self._get_category_id_form_url(cat_url)
        print('category id being scraped: {}'.format(category_id))
        self.driver.get(cat_url)
        self._first_run()
        maximum_page_number = self._get_maximum_num_of_pages_from_cat()
        num_of_pages = self._check_num_of_pages(num_of_pages, maximum_page_number)
        print('number of pages being scraped: {}'.format(num_of_pages))
        for page in range(num_of_pages):
            page_filter = '&p={}'.format(str(page_number))
            url = cat_url + sort_filter + page_filter
            self.driver.get(url)
            self._scrape_cat_page()
            page_number += 1

        self.driver.close()
        utils.save_output_to_json_file('category_scraper_output', '{}.json'.format(category_id), self.scraped_auctions)
