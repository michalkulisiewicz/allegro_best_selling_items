from allegro_best_selling_items.google_sheet import GoogleSheet
from allegro_best_selling_items.allegro_category_scraper import AllegroCategoryScraper
from allegro_best_selling_items.utils import read_auctions_from_json


def run_category_scraper(category_url, num_of_pages=1):
    """
    Scrapes auctions from given category, extracts fields including: price, number of sold items, shipping_price
    saves output as json file in category_scraper output directory
    :param category_url: url of category being scraped (str)
    :param num_of_pages: number of pages to scrape, default is 1 (int)
    """
    category_scraper = AllegroCategoryScraper()
    category_scraper.run_cat_scraper(category_url, num_of_pages)


def add_category_scraper_output_to_google_sheet(secret_filename, output_workbook_name):
    """
    Creates worksheet for every json file inside of category_scraper_output directory
    :param secret_filename: file name of json credentials file needed to work with Google Sheets (str)
    :param output_workbook_name: name of workbook in Google Sheets created by the user (str)
    """
    auction_scraper_output = read_auctions_from_json('category_scraper_output')
    google_sheet = GoogleSheet(secret_filename, output_workbook_name)
    google_sheet.add_items_to_worksheet(auction_scraper_output)


if __name__ == '__main__':
    # Scrapes auctions from given category, saves output as json file in category_scraper_output directory
    run_category_scraper('https://allegro.pl/kategoria/obuwie-damskie-531', 10)
    # Creates report in Google Sheets based on the json file in auction_scraper_output directory
    add_category_scraper_output_to_google_sheet('SECRET_FILENAME', 'GOOGLE_SHEET_WORKBOOK_NAME')
