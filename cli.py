import argparse
from datetime import datetime

DEFAULT_LOCATION     = 'San Francisco'
DEFAULT_DATE         = datetime.now().date()
DATE_FMT             = r'%Y-%m-%d'
CORRECT_DATE_EXAMPLE = '2019-1-1'
INVALID_DATE_MESG    = 'Invalid date, must be in form {} (ie {})'.format(DATE_FMT, CORRECT_DATE_EXAMPLE)

def parse_args():
    parser = argparse.ArgumentParser(description='Display the weather in csv form for a given date and location.')
    parser.add_argument('location', nargs='?', default=DEFAULT_LOCATION,
        help='The location to display the weather for. Default is \'{}\'.'.format(DEFAULT_LOCATION))
    parser.add_argument('date', nargs='?', default=DEFAULT_DATE, type=parse_date,
        help='The date to display the weather for, in form `{}` (ie {}). Default is today.'.format(DATE_FMT.replace(r'%', r'%%'), CORRECT_DATE_EXAMPLE))
    parser.add_argument('--reset-db', action='store_true',
        help='Wipe the db, deleting all cached weather data.')
    return parser.parse_args()

def parse_date(str):
    try:
        return datetime.strptime(str, DATE_FMT).date()
    except ValueError:
        raise argparse.ArgumentTypeError(INVALID_DATE_MESG)
