import gspread
from oauth2client.service_account import ServiceAccountCredentials

from dates import sheets_date
import datetime

import requests
from bs4 import BeautifulSoup

# print('test1')

# use credentials to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive.file']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# print('test2')

# Find the workbook by name and open the first sheet
# sheet = client.open('COVID19_data').sheet1

# Finding the workbook by key, because name wasn't working
spreadsheet = client.open_by_key('1gqXuCcGYdXkpWMrDGwFbfQjSX5pui2QrhjsDeuJkpRM')

# print('test3')

sheet = spreadsheet.sheet1

# sheet.add_cols(10)

# cell = sheet.cell(2, 2)
#
# print(cell.value)

# print(sheet.acell('B1', value_render_option='FORMULA').value)
# print(sheets_date(sheet.cell(2, 2, value_render_option='UNFORMATTED_VALUE').value))

class Day:
    """The class for each data point, a day"""

    def __init___(self, date, home_cell):
        """Takes a datetime object, and a cell object."""

        self.date = date
        self.home_cell = home_cell

def initialise_data(sheet):
    """Takes a worksheet object, and collects the data into a list of Day objects."""

    # The initial cell which the data is relative to
    init_cell = sheet.find('Day')

    # The categories that each day will have
    cats = []
    # The cell below the initial cell
    current_cell = sheet.cell(init_cell.row + 1, init_cell.col)
    while current_cell.value:
        cats.append(current_cell.value)
        current_cell = sheet.cell(current_cell.row + 1, current_cell.col)

    # The day objects already in the sheet
    days = []
    current_cell = sheet.cell(init_cell.row, init_cell.col + 1)
    while current_cell.value:
        days.append(Day(sheets_date(current_cell.value), current_cell))
        current_cell = sheet.cell(current_cell.row, current_cell.col + 1)

    return days

def collect_links(url='https://www.dhhs.vic.gov.au/media-hub-coronavirus-disease-covid-19'):
    """Takes a url string, and returns a list of all the links on that page"""

    # Requests the html, and parses it to be readable
    r = requests.get(url)
    r_html = r.text
    soup = BeautifulSoup(r_html, "html.parser")

    link_list = []

    for link in soup.find_all('a'):
        print(link)
        print()
