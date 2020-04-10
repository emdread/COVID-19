import datetime


# https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes

# datetime.datetime.strptime('13/3/2003', '%d/%m/%Y')
# datetime.datetime(2003, 3, 13, 0, 0)

# datetime.datetime(2003, 3, 13, 0, 0).strftime('%d/%m/%Y')
# '13/03/2003'

# datetime.datetime.strptime('13 March 2003', '%d %B %Y')
# datetime.datetime(2003, 3, 13, 0, 0)

# datetime.datetime(2003, 3, 13, 0, 0).strftime('%d %B %Y')
#'13 March 2003'


# Sheets stores dates as the number of days since 1/1/1900
# So add 693596


def sheets_date(date):
    """Takes an int, representing the number of days since 1/1/1900, which is how Google
    Sheets stores dates, and converts it to a datetime object."""

    return datetime.date.fromordinal(date + 693596)