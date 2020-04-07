import gspread
from oauth2client.service_account import ServiceAccountCredentials

print('test1')

# use credentials to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive.file']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

print('test2')

# Find the workbook by name and open the first sheet
# sheet = client.open('data').sheet1
sheet = client.openall()

print('test3')

# Extract and print all of the values
list_of_hashes = sheet.get_all_records()
print(list_of_hashes)
