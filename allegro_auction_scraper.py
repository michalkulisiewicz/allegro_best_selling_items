from webdriver import init_selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config
import json

class AllegroAuctionScraper:
    def __init__(self):
        self.driver = init_selenium()

    def run_auction_scraper(self):
        pass
