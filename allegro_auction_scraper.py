from webdriver import init_selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config
import json

class AllegroAuctionScraper:
    def __init__(self):
        self.driver = init_selenium()

    def run_auction_scraper(self, url=None):
        self.driver.get(url)
        price_selector =
        test = self.driver.find_element(By.XPATH, price_selector)
        print('test')

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