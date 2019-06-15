class LocationNotFoundError(Exception):
    description = 'Could not find that location.'

class NoWeatherDataFoundError(Exception):
    description = 'No data found.'
