# initialize webdriver set settings that allows to hide browser automation
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import config


def init_selenium():
    try:
        service = ChromeService(executable_path=ChromeDriverManager(version=config.chrome_driver_version).install())
        options = Options()
        options.add_argument('user-data-dir=session')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except Exception as e:
        print('Error while initializing webdriver')
        print(e)
