import gspread
from oauth2client.service_account import ServiceAccountCredentials

import datetime

print('test1')

# use credentials to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive.file']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

print('test2')

# Find the workbook by name and open the first sheet
# sheet = client.open('COVID19_data').sheet1

# Finding the workbook by key, because name wasn't working
spreadsheet = client.open_by_key('1gqXuCcGYdXkpWMrDGwFbfQjSX5pui2QrhjsDeuJkpRM')

print('test3')

sheet = spreadsheet.sheet1

# sheet.add_cols(10)

# cell = sheet.cell(2, 2)
#
# print(cell.value)

print(sheet.acell('B1', value_render_option='FORMULA').value)
