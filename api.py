from requests import get

API_LOCATION_URI = 'https://www.metaweather.com/api/location/search/'
API_WEATHER_URI  = 'https://www.metaweather.com/api/location/{location_id}/{year}/{month}/{day}/'

def fetch_location_id(location_str):
    json = get(API_LOCATION_URI, params={'query': location_str}).json()
    if not len(json):
        return None
    return json[0]['woeid']

def fetch_weather_data(location_id, date):
    uri = API_WEATHER_URI.format(location_id=location_id, year=date.year, month=date.month, day=date.day)
    json = get(uri).json()
    return json
