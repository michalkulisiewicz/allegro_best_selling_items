import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date
from gspread_formatting import *


class GoogleSheet:
    def __init__(self, json_keyfile_name, sheet_name):
        self.worksheet = None
        self.sheet_name = sheet_name
        self.worksheet_total_rows = None
        self.worksheet_total_columns = 6
        self.scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
                      "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile_name, self.scope)
        self.client = gspread.authorize(self.creds)
        self.sheet = self.client.open(self.sheet_name)

    def _get_sheet_id(self):
        return self.worksheet._properties['sheetId']

    # object to resize: 'COLUMNS' or 'ROWS', start_index 0-1 means column A or first row
    def resize(self, object_to_resize, start_index, end_index, pixel_size):
        body = {
            "requests": [
                {
                    "updateDimensionProperties": {
                        "range": {
                            "sheetId": self._get_sheet_id(),
                            "dimension": object_to_resize,
                            "startIndex": start_index,
                            "endIndex": end_index
                        },
                        "properties": {
                            "pixelSize": pixel_size
                        },
                        "fields": "pixelSize"
                    }
                }
            ]
        }
        res = self.sheet.batch_update(body)

    def create_default_columns_names(self):
        today = date.today()
        timestamp = today.strftime("%d/%m/%Y")
        self.worksheet.update_cell(1, 1, 'PRODUCT NAME')
        self.worksheet.update_cell(1, 2, 'PREVIEW IMAGE')
        self.worksheet.update_cell(1, 3, 'PRICE')
        self.worksheet.update_cell(1, 4, 'SHIPPING')
        self.worksheet.update_cell(1, 5, 'NUMBER OF SOLD ITEMS TO DATE: {}'.format(timestamp))
        self.worksheet.update_cell(1, 6, 'AUCTION URL')

    def update_rows_in_batch(self, row_value_list, first_row, first_column, last_row, last_column):
        cell_list = self.worksheet.range(first_row, first_column, last_row, last_column)
        for cell, value in zip(cell_list, row_value_list):
            cell.value = value
        self.worksheet.update_cells(cell_list, value_input_option='USER_ENTERED')

    def apply_formatting(self):
        self.create_default_columns_names()

        self.resize('COLUMNS', 0, 1, 450)
        self.resize('COLUMNS', 1, 2, 350)
        self.resize('COLUMNS', 2, 5, 180)
        self.resize('COLUMNS', 5, 6, 450)
        self.resize('ROWS', 0, 1, 150)
        self.resize('ROWS', 1, self.worksheet_total_rows + 1, 250)

        fmt_columns = cellFormat(
            backgroundColor=color(0, 128, 128),
            textFormat=textFormat(bold=True, foregroundColor=color(255, 255, 255), fontSize=14),
            horizontalAlignment='CENTER',
            verticalAlignment='MIDDLE',
            wrapStrategy='WRAP'
        )

        fmt_rows = cellFormat(
            textFormat=textFormat(bold=True, foregroundColor=color(255, 255, 255), fontSize=14),
            horizontalAlignment='CENTER',
            verticalAlignment='MIDDLE',
            wrapStrategy='WRAP'
        )
        format_cell_range(self.worksheet, 'A1:F1', fmt_columns)
        format_cell_range(self.worksheet, '2:{}'.format(self.worksheet_total_rows + 1), fmt_rows)
        set_frozen(self.worksheet, rows=1, cols=0)

    def create_worksheet(self, worksheet_title, total_rows):
        self.worksheet = self.sheet.add_worksheet(title=str(worksheet_title), rows=total_rows,
                                                  cols=self.worksheet_total_columns)
        self.apply_formatting()

    def add_items_to_worksheet(self, auction_dict):
        for category_id, auction_list in auction_dict.items():
            self.worksheet_total_rows = len(auction_list)
            self.create_worksheet(str(category_id), len(auction_list) + 2)
            self.batch_update_rows(auction_list)

    def get_image_url_field(self, auction):
        image_url = auction['product_image_url']
        image_field = '=IMAGE(\"{}\")'.format(image_url)
        return image_field

    def batch_update_rows(self, auction_list):
        url_fields_list = []
        image_url_fields_list = []
        product_price_fields_list = []
        lowest_delivery_price_fields_list = []
        number_of_sold_items_fields_list = []
        auction_number_fields_list = []
        product_name_fields_list = []

        for auction in auction_list:
            url_fields_list.append(auction['product_url'])
            image_url_fields_list.append(self.get_image_url_field(auction))
            product_price_fields_list.append(auction['product_price'])
            lowest_delivery_price_fields_list.append(auction['shipping_price'])
            number_of_sold_items_fields_list.append(auction['number_of_sold_items'])
            product_name_fields_list.append(auction['product_name'])

        last_row = len(url_fields_list) + 1
        self.update_rows_in_batch(product_name_fields_list, 2, 1, last_row, 1)
        self.update_rows_in_batch(image_url_fields_list, 2, 2, last_row, 2)
        self.update_rows_in_batch(product_price_fields_list, 2, 3, last_row, 3)
        self.update_rows_in_batch(lowest_delivery_price_fields_list, 2, 4, last_row, 4)
        self.update_rows_in_batch(number_of_sold_items_fields_list, 2, 5, last_row, 5)
        self.update_rows_in_batch(url_fields_list, 2, 6, last_row, 6)
