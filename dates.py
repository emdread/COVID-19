import datetime
import calendar


# https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes

# datetime.datetime.strptime('13/3/2003', '%d/%m/%Y')
# datetime.datetime(2003, 3, 13, 0, 0)

# datetime.datetime(2003, 3, 13, 0, 0).strftime('%d/%m/%Y')
# '13/03/2003'

# datetime.datetime.strptime('13 March 2003', '%d %B %Y')
# datetime.datetime(2003, 3, 13, 0, 0)

# datetime.datetime(2003, 3, 13, 0, 0).strftime('%d %B %Y')
# '13 March 2003'


# Sheets stores dates as the number of days since 1/1/1900
# So add 693596


def sheets_date(date):
    """Takes an int, representing the number of days since 30/12/1899 [[[1/1/1900]]], which is how Google
    Sheets stores dates, and converts it to a datetime date object."""

    return datetime.date.fromordinal(date + 693594)


def dhhs_url_date(url):
    """Takes a url for a link to a dhhs coronavirus update as a string, and returns a datetime date object for the date
    of the media release"""

    # eg. 'https://www.dhhs.vic.gov.au/coronavirus-update-victoria-6-april-2020'

    # default year, if missing
    year = '2020'

    # find the day, month and year in the url
    for element in url.split('-'):
        if element.isdigit():
            if len(element) == 4:
                year = element
            else:
                day = element

        elif element.isalpha():
            if element.capitalize() in calendar.month_name:
                month = element.capitalize()

    return datetime.datetime.strptime(' '.join([day, month, year]), '%d %B %Y').date()

