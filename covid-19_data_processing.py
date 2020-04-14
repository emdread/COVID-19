import gspread
from oauth2client.service_account import ServiceAccountCredentials

from dates import sheets_date
import datetime

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def open_worksheet(spreadsheet_key='1gqXuCcGYdXkpWMrDGwFbfQjSX5pui2QrhjsDeuJkpRM', worksheet=None):
    """Takes a spreadsheet key string, and a worksheet identifier, either the name as a string, the index as an int,
    or if left blank: just uses the first worksheet. And returns a worksheet object"""
    # use credentials to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive.file']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    # Finding the spreadsheet by key (because name wasn't working)
    spreadsheet = client.open_by_key(spreadsheet_key)

    # Select a worksheet by index, starting from 0
    if type(worksheet == int):
        sheet = spreadsheet.get_worksheet(worksheet)

    # Or by title
    elif type(worksheet == str):
        sheet = spreadsheet.worksheet(worksheet)

    # Or just open the first worksheet
    else:
        sheet = spreadsheet.sheet1

    return sheet

# sheet.add_cols(10)
# print(sheet.acell('B1', value_render_option='FORMULA').value)
# print(sheets_date(sheet.cell(2, 2, value_render_option='UNFORMATTED_VALUE').value))


class Datum:
    """The class for each data point, a day"""

    def __init__(self, identifier, home_cell_coord):
        """Takes an identifier, eg. a datetime object, and a tuple, representing the coordinates of the home cell."""

        self.identifier = identifier
        self.home_cell_coord = home_cell_coord


def initialise_data(sheet, init_word):
    """Takes a worksheet object, and the word that indicates data to be collect,
    and collects the data into a list of Datum objects.
    Returns a tuple of the list of data objects, and the list of categories"""

    # Collects data in 4 API requests

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

    return data_entries, cats


def media_release_links(href):
    """Takes a href string, and returns True if it is a link to a one of the daily DHHS media releases,
    coronavirus update, for Victoria.
    Configured for those from https://www.dhhs.vic.gov.au/media-hub-coronavirus-disease-covid-19 from 23 March 2020."""

    if href:
        return 'coronavirus-update-victoria-' in href
    return False


def collect_links(url='https://www.dhhs.vic.gov.au/media-hub-coronavirus-disease-covid-19', func=media_release_links):
    """Takes a url string, and a filter function, and returns a list of all the links as strings on that page"""

    # Requests the html, and parses it to be readable
    r = requests.get(url)
    r_html = r.text
    soup = BeautifulSoup(r_html, "html.parser")

    # Adds an absolute url link to the link list
    link_list = []
    for link in soup.find_all('a', href=func):
        link_list.append(urljoin(url, link['href']))

    return link_list


def consolidate_data(data_entries, link_list=collect_links()):
    """Takes a list of Datum objects, which are data entries already in the spreadsheet.
    ALso a list of url string links, to source new data from.
    Returns a tuple of a dictionary of all the data, and just the new data, both: {identifier: Datum object}"""

    data_dict = {}
    new_data_dict = {}

    # Adds the Datum objects from the spreadsheet into the data_dict
    for data_entry in data_entries:
        data_dict[data_entry.identifier] = data_entry

    for link in link_list:
        link_datum = Datum


# def scrape_datum(cats, source_url):
#     """Takes a list of categories to find the values of for this data entry,
#     and a url string for the source webpage, and scrapes this data into a Datum object as attributes.
#     Returns a Datum object"""
#
#     # Requests the html, and parses it to be readable
#     r = requests.get(source_url)
#     r_html = r.text
#     soup = BeautifulSoup(r_html, "html.parser")
#
#
#
#
# def new_data(cats, source=collect_links()):
#     """Takes a source of new data, eg. a list of urls, and returns a list of the new Datum objects."""
#
#     data_list = []
#     for page in source:
#         data_list.append(scrape_datum(cats, source))
#
#     return data_list

