#initialize webdriver set settings that allows to hide browser automation
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

def init_selenium():
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