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


class Datum:
    """The class for each data point, a day"""

    def __init__(self, ident, home_cell_coord):
        """Takes an identifier, eg. a datetime object, and a tuple, representing the coordinates of the home cell."""

        self.ident = ident
        self.home_cell_coord = home_cell_coord


def initialise_data(sheet, init_word):
    """Takes a worksheet object, and the word that indicates data to be collect,
    and collects the data into a list of Datum objects."""

    # Collects data in 3 API requests

    # The initial cell which the data is relative to
    # init_word = 'Day'
    init_cell = sheet.find(init_word)

    # A list of the cells in the same column as the init_cell
    cat_col = sheet.col_values(init_cell.col)

    # A list of the cells in the same row as the init_cell
    data_row = sheet.row_values(init_cell.row, value_render_option='UNFORMATTED_VALUE')

    # The categories that each datum will have (from the cell after the init_cell, to the index of the first empty cell
    cats = cat_col[init_cell.row:cat_col.index('', init_cell.row)]

    # The datum objects already in the sheet
    data_entries = []
    for i in range(init_cell.col, len(data_row)):
        data_entries.append(Datum(sheets_date(data_row[i]), (init_cell.row, i + 2)))

    # Collect the data in one API call, into a list of rows

    # A1(column_number - 1) = the corresponding letter, not really sure how it works
    a1 = lambda n: ~int(n) and a1(int(n / 26) - 1) + chr(65 + n % 26) or ''
    cell_range = (a1(init_cell.col) + str(init_cell.row + 1) + ':' + a1(init_cell.col + len(data_entries) - 1)
                  + str(init_cell.row + len(cats)))

    data_lists = sheet.batch_get([cell_range], major_dimension='COLUMNS', value_render_option='FORMULA')[0]

    # Fill out rest of the categories for each entry
    # Iterates through each datum, and corresponding list of values for their categories
    # then iterates through this list of values and corresponding category name, adding these as attributes
    for i in range(len(data_entries)):
        datum = data_entries[i]
        values = data_lists[i]
        for j in range(len(values)):
            cat = cats[j]
            value = values[j]
            setattr(datum, cat, value)
            # These attributes to the Datum instances have a string (with spaces) as the key, and so cannot be called
            #  manually. They can be viewed with getattr(data[0], 'Confirmed cases)

    return data_entries


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
