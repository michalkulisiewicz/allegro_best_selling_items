from webdriver import init_selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common import TimeoutException
import config
import utils
from utils import save_output_to_json_file
from selenium.webdriver.support.ui import WebDriverWait



class AllegroCategoryScraper:
    def __init__(self):
        self.first_run = self._check_if_first_run()
        self.driver = init_selenium()

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
        If it's first execution it will handle cookie prompt.
        """
        if not self.first_run:
            try:
                wait = WebDriverWait(self.driver, 30)
                wait.until(ec.element_to_be_clickable((By.XPATH, config.accept_cookies_selector))).click()
            except TimeoutException:
                pass



    def _scroll_down_page(self):
        xpath_selector = '//*[@class="mp0t_ji munh_0 m3h2_0 mqu1_1j mgn2_19 mgn2_21_s m9qz_yo mryx_16 mgmw_wo mp4t_0 msts_n7" and contains(text(),"rekomendacje dla Ciebie ")]'
        y = self.driver.find_element(By.XPATH, xpath_selector).location['y']
        for x in range(0, y, 50):
            self.driver.execute_script("window.scrollTo(0, " + str(x) + ");")


    def _toggle_view(self):
        """
        Method used to toggle view of a list of auctions in category.
        Default view makes it harder to scrape images from auction.
        """
        try:
            wait = WebDriverWait(self.driver, 5)
            wait.until(ec.presence_of_element_located((By.XPATH, config.toggle_view_selector))).click()
        except TimeoutException:
            pass


    def _scrape_cat_page(self):
        """
        scrapes urls and product names from a single page.
        :return: dict
        Returns data as a dictionary with key as product name and
        value as  url of the product.
        """
        self._first_run()
        self._toggle_view()
        self._scroll_down_page()
        products = self.driver.find_elements(By.XPATH, config.parent_product_selector)
        auctions = []
        for parent_product in products:
            child_product = parent_product.find_element(By.XPATH, config.child_product_selector)
            product_name = child_product.get_attribute('textContent')
            product_url = child_product.get_attribute('href')
            product_price = parent_product.find_element(By.XPATH, config.product_price_selector)
            shipping_price = parent_product.find_element(By.XPATH, config.shipping_price_selector)
            number_of_sold_items = parent_product.find_element(By.XPATH, config.number_of_sold_items_selector)
            product_image_url = parent_product.find_element(By.XPATH, '//*[@alt="{}"]'.format(product_name)).get_attribute('src')
            # Ommits the special promoted products
            auction = {}
            auction['product_name'] = product_name
            auction['product_url'] = product_url
            auction['product_price'] = product_price
            auction['shipping_price'] = shipping_price
            auction['number_of_sold_items'] = number_of_sold_items
            auction['product_image_url'] = product_image_url
            # if 'clicks?emission_unit' not in url:
            #     auctions[url] = preview_image_url
            auctions.append(auction)
            return auctions

    def _get_maximum_num_of_pages_from_cat(self):
        '''
        Function used to find maximum number of available pages to scrape
        :return: int
        '''

        try:
            WebDriverWait(self.driver, .25).until(
                ec.presence_of_element_located(
                    (By.XPATH, config.max_page_selector)
                )
            )
        except Exception as e:
            print('timeout error element not found: {}'.format(config.max_page_selector))
            print(e)
        max_page = self.driver.find_element(By.XPATH, config.max_page_selector).text
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

    def _get_category_id_form_url(self, url):
        '''
        Method used to get id of category being scraped in order to
        use the id as the name of the output file
        :param url: str
        :return: int
        '''
        category_id = [int(s) for s in url.split('-') if s.isdigit()]
        if len(category_id) == 1:
            return category_id[0]
        else:
            raise ValueError('Incorrect url for category')

    def run_cat_scraper(self, cat_url, num_of_pages=1):
        '''
        Method used to run category scraper and save output to file.
        :param cat_url: (required)
        :param num_of_pages: (optional)
        :return: None. Creates json file with name of the auction as key and url of the auction as value
        '''
        products = []
        page_number = 1
        #filter used to sort auctions by number of sold items
        sort_filter = '?order=qd'
        category_id = self._get_category_id_form_url(cat_url)
        print('category id being scraped: {}'.format(category_id))
        self.driver.get(cat_url)
        maximum_page_number = self._get_maximum_num_of_pages_from_cat()
        num_of_pages = self._check_num_of_pages(num_of_pages, maximum_page_number)
        print('number of pages being scraped: {}'.format(num_of_pages))
        for page in range(num_of_pages):
            page_filter = '&p={}'.format(str(page_number))
            url = cat_url + sort_filter + page_filter
            self.driver.get(url)
            products.append(self._scrape_cat_page())
            page_number += 1

        self.driver.close()
        save_output_to_json_file('category_scraper_output', '{}.json'.format(category_id), products)